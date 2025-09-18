
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

j8506:

CheckKeyboard5345:
    in al, 0x64
    test al, 1
    jz Done5345
    in al, 0x60
    cmp al, 0x80
    jb Pressed5345
    sub al, 0x80
    mov byte [KEYS+eax], 0
    jmp Done5345

Pressed5345:
    mov byte [KEYS+eax], 1

Done5345:
    cmp byte [KEYS+0x1E], 1
    jne false5345
    sub byte [KEYS+0x1E], 1
    jmp true5345


true5345:



; inputs: esi = lfb base
;         x = 100
;         y = 100
;         color = red (0xFF0000)

mov edi, esi          ; edi = lfb base

; compute y * pitch
mov ecx, [y]          ; y
mov dx, [lfb_pitch]   ; pitch
movzx edx, dx         ; edx = pitch (32-bit)
imul ecx, edx         ; ecx = y * pitch

; compute x * 3 (3 bytes per pixel)
mov eax, [x]          ; x
imul eax, 3           ; eax = x * 3

; total offset
add ecx, eax
add edi, ecx          ; edi = pixel address

; write pixel (B G R)
mov dword [edi], 0xFF0000


mov eax, [x]
add eax, 1
mov dword [x], eax
mov eax, [y]
add eax, 1
mov dword [y], eax

jmp escape5345

false5345:


escape5345:

jmp j8506



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