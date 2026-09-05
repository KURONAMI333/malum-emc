"""Generate data/malum/pe_custom_conversions/malum_emc.json.

Malum's content is gated behind custom recipe types that ProjectE can't auto-derive
(spirit_infusion, spirit_focusing, runeworking, void_favor), so we both seed the
keystone primitives (the 9 spirits, ores, trees) AND transcribe those custom recipes
as ProjectE conversions — counting the spirit COST as items (malum:<x>_spirit).

Excludes: durable gear / NBT-state outputs by id pattern, soul_binding (end-game
stateful artifacts), node_smelting/blasting (tag outputs), unchained_transmutation
(vanilla outputs), spirit_repair (durability op).

Usage: python tools/generate_emc.py [path/to/malum.jar]
ProjectE NSS: tags use {type:"projecte:item","tag":...}. See PROJECTE_EMC_NOTES.md.
"""

import json
import os
import zipfile
import glob
import tempfile
from collections import OrderedDict

JAR = (
    os.sys.argv[1]
    if len(os.sys.argv) > 1
    else r"C:\Users\naoki\curseforge\minecraft\Instances\2605_nf21_Magi\mods\malum-1.21.1-1.8.2.jar"
)
OUT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "src",
    "main",
    "resources",
    "data",
    "malum",
    "pe_custom_conversions",
    "malum_emc.json",
)

# Keystone primitives (P2; ProjectE anchors: stone 1, log 32, leaves 1, iron 256,
# gold 2048, diamond 8192). Spirits are mob-harvested and propagate everywhere via
# the transcribed recipes, so they are valued moderately with a rarity gradient.
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
    # malum 1.8.2 は raw_soulstone / raw_brilliance / cthonic_gold / cthonic_gold_fragment を
    # c:raw_materials に直接登録しており、ProjectE の RawMaterialsBlacklistMapper が実行時に
    # 0 を強制する。値は blacklist に掛からない下流へ、比に応じて換算して移す。
    #   raw_soulstone 128  -> 精錬 1:2 -> refined_soulstone 64
    #   raw_brilliance 512 -> 精錬 1:2 -> refined_brilliance 256
    #   cthonic_gold 256   -> 9個クラフト -> block_of_cthonic_gold 2304
    # cthonic_gold は下流に精錬形が無く、fragment も同じく blacklist なので、値を持てるのは
    # 保管ブロックだけ。EMC での入手経路は復活するが、cthonic_gold 自体を材料に取る
    # spirit_infusion 系の産出物は 0 のまま導出される（部分的な復旧）。MALUM_EMC_DECISIONS.md 参照。
    "refined_soulstone": 64,  # soulstone ore drop (raw 128 / 2)
    "block_of_cthonic_gold": 2304,  # cthonic gold ore drop (256 x 9)
    "refined_brilliance": 256,  # brilliant stone drop, high (raw 512 / 2)
    "runewood_log": 32,
    "soulwood_log": 32,
    "runewood_leaves": 1,
    "soulwood_leaves": 1,
    "soulwood_sapling": 32,
    "tainted_rock": 4,
    "blighted_gunk": 16,
    # clinging_blight は BlockItem を持たない設置専用ブロックで、ProjectE が
    # 「Registry minecraft:item does not contain element malum:clinging_blight」で
    # load error を出していた（2026-09-06 実測）。落とし物は blighted_gunk なので上の値で足りる。
}

INCLUDE_TYPES = {
    "malum:spirit_infusion",
    "malum:spirit_focusing",
    "malum:runeworking",
    "malum:void_favor",
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


def nss_item(idv):
    return {"type": "projecte:item", "id": idv}


def nss_tag(tag):
    return {"type": "projecte:item", "tag": tag}


def add(acc, key_obj, n):
    k = json.dumps(key_obj, sort_keys=True)
    acc[k] = acc.get(k, [key_obj, 0])
    acc[k][1] += n


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(JAR) as z:
            for n in z.namelist():
                if n.startswith("data/malum/recipe/") and n.endswith(".json"):
                    z.extract(n, tmp)
        recdir = os.path.join(tmp, "data", "malum", "recipe")
        convs = []
        for f in glob.glob(os.path.join(recdir, "**", "*.json"), recursive=True):
            try:
                o = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            if o.get("type") not in INCLUDE_TYPES:
                continue
            res = o.get("result")
            out = res.get("id") if isinstance(res, dict) else res
            if not out or not out.startswith("malum:"):
                continue
            short = out.split(":", 1)[1]
            if any(s in short for s in EXCLUDE_SUBSTR):
                continue
            acc = OrderedDict()

            def ingest(node):
                if not node:
                    return
                cnt = node.get("count", 1)
                if "item" in node:
                    add(acc, nss_item(node["item"]), cnt)
                elif "tag" in node:
                    add(acc, nss_tag(node["tag"]), cnt)

            ingest(o.get("input"))
            for e in o.get("extraInputs", []) or []:
                ingest(e)
            for sp in o.get("spirits", []) or []:
                t = sp.get("type", "")
                if t.startswith("malum:"):
                    add(acc, nss_item(t + "_spirit"), sp.get("count", 1))
            if not acc:
                continue
            ings = []
            for _, (obj, amt) in acc.items():
                e = dict(obj)
                if amt > 1:
                    e["amount"] = amt
                ings.append(e)
            c = OrderedDict()
            rc = res.get("count", 1) if isinstance(res, dict) else 1
            if rc > 1:
                c["count"] = rc
            c["ingredients"] = ings
            c["output"] = {"type": "projecte:item", "id": out}
            convs.append(c)

    doc = OrderedDict()
    doc["replace"] = False
    doc["comment"] = (
        "Malum EMC integration for ProjectE (KURONAMI). Keystone spirits/ores/trees "
        "seeded; spirit_infusion/focusing/runeworking/void_favor recipes transcribed "
        "(spirit cost counted). Durable gear / jars / curios have no EMC."
    )
    doc["values"] = {
        "before": [
            {"type": "projecte:item", "emc_value": v, "id": f"malum:{k}"}
            for k, v in BEFORE.items()
        ]
    }
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
