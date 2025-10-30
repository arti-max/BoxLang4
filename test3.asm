; Generated with BoxLang4 
; BoxLang4 created by arti 
jmp func__start 
; Function _start 
func__start: 
     psh %bp
     mov %bp %sp
     sub %sp 66
     psh 5    ; 5
     pop %ac
     mov %bs %bp
     sub %bs 3
    sh %bs %ac
     psh 6    ; 6
     pop %ac
     mov %bs %bp
     sub %bs 6
    sh %bs %ac
     psh 30    ; 30
     pop %ac
     mov %bs %bp
     sub %bs 9
    sh %bs %ac
     psh 5    ; 5
     pop %ac
     mov %bs %bp
     sub %bs 12
    sh %bs %ac
     psh 14    ; 14
     pop %ac
     mov %bs %bp
     sub %bs 15
    sh %bs %ac
     psh 16    ; 16
     pop %ac
     mov %bs %bp
     sub %bs 18
    sh %bs %ac
     psh 20    ; 20
     pop %ac
     mov %bs %bp
     sub %bs 21
    sh %bs %ac
     psh 6    ; 6
     pop %ac
     mov %bs %bp
     sub %bs 24
    sh %bs %ac
     psh 16777211    ; -5
     pop %ac
     mov %bs %bp
     sub %bs 27
    sh %bs %ac
     psh 5    ; 5
     pop %ac
     mov %bs %bp
     sub %bs 30
    sh %bs %ac
     psh 16777206    ; -10
     pop %ac
     mov %bs %bp
     sub %bs 33
    sh %bs %ac
     psh 8    ; 8
     pop %ac
     mov %bs %bp
     sub %bs 36
    sh %bs %ac
     psh 100    ; 100
     pop %ac
     mov %bs %bp
     sub %bs 39
    sh %bs %ac
     psh 200    ; 200
     pop %ac
     mov %bs %bp
     sub %bs 42
    sh %bs %ac
     mov %bs %bp
     sub %bs 39
     lh %bs %ac
     psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 45
    sh %bs %ac
     mov %bs %bp
     sub %bs 42
     lh %bs %ac
     psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 48
    sh %bs %ac
     mov %bs %bp
     sub %bs 39
     lh %bs %ac
     psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 51
    sh %bs %ac
     mov %bs %bp
     sub %bs 42
     lh %bs %ac
     psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 54
    sh %bs %ac
     mov %bs %bp
     sub %bs 39
     lh %bs %ac
     psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 57
    sh %bs %ac
     psh 1    ; 1
     mov %bs %bp
     sub %bs 42
     lh %bs %ac
     psh %ac
     pop %ac
     pop %bs
     div %ac %bs
     psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 60
    sh %bs %ac
     psh 0    ; 0
     pop %ac
     mov %bs %bp
     sub %bs 63
    sh %bs %ac
     psh 0    ; 0
     pop %ac
     mov %bs %bp
     sub %bs 66
    sh %bs %ac
.end:
     mov %sp %bp
     pop %bp
     ret
