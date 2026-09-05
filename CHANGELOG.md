# Changelog

## v0.1.2

- Moved the soulstone and brilliance anchors from Raw Soulstone and Raw Brilliance to Refined Soulstone and Refined Brilliance. Malum 1.8.2 puts both raw items in the raw-materials tag, which ProjectE forces to zero, so the old values never applied and both lines went unpriced. One raw smelts into two refined, so the per-item values are halved and the totals are unchanged.
- Moved the cthonic gold anchor to the Block of Cthonic Gold at nine times the old value. Cthonic Gold and its fragments are both in the raw-materials tag and cannot carry EMC, so the storage block is the only node in that line that can. Cthonic gold is obtainable through EMC again; the Spirit Infusion outputs that consume it still derive without its cost.
- Dropped the Clinging Blight value. It is a placed block with no item form, so ProjectE rejected the entry with a load error on every world load. The block drops Blighted Gunk, which is already valued.

## v0.1.1

- No gameplay changes. Repackaged for CurseForge distribution; the EMC data is identical to v0.1.0.

## v0.1.0

Initial release.

- ProjectE EMC integration for Malum (NeoForge 1.21.1).
- Seeds keystone primitives: the 9 spirits, soulstone/cthonic gold/brilliance ores, runewood/soulwood trees.
- Transcribes Malum's custom recipes (spirit infusion, spirit focusing, runeworking, void favor) as ProjectE conversions, counting the spirit cost, so infused content derives EMC.
- Tools / armor / staves / scythes / spirit jars / curios and fractured-impetus states intentionally left without EMC.
- End-game soul-binding artifacts and node-smelting tag outputs not valued in this version.
- Data-only: adds no items, blocks or recipes.
