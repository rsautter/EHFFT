import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np

def hexPlot(mat, cmap = colormaps['viridis'],toRemove=-1):
  '''
    Hexagonal plot with matplotlib colormap
  '''
  th = np.linspace(np.pi/2,5*np.pi/2,7)[:-1]
  for y in range(mat.shape[0]):
    for x in range(mat.shape[1]):
      if mat[y,x]==toRemove:
        continue
      if(np.max(mat)!=0.0):
        filled_poly = plt.fill(0.5*np.sin(th)+0.8*x,0.55*np.cos(th)+y-0.5*(x%2),color=cmap(1e-5+mat[y][x]/np.max(mat)))
        (x0, y0), (x1, y1) = filled_poly[0].get_path().get_extents().get_points()
        "{y},{x}\nV:"
        plt.text((x0 + x1) / 2, (y0 + y1) / 2, f"{int(mat[y][x])}", ha='center', va='center', fontsize=10, color='k')
      else:
        plt.fill(0.5*np.sin(th)+0.8*x,0.55*np.cos(th)+y-0.5*(x%2),color=cmap(0.0))
        

def hexBwPlot(mat,toRemove=-1): 
  '''
    Hexagonal plot Black and Whit
  '''
  th = np.linspace(np.pi/2,5*np.pi/2,7)[:-1]
  for y in range(mat.shape[0]):
    for x in range(mat.shape[1]):
      if mat[y,x]==toRemove:
        continue
      if(np.max(mat)!=0.0):
        filled_poly = plt.fill(0.5*np.sin(th)+0.8*x,0.55*np.cos(th)+y-0.5*(x%2),color='w',edgecolor='k')
        (x0, y0), (x1, y1) = filled_poly[0].get_path().get_extents().get_points()
        "{y},{x}\nV:"
        plt.text((x0 + x1) / 2, (y0 + y1) / 2, f"{int(mat[y][x])}", ha='center', va='center', fontsize=10, color='k')
      else:
        plt.fill(0.5*np.sin(th)+0.8*x,0.55*np.cos(th)+y-0.5*(x%2),color=cmap(0.0))
