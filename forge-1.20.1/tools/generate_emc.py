"""Generate data/malum/pe_custom_conversions/malum_emc.json for ProjectE on
Minecraft 1.20.1 (PE1.0.1).

Same intent as the 1.21.1 sibling — seed Malum's keystone primitives AND transcribe
its custom recipe types (spirit_infusion / spirit_focusing / runeworking /
favor_of_the_void) as ProjectE conversions — but adapted to Malum 1.20.1-1.6.x's
recipe schema and emitted in ProjectE 1.20.1's map/string shape (grounded on
PE1.0.1's bundled defaults.json / metals.json).

Malum 1.6.x schema differences handled here vs the 1.21.1 jar:
  - recipe dir is data/malum/recipes/ (plural)
  - the void type is malum:favor_of_the_void (not void_favor)
  - item ids use the "item" key (not "id")
  - extra spirit-infusion items use "extra_items" (not extraInputs)
  - runeworking uses primaryInput + secondaryInput
  - spirit entries carry a bare element name ("aerial") -> malum:aerial_spirit
  - tags in this jar are already forge:/minecraft: namespaced (no c:-> forge: remap)

Usage: python tools/generate_emc.py [path/to/malum-1.20.1.jar]
"""

import glob
import json
import os
import sys
import tempfile
import zipfile
from collections import OrderedDict

JAR = (
    sys.argv[1]
    if len(sys.argv) > 1
    else os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "_research",
        "v1201-hosts",
        "malum-1.20.1-1.6.7.jar",
    )
)
OUT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "src",
    "data",
    "malum",
    "pe_custom_conversions",
    "malum_emc.json",
)

# Keystone primitives (P2; ProjectE anchors: stone 1, log 32, leaves 1, iron 256,
# gold 2048, diamond 8192). Spirits are mob-harvested and propagate everywhere via
# the transcribed recipes, so they are valued moderately with a rarity gradient.
# (1.6.x names: chunk_of_brilliance is the raw brilliance drop; soulwood_growth is
# the soulwood "sapling".)
BEFORE = {
    "aerial_spirit": 64,
    "aqueous_spirit": 64,
    "earthen_spirit": 64,
    "arcane_spirit": 96,
    "infernal_spirit": 96,
    "umbral_spirit": 96,
    "sacred_spirit": 128,
    "wicked_spirit": 128,
    "eldritch_spirit": 160,
    "raw_soulstone": 128,  # soulstone ore drop
    "cthonic_gold": 256,  # cthonic gold ore drop
    "chunk_of_brilliance": 512,  # brilliant stone drop (high)
    "runewood_log": 32,
    "soulwood_log": 32,
    "runewood_leaves": 1,
    "soulwood_leaves": 1,
    "soulwood_growth": 32,
    "tainted_rock": 4,
    "blighted_gunk": 16,
    # clinging_blight は BlockItem を持たない設置専用ブロックで、ProjectE が load error を出す
    # （1.21.1 セルで実測。1.6.7 も同じく item.malum.clinging_blight が無い）。
    # 落とし物は blighted_gunk なので上の値で足りる。
}

INCLUDE_TYPES = {
    "malum:spirit_infusion",
    "malum:spirit_focusing",
    "malum:runeworking",
    "malum:favor_of_the_void",
}
# stateful / gear outputs to skip (durability or component state)
EXCLUDE_SUBSTR = (
    "staff",
    "scythe",
    "_helmet",
    "_chestplate",
    "_leggings",
    "_boots",
    "_jar",
    "ring",
    "totem",
    "banner",
    "fractured",
    "soul_of_a",
    "mnemonic",
    "_pick",
    "_axe",
    "_shovel",
    "_hoe",
    "_sword",
    "knife",
)


def key_of(node: dict) -> str | None:
    """ProjectE 1.20.1 NSS string key for an ingredient/result node."""
    if not node:
        return None
    if node.get("item"):
        return node["item"]
    if node.get("id"):
        return node["id"]
    if node.get("tag"):
        return "#" + node["tag"]
    return None


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(JAR) as z:
            for n in z.namelist():
                if n.startswith("data/malum/recipes/") and n.endswith(".json"):
                    z.extract(n, tmp)
        recdir = os.path.join(tmp, "data", "malum", "recipes")
        convs = []
        for f in glob.glob(os.path.join(recdir, "**", "*.json"), recursive=True):
            try:
                o = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            if o.get("type") not in INCLUDE_TYPES:
                continue
            res = o.get("output") or o.get("result")
            out = key_of(res) if isinstance(res, dict) else res
            if not out or not out.startswith("malum:"):
                continue
            short = out.split(":", 1)[1]
            if any(s in short for s in EXCLUDE_SUBSTR):
                continue

            ings: "OrderedDict[str, int]" = OrderedDict()

            def add(node: dict) -> None:
                k = key_of(node)
                if k is None:
                    return
                ings[k] = ings.get(k, 0) + node.get("count", 1)

            # spirit_infusion / spirit_focusing / favor_of_the_void: input (+ extras)
            add(o.get("input"))
            for e in o.get("extra_items", []) or o.get("extraInputs", []) or []:
                add(e)
            # runeworking: primaryInput + secondaryInput
            add(o.get("primaryInput"))
            add(o.get("secondaryInput"))
            # spirits (bare element name -> malum:<name>_spirit)
            for sp in o.get("spirits", []) or []:
                t = sp.get("type", "")
                if t:
                    name = t if t.startswith("malum:") else f"malum:{t}_spirit"
                    ings[name] = ings.get(name, 0) + sp.get("count", 1)
            if not ings:
                continue

            c = OrderedDict()
            rc = res.get("count", 1) if isinstance(res, dict) else 1
            if rc > 1:
                c["count"] = rc
            c["ingredients"] = OrderedDict(ings)
            c["output"] = out
            convs.append(c)

    doc = OrderedDict()
    doc["comment"] = (
        "Malum EMC integration for ProjectE (KURONAMI). Keystone spirits/ores/trees "
        "seeded; spirit_infusion/focusing/runeworking/favor_of_the_void recipes "
        "transcribed (spirit cost counted). Durable gear / jars / curios have no EMC."
    )
    doc["values"] = {"before": {f"malum:{k}": v for k, v in BEFORE.items()}}
    doc["groups"] = {
        "malum_recipes": {
            "comment": "Transcribed Malum custom recipes for EMC derivation.",
            "conversions": convs,
        }
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(doc, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(
        f"primitives={len(BEFORE)} conversions={len(convs)} -> {os.path.normpath(OUT)}"
    )


if __name__ == "__main__":
    main()
