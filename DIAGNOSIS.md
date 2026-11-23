# v2 DIAGNOSIS — news-image-20261123 (23 Nov 2026, ~13:30 UTC / 20:30 WIB)

## Round 1 result (v1)
Submission 01a205ef, rank 1,832/7,226, judge win rate 0.583124. v1 loses 42% of
head-to-heads. The 22 Nov proxy bar (~988k for #50) is NOT the same scale as
round 1's Bradley-Terry fit — but the gap is real: v1 is mid-pack, not top-50.

## What v1 looks like at judge size (viewed full / 480px / 300px)
- 480px: masthead, big numbers, lead headlines legible. Cards 4-13 body text,
  briefs 14-30, the timeline strip, DATE CHECK items: all unreadable grey mush.
  ~60% of the page's text is dead weight at judge size.
- 300px: ONLY masthead, big numbers, lead headlines survive. Everything else
  is texture.
- Illustrations are flat abstract blobs (NATO = oval + flags; Cikande = beige
  box; Nepal = lone dome). No storytelling detail. The 22 Nov winners' craft
  lever was full multi-element scene illustrations; v1 has none.
- Timeline strip ("MONDAY, AROUND THE CLOCK...") is microscopic — pure clutter.
- Map pins cluster hard in Europe/South Asia; briefs are 17 lines of tiny type.
- Breadth: 5 regions vs winners' 7 — a criterion-2 loss on the judge's order.

## v1 FACT ERRORS found in the fresh audit (must be fixed, not carried over)
- AUS-ENG T20 "tonight at the MCG" was WRONG: the opener was played SAT 21 Nov
  (Australia won, Chaudhary 66 + 2-21). v1 printed a Saturday match as Monday.
- Cikande "36 missing" is superseded: Monday confirms 24 DEAD, ~30 missing,
  29 safe / 5 in hospital, suspected AC short circuit (Reuters, Mon).
- India-NZ was a preview in v1; the RESULT is in: DRAW, NZ 239/5 in 120 overs,
  Mitchell 49*, Phillips 26* (ESPNcricinfo, Mon).
- Nepal-India was a preview in v1; the OUTCOME is in: NPR 240bn (~$1.63bn)
  package, 8 MoUs, Joint Vision, Kandla + Paradip ports, Saryu-Kamala Express
  flagged off (MEA joint press release / Hindu BusinessLine, Mon).
- JCBC was "20+ expected" in v1; the OUTCOME is in: a RECORD 29 deals
  (PMO Singapore, Mon).
- Haigh CBI speech was a preview in v1; DELIVERED Monday: "Public control is
  not anti-business", no full nationalisation (Reuters, Mon).
- Dhaka wage was "board meets" in v1; Monday: 3rd meeting 11:30 Dhaka, owners
  said to offer Tk14,300 vs workers' Tk32,000, Gazipur protests shut 12
  factories (TBS / Prothom Alo, Mon).

## v2 DESIGN (fix the diagnosis, not the recipe)
- DROP the timeline strip entirely (unreadable).
- Leads: taller, RICH multi-element scenes (dome+columns+flags+handshake;
  council table+12 flags+star; factory+smoke+rescuers+ambulance). Headline
  26px, body 2 lines at 15px.
- Cards: 9 in a 3x3 grid (bigger cells than v1's 2x5), headline 17px bold,
  body 2 lines at 13px, mini-scene strip on top of each card.
- Briefs: 16 in 2 columns at 13.5px, one line each (2 lines max).
- DATE CHECK: 12 items, 2 rows x 6 cols, 11.5px.
- Big numbers: 6, labels 12.5px.
- Map: bigger pins (r=7), per-cluster offsets, re-inspected after render.
- 28 stories, 7 REGIONS: Europe 10, South Asia 3, Asia-Pacific 4, Oceania 4,
  Americas 2, Middle East 3, Africa 2.

## v2 STORY SET (all verified Monday 23 Nov 2026; sources in audit file)
LEADS: 1 Nepal-India $1.63bn (S Asia) | 2 NATO council on Poland (Europe) |
3 Cikande 24 dead confirmed (APAC)
CARDS 4-12: 4 Dymer 11 dead (Europe) | 5 Wellington Test drawn (Oceania) |
6 Dhaka wage talks (S Asia) | 7 Haigh public control (Europe) |
8 China-Singapore 29 deals (APAC) | 9 Gaza UNRWA worker killed (Middle East) |
10 Markets bounce back (Americas) | 11 Ebola toll passes 5,700 (Africa) |
12 Denmark visa curbs (Europe)
BRIEFS 13-28: 13 Hodeida strike 4 killed (ME) | 14 Gulf bourses up (ME) |
15 Johannesburg flags half-mast (Africa) | 16 Kyiv drone debris on schools (EU) |
17 Odesa schools remote (EU) | 18 Tokyo closed (APAC) | 19 Indonesia ship seizure
(APAC) | 20 Wadkute lying-in-state (S Asia) | 21 Canberra last sitting week
(Oceania) | 22 UN organised crime, NY (Americas) | 23 Finance Bill 2nd reading
(EU) | 24 PIP review (EU) | 25 UNSW grad school launches (Oceania) |
26 Asbestos Week opens (Oceania) | 27 Bereavement petition debate (EU) |
28 NHS trusts warn (EU)
BIG NUMBERS: 24 Cikande dead | 11 Dymer bodies | 29 JCBC deals |
32,000 Dhaka wage demand (Tk) | 239/5 NZ draw | 5,700 Ebola deaths
DATE CHECK (12, not Monday): COP31 collapsed SUN | Democrats 258 seats SUN |
AUS-ENG T20 opener SAT | Mlambo-Ngcuka died FRI | Kenya-DRC deal SUN |
Houthi Rabigh claim SUN | Tata Steel deal SUN | Yemen 149 claim SAT |
Hormuz swimmer SUN | UK drone deal SAT | Myanmar-ASEAN SAT | Gaza Sunday deaths SUN
PRESS TIME: 14:00 UTC (set at render; two renders must be byte-identical).
