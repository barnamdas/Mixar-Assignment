Mixar Assignment
3D Mesh Normalization, Quantization and Reconstruction
Submitted by: Barnam Das (RA2211003011506)

This project works with 3D mesh models. The aim is to load them, normalize their scale, quantize them to reduce data size, reconstruct them, and measure the reconstruction error.

The project uses 8 mesh models (OBJ files):
girl, branch, cylinder, explosive, fence, person, table, talwar.

Tools Used:
- Python
- NumPy
- Trimesh
- Matplotlib
- Blender (for viewing meshes)

Tasks in the Project:

Task 1: Mesh Loading and Inspection
- Load each mesh file.
- Check number of vertices and faces.
- Calculate minimum, maximum, mean, and standard deviation of vertex coordinates.
- This helps understand the mesh size and shape.

Task 2: Normalization and Quantization
- Min-Max Normalization: fit the mesh between 0 and 1 range.
- Unit Sphere Normalization: scale the mesh so it fits inside a unit sphere.
- Quantization using 1024 bins to compress coordinate values.
- Save the normalized and quantized mesh files.

Task 3: Reconstruction and Error Analysis
- Convert quantized values back into real coordinates.
- Compare reconstructed mesh with original mesh.
- Measure the difference using MSE (Mean Squared Error) and MAE (Mean Absolute Error).
- Generate error plots and store results.

Project Folder Structure (Summary):
8samples/               - Input mesh files
outputs_task2/          - Normalized and quantized outputs
outputs_task3/          - Reconstructed outputs and error plots
visualizations/         - Screenshots and Blender views
Python scripts          - process_meshes.py, task2_normalize_quantize.py, task3_reconstruct_analyze.py

How to Run:
1. Install Python dependencies and process all the mesh using the script process_meshes.py
2. Run task2 script on each mesh to normalize and quantize.
3. Run task3 script to reconstruct and compute error.

Results (Simple Summary):
- Min-Max normalization keeps mesh shape more accurate.
- Unit Sphere normalization may slightly distort stretched shapes.
- Quantization with 1024 bins gives very small error, so it is good for compression.
- Reconstruction quality remains high.

Conclusion:
This experiment shows how mesh preprocessing affects accuracy. Min-Max normalization is more stable. Quantization can compress data efficiently while keeping the model almost the same as the original.

