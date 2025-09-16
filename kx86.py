import asm86
import argparse
import random

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

def arguments(cmd, splitter, amount):
    replacement = random.randint(1, 10000)
    while str(replacement) in cmd:
        replacement = random.randint(1, 10000)
    cmd = cmd.replace(splitter, str(replacement), amount)
    return cmd.split(str(replacement))

def kx86_compile(body, splitter = ";"):
    final = ""
    labels = []
    packs = {}
    body = body.split(splitter)
    for i in range(len(body)):
        cmd = body[i].strip()
        if cmd.strip() == "":
            continue
        cmd = arguments(cmd, ":", 1)
        match cmd[0].strip():
            case "pixel":
                cmd[1] = arguments(cmd[1].strip(), ",", 2)
                final += draw_pixel(cmd[1][0].strip(), cmd[1][1].strip(), cmd[1][2].strip())
            
            case "pack":
                cmd[1] = arguments(cmd[1].strip(), ",", 1)
                packs[cmd[1][0].strip()] = cmd[1][1].strip()

            case "call":
                final += kx86_compile(packs[cmd[1].strip()], "&")

            case "forever":
                label = random.randint(1,10000)
                while label in labels:
                    label = random.randint(1,10000)
                labels.append(label)
                final += f"j{label}:\n" + kx86_compile(packs[cmd[1].strip()], "&") + f"\njmp j{label}"
            

    return final
    
if __name__ == "__main__":
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