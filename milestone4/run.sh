python parser.py $1
echo "Parsing completed!"
python irparser.py ThreeAddressCode.txt
echo -e "Nasm 32 bit assembly code generated!\n Compiling using nasm:"
nasm -f elf asmfile
gcc -m32 -o nesmex asmfile.o
echo "Enter input:"
./nesmex 

