
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


c57208:
dd 1.0

c8662:
dd 1.0

x:
dd 0

x_f:
dd 0.0

one:
dd 1.0

constant_one:
dd 1.0

divisor:
dd 1.0

y:
dd 1

j9376:

CheckKeyboard7835:
    in al, 0x64
    test al, 1
    jz Done7835
    in al, 0x60
    cmp al, 0x80
    jb Pressed7835
    sub al, 0x80
    mov byte [KEYS+eax], 0
    jmp Done7835

Pressed7835:
    mov byte [KEYS+eax], 1

Done7835:
    cmp byte [KEYS+0x1E], 1
    jne false7835
    sub byte [KEYS+0x1E], 1
    jmp true7835


true7835:



fild dword [x]
fstp dword [x_f]

fld dword [x_f]
fdiv dword [c57208]
fstp dword [x_f]
mov eax, [x_f]
cmp eax, [one]
je true6376
jne false6376

true6376:



    mov eax, esi
    mov ebx, [x]
    mov ecx, [y]
mov edi, eax
mov dx, 1024
movzx edx, dx
imul ecx, edx
add ecx, ebx
imul ecx, 3
add edi, ecx
    mov dword [edi], 0xFF0000

fld dword [one]
fadd dword [c8662]
fstp dword [one]

jmp escape6376

false6376:


escape6376:

mov eax, [x]
add eax, 1
mov dword [x], eax
mov eax, [y]
add eax, 1
mov dword [y], eax

jmp escape7835

false7835:


escape7835:

jmp j9376



align 4
lfb_addr: dd 0

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