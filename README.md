# ProjectE: EMC for Malum

Play [Malum](https://www.curseforge.com/minecraft/mc-mods/malum) with [ProjectE](https://www.curseforge.com/minecraft/mc-mods/projecte) and none of its spirits or arcane materials have an EMC value. This data-only add-on fixes that.

- **Seeds keystone resources** — the nine harvested Spirits, Soulstone and Brilliance materials, Runewood and Soulwood, and the Cthonic Gold storage block on NeoForge 1.21.1.
- **Transcribes Malum's custom recipes** — Spirit Infusion, Spirit Focusing, Runeworking, Void Favor — as ProjectE conversions, including spirit costs. Many infused materials, runes, and processed items can then derive an EMC value from their inputs.
- **Stateful gear carries no EMC by design**: staves, scythes, soul-stained steel tools and armor, Spirit Jars, and curios hold durability or stored spirit/charge state; the degraded "fractured" impetus states are excluded too.

It adds no items, blocks, or recipes — only EMC data. Values apply on world load; open a Transmutation Table to see them.

**Dependencies**

- [ProjectE](https://www.curseforge.com/minecraft/mc-mods/projecte) — required
- [Malum](https://www.curseforge.com/minecraft/mc-mods/malum) — required

The end-game Soul Binding recipes (which produce stateful artifacts) and node-smelting tag outputs are intentionally not valued. EMC values are a considered first pass; balance feedback is welcome.

On NeoForge 1.21.1, ProjectE forces Cthonic Gold items to 0 EMC because they are tagged as raw materials. The storage block has an EMC value and can be converted back into nine Cthonic Gold items, but 14 recipes that use Cthonic Gold derive an output value 256 EMC below their full ingredient cost. This limitation does not apply to the Forge 1.20.1 build, where Cthonic Gold has a working EMC value.

All Rights Reserved (free to put in any modpack, no permission or credit needed). Malum is by Sammy Semicolon; ProjectE by sinkillerj & contributors. Independent integration, not affiliated with either. Source: https://github.com/KURONAMI333/malum-emc

## Versions

The repository root contains the NeoForge 1.21.1 build. The [Forge 1.20.1 build](forge-1.20.1/README.md) is in its own subdirectory; use the JAR matching your loader and Minecraft version.

## Downloads and support

Downloads: [CurseForge](https://www.curseforge.com/minecraft/mc-mods/emc-for-malum).

For bugs and questions, comment on the [CurseForge page](https://www.curseforge.com/minecraft/mc-mods/emc-for-malum) or DM [@kuronami333 on X](https://x.com/kuronami333).

[Source](https://github.com/KURONAMI333/malum-emc) · [License](LICENSE)
