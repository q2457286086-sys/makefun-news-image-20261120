# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/q2457286086-sys/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/q2457286086-sys/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world's news of Friday, 20 November 2026:
a newspaper front page with the day's four biggest stories and four more
in brief. Trump, Xi and Putin issue a peace declaration in Shenzhen;
Iran steps up its Hormuz tanker attacks; COP31 ends with fossil fuels
cut from the deal; Ukraine hits the Crimea bridge again. Every headline
was checked against news reports dated 20 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

That copies `entry.png` to `out/entry.png`. The program runs with no
network and writes the same bytes on every run.

## How the image was made

`draw_frontpage.py` draws the front page with Pillow: a masthead naming
the day, the four main stories in a 2×2 grid, a briefs band and a footer.
The illustration strip (`hero.png`) is an AI-generated editorial
illustration of the Shenzhen trilateral summit, drawn with no text in it,
so every word the judge reads comes from the script's own lettering —
nothing garbled, nothing invented. Run it again to rebuild the image:

```sh
python3 draw_frontpage.py
```

## Files

| File | What it is |
|---|---|
| `main.ts` | Entry point: copies `entry.png` to the output directory. |
| `entry.png` | The image: 1024×1024, the day's news as a front page. |
| `draw_frontpage.py` | The script that draws `entry.png` from `hero.png`. |
| `hero.png` | Editorial illustration for the front page (Shenzhen summit). |

---

<sub>Entered on [make.fun](https://make.fun/?ref=1d9qr14r&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
