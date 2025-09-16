import asm86
import argparse

def draw_pixel(x, y):
    asm86.kernel += f"""
    mov eax, esi
    mov ebx, {x}
    mov ecx, {y}
    mov edx, 1024
    mov edi, eax
    imul ecx, edx
    add ecx, ebx
    imul ecx, 3
    add edi, ecx
    mov dword [edi], 0x00FF0000"""

def kx86_compile(body):
    body = body.split(";")
    for i in range(len(body)):
        cmd = body[i].strip()
        cmd.split("(") # can replace with for c in s if need escapes
        cmd.split(")")
        match cmd[0]:
            case "draw_pixel":
                draw_pixel(cmd[1], cmd[2])
    

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument("-f", "--file", type=str, nargs="+", help="file or files to compile")
group.add_argument("-o", "--output", type=str, help="file to output to")

args = parser.parse_args()
body = ""

for i in range(len(args.file)):
    with open(args.file[i], "r") as f:
        body += "\n" + f.read()

body = kx86_compile(body)
asm86.create_image(args.output)