# Rampart Purple: Rampart Breaker's own shirt (tops_528_wb_m + sleeves tops_002_am_m) recoloured to the reference's
# dark purple by changing only material colour parameters (recolour-shader Color slots, pattern/detail BaseColor
# tints). New skins tops_968_wb_m_00 / tops_968_am_m_00 (copies of Rampart's), registered by the Lua under own IDs.
import bpy, os, re
X = "A:/.ClaudeModding/dd2-extract/DD2_EXTRACT/re_chunk_000/natives/stm/"
MOD = "A:/.ClaudeModding/dd2-mods/new-items/rampart-purple/mod/natives/stm/"
T = MOD + "character/_kit/_equipment/tops/266/"
os.makedirs(T, exist_ok=True); os.makedirs(MOD + "appsystem/charaedit/ch000/parts/tops/wb/skin", exist_ok=True)
os.makedirs(MOD + "appsystem/charaedit/ch000/parts/tops/am/skin", exist_ok=True)
log = []
# dark purple (linear values, like the vanilla near-black ones): main cloth, its darker shade, lighter trims
P_MAIN, P_DARK, P_TRIM = (0.020, 0.008, 0.042, 1.0), (0.012, 0.005, 0.026, 1.0), (0.045, 0.026, 0.075, 1.0)
TINT = (0.42, 0.30, 0.62, 1.0)          # multiplier for the textured (pattern / detail) cloth: purple, darker
RECOLOR = {
    "wb_528_0_0_Cloth_1_mat": {"Color1": P_MAIN, "Color2": P_DARK, "Color3": P_TRIM, "Color4": P_TRIM,
                               "Color5": (0.26, 0.13, 0.013, 1.0)},   # piping along the panel edges (mask 2 green): dark gold
    "wb_528_0_0_Cloth_3_mat": {"Color1": P_TRIM, "Color2": P_DARK, "Color3": P_TRIM},
    "wb_528_0_0_Cloth_5_mat": {"BaseColor": (1.0, 1.0, 1.0, 1.0)},   # shoulder caps: recoloured pattern (p5), no tint
    "am_002_0_0_Cloth_mat": {"BaseColor": TINT},
    "am_002_0_0_skin_mat": {"BaseColor": (1.0, 1.0, 1.0, 1.0)},   # sleeve knit: no grey multiplier (it hid the purple)
}
def build(src, newname):
    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.re_mdf.importfile(files=[{"name": os.path.basename(src)}], directory=os.path.dirname(src))
    c = [c for c in bpy.data.collections][0]
    for o in c.objects:
        m = o.re_mdf_material
        for p in m.propertyList_items:
            v = RECOLOR.get(m.materialName, {}).get(p.prop_name)
            if v is not None:
                p.color_value = v; log.append(f"{m.materialName}.{p.prop_name} -> {v}")
        for t in m.textureBindingList_items:      # knitted leather (vest panels, sleeve knit): darker purple pattern (p3)
            if t.path.lower().endswith("pattern_knittedleather_266_albd.tex"):
                t.path = "Character/_kit/_equipment/tops/266/Pattern_KnittedLeather_968_ALBD.tex"; log.append(f"{m.materialName}: knit -> 968")
            if t.path.lower().endswith("pattern_knittedleather_02_albd.tex"):
                t.path = "Character/_kit/_equipment/tops/266/Pattern_KnittedLeather_968b_ALBD.tex"; log.append(f"{m.materialName}: knit02 -> 968b")
    c.name = newname
    fp = T + newname + ".51"
    bpy.ops.re_mdf.exportfile(filepath=fp, targetCollection=c.name)
    for p in os.listdir(T):
        if ".001" in p: os.replace(T + p, fp)
    log.append(f"{newname}: {os.path.getsize(fp)} bytes")
build(X + "character/_kit/_equipment/tops/266/tops_266_wb_m_00.mdf2.51", "tops_968_wb_m_00.mdf2")
build(X + "character/_kit/_equipment/tops/266/tops_266_am_m_00.mdf2.51", "tops_968_am_m_00.mdf2")
for part in ("wb", "am"):
    d = open(X + f"appsystem/charaedit/ch000/parts/tops/{part}/skin/tops_266_{part}_m_00.pfb.18", "rb").read()
    a, b = f"tops_266_{part}_m_00".encode("utf-16le"), f"tops_968_{part}_m_00".encode("utf-16le")
    assert a in d; d = d.replace(a, b)
    open(MOD + f"appsystem/charaedit/ch000/parts/tops/{part}/skin/tops_968_{part}_m_00.pfb.18", "wb").write(d)
    strs = [m.group().decode('utf-16le') for m in re.finditer(rb'(?:[ -~]\x00){4,}', d)]
    log.append("pfb " + part + ": " + str(strs))
open("A:/.ClaudeModding/dd2-mods/new-items/rampart-purple/p1_log.txt", "w").write("\n".join(log))
