import matplotlib
matplotlib.use("Agg")  # use non-GUI backend
import matplotlib.pyplot as plt
import cv2

def split_into_tiles(img, tiles=4):
    h, w, _ = img.shape
    th = h // tiles
    tw = w // tiles

    tile_list = []

    for i in range(tiles):
        for j in range(tiles):
            tile = img[i*th:(i+1)*th, j*tw:(j+1)*tw]
            tile_list.append(tile)

    return tile_list


# load image (example)
img = cv2.imread("angel.jpg")

# convert BGR -> RGB for matplotlib
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

tiles = split_into_tiles(img)

# create 4x4 visualization
fig, axes = plt.subplots(4, 4, figsize=(8, 8))

for i, ax in enumerate(axes.flat):
    ax.imshow(tiles[i])
    ax.set_title(f"Tile {i}")
    ax.axis("off")

plt.tight_layout()
plt.savefig("tile_plot.png")