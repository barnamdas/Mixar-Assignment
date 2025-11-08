# task3_reconstruct_analyze.py
import argparse, json, csv, os, math
from pathlib import Path
import numpy as np
import trimesh
import matplotlib.pyplot as plt

# ---------- helpers ----------
def minmax_norm(V):
    vmin = V.min(axis=0)
    vmax = V.max(axis=0)
    span = np.clip(vmax - vmin, 1e-12, None)
    return (V - vmin) / span, {"vmin": vmin.tolist(), "vmax": vmax.tolist()}

def minmax_denorm(Vn, cache):
    vmin = np.array(cache["vmin"])
    vmax = np.array(cache["vmax"])
    span = np.clip(vmax - vmin, 1e-12, None)
    return Vn * span + vmin

def unitsphere_norm(V):
    c = V.mean(axis=0)
    Vr = V - c
    r = np.linalg.norm(Vr, axis=1).max()
    r = max(r, 1e-12)
    return Vr / r, {"center": c.tolist(), "radius": float(r)}

def unitsphere_denorm(Vn, cache):
    c = np.array(cache["center"])
    r = float(cache["radius"])
    return Vn * r + c

def quantize_01(Vn, bins):
    # clamp & quantize
    Vc = np.clip(Vn, 0.0, 1.0)
    Q = np.floor(Vc * (bins - 1) + 1e-9).astype(np.int32)
    return Q

def dequantize_01(Q, bins):
    return Q.astype(np.float64) / (bins - 1)

def mse(a, b):
    d = (a - b) ** 2
    return float(d.mean()), d.mean(axis=0).astype(float).tolist()

def mae(a, b):
    d = np.abs(a - b)
    return float(d.mean()), d.mean(axis=0).astype(float).tolist()

def save_plot(values_xyz, title, save_path):
    ax_names = ["x", "y", "z"]
    plt.figure()
    plt.bar(ax_names, values_xyz)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# ---------- main pipeline per method ----------
