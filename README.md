# Conservatism: An Alternate History

A total-conversion mod of [Social Democracy: An Alternate History](https://github.com/aucchen/social_democracy_alternate_history) by Autumn Chen. Instead of the SPD in Weimar Germany, you lead Margaret Thatcher's Conservative Party from **January 1978**. You start in opposition, win power, then govern Britain through the recession, the unions, the SDP and the South Atlantic, and finally fight for re-election.

*Conservatism: An Alternate History* is a working title. Change it in `source/info.dry` and `out/html/index.html`.

## How the game plays

Like the original, each month you play one card from your hand. Historical and conditional events fire between turns.

**Opposition (1978–79).** Callaghan's minority government survives on the Lib-Lab Pact. Build a manifesto, manage the wets and dries, court the minor parties, and decide how to play the Winter of Discontent. If Labour leads in September 1978, Callaghan may call an early election. After the devolution referendums, you can try to bring him down with a no-confidence motion.

**Taking office.** Win a majority, or govern with the Ulster Unionists, the Liberals or as a minority. Then form your Cabinet: Treasury, Employment and Industry each go to a dry or a wet. Like the ministries in the original, the ministers decide which policies you can pursue.

**Government (1979–84).** The Government Affairs deck opens:

| Card | What it does |
| --- | --- |
| The Budget | Shift tax from income to VAT, cut or raise taxes, or reflate (only with a wet Chancellor, or after a U-turn) |
| Monetary Policy | Bank Rate, the Medium-Term Financial Strategy, abolishing exchange controls |
| Public Spending | Cuts, deep cuts (dry Chancellor only), protecting the NHS, capital investment |
| Trade Union Law | A cautious Employment Act, stripping immunities (dry Employment Secretary only), ballots, talks with the TUC |
| Nationalised Industries | Bail-outs, cutting subsidies, privatisation, building coal stocks |
| Housing | Right to buy, discounts, council building, mortgage relief |
| Law and Order | Police pay, the "short sharp shock", the Nationality Act, the Scarman reforms |
| Foreign Affairs | The EEC rebate, compromise with Europe, the special relationship |
| Defence | The Nott review (which invites the Falklands), Trident, HMS Endurance, NATO spending |
| Northern Ireland, Public Sector Pay | Security vs. talks, cash limits vs. peace |
| Reshuffle | Purge the wets, bring them back, promote loyalists |
| Government Business (Commons) | Whip the rebels, keep partners on side |

Pinned Cabinet cards include Number 10, which can call a snap election after three years. Tebbit appears once he joins the Cabinet.

**The economy** runs every month. Interest rates trade inflation against jobs and the pound. The 1979 oil shock and the 1980–81 world recession hit, and recovery comes from 1982. Budget deficits feed inflation, and every January brings North Sea revenue, benefit costs and revenue from growth. Voters respond to unemployment, inflation, mortgage rates, growth and right-to-buy sales.

**Threats**, mirroring the original's coalition dissent, capital strike and coup meters:

- **Backbench rebellion** comes from angry factions, and **Cabinet revolt** from wets resisting cuts.
- **Partner discontent** builds if you govern without a majority, and can lead to a **vote of no confidence**.
- **A sterling crisis** hits if the budget reaches -5.
- **A leadership challenge** can oust you.

**Events, 1979–84:**

- **1979:** Howe's first Budget, the Clegg awards, Lancaster House, the Dublin summit, 17% Bank Rate.
- **1980:** the steel strike, the Iranian Embassy, two million unemployed, "the lady's not for turning" (or a U-turn), Foot.
- **1981:** the Gang of Four and the Alliance, the pit closures, the 1981 Budget, the hunger strike, Brixton and Toxteth, the Cabinet revolt and the September purge, Crosby.
- **1982:** three million unemployed, Hillhead, the Falklands (deterred, negotiated, won or lost).
- **1983:** recovery, the "longest suicide note", and by-elections and defections throughout.

**The end.** The game ends when you lose an election, are ousted, or win re-election. A legacy assessment covers inflation, unemployment, the unions, privatisation, the right to buy, the Falklands, Europe, and whether you turned. There are 23 achievements.

## Building

Requires Node.js (the GitHub workflow uses Node 16).

```sh
npm install          # installs dendrynexus from GitHub
npm run build        # dendrynexus make-html -> out/html/
npm run check        # static checks on the scene files (no dependencies)
```

Then open `out/html/index.html` in a browser. Some browsers block loading `game.json` from `file://`; if so, serve the folder with something like `npx http-server out/html`.

Pushing to `main` runs `.github/workflows/build.yaml`, which builds the game and deploys it to GitHub Pages. To use it, set **Settings → Pages → Source** to "GitHub Actions".

## Code layout

| Path | Purpose |
| --- | --- |
| `source/scenes/root.scene.dry` | The starting state (January 1978): every variable, including the government ones |
| `source/scenes/post_event.scene.dry` | The monthly tick: dates, timers, dissent, the opposition-era drift, the government economy, opinion, threat meters, then routing |
| `source/scenes/election_algorithm.scene.dry` | Vote shares and the regional seat model (with the 1983 boundaries and the Alliance) |
| `source/scenes/taking_office.scene.dry` | Forming the government and the Cabinet |
| `source/scenes/main.scene.dry` | The hand and the decks |
| `source/scenes/status.scene.dry` | The sidebar tabs: Main, Politics, Industry, Polls |
| `source/scenes/party_affairs/`, `commons/`, `campaign/` | Cards usable in opposition and in government |
| `source/scenes/government/` | The Government Affairs deck |
| `source/scenes/advisors/` | Shadow Cabinet and Cabinet pinned cards |
| `source/scenes/events/` | 1978–79 events and the (recurring) general election |
| `source/scenes/govt_events/` | 1979–84 events and threats |
| `source/scenes/game_over.scene.dry` | Endings, the legacy assessment and achievements |
| `tools/check_scenes.js` | Static checker (`npm run check`) |

**Votes.** Support for each party is tracked across four social grades: AB, C1, C2 and DE. Each month, support drifts 8% of the way back towards a baseline, so gains have to be sustained. Lasting shifts, like Labour's lurch left and the Alliance, move the baseline itself.

**Seats.** There are eleven regions, each starting from its approximate October 1974 result and moving with the national swing. Seats follow a square law with efficiency factors and a Liberal/Alliance stronghold floor. Given the real vote shares, the model gives:

| Election | Model (Con/Lab/Lib/SNP/PC) | Actual |
| --- | --- | --- |
| Oct 1974 | 276 / 316 / 15 / 12 / 4 | 277 / 319 / 13 / 11 / 3 |
| Feb 1974 | 303 / 293 / 17 / 6 / 4 | 297 / 301 / 14 / 7 / 2 |
| 1979 | 357 / 250 / 11 / 3 / 2 | 339 / 269 / 11 / 2 / 2 |
| 1983 (650 seats) | 414 / 189 / 26 / 2 / 2 | 397 / 209 / 23 / 2 / 2 |

The regional baselines are approximations and are worth refining against real constituency data.

## Balance

From automated playthroughs of the full game on normal difficulty (300 games per strategy):

| Strategy | Re-elected | Ousted | Lost re-election | Lost in 1979 |
| --- | --- | --- | --- | --- |
| Thatcher's historical choices | 79% | 9% | 3% | 10% |
| Random choices | 65% | 15% | 5% | 15% |
| Chasing the polls | 74% | 24% | 0% | 2% |
| Doing nothing on your own turns | 44% | 6% | 7% | 43% |

On the historical path, inflation ends near 4% and unemployment near 14%, close to the real 1983 figures. Chasing the polls avoids the recession but leaves inflation near 15%. Most of that strategy's ousters follow a lost Falklands war after the Nott defence cuts.

## Adding content

A new card is one file. Here is a minimal example of a Government Affairs card:

```
title: My New Card
new-page: true
is-card: true
tags: govt_affairs
view-if: con_in_government = 1 and my_card_timer <= 0
on-arrival: my_card_timer = 6; month_actions += 1

= My New Card

Some text.

- @option_a: First option.
- @easy_discard

@option_a
subtitle: -1 budget
on-arrival: budget -= 1; c2_con += 3*(1-dissent); wet_dissent -= 2

What happened.
```

Add `'my_card'` to `Q.timers` in `root.scene.dry` and initialise any new variables there. Then run `npm run check`.

For opposition-era cards, use `tags: party_affairs` or `commons` (add `con_in_government = 0` to `view-if` if the card only makes sense in opposition). Events use `tags: event` and a `view-if` on `time` (1 = January 1978, 17 = May 1979, 61 = January 1983).

## Not done yet

- The second term (1983–87): the miners' strike, Brighton, Westland, the Big Bang. The game ends at re-election; `Q.final_election` in `root.scene.dry` controls when.
- Images and music. Card and event art is optional in dendrynexus and none is included.
- Losing the 1979 election ends the game. In the original, defeat means continuing in opposition.
- The build hasn't yet been run end-to-end with dendrynexus. The scene files pass the static checker and an automated playtest harness that interprets them, but the first real build may still turn up syntax issues.

## Credits and licence

Based on *Social Democracy: An Alternate History* © 2024 Autumn Chen, used under the MIT License. Built with [dendrynexus](https://github.com/aucchen/dendrynexus). Uses jQuery, d3.js and d3-parliament.

MIT License; see `LICENSE`.
