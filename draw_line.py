from matplotlib import pyplot as plt

data = [1 for _ in range(60 * 80)]


def draw_line(sx, sy, ex, ey):
    dx = ex - sx
    dy = ey - sy

    if abs(dx) > abs(dy):
        if dx == 0:
            return

        x_dir = int(abs(dx) / dx)

        for x in range(abs(dx) + 1):
            print(sx + x * x_dir)
            data[int((sy + dy / dx * x * x_dir)) * 80 + sx + x * x_dir] = 0
    else:
        if dy == 0:
            return

        y_dir = int(abs(dy) / dy)

        for y in range(abs(dy) + 1):
            data[int((sy + y * y_dir)) * 80 + int(sx + y * dx / dy * y_dir)] = 0


def draw_tri(p0, p1, p2):
    draw_line(p0[0], p0[1], p1[0], p1[1])
    draw_line(p0[0], p0[1], p2[0], p2[1])
    draw_line(p2[0], p2[1], p1[0], p1[1])


draw_tri((20, 10), (10, 50), (40, 59))

img = [data[80 * i:80 * (i + 1)] for i in range(60)]

print(img[40][40])

plt.imshow(img, interpolation='nearest', cmap='gray')
plt.show()
