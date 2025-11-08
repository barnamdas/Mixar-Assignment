# process_meshes.py
import argparse
from pathlib import Path
import numpy as np
import trimesh

def mesh_stats(vertices: np.ndarray):
    return {
        "num_vertices": int(vertices.shape[0]),
        "min": vertices.min(axis=0).tolist(),
        "max": vertices.max(axis=0).tolist(),
        "mean": vertices.mean(axis=0).tolist(),
        "std": vertices.std(axis=0).tolist(),
    }

def inspect_mesh(mesh_path: Path):
    if not mesh_path.exists():
        raise FileNotFoundError(f"Mesh not found: {mesh_path.resolve()}")

    mesh = trimesh.load(mesh_path, force='mesh')
    V = np.asarray(mesh.vertices)

    stats = mesh_stats(V)

    # Pretty print
    print(f"File: {mesh_path}")
    print(f"Number of vertices: {stats['num_vertices']}")
    print(f"Min: {np.array(stats['min'])}")
    print(f"Max: {np.array(stats['max'])}")
    print(f"Mean: {np.array(stats['mean'])}")
    print(f"Std: {np.array(stats['std'])}")

    # Optional: save stats next to the mesh
    out_path = mesh_path.with_suffix(".stats.json")
    try:
        import json
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
        print(f"Saved stats -> {out_path}")
    except Exception as e:
        print(f"(Skipping save) Could not write stats: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Task 1: Load a mesh and print basic statistics.")
    parser.add_argument(
        "--mesh",
        type=str,
        required=True,
        help="Path to a single .obj mesh (relative or absolute).")
    args = parser.parse_args()

    mesh_path = Path(args.mesh)
    inspect_mesh(mesh_path)

if __name__ == "__main__":
    main()
