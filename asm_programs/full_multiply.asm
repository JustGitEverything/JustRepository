# result in 258 259
LDI 0
STA 258
LDI 0
STA 259

# new compute

LDI 177
STA 260
LDI 255
STA 261

PRN .260

LDI 100
STA 270
LDI 254
STA 271

PRN .270

PRN start

# start

f start

# check if second numer is zero
LDA 270
ADI 0
JPZ cone
JMP not_zero
f cone
LDA 271
ADI 0
JPZ end

f not_zero

# shift second number
LDA 271
SHR
STA 271
LDA 270
SRC
STA 270

PRN new mult
PRN .270

JPS overflow
JMP next

f overflow
PRN did overflow

# add first number to result
LDA 258
ADD 260
STA 258
LDA 259
ADC 261
STA 259

f next

# shift first number to left
LDA 260
ADD 260
STA 260
LDA 261
ADC 261
STA 261

JMP start

f end

PRN result
PRN .258

BRK
