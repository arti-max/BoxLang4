; Generated with BoxLang4 
; BoxLang4 created by arti 
jmp func__start 
; Function putc 
func_putc: 
     psh %bp
     mov %bp %sp
    psh %ac
    psh %bs
    mov %bs %bp
    add %bs 6
    lb %bs %ac
    pop %bs
    phs %ac
    pop %ac
    int $2
.end:
     mov %sp %bp
     pop %bp
     ret
; Function get_five 
func_get_five: 
     psh %bp
     mov %bp %sp
     psh 5    ; 5
    pop %ac
    jmp .end
.end:
     mov %sp %bp
     pop %bp
     ret
; Function add 
func_add: 
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
; Function multiply 
func_multiply: 
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
     mul %ac %bs
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
     sub %sp 24
     psh 4    ; 4
     pop %ac
     mov %bs %bp
     sub %bs 3
    sh %bs %ac
     psh 10    ; 10
     pop %ac
     mov %bs %bp
     sub %bs 6
    sh %bs %ac
     psh 30    ; 30
     pop %ac
     mov %bs %bp
     sub %bs 9
    sh %bs %ac
     psh 30    ; 30
     pop %ac
     mov %bs %bp
     sub %bs 12
    sh %bs %ac
     jsr func_get_five
    psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 15
    sh %bs %ac
     psh 10    ; 10
     mov %bs %bp
     sub %bs 15
     lh %bs %ac
     psh %ac
     jsr func_add
     add %sp 6
    psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 18
    sh %bs %ac
     mov %bs %bp
     sub %bs 18
     lh %bs %ac
     psh %ac
     psh 30    ; 30
     jsr func_multiply
     add %sp 6
    psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 21
    sh %bs %ac
     psh 30    ; 30
     mov %bs %bp
     sub %bs 21
     lh %bs %ac
     psh %ac
     pop %ac
     pop %bs
     sub %ac %bs
     psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 24
    sh %bs %ac
     mov %bs %bp
     sub %bs 24
     lh %bs %ac
     psh %ac
     jsr func_putc
     add %sp 3
.end:
     mov %sp %bp
     pop %bp
     ret
