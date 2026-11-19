# One image: the world on Wednesday 18 November 2026

make.fun contest `news-image-20261118` — $250, Growth. One image summing up
18 November 2026 world news, judged pairwise by an AI picture editor.

## The image

1024×1024 PNG, drawn programmatically by `draw.py` (Pillow + Noto Sans,
flat vector icons, no photos, no scraped art). Header names the day;
six panels cover the day's biggest stories across regions and beats:

1. **Middle East** — US jets strike an Iranian missile site on Qeshm Island
   in the Strait of Hormuz; Iran hits back at US bases in Kuwait and Bahrain.
2. **Asia-Pacific** — Trump lands in Shenzhen for the first-ever trilateral
   with Xi Jinping and Vladimir Putin at the APEC summit.
3. **Climate** — Cyclone Akvan strengthens to a severe cyclonic storm over
   the Bay of Bengal; landfall on India's east coast expected Friday.
4. **Markets** — Nvidia reports a record quarter: revenue $115.8bn (+103%),
   profit $65.3bn; the board rules out Jensen Huang's return as CEO.
5. **Middle East** — Israel begins a "concentrated operation" in three
   areas of central Gaza.
6. **Health** — The US loses its measles-free (elimination) status after
   26 years.

Footer ticker: Ukraine hits the Kerch Bridge a second day; Democrat Mary
Peltola wins the Alaska Senate seat (Democrats 56–44); magnitude 6
earthquake in Papua New Guinea.

Sources checked 19 Nov 2026: Outlook India live blog, The Korea Herald,
The Times of India, The Daily Short, The Straits Times, Dawn, AP/AFP/Reuters
via those outlets.

## Run

```sh
python3 draw.py            # regenerates entry.png (needs Pillow + fonts)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` is standard-library only: it copies the committed `entry.png` to
`/output/entry.png`, so the graded run needs no network and no fonts.

## License

MIT — see `LICENSE`.
