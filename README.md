# Atlas of a Day — news-image-20261125 (variant B)

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/prellxz-gm/news-image-20261125-b/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/prellxz-gm/news-image-20261125-b/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for the [news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125):
a world-map-led front page for **Wednesday, 25 November 2026**.

## What it is

"Atlas of a Day" — a simplified world map as the centrepiece, with
numbered pins at the location of each of the 12 verified stories of the
day, and numbered story cards below the map (headline + one-line summary
+ source tag). The Hormuz / Yemen thread (stories 1–3) is the visual
anchor: red hero pins clustered on the Arabian Peninsula, with
amber-tinted hero cards.

Stories covered (all reported Wednesday, 25 November 2026):

1. Two tankers hit mines in the Strait of Hormuz — Reuters
2. Houthis strike Ras Tanura refinery and Riyadh — Reuters
3. Saudi-led coalition strikes Hodeidah port — WireMinute
4. All hostages freed in dawn raid in Cartagena — Reuters / AFP
5. Pakistan's first astronaut reaches Tiangong — Reuters / Xinhua
6. Markets slide on a fresh US tariff threat — Reuters
7. Bangladesh garment wage rises 36% — WireMinute
8. Australia–Solomon Islands security treaty signed — WireMinute
9. Russian jets enter South Korea air defence zone — SRI
10. Three bodies found in flooded Bogor gold mine — Reuters
11. Hong Kong mourns 168 dead, a year after Tai Po fire — Reuters
12. Iraq orders federal forces to seize Kurdish oilfields — Starlit Daily

## How it works

`main.py` (Python 3.13 + PIL 10.2.0) draws `entry.png` from scratch —
no image assets, no network, no timestamps, no randomness. The date
string is embedded. Running it twice produces byte-identical output.

```sh
MAKEFUN_OUTPUT_DIR=/output python3 main.py
```

Output: 1024×1024 PNG, ≤ 1 MiB.
