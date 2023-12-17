from matplotlib.image import imread

img = imread(r"/Users/justinhohenstein/Downloads/images.jpg")  # * 255

# print("img", img * 255)

res = []

for y in range(60):
    for x in range(80):
        n = int(img[y][x][0] / 256 * 4) + int(img[y][x][1] / 256 * 4) * 4 + int(img[y][x][2] / 256 * 4) * 16

        res.append("LDI " + str(n))
        res.append("SVA " + str(x + y * 2 ** 7))

    res.append("PRN UPD")

print("RES", res, len(res))

with open('asm_programs/image.asm', mode='wt', encoding='utf-8') as myfile:
    myfile.write('\n'.join(res))
