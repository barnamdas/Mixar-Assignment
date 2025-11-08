# Mixar-Assignment

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

## **Folder Structure**
Submission/
│
│─ process_meshes.py
│─ task2_normalize_quantize.py
│─ task3_reconstruct_analyze.py
│
├─ outputs_task2/                # Normalized and Quantized Meshes
│   ├─ *_minmax_norm.ply
│   ├─ *_minmax_quant.ply
│   ├─ *_unitsphere_norm.ply
│   └─ *_unitsphere_quant.ply
│
├─ outputs_task3/                # Reconstruction + Error Analysis
│   ├─ *_minmax_quant.ply
│   ├─ *_unitsphere_quant.ply
│   ├─ mse_per_axis.png
│   ├─ mae_per_axis.png
│   └─ metrics/
│       ├─ *_metrics.json
│       └─ all_metrics.csv
│
├─ visualizations/               # Blender / Scatter screenshots (insert manually)
│
└─ Final_Report.pdf              # End-to-end summary report

