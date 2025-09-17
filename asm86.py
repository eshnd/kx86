import os
import sys
import random

bootloader = """
org 0x7C00
bits 16

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00





    mov [dap_num_sectors], word 127 
    mov [dap_offset], word 0x7E00 
    mov [dap_segment], word 0x0000
    mov dword [dap_lba], 1          
    mov dword [dap_lba+4], 0     

    mov si, dap
    mov ah, 0x42
    mov dl, 0x80   
    int 0x13
    jc disk_error
idx_53479354:
    dw 4
loop_2054387:
    add dword [dap_lba], 127
    mov cx, 127
    advance_offset1:
        add word [dap_offset], 512
        loop advance_offset1
    mov word [dap_num_sectors], 127
    int 0x13
    jc disk_error
    sub word [idx_53479354], 1
    cmp word [idx_53479354], 0
    jne loop_2054387




    jmp 0x0000:0x7E00 


disk_error:
    hlt

dap:
dap_size:       db 0x10
dap_reserved:   db 0
dap_num_sectors: dw 0
dap_offset:     dw 0
dap_segment:    dw 0
dap_lba:        dq 0

times 510-($-$$) db 0
dw 0xAA55

"""

kernel = """
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
; mouse.asm
[BITS 32]

section .bss
mouse_x: resd 1
mouse_y: resd 1
mouse_buttons: resb 1

section .data
; Mouse packet buffer
mouse_packet: times 3 db 0
mouse_cycle: db 0

section .text
global mouse_init
extern irq12_handler_end

; -----------------------
; Write byte to PS/2 controller
; -----------------------
write_mouse:
    push eax
.wait:
    in al, 0x64        ; read status
    test al, 2
    jnz .wait
    pop eax
    out 0x60, al
    ret

; -----------------------
; Mouse IRQ handler
; -----------------------
mouse_irq_handler:
    pusha

    in al, 0x60            ; read byte from mouse
    mov bl, [mouse_cycle]

    cmp bl, 0
    je .first_byte
    cmp bl, 1
    je .second_byte
    cmp bl, 2
    je .third_byte

.first_byte:
    mov [mouse_packet], al
    inc byte [mouse_cycle]
    jmp .done

.second_byte:
    mov [mouse_packet+1], al
    inc byte [mouse_cycle]
    jmp .done

.third_byte:
    mov [mouse_packet+2], al
    xor byte [mouse_cycle], 0       ; reset to 0

    ; update mouse_x and mouse_y
    movsx eax, byte [mouse_packet+1]
    add dword [mouse_x], eax

    movsx eax, byte [mouse_packet+2]
    add dword [mouse_y], eax

    ; store buttons
    mov al, [mouse_packet]
    and al, 7                  ; left, right, middle
    mov [mouse_buttons], al

.done:
    ; send EOI to PIC
    mov al, 0x20
    out 0xA0, al     ; slave
    out 0x20, al     ; master

    popa
    iretd

; -----------------------
; Initialize mouse
; -----------------------
mouse_init:
    ; Enable IRQ12 on PIC (unmask)
    in al, 0xA1
    and al, 0xEF      ; clear bit 4 (IRQ12)
    out 0xA1, al

    ; Enable mouse device
    mov al, 0xA8
    out 0x64, al

    ; Tell mouse to use default settings
    mov al, 0xD4
    out 0x64, al
    mov al, 0xF4
    out 0x60, al

    ret

"""

def create_image(name, show="*"):
    global kernel
    kernel += """


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
    if show != "*":
        with open(show, "w") as f:
            f.write(kernel)
    os.system(f"nasm -f bin .boot{id_num}.asm -o .boot{id_num}.bin")
    os.system(f"nasm -f bin .kernel{id_num}.asm -o .kernel{id_num}.bin")
    os.system(f"dd if=/dev/zero of={name} bs=512 count=200")
    os.system(f"dd if=.boot{id_num}.bin of={name} conv=notrunc")
    os.system(f"dd if=.kernel{id_num}.bin of={name} bs=512 seek=1 conv=notrunc")
    
    os.remove(f".boot{id_num}.asm")
    os.remove(f".boot{id_num}.bin")
    os.remove(f".kernel{id_num}.asm")
    os.remove(f".kernel{id_num}.bin")