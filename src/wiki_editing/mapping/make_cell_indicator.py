import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, PathPatch
from matplotlib.path import Path
from PIL import Image
from pathlib import Path as PathlibPath
import numpy as np

plt.rcParams.update({
    # "text.usetex": True,
    "font.family": "Roboto",
    # "font.size": 20,
    #"font.weight":"normal",
    #"axes.labelweight":"normal"
})

# disable PIL decompression bomb check for large images
# the map image is just very very large
Image.MAX_IMAGE_PIXELS = None

MAP_FILE = PathlibPath("./PZ_Vanilla_map_b42/Map.png")

# map with grid output
OUT_GRID_MAP = PathlibPath("./Images/Cell grid - placement comparison.png")

GRID_BUILD41 = 300
GRID_BUILD42 = 256

GRID_BUILD41_STYLE = {'color': 'yellow', 'linestyle': '-', 'alpha': 1, 'zorder': 10}
GRID_BUILD42_STYLE = {'color': 'magenta', 'linestyle': '-', 'alpha': 1, 'zorder': 11}


XLIM = (8949, 10255)
YLIM = (7681, 6262) # inversed due to image coordinates being flipped


# example cell output
OUT_EXAMPLE_CELL = PathlibPath("./Images/Cell grid - example selection.png")

CENTER_CELL_300 = (31,23)


# cells colliding with the example cell output
OUT_COLLIDING_CELLS = PathlibPath("./Images/Cell grid - exported cells.png")


# active and inactive areas output
OUT_ACTIVE_INACTIVE = PathlibPath("./Images/Cell grid - active vs inactive areas.png")

## UTILITY

def draw_grid_lines(grid_size, img_size, label, xlim, ylim, coordinates=True, color='white', **kwargs):
    min_x = min(xlim)
    max_x = max(xlim)
    min_y = min(ylim)
    max_y = max(ylim)

    # draw vertical and horizontal grid lines
    legend_set = False
    for x in range(0, img_size[0], grid_size):
        # skip useless lines outside of the plot area
        if x < min_x or x > max_x:
            continue

        # add a legend to the first line only
        if not legend_set:
            plt.axvline(x, **kwargs, color=color, label=label)
            legend_set = True
        else:
            plt.axvline(x, **kwargs, color=color)
    for y in range(0, img_size[1], grid_size):
        if y < min_y or y > max_y:
            continue
        plt.axhline(y, **kwargs, color=color)

    # add cell coordinate marker
    if not coordinates:
        return

    for x in range(0, img_size[0], grid_size):
        for y in range(0, img_size[1], grid_size):
            # we need to skip those bcs they will do weird shit outside of the plot area
            new_x = x + 5
            new_y = y + 20
            if (new_x < min_x or new_x > max_x-60 
                or new_y < min_y or new_y > max_y-5):
                continue
            cell_x = x // grid_size
            cell_y = y // grid_size
            plt.text(new_x, new_y, f'({cell_x}, {cell_y})', fontsize=8, color=color, zorder=50)

def draw_main_map(img, grid=True, coordinates=True):
    img_size = img.size
    plt.figure(figsize=(10, 10))
    plt.imshow(img, alpha=0.8)

    # show grid lines for Build 41 and Build 42
    if grid:
        draw_grid_lines(GRID_BUILD41, img_size, label='Build 41 (300x300)', xlim=XLIM, ylim=YLIM, coordinates=coordinates, **GRID_BUILD41_STYLE)
        draw_grid_lines(GRID_BUILD42, img_size, label='Build 42 (256x256)', xlim=XLIM, ylim=YLIM, coordinates=coordinates, **GRID_BUILD42_STYLE)

    # set limits
    plt.xlim(XLIM)
    plt.ylim(YLIM)

    # cleanup
    legend = plt.legend(loc='upper right')
    legend.set_zorder(100)
    plt.axis('off')


## EXPORT VANILLA MAP WITH GRID VIEW FOR COMPARISON
print("Exporting vanilla map with grid view for comparison...")

# read image and plot it
img = Image.open(MAP_FILE)

draw_main_map(img)

# save the figure
plt.savefig(OUT_GRID_MAP, bbox_inches='tight', pad_inches=0)
plt.close()


## PICK AN EXAMPLE CELL AS THE MAPPED CELL
print("Exporting an example cell as the mapped cell...")

draw_main_map(img)

