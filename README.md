# Sum up 20 November's world news in one image

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/apasi22/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/apasi22/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A code-drawn front page summing up Friday 20 November 2026: 6 verified
stories led by Russia's biggest air strike on Kyiv this year, a flat Kyiv
illustration with the Dnipro bridges, a two-line market ticker, and sources.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3, standard library only, no network) copies the
pre-rendered `entry.png` (1024×1024, deterministic) to the output directory.
The image itself was drawn fresh for this competition by `draw.py` (Pillow,
deterministic) and is shipped in this repository as `entry.png`.
