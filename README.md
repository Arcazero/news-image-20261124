# The World Today — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Arcazero/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Arcazero/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A single 1024×1024 front page that sums up Tuesday 24 November 2026.

## The six stories

- **Poland** — NATO sends AWACS radar jets to Poland after Russian missiles landed there.
- **Weather** — Thanksgiving storms threaten both US coasts.
- **USA** — Trump halts the Iowa lead-azide detonation.
- **Gulf** — Iran vows to defy the US naval blockade.
- **Libya** — Ukraine sinks a Russian warship in Benghazi port.
- **Asia** — the Indonesia factory fire that killed 24.

Every story was checked against reporting dated 24 November 2026 (Reuters, CNN, US National Weather Service). The weather strip shows real Open-Meteo forecast figures for five of the story cities. Each card's picture was generated for this entry and carries no lettering — every word on the page is drawn by `draw.py` in DejaVu.

## How it works

`draw.py` (Python + Pillow) composes the sheet from the illustrations in `assets/` and writes `entry.png`. `main.ts` (Node 22, standard library only) hands that file to the grader byte-for-byte.

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ackjrmv3&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
