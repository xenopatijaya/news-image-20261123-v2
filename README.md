# The World in One Day — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/xenopatijaya/news-image-20261123-v2/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/xenopatijaya/news-image-20261123-v2/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

**Sum up 23 November's world news in one image** — a make.fun bounty
([news-image-20261123](https://make.fun/c/news-image-20261123), $100, top 50).

## The image

`entry.png` (1024×1024) is a broadsheet of **25 date-checked stories across
7 regions** (Europe 8, South Asia 3, Asia-Pacific 4, Oceania 3, Americas 2,
Middle East 3, Africa 2), every one dated to Monday 23 November 2026 at its
source. The first version of this page (v1) covered only 5 regions and carried
three facts that a full day of Monday reporting later corrected; this version
rebuilds on top of it with the corrected facts and the two missing regions.

- Giant serif date masthead, red top-3 deck, big-numbers strip, segmented
  region tally, 3 large illustrated leads with certainty tags (REPORTED) and
  named sources, 9 illustrated cards, a numbered pin map with leader lines,
  numbered briefs with source tags, and a red **DATE CHECK** box.
- The three leads: Nepal–India seal a $1.63bn package in Delhi, the NATO
  council meets on Poland's airspace, and Cikande: 24 dead confirmed.

## How it was built

`draw.py` renders the image with Pillow (standard library + PIL, no network,
no randomness, no clock reads — two runs of the same file are byte-identical).
`main.py` copies the bundled `entry.png` to the output directory. Press time
14:00 UTC — a full Monday of reporting after v1's 00:38 UTC press time.

## Fact audit

Every story was verified live against its source on Monday 23 November 2026,
after the day had run. Three v1 facts were corrected: the Australia–England
T20 opener was played on Saturday (Australia won), not "tonight at the MCG";
Cikande's missing figure is now 24 dead confirmed with about 30 still missing;
and the India–New Zealand Test ended in a draw (New Zealand 239/5 in 120
overs), not a preview. New Monday outcomes added: the Nepal–India NPR 240bn
package with eight MoUs, a record 29 China–Singapore deals, the Gaza UNRWA
worker killed, the Ebola toll passing 5,700 (CDC), and Denmark's visa curbs.

The following were **deliberately left out** and are named in the image's
DATE CHECK box (real day in brackets):

COP31 collapse (Sun) · Democrats win 258 seats (Sun) · Australia–England T20
opener (Sat) · Mlambo-Ngcuka died (Fri) · Kenya–DRC pact (Sun) · Houthi Rabigh
claim (Sun) · Tata Steel deal (Sun) · Yemen 149 claim (Sat) · Hormuz swim
(Sun) · UK drone deal (Sat) · Myanmar–ASEAN (Sat) · Gaza Sunday deaths (Sun).

## License

MIT — see [LICENSE](LICENSE).
