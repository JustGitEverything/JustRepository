import numpy as np
import pygame as pg

data = [1 for _ in range(120 * 160)]


def draw_line(sx, sy, ex, ey):
    dx = ex - sx
    dy = ey - sy

    if abs(dx) > abs(dy):
        if dx == 0:
            return

        x_dir = int(abs(dx) / dx)

        for x in range(abs(dx) + 1):
            yp = int((sy + dy / dx * x * x_dir))
            xp = sx + x * x_dir

            if 0 <= yp < 120 and 0 <= xp < 160:
                data[yp * 160 + xp] = 0
    else:
        if dy == 0:
            return

        y_dir = int(abs(dy) / dy)

        for y in range(abs(dy) + 1):
            yp = int(sy + y * y_dir)
            xp = int(sx + y * dx / dy * y_dir)

            if 0 <= yp < 120 and 0 <= xp < 160:
                data[yp * 160 + xp] = 0


def draw_tri(p0, p1, p2):
    draw_line(p0[0], p0[1], p1[0], p1[1])
    draw_line(p0[0], p0[1], p2[0], p2[1])
    draw_line(p2[0], p2[1], p1[0], p1[1])


cube = [[[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]],
        [[0.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 0.0, 0.0]],

        # EAST
        [[1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 1.0, 1.0]],
        [[1.0, 0.0, 0.0], [1.0, 1.0, 1.0], [1.0, 0.0, 1.0]],

        # NORTH
        [[1.0, 0.0, 1.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0]],
        [[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 0.0, 1.0]],

        # WEST
        [[0.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 1.0, 0.0]],
        [[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]],

        # TOP
        [[0.0, 1.0, 0.0], [0.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
        [[0.0, 1.0, 0.0], [1.0, 1.0, 1.0], [1.0, 1.0, 0.0]],

        # BOTTOM
        [[1.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]],
        [[1.0, 0.0, 1.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]]


def rotate_x(a, p):
    return [p[0], p[1] * np.cos(a) - p[2] * np.sin(a), p[1] * np.sin(a) + p[2] * np.cos(a)]


def rotate_y(a, p):
    return [p[0] * np.cos(a) + p[2] * np.sin(a), p[1], - p[0] * np.sin(a) + p[2] * np.cos(a)]


def rotate_z(a, p):
    return [p[0] * np.cos(a) - p[1] * np.sin(a), p[0] * np.sin(a) + p[1] * np.cos(a), p[2]]


shift = [2, 4, 1]
alpha = 15 / 360 * 2 * np.pi

win = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

SCALE = 1 / np.tanh(np.pi / 4)

print("f_fov = ", 1 / np.tanh((np.pi / 2) / 2), SCALE)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    for tri in cube:
        points = []

        for i in range(3):
            pt = rotate_y(alpha, rotate_x(alpha, tri[i]))

            px = int((pt[0] + shift[0]) / (pt[1] + shift[1]) * 160)
            py = int((pt[2] + shift[2]) / (pt[1] + shift[1]) * 160)

            points.append(np.array([px, py, tri[i][2]], dtype=int))

        v1 = points[1] - points[0]
        v2 = points[1] - points[2]

        c = np.cross(v2, v1)

        if c[2] > 0:
            draw_tri(points[0], points[1], points[2])

    # img = [data[80 * i:80 * (i + 1)] for i in range(60)]

    for i in range(120 * 160):
        col = data[i] * 255

        pg.draw.rect(win, (col, col, col), [[(i % 160) * 5, (i // 160) * 5], [10, 10]])

    pg.display.update()
    clock.tick(10)

    data = [1 for _ in range(120 * 160)]

    alpha += 0.1
