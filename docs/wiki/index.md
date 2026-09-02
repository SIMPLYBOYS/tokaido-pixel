<!-- wiki-rev: PENDING -->
# Tōkaidō Pixel — 架構 Wiki

> 這份文件是給**人與 agent 共用的心智模型**：人記概念、模型記符號。
> 它不是 API 參考（原始碼自己會說），也不是 README（那份給第一次來的訪客）。
> 每個說法都附〔路徑:行號 · 錨點〕，並用 `verify_citations` 驗過。

## 這是什麼

**Tōkaidō Pixel（東海道五十三次・像素道中記）** 是一個**單檔 HTML 遊戲**：玩家扮演旅人，從江戶日本橋走到京都，逐一走進廣重《東海道五十三次》的 55 幅浮世繪，在每幅畫裡找出三個隱藏細節（狗、風箏、遠富士…），全找齊便解鎖博物館原圖。

技術定性一句話：**沒有框架、沒有 build step、沒有伺服器邏輯**——一個 `index.html`（約 1839 行）、公有領域畫作、一條離線的 Python 資產管線。進度存在 `localStorage`，載入後可完全離線遊玩。〔`tokaido-pixel/README.md:9` · `No framework, no build step`〕

## 系統的三層

| 層 | 是什麼 | 在哪 | Wiki 頁 |
|---|---|---|---|
| **遊戲外殼** | 單檔 HTML：視圖切換、狀態機、55 站資料 | `index.html`（HTML/CSS/JS 全在內） | [1-game-shell](1-game-shell.md) |
| **玩法核心** | 找細節命中判定、天數/事件、卡片/圖鑑/繪卷/證書/終局 | `index.html` `<script>` 區塊 | [2-gameplay](2-gameplay.md) |
| **資產管線** | 博物館掃描 → 三種遊戲資產（離線 Python + PIL） | `tokaido-pixel/tools/*.py` | [3-asset-pipeline](3-asset-pipeline.md) |
| **建置日誌** | Phase B 批量擴充 40 站的工序與資料契約 | `tokaido-pixel/phase-b/` | [4-build-log-phaseb](4-build-log-phaseb.md) |

執行環境是**瀏覽器 + 一個靜態檔案伺服器**（`python3 -m http.server`）；Python 只在**離線做資產**時用，遊戲本身不需要它。〔`tokaido-pixel/README.md:21` · `python3 -m http.server 8791`〕

## 概念 → 程式實體 總對映表

| 概念 | 程式實體 | 說明 |
|---|---|---|
| 55 站資料模型 | `STATIONS` 〔`tokaido-pixel/index.html:519` · `const STATIONS = [`〕 | 每站 slug/ja/pic/map/details/desc/facts/credit |
| 視圖切換（單頁多視圖） | `show()` 〔`tokaido-pixel/index.html:999` · `function show(view)`〕 | 靠 CSS class `active` 切 map/scene/zukan/emaki/finale |
| 進度存檔 | `state` + `save()` 〔`tokaido-pixel/index.html:982` · `let state = load()`〕 | localStorage key `tokaido-progress-v2` |
| 找細節命中判定 | `tapScene()` 〔`tokaido-pixel/index.html:1110` · `function tapScene`〕 | 座標正規化後 aspect 校正比距離 |
| 命中半徑常數 | `HIT_R` 〔`tokaido-pixel/index.html:978` · `const HIT_R = 0.075`〕 | 相對場景寬 0.075 |
| 旅程天數 / 隨機事件 | `travelTo()` + `EVENTS` 〔`tokaido-pixel/index.html:1040` · `function travelTo`〕 | 移動一站加天數，加權抽事件 |
| 大地圖節點 | `buildMap()` 〔`tokaido-pixel/index.html:1016` · `function buildMap`〕 | 依 `map:[x,y]` 座標擺節點 |
| 過關卡片 / 圖鑑 | `openCard()` / `buildZukan()` 〔`tokaido-pixel/index.html:1213` · `function openCard`〕 | 解鎖原圖、圖鑑翻頁 |
| 繪卷模式 | `buildEmaki()` 〔`tokaido-pixel/index.html:1523` · `function buildEmaki`〕 | 55 圖接成一條橫卷，右到左自動展 |
| 完走證書 | `drawCert()` 〔`tokaido-pixel/index.html:1442` · `async function drawCert`〕 | canvas 畫 kanpo-shō，青海波邊框 |
| 像素化資產生成 | `make-station-assets.py` 〔`tokaido-pixel/tools/make-station-assets.py:1` · `從博物館掃描產出`〕 | 裁邊→縮圖→14 色抖動量化 |
| 地圖節點座標來源 | `detect-ref-circles.py` 〔`tokaido-pixel/tools/detect-ref-circles.py:1` · `偵測 53 宿的紅圈`〕 | 從參照圖偵測 53 宿紅圈 |
| 建置進度真相 | `tokaido-pixel/phase-b/manifest.json` 〔`tokaido-pixel/phase-b/PHASE-B.md:9` · `唯一的進度真相來源`〕 | 40 站 todo→assets→authored→verified |

## 為什麼是「單檔」

這是刻意的架構選擇，不是偷懶。README「Tech notes」把資料（`STATIONS` 55 站陣列，含座標、謎題點、解說）、CSS、JS 全放進 `index.html`，目的是**零依賴、可離線、GitHub Pages 直接可跑**。代價是單檔會長（~1839 行），未來若擴張，Phase C 計畫把 `STATIONS` 抽成獨立 `stations.js`。〔`tokaido-pixel/phase-b/PHASE-B.md` · `STATIONS 抽出為 stations.js`〕

## 詞彙

專案內部黑話（宿場、保永堂版、青海波、gagō…）見 [glossary](glossary.md)。
