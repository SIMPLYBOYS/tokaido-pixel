#!/usr/bin/env python3
"""從博物館掃描產出單站三種遊戲資產：
  originals/{slug}.jpg  1000px 寬（卡片主圖）
  large/{slug}.jpg      2600px 寬（全螢幕檢視）
  scenes/{slug}.png     320px 寬、14 色量化（像素道中版）

用法：python3 tools/make-station-assets.py assets/12-mishima.jpg [--crop L,T,R,B]
--crop 為去紙邊留畫芯的比例（各邊裁掉的分數，如 0.04,0.05,0.04,0.05）
"""
import json, argparse
from pathlib import Path
from PIL import Image

LANCZOS = Image.Resampling.LANCZOS
ROOT = Path(__file__).resolve().parent.parent
PALETTE = [tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
           for c in json.load(open(ROOT / "assets/palette.json"))["colors"]]


def quantize(im: Image.Image) -> Image.Image:
    """Floyd-Steinberg 抖動量化到 14 色浮世繪色盤（與既有 11 站同風格）"""
    p = Image.new("P", (1, 1))
    flat = [v for c in PALETTE for v in c]
    p.putpalette(flat + flat[:3] * (256 - len(PALETTE)))
    return im.convert("RGB").quantize(palette=p, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scan")
    ap.add_argument("--crop", help="L,T,R,B 各邊裁掉比例（0–0.5）")
    args = ap.parse_args()

    slug = Path(args.scan).stem
    im = Image.open(args.scan).convert("RGB")
    if args.crop:
        l, t, r, b = (float(x) for x in args.crop.split(","))
        w, h = im.size
        im = im.crop((int(w * l), int(h * t), int(w * (1 - r)), int(h * (1 - b))))

    def resize_w(width):
        return im.resize((width, round(im.height * width / im.width)), LANCZOS)

    out_orig = ROOT / f"game-assets/originals/{slug}.jpg"
    out_large = ROOT / f"game-assets/large/{slug}.jpg"
    out_scene = ROOT / f"game-assets/scenes/{slug}.png"
    resize_w(min(1000, im.width)).save(out_orig, quality=85)
    resize_w(min(2600, im.width)).save(out_large, quality=78)  # 不超采樣，來源多小就多大
    quantize(resize_w(320)).save(out_scene, optimize=True)
    for p in (out_orig, out_large, out_scene):
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
