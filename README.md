[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/prasadreddys/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/prasadreddys/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125)

# The World in One Page — 25 November 2026

A make.fun entry for the bounty
[Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125):
a program that writes one image to `/output/entry.png` summing up the
world's news of Wednesday 25 November 2026.

The image is a newspaper front page, drawn with Pillow by `draw_image.py`
and shipped as `entry.png`. `main.py` checks that the bundled PNG is whole
and inside the contest limits, then copies its exact bytes to the output.
No network, no clock, no randomness: two runs write identical bytes.

## The day, in one page

- **Space:** Shenzhou-24 lifts off from Jiuquan at 00:18 UTC carrying Tang
  Hongbo, Wu Yi and Muhammad Zeeshan Ali — the first Pakistani in orbit and
  the first foreign astronaut to board China's Tiangong station.
- **USA:** the CIA and ODNI found a breach of an unclassified open-source
  intelligence network, reported by the NYT; no classified data was hit.
- **Riyadh:** a Houthi strike hits a tower in the King Abdullah Financial
  District; 11 injured.
- **Gaza:** Israeli strikes kill at least nine in 24 hours, including Hamas
  security chief Naeem Abu Nahel.
- **Colombia:** about 20 hostages still held in a Cartagena supermarket
  after a failed armoured-car robbery; a Villavicencio car bomb injures 22.
- **Markets:** Washington is poised to unveil new tariffs after a probe of
  16 partners; Asian stocks slide and Nvidia falls 5.9%.

Sources, as reported on 25 Nov 2026: Reuters, AP, Al Jazeera, Dawn,
Channel News Asia, NYT.

## Run it

```sh
python3 draw_image.py   # regenerate entry.png
python3 main.py         # write /output/entry.png
```

## License

MIT — see `LICENSE`.
