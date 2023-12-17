import gzip
import _pickle as pickle


def get(size=200):
    f = gzip.open(r'C:\Users\Justin Hohenstein\PycharmProjects\data\MNIST\mnist.pkl.gz', 'rb')
    (tip, tres), _, _ = pickle.load(f, encoding='latin1')
    f.close()

    data = []
    yd = []

    ct = 28 / 8

    for i in range(size):
        sample = []

        for y in range(8):
            for x in range(8):
                mean = 0

                for mx in range(3):
                    for my in range(3):
                        try:
                            mean += tip[i][int(int((y * ct + my * ct / 3)) * 28 + x * ct + mx * ct / 3)]
                        except IndexError:
                            pass

                sample.append(1 if mean > 3 else 0)

        data.append(sample)

        yd.append([0 for _ in range(10)])
        yd[-1][tres[i]] = 1

    return data, yd


def display(smp):
    import pygame as pg

    win = pg.display.set_mode((8 * 20, 8 * 20))

    run = True

    while run:
        win.fill((255, 255, 255))

        for yp in range(8):
            for xp in range(8):
                c = 255 - 100 * smp[yp * 8 + xp]

                pg.draw.rect(win, (c, c, c), [[xp * 20, yp * 20], [20, 20]], 10)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

                run = False


def get_user():
    import pygame as pg

    smp = [0 for _ in range(64)]

    win = pg.display.set_mode((8 * 20, 8 * 20))

    down = False

    run = True

    while run:
        win.fill((255, 255, 255))

        for yp in range(8):
            for xp in range(8):
                c = 255 - 100 * smp[yp * 8 + xp]

                pg.draw.rect(win, (c, c, c), [[xp * 20, yp * 20], [20, 20]], 10)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                down = True

                xp, yp = pg.mouse.get_pos()

                smp[int(int(yp // 20) * 8 + xp // 20)] = 1

            if event.type == pg.MOUSEBUTTONUP:
                down = False

            if event.type == pg.MOUSEMOTION:
                if down:
                    xp, yp = pg.mouse.get_pos()

                    smp[int(int(yp // 20) * 8 + xp // 20)] = 1

    return smp


if __name__ == "__main__":
    dat, res = get()

    print("dat", dat)
    print("res", res)

    u_dat = get_user()

    # display(dat[0])
