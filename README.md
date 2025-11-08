# Mixar-Assignment, by Barnam Das [RA2211003011506]
 
# 3D Mesh Normalization, Quantization & Reconstruction  
*Computer Graphics / Geometry Processing Assignment*

![banner](https://dummyimage.com/900x200/222/fff&text=3D+Mesh+Processing+Pipeline)

---

## **Badges**
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)
![Meshes](https://img.shields.io/badge/Data-OBJ%20Meshes-orange)
![License](https://img.shields.io/badge/Academic-Use%20Only-yellow)

---

## **Table of Contents**
1. [Overview](#overview)  
2. [Dataset](#dataset)  
3. [Environment Setup](#environment-setup)  
4. [Folder Structure](#folder-structure)  
5. [How to Run the Code](#how-to-run-the-code)  
6. [Task Breakdown](#task-breakdown)  
   - Task 1: Mesh Inspection  
   - Task 2: Normalization & Quantization  
   - Task 3: Reconstruction & Error Analysis  
7. [Outputs Explained](#outputs-explained)  
8. [Results & Observations](#results--observations)  
9. [Conclusion](#conclusion)  
10. [Screenshots & Visuals (Insert Manually)](#screenshots--visuals)

---

## **Overview**
This project processes and analyzes 3D mesh models by performing:

- **Mesh Loading & Inspection**
- **Normalization**
  - Min–Max Normalization
  - Unit Sphere Normalization
- **Quantization** (1024 bins)
- **Reconstruction**
- **Error Evaluation** using:
  - MSE (Mean Squared Error)
  - MAE (Mean Absolute Error)

The goal is to understand how normalization affects shape consistency and how quantization introduces small reconstruction errors.

---

## **Dataset**
The dataset consists of **8 OBJ files**:

| Mesh | Category |
|------|----------|
| girl | Human character |
| branch | Natural object |
| cylinder | Primitive shape |
| explosive | Tool-like object |
| fence | Structure |
| person | Full-body human |
| table | Furniture |
| talwar | Sword model |

---

## **Environment Setup**
```bash
python -m pip install numpy trimesh matplotlib
```
```bash
## **Folder Structure**
Mixar-Assignment/
│
├── 8samples/8samples/              # Input mesh models (.obj)
│   ├── branch.obj
│   ├── cylinder.obj
│   ├── explosive.obj
│   ├── fence.obj
│   ├── girl.obj
│   ├── person.obj
│   ├── table.obj
│   └── talwar.obj
│
├── outputs_task2/                  # Task 2 results (normalized + quantized)
│   ├── *_minmax_norm.ply
│   ├── *_minmax_quant.ply
│   ├── *_unitsphere_norm.ply
│   └── *_unitsphere_quant.ply
│
├── outputs_task3/                  # Task 3 reconstruction + error analysis
│   ├── *_minmax_norm.ply
│   ├── *_minmax_quant.ply
│   ├── *_unitsphere_norm.ply
│   ├── *_unitsphere_quant.ply
│   ├── mse_per_axis.png
│   ├── mae_per_axis.png
│   └── metrics/
│       ├── *.json                  # per-model error metrics
│       └── all_metrics.csv         # combined comparison table
│
├── visualizations/                 # Blender / Screenshots 
│   └── *.png
│
├── process_meshes.py               # Task 1: Mesh inspection
├── task2_normalize_quantize.py     # Task 2: Normalization + Quantization
├── task3_reconstruct_analyze.py    # Task 3: Reconstruction + Error plots
├── quick_scatter.py                # Helper script: 3D scatter viewer
│
├── README.md                       # Instructions to run project
└── Final_Mixar_Report.pdf          # Final report (to submit)

```
## **How to Run the Code**

### Task 1 — Mesh Loading & Inspection
```bash
python process_meshes.py --mesh path/to/file.obj
```
### Task 2 — Normalization & Quantization
```bash
python task2_normalize_quantize.py --mesh path/to/file.obj --outdir outputs_task2 --bins 1024

```
### Task 3 — Reconstruction & Error Analysis
```bash
python task3_reconstruct_analyze.py --mesh path/to/file.obj --outdir outputs_task3 --bins 1024

```
### Run for All Meshes (PowerShell)
```bash
Get-ChildItem "8samples/8samples" -Filter *.obj | ForEach-Object {
  python task2_normalize_quantize.py --mesh $_.FullName --outdir outputs_task2 --bins 1024
  python task3_reconstruct_analyze.py --mesh $_.FullName --outdir outputs_task3 --bins 1024
}    
```
## **Task Breakdown**

### **Task 1: Mesh Loading and Inspection (20 Marks)**
- Loaded meshes from dataset.
- Computed:
  - Number of vertices and faces
  - Min, Max, Mean, Std for each axis
- Identified scale and bounding box.

### **Task 2: Normalization and Quantization (40 Marks)**
- Min–Max Normalization (fits mesh to [0,1])
- Unit Sphere Normalization (fits mesh into a radius-1 sphere)
- Quantization to 1024 bins
- Exported normalized and reconstructed meshes

### **Task 3: Reconstruction & Error Analysis (40 Marks)**
- Computed MSE & MAE between original and reconstructed meshes
- Compared Min–Max vs Unit Sphere normalization impact

---

## **Outputs Explained**
| Output Type | Location | Description |
|------------|----------|-------------|
| Output Meshes | outputs_task2/ & outputs_task3/ | Generated .PLY models after each step |
| Visualizations | visualizations/ | Blender or scatter screenshots |
| Plots | outputs_task3/mse_per_axis.png, mae_per_axis.png | Error evaluation charts |
| Metrics Table | outputs_task3/metrics/all_metrics.csv | Summary of errors per mesh |

---

## **Results & Observations**
| Method | Error Behavior | Interpretation |
|-------|----------------|----------------|
| Min–Max Normalization | Lower error | Better shape preservation |
| Unit Sphere Normalization | Slightly higher error | Can distort elongated meshes |
| Quantization (1024 bins) | Very small error | Good compression-quality trade-off |

---

## **Conclusion**
- Min–Max normalization is generally better for preserving the original proportions.
- Unit Sphere normalization is still useful when a uniform scaling reference is required.
- Quantization at 1024 bins introduces negligible geometry loss.


---

## **Submitted By**
**Name:** *Barnam Das*  
**Register Number:** *RA2211003011506*          
**Institution:** *SRM Institute of Science and Technology*
