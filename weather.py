"""Open-Meteo から各基準港の天気・風・波の予報（7日分・1時間ごと）を取って weather.json に書き出す。
アプリの db ドキュメント weather/latest にこの JSON をそのまま入れる。"""
import json, time, urllib.request, pathlib

PORTS = {  # 港コード: (緯度, 経度)
    17: (35.08, 136.88), 16: (34.90, 136.83), 15: (34.87, 136.83), 14: (34.70, 136.98), 19: (34.70, 136.93),
    3: (34.68, 137.00), 13: (34.85, 136.93), 12: (34.82, 137.00), 11: (34.78, 137.17), 10: (34.78, 137.18),
    8: (34.82, 137.25), 7: (34.72, 137.33), 6: (34.63, 137.12), 1: (34.58, 137.02), 18: (34.60, 137.20),
}
UA = {"User-Agent": "Mozilla/5.0"}


def get(url):
    for _ in range(3):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
        except Exception:
            time.sleep(2)
    return None


def main():
    lats = ",".join(f"{v[0]}" for v in PORTS.values())
    lons = ",".join(f"{v[1]}" for v in PORTS.values())
    common = f"latitude={lats}&longitude={lons}&timezone=Asia%2FTokyo&forecast_days=7&timeformat=unixtime"
    wx = get("https://api.open-meteo.com/v1/forecast?" + common +
             "&hourly=weather_code,temperature_2m,precipitation_probability,precipitation,wind_speed_10m,wind_direction_10m,wind_gusts_10m&wind_speed_unit=ms")
    mar = get("https://marine-api.open-meteo.com/v1/marine?" + common + "&hourly=wave_height")
    out = {"updated": int(time.time() * 1000), "source": "Open-Meteo", "ports": {}}
    for i, p in enumerate(PORTS):
        h = wx[i]["hourly"]
        r = lambda a, n=1: [None if v is None else round(v, n) for v in a]
        d = {"t0": h["time"][0] * 1000, "code": h["weather_code"], "temp": r(h["temperature_2m"], 0),
             "pop": h["precipitation_probability"], "rain": r(h["precipitation"]), "ws": r(h["wind_speed_10m"]),
             "wd": r(h["wind_direction_10m"], 0), "wg": r(h["wind_gusts_10m"])}
        if mar and mar[i].get("hourly"):
            d["wave"] = r(mar[i]["hourly"]["wave_height"], 2)
        out["ports"][str(p)] = d
    path = pathlib.Path(__file__).with_name("weather.json")
    path.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(path, path.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
