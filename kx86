#!/bin/python3
import asm86
import argparse
import random

data = {}
packs = {}
labels = []
bools = []
mice = []

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
    mov dword [edi], 0x{color[1:]}
"""

def arguments(cmd, splitter, amount):
    replacement = random.randint(1, 10000)
    while str(replacement) in cmd:
        replacement = random.randint(1, 10000)
    cmd = cmd.replace(splitter, str(replacement), amount)
    return cmd.split(str(replacement))

def kx86_compile(body, splitter = ";"):
    while "/:" and ":/" in body:
        body = body[:body.index("/:")] + body[body.index(":/") + 2:]
    final = ""
    global data, packs, labels, bools
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
                params = 1
                try:
                    func = packs[cmd[1][:cmd[1].index(",")].strip()]
                    while f"${params}" in func:
                        params += 1
                    cmd[1] = arguments(cmd[1].strip(), ",", params)
                    for g in range(1, params):
                        func = func.replace(f"${g}", cmd[1][g])
                    final += kx86_compile(func, "&") + "\n"
                except:
                    final += kx86_compile(packs[cmd[1].strip()], "&") + "\n"


            case "forever":
                label = random.randint(1,10000)
                while label in labels:
                    label = random.randint(1,10000)
                labels.append(label)

                params = 1
                try:
                    func = packs[cmd[1][:cmd[1].index(",")].strip()]
                    while f"${params}" in func:
                        params += 1
                    cmd[1] = arguments(cmd[1].strip(), ",", params)
                    for g in range(1, params):
                        func = func.replace(f"${g}", cmd[1][g])

                    final += f"\nj{label}:\n" + kx86_compile(func, "&") + f"\njmp j{label}\n"
                except:
                    final += f"\nj{label}:\n" + kx86_compile(packs[cmd[1].strip()], "&") + f"\njmp j{label}\n"

            case "//":
                pass

            case "num":
                cmd[1] = arguments(cmd[1].strip(), ",", 1)
                data["[" + cmd[1][0].strip() + "]"] = "num"
                final += "\n" + cmd[1][0].strip() + f":\ndd {cmd[1][1].strip()}\n"

            case "edit":
                cmd[1] = arguments(cmd[1].strip(), ",", 1)
                final += f"\nmov dword {cmd[1][0].strip()}, {cmd[1][1].strip()}\n"
                    
            case "if":
                bool_num = random.randint(1,10000)
                while bool_num in bools:
                    bool_num = random.randint(1,10000)
                bools.append(bool_num)
                
                
                cmd[1] = arguments(cmd[1].strip(), ",", 2)
                if ">=" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split(">=")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\njge true{bool_num}\njl false{bool_num}\n"
                elif "<=" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split("<=")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\njle true{bool_num}\njg false{bool_num}\n"
                elif "==" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split("==")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\nje true{bool_num}\njne false{bool_num}\n"
                elif "!=" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split("!=")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\njne true{bool_num}\nje false{bool_num}\n"
                elif "<" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split("<")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\njl true{bool_num}\njge false{bool_num}\n"
                elif ">" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split(">")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\njg true{bool_num}\njle false{bool_num}\n"
                else:
                    bool = cmd[1][0].strip() # this is the key that you're checking is pressed
                    final += f"""

