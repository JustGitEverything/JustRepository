# result in 258
LDI 0
STA 258

# compute
LDI 9
STA 256
LDI 80
STA 257

PRN start

# start

f start
LDA 257
ADI 0
JPZ end

LDA 257
SHR
STA 257

PRN new mult
PRN 257

JPS overflow
JMP next

f overflow
PRN did overflow

LDA 258
ADD 256
STA 258

f next

LDA 256
ADD 256
STA 256

JMP start

f end
LDA 258

BRK
