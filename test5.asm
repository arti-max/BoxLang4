; Generated with BoxLang4 
; BoxLang4 created by arti 
jmp func__start 
; Function cli_putc 
func_cli_putc: 
     psh %bp
     mov %bp %sp
     mov %bs %bp
     add %bs 6
     lb %bs %ac
     psh %ac
     int $2
.end:
     mov %sp %bp
     pop %bp
     ret
; Function cli_puts 
func_cli_puts: 
     psh %bp
     mov %bp %sp
_while_start_cli_puts_1:
     psh 0    ; 0
     mov %bs %bp
     add %bs 6
     lh %bs %ac
     psh %ac
    pop %bs
    lb %bs %ac
    psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jne _true_cli_puts_3
    psh 0
    jmp _end_cmp_cli_puts_4
_true_cli_puts_3:
    psh 1
_end_cmp_cli_puts_4:
    pop %ac
    cmp %ac 0
    je _while_end_cli_puts_2
     mov %bs %bp
     add %bs 6
     lh %bs %ac
     psh %ac
    pop %bs
    lb %bs %ac
    psh %ac
     jsr func_cli_putc
     add %sp 3
     psh 1    ; 1
     mov %bs %bp
     add %bs 6
     lh %bs %ac
     psh %ac
     pop %ac
     pop %bs
     add %ac %bs
     psh %ac
     pop %ac
     mov %bs %bp
     add %bs 6
     sh %bs %ac
    jmp _while_start_cli_puts_1
_while_end_cli_puts_2:
.end:
     mov %sp %bp
     pop %bp
     ret
; Function _start 
func__start: 
     psh %bp
     mov %bp %sp
     mov %ac __str_0
     psh %ac
     jsr func_cli_puts
     add %sp 3
     psh 10
     jsr func_cli_putc
     add %sp 3
     psh 0
     int $0
.end:
     mov %sp %bp
     pop %bp
     ret

;section data
__str_0: bytes "Hello, World!" 0