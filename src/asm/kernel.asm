
org 0x7E00

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    mov ax, 0x4F02
    mov bx, 0x11F | 0x4000
    int 0x10

    mov ax, 0x4F01
    mov cx, 0x11F
    mov di, mode_info
    int 0x10
    
    

    mov eax, [mode_info + 0x28]
    mov [lfb_addr], eax

    mov ax, [mode_info + 0x12]
    mov [lfb_pitch], ax

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


x:
dd 0

y:
dd 0

j5704:

CheckKeyboard9891:
    in al, 0x64
    test al, 1
    jz Done9891
    in al, 0x60
    cmp al, 0x80
    jb Pressed9891
    sub al, 0x80
    mov byte [KEYS+eax], 0
    jmp Done9891

Pressed9891:
    mov byte [KEYS+eax], 1

Done9891:
    cmp byte [KEYS+0x1E], 1
    jne false9891
    sub byte [KEYS+0x1E], 1
    jmp true9891


true9891:




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


mov eax, [x]
add eax, 1
mov dword [x], eax
mov eax, [y]
add eax, 1
mov dword [y], eax

jmp escape9891

false9891:


escape9891:

jmp j5704



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