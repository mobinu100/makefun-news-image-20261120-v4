# THE WORLD TODAY — 20 November 2026

[![owner](https://img.shields.io/badge/owner-mobinu100-blue)](https://github.com/mobinu100)
[![repo](https://img.shields.io/badge/repo-makefun--news--image--20261120--v4-blue)](https://github.com/mobinu100/makefun-news-image-20261120-v4)
[![bounty](https://img.shields.io/badge/bounty-news--image--20261120-green)](https://make.fun/bounty/news-image-20261120)

One image that sums up Friday, 20 November 2026's world news — a newspaper
front page drawn entirely in code (PIL, deterministic, no network, no external
images).

**Lead story:** the Trump–Xi–Putin three-way summit in Shenzhen and its peace
declaration — *"A nuclear war cannot be won and must never be fought."*

**18 stories in total:** 1 hero lead + 9 featured stories in a 3×3 grid +
8 more in the MORE strip. Every story is dated "20 NOV" in its kicker, every
figure is verified from live reporting of the day (ICJ 9–6 Myanmar genocide
ruling, Anthropic's IPO debut at $83 / $111.50 open / $97.17 close, Cyclone
Akvan's Odisha landfall, the Senate's 51–48 Iran war-powers vote, the Houthi
strike on Riyadh's PIF Tower, Voyager 1 crossing one light-day, JAXA calling
off the Hayabusa2 landing, GTA VI's 24.6M launch-day copies), and every number
appears in exactly one place on the page.

## Run

```bash
python3 generate.py        # draws entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/entry.png
```

## Bounty

[news-image-20261120 on make.fun](https://make.fun/bounty/news-image-20261120?ref=8qvwkc7x)
