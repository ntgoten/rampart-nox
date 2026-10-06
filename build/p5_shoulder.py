# Shoulder caps (Cloth_5, Pattern_KnittedLeather_02) -> darker purple than the doublet: Pattern_KnittedLeather_968_ALBD
import sys, os, struct, numpy as np, bpy
sys.path.insert(0, r"A:\.ClaudeModding\tools\blender-5.0.1-windows-x64\portable\scripts\addons")
tu = __import__("RE-Mesh-Editor-main.modules.tex.re_tex_utils", fromlist=["x"])
tc = __import__("RE-Mesh-Editor-main.modules.ddsconv.directx.texconv", fromlist=["x"])
R = "A:/.ClaudeModding/dd2-mods/new-items/rampart-purple/"
SRC = [p for p in __import__("glob").glob("A:/.ClaudeModding/dd2-extract/DD2_EXTRACT/re_chunk_000/natives/stm/**/pattern_knittedleather_02_albd.tex.251211553", recursive=True)][-1]
OUT = R + "mod/natives/stm/character/_kit/_equipment/tops/266/Pattern_KnittedLeather_968b_ALBD.tex.251211553"
W_ = R + "work/"; os.makedirs(W_ + "raw", exist_ok=True)
conv = tc.Texconv()
tu.convertTexFileToDDS(SRC, W_ + "k02.dds")
raw = conv.convert_to_dds(file=W_ + "k02.dds", dds_fmt="R8G8B8A8_UNORM", out=W_ + "raw", no_mip=True, verbose=False)
d = open(raw, "rb").read(); h, w = struct.unpack_from("<II", d, 12); off = 128 + (20 if d[84:88] == b"DX10" else 0)
a = np.frombuffer(d, np.uint8, h * w * 4, off).reshape(h, w, 4).astype(np.float32) / 255.0
rgb = a[..., :3]
L = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
t = np.clip(L / max(np.percentile(L, 60), 1e-4), 0, 3.0)
stops = np.array([0.0, 0.35, 1.0, 3.0])
cols = np.array([[0.03, 0.015, 0.05], [0.09, 0.045, 0.135], [0.155, 0.08, 0.225], [0.28, 0.17, 0.38]])   # median = the doublet purple (sRGB of Color1)
for c in range(3): a[..., c] = np.interp(t, stops, cols[:, c])
mips = [a]
while min(mips[-1].shape[:2]) > 1:
    m = mips[-1]; hh, ww = m.shape[0] // 2, m.shape[1] // 2
    mips.append(m[:hh*2, :ww*2].reshape(hh, 2, ww, 2, 4).mean((1, 3)))
hdr = struct.pack("<4s7I44x2I4s5I5I", b"DDS ", 124, 0x1|0x2|0x4|0x1000|0x20000|0x8, h, w, w*4, 1, len(mips),
                  32, 0x4, b"DX10", 0, 0, 0, 0, 0, 0x1000|0x400000|0x8, 0, 0, 0, 0)
with open(W_ + "k02_src.dds", "wb") as f:
    f.write(hdr); f.write(struct.pack("<IIIII", 28, 3, 0, 1, 0))
    for m in mips: f.write((np.clip(m, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
dds = conv.convert_to_dds(file=W_ + "k02_src.dds", dds_fmt="BC7_UNORM_SRGB", out=W_ + "bc", no_mip=False, verbose=False)
tu.DDSToTex([dds], 251211553, OUT)
im = bpy.data.images.new("p", w, h); im.colorspace_settings.name = "Non-Color"; im.pixels = a[::-1].ravel()
im.filepath_raw = W_ + "k02_preview.png"; im.file_format = "PNG"; im.save()
open(R + "p5_log.txt", "w").write(f"knit {w}x{h} -> {os.path.getsize(OUT)} bytes; src mean L {L.mean():.3f}")
tc.unload_texconv()
