# Conservatism: An Alternate History

A total-conversion mod of [Social Democracy: An Alternate History](https://github.com/aucchen/social_democracy_alternate_history) by Autumn Chen. Instead of the SPD in Weimar Germany, you lead Margaret Thatcher's Conservative Party in opposition, starting in **January 1978**.

Callaghan's minority Labour government survives on the Lib-Lab Pact. Inflation is falling and "Sunny Jim" is more popular than you. Parliament must be dissolved by autumn 1979. You have until then (or until Callaghan calls an early election, or you bring him down in the Commons) to win.

*Conservatism: An Alternate History* is a working title. Change it in `source/info.dry` and `out/html/index.html`.

## Playing

Each month you play one card from your hand:

- **Party Affairs**: fundraising, speaking tours, media strategy, the policy group (adopt manifesto planks), Shadow Cabinet management, target voters and the other parties.
- **The Commons**: Opposition Day debates, PMQs, devolution, pay policy and the motion of no confidence.
- **The Campaign**: the manifesto launch, the TV debate challenge and the campaign trail. Only available in the two months before polling day.
- **Shadow Cabinet** (pinned cards): Whitelaw, Joseph, Howe and Reece each have special actions, with one action every six months.

Historical events fire on their dates, including the World in Action interview, Ilford North, Saatchi & Saatchi, the 5% pay norm, Callaghan's autumn decision, the Ford strike, the Winter of Discontent, the devolution referendums, the no-confidence vote and the election. Some of them branch. If Labour leads the polls in September 1978, Callaghan may call an October election.

The current version ends at the first general election, with endings for a majority, a Unionist deal, a Liberal deal, a minority government, or defeat.

## Building

Requires Node.js (the GitHub workflow uses Node 16).

```sh
npm install          # installs dendrynexus from GitHub
npm run build        # dendrynexus make-html -> out/html/
npm run check        # static checks on the scene files (no dependencies)
```

Then open `out/html/index.html` in a browser. Some browsers block `game.json` loading from `file://`; if so, serve the folder with something like `npx http-server out/html`.

Pushing to `main` runs `.github/workflows/build.yaml`, which builds the game and deploys it to GitHub Pages. To use it, set **Settings → Pages → Source** to "GitHub Actions" in the repository.

## How it works

| File | Purpose |
| --- | --- |
| `source/scenes/root.scene.dry` | The starting state (January 1978): parties, factions, social grades, the Commons, the economy |
| `source/scenes/post_event.scene.dry` | The monthly tick: dates, timers, faction dissent, economy and opinion drift, then routing to events or the main hand |
| `source/scenes/election_algorithm.scene.dry` | The election model: vote shares and the regional seat model |
| `source/scenes/main.scene.dry` | The hand and the decks |
| `source/scenes/status.scene.dry` | The sidebar tabs: Main, Politics, Industry, Polls |
| `source/scenes/party_affairs/`, `commons/`, `campaign/` | Cards |
| `source/scenes/advisors/` | Shadow Cabinet pinned cards |
| `source/scenes/events/` | Dated and conditional events, including the general election |
| `source/scenes/game_over.scene.dry` | Endings and achievements |
| `source/scenes/library.scene.dry` | In-game background reading |
| `tools/check_scenes.js` | Static checker (run with `npm run check`) |

**Votes.** Support for each party is tracked across four social grades: AB (professional), C1 (white-collar), C2 (skilled manual) and DE (unskilled and pensioners). Cards and events move these numbers. Each month, support drifts 8% of the way back towards its January 1978 level, so gains have to be sustained. When the Conservative lead grows, Labour pushes back.

**Seats.** There are eleven regions, each starting from its approximate October 1974 result and moving with the national swing (the South swings harder than the North). Within each region, seats follow a "square law", with efficiency factors for the thinly spread Liberals and the concentrated Plaid vote. The Liberals get a stronghold floor, and Northern Ireland's 12 seats are fixed. Given the real vote shares, the model gives:

| Election | Model (Con/Lab/Lib/SNP/PC) | Actual |
| --- | --- | --- |
| Oct 1974 | 276 / 316 / 15 / 12 / 4 | 277 / 319 / 13 / 11 / 3 |
| Feb 1974 | 303 / 293 / 17 / 6 / 4 | 297 / 301 / 14 / 7 / 2 |
| 1979 | 357 / 250 / 11 / 3 / 2 | 339 / 269 / 11 / 2 / 2 |

The regional baseline figures are approximations and are worth refining against real constituency data.

**Balance** (from automated playtests on normal difficulty): random play wins a majority about 70% of the time and loses about 13%. Doing nothing at all wins a majority only about 30% of the time. A strong strategy averages around 358 seats.

## Adding content

A new card is one file. Here is a minimal example of a Party Affairs card:

```
title: My New Card
new-page: true
is-card: true
tags: party_affairs
view-if: my_card_timer <= 0
on-arrival: my_card_timer = 4; month_actions += 1

= My New Card

Some text.

- @option_a: First option.
- @easy_discard

@option_a
on-arrival: c2_con += 3*(1-dissent)

What happened.
```

Add `'my_card'` to `Q.timers` in `root.scene.dry` and initialise any new variables there. Then run `npm run check`.

Events use `tags: event`, a `view-if` on `time` (1 = January 1978, 13 = January 1979) and `max-visits: 1`.

## Not done yet

- The years in government (1979 onwards).
- Images and music. Card and event art is optional in dendrynexus and none is included yet.
- Leadership challenges, a full Shadow Cabinet reshuffle system, by-elections beyond Ilford North, and the National Front as a separate party.
- The build hasn't yet been run end-to-end with dendrynexus. The scene files pass the static checker and an automated playtest harness, but the first real build may turn up syntax issues.

## Credits and licence

Based on *Social Democracy: An Alternate History* © 2024 Autumn Chen, used under the MIT License. Built with [dendrynexus](https://github.com/aucchen/dendrynexus). Uses jQuery, d3.js and d3-parliament.

MIT License; see `LICENSE`.
