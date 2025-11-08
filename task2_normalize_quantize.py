# task2_normalize_quantize.py
import argparse, json, os
import numpy as np
import trimesh as tm

BINS_DEFAULT = 1024

def stats(name, arr):
    return {
        "name": name,
        "count": int(len(arr)),
        "min": arr.min(axis=0).tolist(),
        "max": arr.max(axis=0).tolist(),
        "mean": arr.mean(axis=0).tolist(),
        "std": arr.std(axis=0, ddof=0).tolist(),
    }

# ---------- Normalizations ----------
def minmax_0_1(V):
    vmin = V.min(axis=0)
    vmax = V.max(axis=0)
    scale = np.where((vmax - vmin) == 0, 1.0, (vmax - vmin))
    Vn = (V - vmin) / scale
    ctx = {"type": "minmax_0_1", "vmin": vmin.tolist(), "vmax": vmax.tolist()}
    return Vn, ctx

def unit_sphere_to_0_1(V):
    c = V.mean(axis=0)           # center at centroid
    Vr = V - c
    r = np.linalg.norm(Vr, axis=1).max()
    r = 1.0 if r == 0 else r
    Vunit = Vr / r               # in [-1,1] roughly (inside unit sphere)
    Vn = (Vunit + 1.0) / 2.0     # map to [0,1] for quantization
    ctx = {"type": "unit_sphere", "centroid": c.tolist(), "radius": float(r)}
    return Vn, ctx

# ---------- Quantize / Dequantize ----------
def quantize_0_1(Vn, bins):
    q = np.clip(np.floor(Vn * (bins - 1) + 1e-9), 0, bins - 1).astype(np.int32)
    return q

def dequantize_to_0_1(Q, bins):
    return Q.astype(np.float64) / (bins - 1)

# ---------- Denormalize ----------
def denorm_from_minmax_0_1(Vd, ctx):
    vmin = np.array(ctx["vmin"], dtype=np.float64)
    vmax = np.array(ctx["vmax"], dtype=np.float64)
    return Vd * (vmax - vmin) + vmin

def denorm_from_unit_sphere_0_1(Vd, ctx):
    c = np.array(ctx["centroid"], dtype=np.float64)
    r = float(ctx["radius"])
    Vunit = Vd * 2.0 - 1.0
    return Vunit * r + c

def process(mesh_path, outdir, bins):
    os.makedirs(outdir, exist_ok=True)
    mesh = tm.load(mesh_path, force='mesh')
    V = mesh.vertices.view(np.ndarray).astype(np.float64)
    F = mesh.faces if hasattr(mesh, "faces") and mesh.faces is not None else None

    base = os.path.splitext(os.path.basename(mesh_path))[0]

    # 1) Min–Max -> [0,1]
    Vn_mm, ctx_mm = minmax_0_1(V)
    Q_mm = quantize_0_1(Vn_mm, bins)
    Vd_mm = dequantize_to_0_1(Q_mm, bins)
    Vrec_mm = denorm_from_minmax_0_1(Vd_mm, ctx_mm)

    # 2) Unit-sphere -> [0,1]
    Vn_us, ctx_us = unit_sphere_to_0_1(V)
    Q_us = quantize_0_1(Vn_us, bins)
    Vd_us = dequantize_to_0_1(Q_us, bins)
    Vrec_us = denorm_from_unit_sphere_0_1(Vd_us, ctx_us)

    # Save quantized meshes (as reconstructed float meshes so viewers can load)
    def save_mesh(vertices, name_suffix):
        m = tm.Trimesh(vertices=vertices, faces=F, process=False)
        out_path = os.path.join(outdir, f"{base}_{name_suffix}.ply")
        m.export(out_path)
        return out_path

    out_mm_norm = save_mesh(Vn_mm, "minmax_norm")      # normalized [0,1]
    out_mm_quant = save_mesh(Vrec_mm, "minmax_quant")  # reconstructed after Q/DQ/DN
    out_us_norm = save_mesh(Vn_us, "unitsphere_norm")
    out_us_quant = save_mesh(Vrec_us, "unitsphere_quant")

    # Errors (Task 3 preview; we’ll plot later)
    mse_mm = float(np.mean((V - Vrec_mm) ** 2))
    mse_us = float(np.mean((V - Vrec_us) ** 2))
    mae_mm = float(np.mean(np.abs(V - Vrec_mm)))
    mae_us = float(np.mean(np.abs(V - Vrec_us)))

    # Per-axis errors (useful later)
    per_axis = {
        "mse_mm": np.mean((V - Vrec_mm) ** 2, axis=0).tolist(),
        "mse_us": np.mean((V - Vrec_us) ** 2, axis=0).tolist(),
        "mae_mm": np.mean(np.abs(V - Vrec_mm), axis=0).tolist(),
        "mae_us": np.mean(np.abs(V - Vrec_us), axis=0).tolist(),
    }

    # Save a small report JSON
    report = {
        "file": mesh_path,
        "bins": bins,
        "original": stats("original", V),
        "norm_minmax": stats("norm_minmax_[0,1]", Vn_mm),
        "norm_unitsphere": stats("norm_unitsphere_[0,1]", Vn_us),
        "errors": {
            "mse_minmax": mse_mm, "mae_minmax": mae_mm,
            "mse_unitsphere": mse_us, "mae_unitsphere": mae_us,
            "per_axis": per_axis
        },
        "outputs": {
            "minmax_normalized": out_mm_norm,
            "minmax_quantized_recon": out_mm_quant,
            "unitsphere_normalized": out_us_norm,
            "unitsphere_quantized_recon": out_us_quant
        },
        "contexts": {"minmax": ctx_mm, "unitsphere": ctx_us}
    }
    with open(os.path.join(outdir, f"{base}_task2_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nSaved:")
    for k, v in report["outputs"].items():
        print(" -", k, "->", v)
    print("\nErrors (lower is better):")
    print(f" MSE  Min–Max : {mse_mm:.8f}")
    print(f" MSE  UnitSphere: {mse_us:.8f}")
    print(f" MAE  Min–Max : {mae_mm:.8f}")
    print(f" MAE  UnitSphere: {mae_us:.8f}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mesh", required=True, help="Path to .obj")
    ap.add_argument("--outdir", default="outputs_task2", help="Where to save results")
    ap.add_argument("--bins", type=int, default=BINS_DEFAULT)
    args = ap.parse_args()
    process(args.mesh, args.outdir, args.bins)
