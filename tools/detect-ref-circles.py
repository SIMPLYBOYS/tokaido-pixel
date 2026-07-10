#!/usr/bin/env python3
"""從 assets/00-overworld-reference-vault.png 偵測 53 宿的紅圈標註位置。

輸出：
  phase-b/circles.json      所有紅圈中心的正規化座標（未定編號，number 待人工指認）
  phase-b/circle-tiles/     每個紅圈的放大切片（圈+下方名籤），供逐一指認宿場編號

指認後把編號填回 circles.json 的 number 欄即成為節點座標來源。
"""
import json
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "phase-b"
TILES = OUT / "circle-tiles"
TILES.mkdir(parents=True, exist_ok=True)

im = Image.open(ROOT / "assets/00-overworld-reference-vault.png").convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
# 標註紅圈為橘紅 (~220,95,55)；靠 R-G 落差區隔地圖上的淡粉紅道路（落差僅 ~50）
mask = (r > 195) & (r - g > 95) & (r - b > 120)

# 簡易連通聚類：逐點併入鄰近 cluster（點數少，O(n·k) 可接受）
ys, xs = np.nonzero(mask)
clusters = []  # [cx, cy, count]
for x, y in zip(xs, ys):
    for c in clusters:
        if abs(c[0] - x) < 18 and abs(c[1] - y) < 18:
            c[0] = (c[0] * c[2] + x) / (c[2] + 1)
            c[1] = (c[1] * c[2] + y) / (c[2] + 1)
            c[2] += 1
            break
    else:
        clusters.append([float(x), float(y), 1])

# 紅圈直徑約 14-20px（1408 寬）→ 面積閾值濾掉雜點（太陽、印章另外大很多，也濾）
found = [c for c in clusters if 60 < c[2] < 800]
w, h = im.size
items = []
for i, (cx, cy, n) in enumerate(sorted(found, key=lambda c: (c[1], c[0]))):
    nx, ny = round(cx / w, 4), round(cy / h, 4)
    items.append({"id": i, "x": nx, "y": ny, "px": n, "number": None})
    # 切片：圈為中心，含下方名籤，放大 4 倍
    box = im.crop((int(cx - 30), int(cy - 18), int(cx + 30), int(cy + 60)))
    box = box.resize((box.width * 4, box.height * 4), Image.Resampling.LANCZOS)
    box.save(TILES / f"c{i:02d}.png")

json.dump({"source": "00-overworld-reference-vault.png",
           "note": "number=宿場番號（1=品川…53=大津；日本橋/京都端點不在圈內）待指認",
           "circles": items},
          open(OUT / "circles.json", "w"), ensure_ascii=False, indent=1)
print(f"detected {len(items)} circles → phase-b/circles.json + {len(items)} tiles")
