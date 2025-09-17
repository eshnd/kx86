import os
import sys
import random

bootloader = """
org 0x7C00

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax

    mov ah, 0x02
    mov al, 0x01
    mov ch, 0x00
    mov cl, 0x02
    mov dh, 0x00
    mov dl, 0x80
    mov bx, 0x1000
    int 0x13
    jc disk_error
    jmp 0x1000
disk_error:
    hlt

times 510-($-$$) db 0
dw 0xAA55
"""

kernel = """
org 0x1000

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
"""

def create_image(name):
    global kernel
    kernel += """
.hang:
    hlt
    jmp .hang
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
DATA_SEL equ 0x10"""
    id_num = random.randint(1000,10000)
    attempts = 0
    while os.path.exists(f".boot{id_num}.asm") or os.path.exists(f".boot{id_num}.bin") or os.path.exists(f".kernel{id_num}.asm") or os.path.exists(f".kernel{id_num}.bin"):
        if attempts > 1000:
            print(f"please don't have lots of files with similar names to '.boot{id_num}.asm'/'.boot{id_num}.bin'/'.kernel{id_num}.asm'/'.boot{id_num}.bin'")
            sys.exit()
        id_num = random.randint(1000,10000)
        attempts += 1

    with open(f".boot{id_num}.asm", "w") as f:
        f.write(bootloader)

    with open(f".kernel{id_num}.asm", "w") as f:
        f.write(kernel)
    
    os.system(f"nasm -f bin .boot{id_num}.asm -o .boot{id_num}.bin")
    os.system(f"nasm -f bin .kernel{id_num}.asm -o .kernel{id_num}.bin")
    os.system(f"cat .boot{id_num}.bin .kernel{id_num}.bin > {name}")
    
    os.remove(f".boot{id_num}.asm")
    os.remove(f".boot{id_num}.bin")
    # os.remove(f".kernel{id_num}.asm")
    os.remove(f".kernel{id_num}.bin")