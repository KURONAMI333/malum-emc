<!-- Modrinth/CurseForge description source of truth. Paste verbatim into Modrinth;
     paste into CurseForge in MARKDOWN mode. Title/summary below are the search-indexed fields. -->

<!-- TITLE (<=64 chars): Malum ProjectE EMC -->
<!-- SUMMARY (search-indexed, plain text): ProjectE EMC for Malum: values the spirits, ores and trees and transcribes its spirit-infusion recipes so its content gains EMC. -->

# Malum ProjectE EMC

Play [Malum](https://www.curseforge.com/minecraft/mc-mods/malum) with [ProjectE](https://modrinth.com/mod/projecte) and find none of its spirits or arcane materials have an EMC value? This add-on fixes that.

## What it does

A **data-only** add-on that teaches ProjectE about Malum:

- **Seeds the keystone resources** — the nine harvested Spirits, Soulstone / Cthonic Gold / Brilliance ores, and the Runewood / Soulwood trees.
- **Transcribes Malum's custom recipes** (Spirit Infusion, Spirit Focusing, Runeworking, Void Favor) as ProjectE conversions — including the spirit cost — so infused materials, runes and processed items **derive their EMC automatically** instead of being invisible to ProjectE.
- **Stateful gear has no EMC by design**: staves, scythes, soul-stained steel tools and armor, Spirit Jars and curios carry durability or stored spirit/charge state; the degraded "fractured" impetus states are also excluded.

It adds **no items, blocks or recipes** — only EMC data.

## Compatibility

| | 1.21.1 |
|---|---|
| NeoForge | ✅ |

Requires **ProjectE** and **Malum** (NeoForge 1.21.1).

## Install

Drop the jar into your `mods` folder alongside ProjectE and Malum. EMC values apply on world load — open a Transmutation Table to see them.

## Dependencies

- **ProjectE** — required
- **Malum** — required

## Scope & limitations

- NeoForge 1.21.1 only.
- EMC values are a considered first pass; balance feedback is welcome via the issue tracker.
- The end-game Soul Binding recipes (which produce stateful artifacts) and the node-smelting tag outputs are intentionally not valued.
- Tools, armor, staves, scythes, spirit jars and curios intentionally carry no EMC (see above).

## License & credits

MIT. Malum is by Sammy Semicolon; ProjectE by sinkillerj & contributors. This add-on is an independent integration and is not affiliated with either.
