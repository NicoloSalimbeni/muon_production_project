import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


c=299792458 # m/s
e=1.602176634e-19 # C 
muon_mass = 105.6583755e6*e / (c**2) # kg
electron_mass = 0.51099895000*e/(c**2) # kg

def get_velocity(p,m):
    vx = p["x"]*1e9*e/(c*m)
    vy = p["y"]*1e9*e/(c*m)
    vz = p["z"]*1e9*e/(c*m)
    v=pd.DataFrame({"x":vx,"y":vy,"z":vz})
    print("ciao")
    return v

def propagate_particles(r_old, p, z_new, m):
    # find proper time
    v=get_velocity(p,m)
    t=(z_new-r_old["z"])/v["z"]

    # compute new positions
    x_new = r_old["x"] + v["x"]*t
    y_new = r_old["y"] + v["y"]*t
    z_new = r_old["z"] + v["z"]*t
    
    r_new = pd.DataFrame({"x":x_new,"y":y_new,"z":z_new})
    return r_new

def get_edges(r,pixel_length):
    # lets find a good dimention for the detector
    x_min, x_max = r["x"].min(), r["x"].max()
    y_min, y_max = r["y"].min(), r["y"].max()

    plot_oversize_factor = 1.2
    edges_x = np.arange(x_min*plot_oversize_factor,x_max*plot_oversize_factor,pixel_length)
    edges_y = np.arange(y_min*plot_oversize_factor,y_max*plot_oversize_factor,pixel_length)


    return [edges_x, edges_y]

def create_hits_map_positrions(r,pixel_length):

    fig, ax = plt.subplots(1,1)
    hist = ax.hist2d(r["x"],r["y"],bins=get_edges(r,pixel_length), cmap = "viridis")
    cbar = fig.colorbar(hist[3], ax=ax, cmap="viridis")
    pixel_length_label = round(pixel_length*1e6)
    cbar.set_label('Count in {}x{} μm pixels'.format(pixel_length_label,pixel_length_label))
    ax.set_xlabel("position x [m]")
    ax.set_ylabel("position y [m]")
    ax.set_title("hits at z = {} m".format(r["z"][0]))

    return ax

def place_detector_on_hitsmap(r, tolerance, ax):
    # find max and min 
    x_min, x_max = r["x"].min()*tolerance, r["x"].max()*tolerance
    y_min, y_max = r["y"].min()*tolerance, r["y"].max()*tolerance

    square = Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=1.5, edgecolor='red', facecolor='none',label="detector")

    _ = ax.add_patch(square)
    ax.legend()

    #brief summary
    length_detector_x = round((x_max-x_min)*tolerance,4)
    length_detector_y = round((y_max-y_min)*tolerance,4)
    print("for detector at z={} m we use".format(r["z"][0]),
            "a detector of length {} m along x and {} m along y".format(length_detector_x, length_detector_y))
    return



    