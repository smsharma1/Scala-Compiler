section .text
global main
extern printf

main:

  mov eax, 0x10
  push eax
  push message
  call printf
  add esp, 8
  ret

message db "Register = %d", 10, 0
