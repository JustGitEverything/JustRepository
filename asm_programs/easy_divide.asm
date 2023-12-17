# result in 258
LDI 0
STA 258

# compute
LDI 120
STA 256
LDI 5
STA 257

PRN start

# start

f start

LDA 256
SUB 257
STA 256

JPN end

LDA 258
ADI 1
STA 258

JMP start

f end

LDA 258

BRK
