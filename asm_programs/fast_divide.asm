# result in 258
LDI 0
STA 258

# compute
LDI 76
STA 256
LDI 4
STA 257

# power
LDI 1
STA 259

PRN start

# start

f start

LDA 257
ADD 257
JPN next
STA 257
# shift power
LDA 259
ADD 259
STA 259
JMP start

f next

PRN shifting done

LDA 256
SUB 257
JPN negative
STA 256

# add to result
LDA 258
ADD 259
STA 258

f negative

# shift power
LDA 259
SHR
STA 259
ADI 0
JPZ end

# shift dividend
LDA 257
SHR
STA 257

JMP next

f end

LDA 258

BRK
