# kx86 docs
an imperative, modular programming language to make x86 kernel development easy
# num
to define: `num: VAR_NAME, VALUE;` (these can only be defined at the top of your code)     
to access values: `[VAR_NAME]`
# array
to define: `array: ARR_NAME, {VALUE1, VALUE2, VALUE3, ...};` (also only at top of code)     
to access values: `[ARR_NAME@1]` for index 1 which is VALUE2
# pack (function)
```
pack: FUNCTION_NAME,
    COMMAND1: PARAMS1 &
    COMMAND2: PARAMS2 &
    COMMAND3: PARAMS3 &
    ...
;
```
# call pack
`call: FUNCTION_NAME;`
# infinite loop
`forever: FUNCTION_NAME;`
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
if statements can also be used to check if a key is down (the same doesn't apply to while loops)      
for example: `if: key=a, then=FUNCTION_NAME, else=FUNCTION2_NAME;`
# pixel
`pixel: X_COORD, Y_COORD, #COLORHEX;`
# commenting
`//: single-line comment;`     
```
/:
multi-line comment
:/
```
