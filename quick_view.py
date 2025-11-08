import sys, trimesh
m = trimesh.load(sys.argv[1], force='mesh')
m.show()  