def ftest(int bout) > int ret {
    print("from subroutine")
    print(bout)

    ret = bout

    ret = ret - 2

    print("return")
    print(ret)
}

int sure = 17

int nt = 3

print("begin of sus")

nt = 15 - (1 - ftest(sure) - (1 - 2))

<< nt

print("nt")
print(nt)

print("functions down here")

halt