"""


                final += f"\ntrue{bool_num}:\n\n"
                final += "\n" + kx86_compile(packs[cmd[1][1].strip()[5:]], "&") + "\n"
                final += "\n" + f"jmp escape{bool_num}" + "\n"
                final += f"\nfalse{bool_num}:\n\n"
                if cmd[1][2].strip()[5:] != "NONE": # DO THIS AGAIN THE TRUE GOES INTO THE FALSE OH NO
                    final += "\n" + kx86_compile(packs[cmd[1][2].strip()[5:]], "&") + "\n"
                final += "\n" + f"escape{bool_num}:" + "\n"
                    
            case "while":
                bool_num = random.randint(1,10000)
                while bool_num in bools:
                    bool_num = random.randint(1,10000)
                bools.append(bool_num)
                
                cmd[1] = arguments(cmd[1].strip(), ",", 1)
                final += f"\nwhile{bool_num}:\n"
                if ">=" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split(">=")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\njge true{bool_num}\njl false{bool_num}\n"
                elif "<=" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split("<=")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\njle true{bool_num}\njg false{bool_num}\n"
                elif "==" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split("==")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\nje true{bool_num}\njne false{bool_num}\n"
                elif "!=" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split("!=")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\njne true{bool_num}\nje false{bool_num}\n"
                elif "<" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split("<")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\njl true{bool_num}\njge false{bool_num}\n"
                elif ">" in cmd[1][0]:
                    bool = cmd[1][0].strip()
                    bool = bool.split(">")
                    final += f"\nmov eax, {bool[0].strip()}\ncmp eax, {bool[1].strip()}\njg true{bool_num}\njle false{bool_num}\n"
                
                final += f"\ntrue{bool_num}:\n\n"
                final += "\n" + kx86_compile(packs[cmd[1][1].strip()[5:]], "&") + "\n"
                final += "\n" + f"jmp while{bool_num}" + "\n"
                final += f"\nfalse{bool_num}:\n\n"
            case "op":
                cmd[1] = arguments(cmd[1].strip(), ",", 1)
                
                if "+" in cmd[1][0]: # add compiler type corresponding THIS ISNT DONE FUNCTIONS NEED TO BE ASSSIGNED
                    bool = cmd[1][0].strip()
                    bool = bool.split("+")
                    final += f"\nmov eax, {bool[0].strip()}\nadd eax, {bool[1].strip()}\nmov dword {cmd[1][1]}, eax"
                if "-" in cmd[1][0]: # add compiler type corresponding THIS ISNT DONE FUNCTIONS NEED TO BE ASSSIGNED
                    bool = cmd[1][0].strip()
                    bool = bool.split("-")
                    final += f"\nmov eax, {bool[0].strip()}\nsub eax, {bool[1].strip()}\nmov dword {cmd[1][1]}, eax"
                if "*" in cmd[1][0]: # add compiler type corresponding THIS ISNT DONE FUNCTIONS NEED TO BE ASSSIGNED
                    bool = cmd[1][0].strip()
                    bool = bool.split("*")
                    final += f"\nmov eax, {bool[0].strip()}\nimul eax, {bool[1].strip()}\nmov dword {cmd[1][1]}, eax"
                if "/" in cmd[1][0]: # add compiler type corresponding THIS ISNT DONE FUNCTIONS NEED TO BE ASSSIGNED
                    bool = cmd[1][0].strip()
                    bool = bool.split("/")
                    final += f"\nmov eax, {bool[0].strip()}\nidiv eax, {bool[1].strip()}\nmov dword {cmd[1][1]}, eax"
                
            case "array":
                cmd[1] = arguments(cmd[1].strip(), ",", 1)
                data["[" + cmd[1][0].strip() + "]"] = "array"
                final += "\n" + cmd[1][0].strip() + f":\ndd {cmd[1][1].strip()}\n"

            case "cast":
                cmd[1] = arguments(cmd[1].strip(), ",", 1)
                if cmd[1][0].strip() == "float":
                    final += f"""
{cmd[1][1].strip()[1:-1]}_f:
dd 0
fild dword {cmd[1][1].strip()}
fstp dword [{cmd[1][1].strip()[1:-1]}_f]
"""
                elif cmd[1][0].strip() == "int":
                    final += f"""
{cmd[1][1].strip()[1:-1]}_i:
dd 0
fld dword {cmd[1][1].strip()}
fistp dword [{cmd[1][1].strip()[1:-1]}_i]
"""

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

    asm86.kernel += kx86_compile(body).replace("@", " + ").replace("{", "").replace("}", "")
    asm86.create_image(args.output)
