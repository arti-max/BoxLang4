; Generated with BoxLang4 
; BoxLang4 created by arti 
jmp func__start 
; Function putc 
func_putc: 
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
; Function print_nl 
func_print_nl: 
     psh %bp
     mov %bp %sp
     psh 10    ; 10
     jsr func_putc
     add %sp 3
.end:
     mov %sp %bp
     pop %bp
     ret
; Function trap 
func_trap: 
     psh %bp
     mov %bp %sp
     trap
.end:
     mov %sp %bp
     pop %bp
     ret
; Function _start 
func__start: 
     psh %bp
     mov %bp %sp
    sub %sp 20
     psh 10    ; 10
     pop %ac
     mov %bs %bp
     sub %bs 3
    sh %bs %ac
     psh 20    ; 20
     pop %ac
     mov %bs %bp
     sub %bs 6
    sh %bs %ac
     mov %bs %bp
     sub %bs 6
     lh %bs %ac
     psh %ac
     mov %bs %bp
     sub %bs 3
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_3
    psh 0
    jmp _end_cmp__start_4
_true__start_3:
    psh 1
_end_cmp__start_4:
     pop %ac
     cmp %ac 0
     je _else__start_1
     psh 65
     jsr func_putc
     add %sp 3
     jmp _endif__start_2
_else__start_1:
     psh 66
     jsr func_putc
     add %sp 3
_endif__start_2:
     jsr func_print_nl
     psh 100    ; 100
     pop %ac
     mov %bs %bp
     sub %bs 9
    sh %bs %ac
     psh 100    ; 100
     mov %bs %bp
     sub %bs 9
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_7
    cmp %ac %bs
    je _true__start_7
    psh 0
    jmp _end_cmp__start_8
_true__start_7:
    psh 1
_end_cmp__start_8:
     pop %ac
     cmp %ac 0
     je _endif__start_6
     psh 50    ; 50
     pop %ac
     mov %bs %bp
     sub %bs 12
    sh %bs %ac
     psh 40    ; 40
     mov %bs %bp
     sub %bs 12
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jl _true__start_11
    psh 0
    jmp _end_cmp__start_12
_true__start_11:
    psh 1
_end_cmp__start_12:
     pop %ac
     cmp %ac 0
     je _else__start_9
     psh 88
     jsr func_putc
     add %sp 3
     jmp _endif__start_10
_else__start_9:
     psh 89
     jsr func_putc
     add %sp 3
_endif__start_10:
_endif__start_6:
     jsr func_print_nl
     psh 5    ; 5
     pop %ac
     mov %bs %bp
     sub %bs 15
    sh %bs %ac
_while_start__start_13:
     psh 0    ; 0
     mov %bs %bp
     sub %bs 15
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_15
    psh 0
    jmp _end_cmp__start_16
_true__start_15:
    psh 1
_end_cmp__start_16:
    pop %ac
    cmp %ac 0
    je _while_end__start_14
     psh 42
     jsr func_putc
     add %sp 3
     psh 1    ; 1
     mov %bs %bp
     sub %bs 15
     lh %bs %ac
     psh %ac
     pop %ac
     pop %bs
     sub %ac %bs
     psh %ac
     pop %ac
     mov %bs %bp
     sub %bs 15
     sh %bs %ac
    jmp _while_start__start_13
_while_end__start_14:
     jsr func_print_nl
     psh 99
     pop %ac
     mov %bs %bp
     sub %bs 16
    sb %bs %ac
     psh 0    ; 0
     pop %ac
     mov %bs %bp
     sub %bs 19
    sh %bs %ac
     mov %bs %bp
     sub %bs 16
     lb %bs %ac
     psh %ac
     pop %ac
     psh %ac
     psh %ac
     psh 97
     pop %bs
     pop %ac
     cmp %ac %bs
    je _case_body_0__start_19
     pop %ac
     psh %ac
     psh %ac
     psh 98
     pop %bs
     pop %ac
     cmp %ac %bs
    je _case_body_1__start_20
     pop %ac
     psh %ac
     psh %ac
     psh 99
     pop %bs
     pop %ac
     cmp %ac %bs
    je _case_body_2__start_21
     add %sp 3
    jmp _default__start_18
_case_body_0__start_19:
     add %sp 3
     psh 1    ; 1
     pop %ac
     mov %bs %bp
     sub %bs 19
     sh %bs %ac
    jmp _switch_end__start_17
_case_body_1__start_20:
     add %sp 3
     psh 2    ; 2
     pop %ac
     mov %bs %bp
     sub %bs 19
     sh %bs %ac
    jmp _switch_end__start_17
_case_body_2__start_21:
     add %sp 3
     psh 3    ; 3
     pop %ac
     mov %bs %bp
     sub %bs 19
     sh %bs %ac
    jmp _switch_end__start_17
_default__start_18:
     psh 99    ; 99
     pop %ac
     mov %bs %bp
     sub %bs 19
     sh %bs %ac
_switch_end__start_17:
     psh 3    ; 3
     mov %bs %bp
     sub %bs 19
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    je _true__start_24
    psh 0
    jmp _end_cmp__start_25
_true__start_24:
    psh 1
_end_cmp__start_25:
     pop %ac
     cmp %ac 0
     je _endif__start_23
     psh 51
     jsr func_putc
     add %sp 3
_endif__start_23:
     jsr func_print_nl
     psh 122
     pop %ac
     mov %bs %bp
     sub %bs 20
    sb %bs %ac
     mov %bs %bp
     sub %bs 20
     lb %bs %ac
     psh %ac
     pop %ac
     psh %ac
     psh %ac
     psh 120
     pop %bs
     pop %ac
     cmp %ac %bs
    je _case_body_0__start_28
     pop %ac
     psh %ac
     psh %ac
     psh 121
     pop %bs
     pop %ac
     cmp %ac %bs
    je _case_body_1__start_29
     add %sp 3
    jmp _default__start_27
_case_body_0__start_28:
     add %sp 3
     psh 88
     jsr func_putc
     add %sp 3
    jmp _switch_end__start_26
_case_body_1__start_29:
     add %sp 3
     psh 89
     jsr func_putc
     add %sp 3
    jmp _switch_end__start_26
_default__start_27:
     psh 68
     jsr func_putc
     add %sp 3
_switch_end__start_26:
     jsr func_print_nl
     psh 0
     int $0
.end:
     mov %sp %bp
     pop %bp
     ret
