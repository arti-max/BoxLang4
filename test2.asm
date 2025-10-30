; Generated with BoxLang4 
; BoxLang4 created by arti 
jmp func__start 
; Function puts 
func_puts: 
     psh %bp
     mov %bp %sp
.end:
     mov %sp %bp
     pop %bp
     ret
; Function putc 
func_putc: 
     psh %bp
     mov %bp %sp
     mov %bs %bp
     add %bs 6
     lh %bs %ac
     psh %ac
    int $2
.end:
     mov %sp %bp
     pop %bp
     ret
; Function sum 
func_sum: 
     psh %bp
     mov %bp %sp
     mov %bs %bp
     add %bs 9
     lh %bs %ac
     psh %ac
     mov %bs %bp
     add %bs 6
     lh %bs %ac
     psh %ac
     pop %ac
     pop %bs
     add %ac %bs
     psh %ac
    pop %ac
    jmp .end
.end:
     mov %sp %bp
     pop %bp
     ret
; Function _start 
func__start: 
     psh %bp
     mov %bp %sp
     sub %sp 13
     psh 98
     pop %ac
     mov %bs %bp
     sub %bs 1
    sb %bs %ac
     psh 1    ; 1
     psh 101
     jsr func_sum
     add %sp 6
    psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 6
    sb %bs %ac
     mov %bs %bp
     sub %bs 9
     lh %bs %ac
     psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 12
    sh %bs %ac
     psh 116
     psh 1    ; 1
    mov %ac %bp
    sub %ac 2
    psh %ac
     pop %ac
     pop %bs
     add %ac %bs
     psh %ac
     pop %bs
     pop %ac
     sb %bs %ac
    mov %ac %bp
    sub %ac 1
    psh %ac
    pop %bs
    lb %bs %ac
    psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 13
    sb %bs %ac
     psh 1    ; 1
    mov %ac %bp
    sub %ac 2
    psh %ac
     pop %ac
     pop %bs
     add %ac %bs
     psh %ac
    pop %bs
    lb %bs %ac
    psh %ac
     jsr func_putc
     add %sp 3
     psh 10    ; 10
     jsr func_putc
     add %sp 3
     mov %bs %bp
     sub %bs 6
     lb %bs %ac
     psh %ac
     jsr func_putc
     add %sp 3
     psh 10    ; 10
     jsr func_putc
     add %sp 3
     mov %ac __str_0
     psh %ac
     jsr func_puts
     add %sp 3
    psh 0
    int $0
.end:
     mov %sp %bp
     pop %bp
     ret

;section data
__str_0: bytes "Hello, World!" 0