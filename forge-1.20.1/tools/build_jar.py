"""Package the lowcodefml data jar (no compilation).

A lowcodefml mod is a plain zip: META-INF/mods.toml + pack.mcmeta + data/** + logo.
Everything under src/ is zipped verbatim. Output -> build/<mod_id>-<version>.jar.

Usage: python tools/build_jar.py
"""

import os
import zipfile

HERE = os.path.dirname(__file__)
SRC = os.path.normpath(os.path.join(HERE, "..", "src"))
BUILD = os.path.normpath(os.path.join(HERE, "..", "build"))
MOD_ID = "malum_emc"
VERSION = "0.1.0"


def main() -> None:
    os.makedirs(BUILD, exist_ok=True)
    out = os.path.join(BUILD, f"{MOD_ID}-{VERSION}-forge-1.20.1.jar")
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _dirs, files in os.walk(SRC):
            for name in files:
                full = os.path.join(root, name)
                arc = os.path.relpath(full, SRC).replace(os.sep, "/")
                z.write(full, arc)
                n += 1
    print(f"packed {n} entries -> {out}")


if __name__ == "__main__":
    main()
