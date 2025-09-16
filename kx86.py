import asm86
import argparse
import re

def draw_pixel(x, y, color):
    return f"""
    mov eax, esi
    mov ebx, {x}
    mov ecx, {y}
    mov edx, 1024
    mov edi, eax
    imul ecx, edx
    add ecx, ebx
    imul ecx, 3
    add edi, ecx
    mov dword [edi], 0x{color[1:]}"""

def kx86_compile(body):
    final = ""
    body = body.split(";")
    for i in range(len(body)):
        cmd = body[i].strip()
        cmd = re.split(r'[()]+', cmd) # can replace with for c in s if need escapes
        match cmd[0].strip():
            case "draw_pixel":
                cmd[1] = cmd[1].split(",")
                for j in range(len(cmd[1])):
                    cmd[1][j] = cmd[1][j].strip()
                final += draw_pixel(cmd[1][0], cmd[1][1], cmd[1][2])
    return final
    

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, nargs="+", help="file or files to compile")
parser.add_argument("-o", "--output", type=str, help="file to output to")

args = parser.parse_args()
body = ""

for i in range(len(args.file)):
    with open(args.file[i], "r") as f:
        body += "\n" + f.read()

asm86.kernel += kx86_compile(body)
asm86.create_image(args.output)