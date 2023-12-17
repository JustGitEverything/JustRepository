import reformat_mnist
from Network import N

dat, res = reformat_mnist.get(100)

# print(len(dat), len(res))

n = N([64, 20, 10], 10)

for i in range(200):
    loss = 0

    for x in range(100):
        n.forward(dat[x])

        loss += n.backwards(res[x])

    n.update(100)

    print("i:", i, "loss: ", loss / 100)


while True:
    test = reformat_mnist.get_user()
    res = n.forward(test)

    print(res.index(max(res)), res)
