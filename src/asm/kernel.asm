
org 0x7E00

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    mov ax, 0x4F02
    mov bx, 0x118 | 0x4000
    int 0x10

    mov ax, 0x4F01
    mov cx, 0x118
    mov di, mode_info
    int 0x10
    
    

    mov eax, [mode_info + 0x28]
    mov [lfb_addr], eax

    movzx eax, word [mode_info + 0x10]
    mov [lfb_pitch], eax 

    lgdt [gdt_desc]

    mov eax, cr0
    or  eax, 1
    mov cr0, eax

    jmp CODE_SEL:pm_start

bits 32
pm_start:
    mov ax, DATA_SEL
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x90000

    mov esi, [lfb_addr]

KEYS dd 128 dup(0)


c90508:
dd 10.0

c10576:
dd 1.0

x:
dd 0

one_constant:
dd 1.0

x_f:
dd 0.0

y:
dd 0

j7499:

CheckKeyboard2643:
    in al, 0x64
    test al, 1
    jz Done2643
    in al, 0x60
    cmp al, 0x80
    jb Pressed2643
    sub al, 0x80
    mov byte [KEYS+eax], 0
    jmp Done2643

Pressed2643:
    mov byte [KEYS+eax], 1

Done2643:
    cmp byte [KEYS+0x1E], 1
    jne false2643
    sub byte [KEYS+0x1E], 1
    jmp true2643


true2643:



fild dword [x]
fstp dword [x_f]

fld dword [x_f]
fdiv dword [c90508]
fstp dword [x_f]
mov eax, [x_f]
cmp eax, [one_constant]
je true2837
jne false2837

true2837:





mov edi, esi       
mov ecx, [y]    
mov dx, [lfb_pitch] 
movzx edx, dx      
imul ecx, edx   

mov eax, [x]        
imul eax, 3         

add ecx, eax
add edi, ecx        

mov dword [edi], 0xFF0000



fld dword [one_constant]
fadd dword [c10576]
fstp dword [one_constant]

jmp escape2837

false2837:


escape2837:

mov eax, [x]
add eax, 1
mov dword [x], eax
mov eax, [y]
add eax, 1
mov dword [y], eax

jmp escape2643

false2643:


escape2643:

jmp j7499



align 4
lfb_addr: dd 0
lfb_pitch: dd 0
zero: dd 0


mode_info: times 256 db 0

align 8
gdt:
    dq 0x0000000000000000
    dq 0x00CF9A000000FFFF
    dq 0x00CF92000000FFFF

gdt_desc:
    dw gdt_end - gdt - 1
    dd gdt
gdt_end:

CODE_SEL equ 0x08
DATA_SEL equ 0x10