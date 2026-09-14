# Malum ProjectE EMC — Forge 1.20.1

The Minecraft **1.20.1 Forge** build of the EMC addon (the repo root is the 1.21.1 NeoForge build).

Same intent as the 1.21.1 sibling — seed Malum's keystone spirits/ores/trees AND
transcribe its custom recipe types (spirit_infusion / spirit_focusing / runeworking /
favor_of_the_void) as ProjectE conversions — re-emitted in ProjectE 1.20.1 (PE1.0.1)'s
map/string shape and shipped as a **lowcodefml** data jar. Targets Malum 1.20.1-1.6.7
(needs lodestonelib + curios).

The generator is **jar-driven**: it reads the target jar's `data/malum/recipes/**` and
adapts to Malum 1.6.x's schema (plural `recipes/`, `favor_of_the_void`, `item` key,
`extra_items`, `primaryInput`/`secondaryInput`, bare spirit names). Tags come out
`forge:`-namespaced straight from the jar — no `c:`→`forge:` remap.

## Build (no Gradle / JDK)

```bash
python tools/generate_emc.py <path-to-malum-1.20.1-jar>
python tools/build_jar.py
```

## Verify

Load with ProjectE 1.20.1 + Malum (+ LodestoneLib + Curios) on a Forge 1.20.1 server and
confirm `mo.pr.PECore` parses `malum:pe_custom_conversions/malum_emc.json` without an error.

For the mod overview and support route, see the [repository README](../README.md).
