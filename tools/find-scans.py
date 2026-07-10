#!/usr/bin/env python3
"""為 phase-b/manifest.json 中 status=todo 的宿場批量搜尋 Wikimedia Commons 掃描候選。

輸出 phase-b/scan-candidates.json：每站前幾名候選（標題/尺寸/授權/直連 URL），
供人工（或 agent）挑選後下載。優先序：LOC 全解析 LCCN 掃描 > 博物館 CC0/PD 大圖。

用法：python3 tools/find-scans.py [slug ...]   # 不帶參數 = 全部 todo
"""
import json, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://commons.wikimedia.org/w/api.php"

def api(params):
    qs = urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(f"{API}?{qs}", headers={"User-Agent": "tokaido-pixel/1.0 (game asset sourcing)"})
    for wait in (0, 15, 45, 90):  # 429 退避重試
        if wait:
            time.sleep(wait)
        try:
            return json.load(urllib.request.urlopen(req, timeout=30))
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
    raise RuntimeError("Commons API 持續 429，稍後再試")

def search(query, limit=6):
    d = api({"action": "query", "generator": "search", "gsrsearch": query,
             "gsrnamespace": 6, "gsrlimit": limit,
             "prop": "imageinfo", "iiprop": "url|size|extmetadata"})
    out = []
    for p in (d.get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        gv = lambda k: (em.get(k, {}) or {}).get("value", "")
        out.append({"title": p["title"], "width": ii.get("width"), "height": ii.get("height"),
                    "license": gv("LicenseShortName"), "url": ii.get("url")})
    return sorted(out, key=lambda x: -(x["width"] or 0))

def main():
    man = json.load(open(ROOT / "phase-b/manifest.json"))["stations"]
    only = set(sys.argv[1:])
    result_path = ROOT / "phase-b/scan-candidates.json"
    results = json.load(open(result_path)) if result_path.exists() else {}
    for s in man:
        if s["status"] != "todo" or (only and s["slug"] not in only):
            continue
        romaji = s["slug"].split("-", 1)[1]
        cands = search(f"Hiroshige Tokaido {romaji} Hoeido")
        cands += [c for c in search(f"{s['ja']} LCCN Hiroshige", 4)
                  if c["title"] not in {x["title"] for x in cands}]
        results[s["slug"]] = cands
        print(f"{s['slug']}: {len(cands)} candidates, best {cands[0]['width']}px" if cands
              else f"{s['slug']}: NONE FOUND", flush=True)
        json.dump(results, open(result_path, "w"), ensure_ascii=False, indent=1)  # 逐站落盤，中斷可續
        time.sleep(3)
    json.dump(results, open(result_path, "w"), ensure_ascii=False, indent=1)
    print(f"→ {result_path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
