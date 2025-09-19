# kx86
an imperative, modular programming language to make x86 kernel development easy
# how it works
kx86 programs compile to a kernel which is then combined with a bootloader to make an os image
# to run
`qemu-system-i386 -drive format=raw,file=<IMAGE-FILE-PATH> -vga std -accel kvm -cpu max -m 1G`
# stack
the functionality is written in x86 assembly and the parser is written in python3
