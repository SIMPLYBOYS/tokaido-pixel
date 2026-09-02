# 詞彙表（Glossary）

Tōkaidō Pixel 專案的核心術語。看不懂其他頁的名詞時回來查這裡。

| 術語 | 說明 | 相關頁 |
|---|---|---|
| **東海道五十三次** | 江戶時代連結江戶（日本橋）與京都（京師）的驛道，途中 53 個宿場。本作是照這條路線走一遍的像素道中遊戲，共 55 個節點（含起點日本橋與終點京師）。 | index |
| **宿場（しゅくば）** | 驛道上的驛站城鎮。每站在遊戲中對應一個地圖節點 + 一幅浮世繪場景。 | index, 2-gameplay |
| **STATIONS** | `index.html` 裡的站點資料陣列，每筆含 slug/ja/pic/map[x,y]/details/desc/facts/credit——遊戲全部內容的資料模型。 | 1-game-shell, 2-gameplay |
| **slug** | 站點的檔名前綴，如 `16-kanbara`。資產檔（jpg/png）與 manifest 記錄都用它當 key。 | 3-asset-pipeline, 4-build-log |
| **pic（畫題）** | 該站採用的浮世繪標題，如蒲原的「夜之雪」。**選圖時必須與此欄核對**，避免掛錯畫師的別系列。 | 4-build-log |
| **EVENTS** | `index.html` 的旅途事件加權池；`travelTo` 每次移動抽一則 [extra, text]，`state.days` 推進 `1+extra` 天。 | 2-gameplay |
| **命中半徑（HIT_R）** | 場景細節點的點擊判定半徑，`0.075`（畫面寬度比例）。`tapScene` 判斷點擊是否落在某個 detail 上。 | 2-gameplay |
| **details** | 一幅場景裡可點的細節點位，格式 `[x, y, label]`，座標為 0–1 正規化。找到會計入圖鑑。 | 2-gameplay |
| **圖鑑（Zukan）／繪卷（Emaki）** | 收集成就介面。`buildZukan` 列站點收集狀態；集滿條件解鎖 `buildEmaki` 播放的繪卷結局。 | 2-gameplay |
| **progress / localStorage** | 玩家進度存於瀏覽器 localStorage（KEY 常數）；`load()`/`save` 讀寫，`foundOf`/`doneCount` 統計完成度。 | 1-game-shell |
| **資產三尺寸** | `make-station-assets.py` 為每站產：originals(1000px jpg 預覽)、large(2600px jpg)、scenes(320px png 14 色量化)。 | 3-asset-pipeline |
| **palette.json（14 色）** | 像素場景的固定調色盤。`quantize()` 以此 14 色 + Floyd-Steinberg dither 把掃描圖轉成像素風。 | 3-asset-pipeline |
| **Floyd-Steinberg dither** | 誤差擴散抖動演算法；用少數顏色模擬漸層，是像素場景「有顆粒紋理」的來源，屬預期行為。 | 3-asset-pipeline |
| **--crop L,T,R,B** | `make-station-assets.py` 的裁邊參數，各邊裁掉的比例，用來去掉掃描台紙邊。LOC 掃描常用 0.03–0.06。 | 3-asset-pipeline |
| **circles.json** | `detect-ref-circles.py` 從紅圈參照總圖偵測出的 53 宿正規化座標，是地圖節點座標的**座標契約**。 | 3-asset-pipeline, 4-build-log |
| **manifest.json** | Phase B 的**進度契約 / 唯一真相來源**：40 站各自的四態狀態（todo→assets→authored→verified）。 | 4-build-log |
| **狀態流四態** | `todo`（待辦）→ `assets`（資產完成）→ `authored`（寫入 index.html）→ `verified`（瀏覽器驗證過）。單向推進。 | 4-build-log |
| **Phase A / Phase B** | A＝手工做前 15 站並驗證流程；B＝照該流程批量擴充剩餘 40 站（編號 16–55）。 | 4-build-log |
| **京師例外** | 終點京師在參照總圖上無紅圈（只標 53 宿），其地圖座標是人工目測放置，不來自 circles.json。 | 4-build-log |
| **sources.json** | `assets/sources.json`，每張掃描圖的溯源與授權記錄，讓成品可追。 | 3-asset-pipeline, 4-build-log |
