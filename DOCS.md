# kx86 docs
kdx86 is an imperative, modular programming language to make x86 kernel development easy
# requirements
to run the kx86 compiler, you need to have python3 & nasm installed and added to path. to run the compiled image, you need to have qemu installed and added to path. both work on windows, mac, and linux
# num
to define: `num: VAR_NAME, VALUE;`        
to access values: `[VAR_NAME]`      
(i would recommend naming everything in camelCase as to not interfere with the compiler)
# array
to define: `array: ARR_NAME, {VALUE1, VALUE2, VALUE3, ...};` (also only at top of code)     
to access values: `[ARR_NAME@1]` for index 1 which is VALUE2
# string
to define: `str: STRING_NAME, "Hello, World!<endl>";`
literally just here so that i can say i have strings, you can't do anything with them since this lang is graphical      
# pack (function)
```
pack: FUNCTION_NAME,
    COMMAND1: PARAMS1 &
    COMMAND2: PARAMS2 &
    COMMAND3: PARAMS3 &
    ...
;
```
# asmpack (assembly snippet)
```
asmpack: FUNCTION_NAME,
    ASM_COMMAND1
    ASM_COMMAND2
    ASM_COMMAND3
    ...
;
```
# call pack
`call: FUNCTION_NAME;`
# call asmpack
`asmcall: FUNCTION_NAME;`
# infinite loop
`inf: FUNCTION_NAME;`
# edit num or array val
`edit: VAR_NAME, VALUE;`
# operations
`op: OPERATION, OUTPUT_VARIABLE;`     
list of operations:
- `++`: integer addition
- `--`: integer subtraction
- `**`: integer multiplication
- `//`: integer division
- `+`: float & float addition
- `-`: float & float subtraction
- `*`: float & float multiplication
- `/`: float & float division
- `+++`: float & constant addition
- `---`: float & constant subtraction
- `***`: float & constant multiplication
- `///`: float & constant division
- `>f`: integer to float conversion
- `>i`: float to integer conversion
# while loop
`while: CONDITIONAL, then=FUNCTION_NAME;`
# if/else statements
for if: `if: CONDITIONAL, then=FUNCTION_NAME, else=NONE;`     
for if/else: `if: CONDITIONAL, then=FUNCTION_NAME, else=FUNCTION2_NAME;`     
if statements can also be used to check if a key is down (the same applies to while loops)      
for example: `if: key=a, then=FUNCTION_NAME, else=FUNCTION2_NAME;`      
oh yeah also if you want to compare a float and a constant, you have to put an exclamation mark after conditional       
for example: `if: [FLOAT_VAR] <=! 1.0`
# generate random number
`random: MIN, MAX, OUTPUT_VARIABLE;` (MIN inclusive, MAX exclusive)
# make pixel rect
`rect: X1, Y1, X2, Y2, #COLORHEX;` (X1Y1 inclusive, X2Y2 exclusive)
# pause
`pause: APPROX_MILLISECONDS;`
# hang
to finish code so that it doesnt start reading garbage memory     
`halt;`
# commenting
`//: single-line comment;`     
```
/:
multi-line comment
:/
```
# to compile
`kx86 -f <KERNEL-FILE-PATH> -o <OS-IMAGE-FILEPATH> -c <COMPILE-TYPE>`
# to run (linux)
`qemu-system-i386 -drive format=raw,file=<OS-IMAGE-FILEPATH> -vga std -accel kvm -cpu max -m <MEM-AMOUNT>`
# to run (windows)
`qemu-system-i386 -drive format=raw,file=<OS-IMAGE-FILEPATH> -vga std -cpu max -m <MEM-AMOUNT>`
# to run (mac)
`qemu-system-i386 -drive format=raw,file=<OS-IMAGE-FILEPATH> -vga std -accel hvf -cpu max -m <MEM-AMOUNT>`
