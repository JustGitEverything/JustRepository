# result in 258 259
LDI 0
STA 258
LDI 0
STA 259

# new compute

LDI 252
STA 260
LDI 1
STA 261

PRN .260

LDI 4
STA 270
LDI 0
STA 271

PRN .270

# power
LDI 1
STA 280
LDI 0
STA 281

PRN start

# start

f start

# check if second is shifted till negative
LDA 271
ADD 271
JPN next

# shift second completely
LDA 270
ADD 270
STA 270
LDA 271
ADC 271
STA 271

# shift power
LDA 280
ADD 280
STA 280
LDA 281
ADC 281
STA 281

JMP start

f next

PRN shifting done

PRN .270
PRN .280

# check if can subtract second from first
LDA 260
SUB 270
LDA 261
SUC 271
JPN negative

# can subtract
STA 261
# (already calculated above)
LDA 260
SUB 270
STA 260

# add to result
LDA 258
ADD 280
STA 258
LDA 259
ADC 281
STA 259

f negative

# shift power
LDA 281
SHR
STA 281
LDA 280
SRC
STA 280

# check if zero
LDA 280
ADD 0
JPZ possible
JMP sec

f possible
LDA 281
ADD 0
JPZ end

f sec

# shift dividend
LDA 271
SHR
STA 271
LDA 270
SRC
STA 270

JMP next

f end

PRN .258

BRK