def run_method(name, V, F, bins, outdir, tag):
    if name == "minmax":
        Vn, cache = minmax_norm(V)
        to_denorm = lambda X: minmax_denorm(X, cache)
    elif name == "unitsphere":
        Vn, cache = unitsphere_norm(V)
        to_denorm = lambda X: unitsphere_denorm(X, cache)
    else:
        raise ValueError("unknown method")

    # save normalized mesh
    norm_mesh_path = outdir / f"{tag}_{name}_norm.ply"
    trimesh.Trimesh(vertices=Vn, faces=F, process=False).export(norm_mesh_path)

    # bring to [0,1] before quantize
    # minmax normalization is already [0,1]; unitsphere is [-1,1] -> map to [0,1]
    if name == "unitsphere":
        Vn01 = (Vn + 1.0) * 0.5
    else:
        Vn01 = Vn

    Q = quantize_01(Vn01, bins)
    Vn01_rec = dequantize_01(Q, bins)

    # map back to method's normalized range
    if name == "unitsphere":
        Vn_rec = Vn01_rec * 2.0 - 1.0
    else:
        Vn_rec = Vn01_rec

    # denormalize to original space
    Vrec = to_denorm(Vn_rec)

    # save reconstructed mesh
    rec_mesh_path = outdir / f"{tag}_{name}_quant.ply"
    trimesh.Trimesh(vertices=Vrec, faces=F, process=False).export(rec_mesh_path)

    # errors
    mse_all, mse_xyz = mse(V, Vrec)
    mae_all, mae_xyz = mae(V, Vrec)

    return {
        "method": name,
        "mse": mse_all,
        "mse_xyz": mse_xyz,
        "mae": mae_all,
        "mae_xyz": mae_xyz,
        "norm_mesh": str(norm_mesh_path),
        "rec_mesh": str(rec_mesh_path),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mesh", required=True, help="path to .obj")
    ap.add_argument("--outdir", default="outputs_task3", help="output directory")
    ap.add_argument("--bins", type=int, default=1024, help="quantization bins")
    ap.add_argument("--tag", default=None, help="suffix tag for filenames; default = mesh basename")
    args = ap.parse_args()

    mesh_path = Path(args.mesh)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    metrics_dir = outdir / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)

    tag = args.tag or mesh_path.stem

    mesh = trimesh.load(mesh_path.as_posix(), force="mesh")
    if not isinstance(mesh, trimesh.Trimesh):
        if isinstance(mesh, trimesh.Scene):
            mesh = trimesh.util.concatenate(tuple(m for m in mesh.geometry.values()))
        else:
            raise ValueError("Unsupported mesh type")

    V = mesh.vertices.view(np.ndarray)
    F = mesh.faces.view(np.ndarray) if mesh.faces is not None else np.empty((0, 3), dtype=np.int32)

    print(f"Loaded: {args.mesh}")
    print(f"Vertices: {len(V)} | Faces: {len(F)}")
    print(f"Quantization bins: {args.bins}\n")

    m_min = run_method("minmax", V, F, args.bins, outdir, tag)
    m_uni = run_method("unitsphere", V, F, args.bins, outdir, tag)

    # console summary
    print("Errors (lower is better):")
    print(f" MSE  Min–Max   : {m_min['mse']:.8f}")
    print(f" MSE  UnitSphere: {m_uni['mse']:.8f}")
    print(f" MAE  Min–Max   : {m_min['mae']:.8f}")
    print(f" MAE  UnitSphere: {m_uni['mae']:.8f}\n")

    # save per-axis plots with tag so they don't overwrite
    save_plot(m_min["mse_xyz"], f"MSE per axis — minmax — {tag}", outdir / f"{tag}_minmax_mse.png")
    save_plot(m_min["mae_xyz"], f"MAE per axis — minmax — {tag}", outdir / f"{tag}_minmax_mae.png")
    save_plot(m_uni["mse_xyz"], f"MSE per axis — unitsphere — {tag}", outdir / f"{tag}_unitsphere_mse.png")
    save_plot(m_uni["mae_xyz"], f"MAE per axis — unitsphere — {tag}", outdir / f"{tag}_unitsphere_mae.png")

    # write metrics JSON
    metrics_json = {
        "mesh": mesh_path.name,
        "tag": tag,
        "bins": args.bins,
        "minmax": m_min,
        "unitsphere": m_uni,
    }
    json_path = metrics_dir / f"{tag}_metrics.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metrics_json, f, indent=2)

    # append CSV row
    csv_path = metrics_dir / "all_metrics.csv"
    header = [
        "mesh","tag","bins",
        "mse_minmax","mae_minmax","mse_x_minmax","mse_y_minmax","mse_z_minmax","mae_x_minmax","mae_y_minmax","mae_z_minmax",
        "mse_unitsphere","mae_unitsphere","mse_x_unitsphere","mse_y_unitsphere","mse_z_unitsphere","mae_x_unitsphere","mae_y_unitsphere","mae_z_unitsphere"
    ]
    row = [
        mesh_path.name, tag, args.bins,
        m_min["mse"], m_min["mae"], *m_min["mse_xyz"], *m_min["mae_xyz"],
        m_uni["mse"], m_uni["mae"], *m_uni["mse_xyz"], *m_uni["mae_xyz"]
    ]
    write_header = not csv_path.exists()
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(header)
        w.writerow(row)

    print("Saved:")
    print(f" - minmax_normalized     -> {m_min['norm_mesh']}")
    print(f" - minmax_reconstructed  -> {m_min['rec_mesh']}")
    print(f" - unitsphere_normalized -> {m_uni['norm_mesh']}")
    print(f" - unitsphere_reconstructed -> {m_uni['rec_mesh']}")
    print(f" - plots (*.png) in      -> {outdir}")
    print(f" - metrics JSON          -> {json_path}")
    print(f" - metrics CSV (append)  -> {csv_path}")

if __name__ == "__main__":
    main()
