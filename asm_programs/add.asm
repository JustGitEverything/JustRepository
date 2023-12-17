# x
LDI 200
STA 256
LDI 100
STA 257

PRN .256

# add
LDI 200
STA 258
LDI 11
STA 259

PRN .258

PRN start

LDA 256
ADD 258
STA 256

# second part

LDA 257
ADC 259
STA 257

PRN .256

BRK
