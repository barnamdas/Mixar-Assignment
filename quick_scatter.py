import sys
import numpy as np
import trimesh
import matplotlib.pyplot as plt

mesh = trimesh.load(sys.argv[1], force='mesh')
V = np.asarray(mesh.vertices)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(V[:,0], V[:,1], V[:,2], s=1)
ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
ax.set_title(sys.argv[1])
plt.show()

