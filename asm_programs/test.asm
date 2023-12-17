# result in 258
LDI 0
STA 258

# compute
LDI 200
STA 256
LDI 100
STA 257

PRN start

LDA 256
ADD 66
STA 256

# second part

LDA 257
ACI 10
STA 257

PRN .256

BRK
