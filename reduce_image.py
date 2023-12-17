from PIL import Image
from matplotlib.image import imread
import numpy as np

img = imread(r"C:\Users\Justin Hohenstein\Downloads\commodore (1).png") * 255

print("img", img * 255)

res = []

for y in range(60):
    res.append([])

    for x in range(80):
        n = [int(int(img[y][x][0] / (255 / 8)) * (255 / 7)),
             int(int(img[y][x][1] / (255 / 4)) * (255 / 3)),
             int(int(img[y][x][2] / (255 / 8)) * (255 / 7))]

        res[-1].append(n)

print(np.array(res)[:, :, 1])
print(np.unique(np.array(res)[:, :, 1]))

img = Image.fromarray(np.asarray(res, dtype=np.uint8), 'RGB')
img.save('image.png')
img.show()
