def aaa(short r, short g) > short ret {
    print("called")

    ret = r + g
}

short first = 0
short b = 4

first = 7 - aaa(aaa(2, 1), aaa(5 - 3, 1) - 1)

# first = 1 + first + (hehe) - hehe + aaa(hehe, first) + 6 - (first)

# ((first + 1) + 1)

print("WHAT")
print(first)

halt
