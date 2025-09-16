import asm86
import argparse

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

def kx86_compile(body, splitter = ";"):
    final = ""
    packs = {}
    body = body.split(splitter)
    for i in range(len(body)):
        cmd = body[i].strip()
        if cmd.strip() == "":
            continue
        cmd = [cmd[:cmd.index(":")].strip(), cmd[cmd.index(":") + 1:].strip()]
        match cmd[0].strip():
            case "draw_pixel":
                cmd[1] = [cmd[1][:cmd[1].index(",")].strip(), cmd[1][cmd[1].index(",") + 1:].strip()]
                cmd[1] = [cmd[1][0], cmd[1][1][:cmd[1][1].index(",")].strip(), cmd[1][1][cmd[1][1].index(",") + 1:].strip()]
                final += draw_pixel(cmd[1][0], cmd[1][1], cmd[1][2])
            
            case "pack":
                cmd[1] = [cmd[1][:cmd[1].index(",")].strip(), cmd[1][cmd[1].index(",") + 1:].strip()]
                packs[cmd[1][0]] = cmd[1][1]

            case "call":
                final += kx86_compile(packs[cmd[1]], "&")
                

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