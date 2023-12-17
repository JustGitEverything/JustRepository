import pygame as pg

win = pg.display.set_mode((80 * 10, 60 * 10))


def draw_ram(v_ram):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    for y in range(60):
        for x in range(80):
            c = v_ram[x + y * 2 ** 7]

            r = c % 4 * 255 / 4
            g = (c // 4) % 2 ** 2 * 255 / 4
            b = (c // 16) % 2 ** 2 * 255 / 4

            pg.draw.rect(win, (r, g, b), [[x * 10, y * 10], [10, 10]])

    pg.display.update()
