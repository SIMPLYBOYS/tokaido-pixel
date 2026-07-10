# Phase B 執行手冊 — 蒲原→京師 40 站批量擴充

Phase A（12–15 站）已驗證整條管線。本手冊讓任何新 session 不需重新摸索即可續作。

## 工作清單

`phase-b/manifest.json` — 40 站的 slug／宿名／畫題／狀態。
狀態流：`todo → assets（資產完成）→ authored（資料寫入 index.html）→ verified（瀏覽器驗證過）`。
每完成一站就更新 status，這是唯一的進度真相來源。

## 單站工序（Phase A 驗證過的流程）

### 1. 選圖
```bash
python3 tools/find-scans.py 16-kanbara        # 不帶參數 = 全部 todo
```
候選寫入 `phase-b/scan-candidates.json`。挑選規則：
- 優先 LOC 全解析（檔名含 LCCN，~9000px）＞博物館 CC0/PD 大圖（Rijksmuseum／Cleveland／MET）
- **陷阱**：務必核對畫題與 manifest 的 `pic` 欄一致。Commons 上混有北齋、行書/隷書東海道等別系列
  （Phase A 實例：`Numazu LCCN2009615349` 是北齋的沼津，不是廣重保永堂版）。
  拿不準就抓 500px 縮圖目視。
- 下載到 `assets/{slug}.jpg`，並把溯源補進 `assets/sources.json`（欄位照既有 16 筆）。

### 2. 產資產
```bash
python3 tools/make-station-assets.py assets/16-kanbara.jpg --crop 0.05,0.03,0.04,0.03
```
- `--crop L,T,R,B` 為各邊裁掉比例，目標是「留紙芯、去掃描台背景」。LOC 掃描通常 0.03–0.06。
- 產出後看 `game-assets/originals/{slug}.jpg` 400px 預覽確認無殘邊、無缺角，畫面長寬比應在 1.45–1.49。
- 像素版有 Floyd-Steinberg 抖動紋理是**預期行為**（與既有站一致）。

### 3. 大地圖座標
- `phase-b/circles.json` 已存 53 個紅圈標註的正規化座標（偵測誤差 ≤0.002，已用 Phase A 四站驗證）。
- 其中 4 筆已填 `number`（宿 11 三島／12 沼津／13 原／14 吉原）。其餘指認方式：
  看 `phase-b/circle-tiles/cNN.png`（紅圈＋下方名籤放大 4 倍），配合路線連續性定編號。
- 遊戲節點座標 = 該圈的 `x,y`。遊戲編號 = 宿場番號 + 1（日本橋為 1）。
- **例外**：終點 55-kyoto（京師）沒有紅圈——參照版只標 53 宿。地圖右上「京都」朱印旁目測，
  約 (0.87, 0.07) 附近，放節點前先目視。

### 4. 遊戲內容
- 用 10% 網格疊圖看 `originals/{slug}.jpg`，挑 3 個找細節點位（構圖上有故事性的元素：人物、名物、地標）。
- 座標為 0–1 正規化，命中半徑 0.075（寬度比例），不必太精準但要落在物件中心。
- 照既有格式 append 進 index.html 的 `STATIONS`（slug/ja/pic/map/details/desc/credit）。
- desc 風格：一至兩句，講畫面裡正在發生的事＋一個歷史/構圖亮點（參考既有 15 站）。

### 5. 驗證（每站或每批）
Playwright 對 `http://localhost:8791`（`python3 -m http.server 8791`）：
- `document.querySelectorAll('.node').length` = STATIONS 總數
- 三個資產檔 `fetch HEAD` 全 200
- `openScene(idx)` 後以 `tapScene(x, y)` 打三個細節座標，應全部回 `true`
- 截圖地圖確認節點落在合理位置（對照 `assets/00-overworld-reference-vault.png`）

## 批次建議

- 一批 6–10 站（依地圖分區：駿河 16–25、遠江 26–33、三河/尾張 34–42、伊勢/近江 43–55）。
- 批內可平行：選圖與產資產是機械工序；內容撰寫需逐幅看圖。
- 每批結束跑一次完整驗證＋更新 manifest status，再開下一批。

## 里程碑收尾（做到才算該批完成）

- header 副標「日本橋→◯◯」隨最後一站更新
- `sources.json` 與 manifest status 同步
- 全部 55 站完成後進 Phase C：RANKS 天數平衡（全程約 55–70 日）、地圖 min-width 加寬＋
  自動捲到當前進度、STATIONS 抽出為 stations.js、（可選）壓縮 large/ 總量

## 已知資源

| 檔案 | 用途 |
|---|---|
| `tools/make-station-assets.py` | 掃描 → 三種遊戲資產 |
| `tools/find-scans.py` | Commons 批量搜圖 |
| `tools/detect-ref-circles.py` | 重跑紅圈偵測（已跑過，一般不需要） |
| `phase-b/manifest.json` | 40 站工作清單＋狀態 |
| `phase-b/circles.json` | 53 宿地圖座標（待指認編號） |
| `phase-b/circle-tiles/` | 每圈放大切片，指認用 |
| `phase-b/scan-candidates.json` | 搜圖結果快取 |
| `assets/00-overworld-reference-vault.png` | 53 宿紅圈標註參照圖 |
