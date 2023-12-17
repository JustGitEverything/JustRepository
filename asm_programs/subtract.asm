# x
LDI 50
STA 256
LDI 30
STA 257

PRN .256

# sub
LDI 30
STA 258
LDI 45
STA 259

PRN .258

PRN start

LDA 256
SUB 258
STA 256

# second part

LDA 257
SCI 45
STA 257

PRN .256

BRK