poly = Rectangle((CENTER_CELL_300[0]*GRID_BUILD41, CENTER_CELL_300[1]*GRID_BUILD41), GRID_BUILD41, GRID_BUILD41, color='cyan', fill=True, alpha=0.5, zorder=5, label='Mapped cell example')
plt.gca().add_patch(poly)

# cleanup
legend = plt.legend(loc='upper right')
legend.set_zorder(100)

# save the figure
plt.savefig(OUT_EXAMPLE_CELL, bbox_inches='tight', pad_inches=0)
plt.close()


## SHOW THE EXPORTED 256 CELLS THAT COLLIDE WITH THE EXAMPLE CELL
print("Exporting the cells that collide with the example cell...")

draw_main_map(img)

cells = [
    (36, 26),
    (37, 26),
    (36, 27),
    (37, 27),
    (36, 28),
    (37, 28),
]

poly = Rectangle((CENTER_CELL_300[0]*GRID_BUILD41, CENTER_CELL_300[1]*GRID_BUILD41), GRID_BUILD41, GRID_BUILD41, color='cyan', fill=False, hatch='//', alpha=1, zorder=5, label='Mapped cell example')
plt.gca().add_patch(poly)

label = 'Exported cells'
for cell in cells:
    poly = Rectangle((cell[0]*GRID_BUILD42, cell[1]*GRID_BUILD42), GRID_BUILD42, GRID_BUILD42, color='green', fill=True, alpha=0.3, zorder=4, label=label)
    label = None
    plt.gca().add_patch(poly)


# cleanup
legend = plt.legend(loc='upper right')
legend.set_zorder(100)

# save the figure
plt.savefig(OUT_COLLIDING_CELLS, bbox_inches='tight', pad_inches=0)
plt.close()


## SHOW ACTIVE AND INACTIVE AREAS
# active areas are the tiles which are in the 256 cells and present in the 300 mapped cell
# inactive ones are the other tiles of the 256 cells which are not mapped

draw_main_map(img)

min_main_x = CENTER_CELL_300[0]*GRID_BUILD41
max_main_x = min_main_x + GRID_BUILD41
min_main_y = CENTER_CELL_300[1]*GRID_BUILD41
max_main_y = min_main_y + GRID_BUILD41

active_label = 'Filled cell area'
inactive_label = 'Empty in export'
for cell in cells:
    min_x = cell[0]*GRID_BUILD42
    max_x = min_x + GRID_BUILD42
    min_y = cell[1]*GRID_BUILD42
    max_y = min_y + GRID_BUILD42

    # find borders via min max etc
    active_min_x = max(min_main_x, min_x)
    active_max_x = min(max_main_x, max_x)
    active_min_y = max(min_main_y, min_y)
    active_max_y = min(max_main_y, max_y)

    # make polygon for active area
    ACTIVE_STYLE = {'color': 'green', 'fill': True, 'alpha': 0.2, 'zorder': 5, 'label': active_label}
    active_poly = Rectangle((active_min_x, active_min_y), active_max_x - active_min_x, active_max_y - active_min_y, **ACTIVE_STYLE)
    plt.gca().add_patch(active_poly)

    # make polygon for inactive area

    INACTIVE_STYLE = {'color': 'red', 'fill': True, 'alpha': 0.2, 'zorder': 4, 'label': inactive_label}

    # Create a single polygon for the inactive area with a hole in the active area
    outer_verts = np.array([
        [min_x, min_y],
        [min_x, max_y],
        [max_x, max_y],
        [max_x, min_y],
        [min_x, min_y],  # close the polygon
    ])
    
    hole_verts = np.array([
        [active_min_x, active_min_y],
        [active_max_x, active_min_y],
        [active_max_x, active_max_y],
        [active_min_x, active_max_y],
        [active_min_x, active_min_y],  # close the polygon
    ])
    
    verts = np.concatenate([outer_verts, hole_verts])
    codes = np.array([Path.MOVETO] + [Path.LINETO] * 3 + [Path.CLOSEPOLY] +
                      [Path.MOVETO] + [Path.LINETO] * 3 + [Path.CLOSEPOLY])
    
    path = Path(verts, codes)
    patch = PathPatch(path, **INACTIVE_STYLE)
    plt.gca().add_patch(patch)

    active_label = None
    inactive_label = None

# cleanup
legend = plt.legend(loc='upper right')
legend.set_zorder(100)

# save the figure
plt.savefig(OUT_ACTIVE_INACTIVE, bbox_inches='tight', pad_inches=0)
plt.close()
