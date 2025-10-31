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
; Function cli_print_nl 
func_cli_print_nl: 
     psh %bp
     mov %bp %sp
     psh 10    ; 10
     jsr func_cli_putc
     add %sp 3
.end:
     mov %sp %bp
     pop %bp
     ret
; Function _start 
func__start: 
     psh %bp
     mov %bp %sp
    sub %sp 12
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
     psh 5    ; 5
     mov %bs %bp
     sub %bs 3
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_9
    psh 0
    jmp _end_cmp__start_10
_true__start_9:
    psh 1
_end_cmp__start_10:
     pop %ac
     cmp %ac 0
     je _land_false__start_7
     psh 15    ; 15
     mov %bs %bp
     sub %bs 6
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_11
    psh 0
    jmp _end_cmp__start_12
_true__start_11:
    psh 1
_end_cmp__start_12:
     pop %ac
     cmp %ac 0
     je _land_false__start_7
     psh 1
     jmp _land_end__start_8
_land_false__start_7:
     psh 0
_land_end__start_8:
     pop %ac
     cmp %ac 0
     je _else__start_5
     psh 84
     jsr func_cli_putc
     add %sp 3
     jmp _endif__start_6
_else__start_5:
     psh 70
     jsr func_cli_putc
     add %sp 3
_endif__start_6:
     psh 5    ; 5
     mov %bs %bp
     sub %bs 3
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jl _true__start_17
    psh 0
    jmp _end_cmp__start_18
_true__start_17:
    psh 1
_end_cmp__start_18:
     pop %ac
     cmp %ac 0
     je _land_false__start_15
     psh 15    ; 15
     mov %bs %bp
     sub %bs 6
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_19
    psh 0
    jmp _end_cmp__start_20
_true__start_19:
    psh 1
_end_cmp__start_20:
     pop %ac
     cmp %ac 0
     je _land_false__start_15
     psh 1
     jmp _land_end__start_16
_land_false__start_15:
     psh 0
_land_end__start_16:
     pop %ac
     cmp %ac 0
     je _else__start_13
     psh 70
     jsr func_cli_putc
     add %sp 3
     jmp _endif__start_14
_else__start_13:
     psh 83
     jsr func_cli_putc
     add %sp 3
_endif__start_14:
     jsr func_cli_print_nl
     psh 20    ; 20
     mov %bs %bp
     sub %bs 3
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_25
    psh 0
    jmp _end_cmp__start_26
_true__start_25:
    psh 1
_end_cmp__start_26:
     pop %ac
     cmp %ac 0
     jne _lor_true__start_23
     psh 15    ; 15
     mov %bs %bp
     sub %bs 6
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_27
    psh 0
    jmp _end_cmp__start_28
_true__start_27:
    psh 1
_end_cmp__start_28:
     pop %ac
     cmp %ac 0
     jne _lor_true__start_23
     psh 0
     jmp _lor_end__start_24
_lor_true__start_23:
     psh 1
_lor_end__start_24:
     pop %ac
     cmp %ac 0
     je _else__start_21
     psh 84
     jsr func_cli_putc
     add %sp 3
     jmp _endif__start_22
_else__start_21:
     psh 70
     jsr func_cli_putc
     add %sp 3
_endif__start_22:
     psh 5    ; 5
     mov %bs %bp
     sub %bs 3
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_33
    psh 0
    jmp _end_cmp__start_34
_true__start_33:
    psh 1
_end_cmp__start_34:
     pop %ac
     cmp %ac 0
     jne _lor_true__start_31
     psh 25    ; 25
     mov %bs %bp
     sub %bs 6
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_35
    psh 0
    jmp _end_cmp__start_36
_true__start_35:
    psh 1
_end_cmp__start_36:
     pop %ac
     cmp %ac 0
     jne _lor_true__start_31
     psh 0
     jmp _lor_end__start_32
_lor_true__start_31:
     psh 1
_lor_end__start_32:
     pop %ac
     cmp %ac 0
     je _else__start_29
     psh 83
     jsr func_cli_putc
     add %sp 3
     jmp _endif__start_30
_else__start_29:
     psh 70
     jsr func_cli_putc
     add %sp 3
_endif__start_30:
     jsr func_cli_print_nl
     psh 5    ; 5
     pop %ac
     mov %bs %bp
     sub %bs 9
    sh %bs %ac
     psh 12    ; 12
     pop %ac
     mov %bs %bp
     sub %bs 12
    sh %bs %ac
     psh 4    ; 4
     mov %bs %bp
     sub %bs 12
     lh %bs %ac
     psh %ac
     mov %bs %bp
     sub %bs 9
     lh %bs %ac
     psh %ac
     pop %ac
     pop %bs
  and %ac %bs
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    je _true__start_39
    psh 0
    jmp _end_cmp__start_40
_true__start_39:
    psh 1
_end_cmp__start_40:
     pop %ac
     cmp %ac 0
     je _endif__start_38
     psh 38
     jsr func_cli_putc
     add %sp 3
_endif__start_38:
     psh 13    ; 13
     mov %bs %bp
     sub %bs 12
     lh %bs %ac
     psh %ac
     mov %bs %bp
     sub %bs 9
     lh %bs %ac
     psh %ac
     pop %ac
     pop %bs
   or %ac %bs
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    je _true__start_43
    psh 0
    jmp _end_cmp__start_44
_true__start_43:
    psh 1
_end_cmp__start_44:
     pop %ac
     cmp %ac 0
     je _endif__start_42
     psh 124
     jsr func_cli_putc
     add %sp 3
_endif__start_42:
     psh 9    ; 9
     mov %bs %bp
     sub %bs 12
     lh %bs %ac
     psh %ac
     mov %bs %bp
     sub %bs 9
     lh %bs %ac
     psh %ac
     pop %ac
     pop %bs
  xor %ac %bs
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    je _true__start_47
    psh 0
    jmp _end_cmp__start_48
_true__start_47:
    psh 1
_end_cmp__start_48:
     pop %ac
     cmp %ac 0
     je _endif__start_46
     psh 94
     jsr func_cli_putc
     add %sp 3
_endif__start_46:
     jsr func_cli_print_nl
     psh 0    ; 0
     mov %bs %bp
     sub %bs 3
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_55
    psh 0
    jmp _end_cmp__start_56
_true__start_55:
    psh 1
_end_cmp__start_56:
     pop %ac
     cmp %ac 0
     je _land_false__start_53
     psh 0    ; 0
     mov %bs %bp
     sub %bs 6
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_57
    psh 0
    jmp _end_cmp__start_58
_true__start_57:
    psh 1
_end_cmp__start_58:
     pop %ac
     cmp %ac 0
     je _land_false__start_53
     psh 1
     jmp _land_end__start_54
_land_false__start_53:
     psh 0
_land_end__start_54:
     pop %ac
     cmp %ac 0
     jne _lor_true__start_51
     psh 100    ; 100
     mov %bs %bp
     sub %bs 9
     lh %bs %ac
     psh %ac
    pop %ac
    pop %bs
    cmp %ac %bs
    jg _true__start_59
    psh 0
    jmp _end_cmp__start_60
_true__start_59:
    psh 1
_end_cmp__start_60:
     pop %ac
     cmp %ac 0
     jne _lor_true__start_51
     psh 0
     jmp _lor_end__start_52
_lor_true__start_51:
     psh 1
_lor_end__start_52:
     pop %ac
     cmp %ac 0
     je _else__start_49
     psh 80
     jsr func_cli_putc
     add %sp 3
     jmp _endif__start_50
_else__start_49:
     psh 102
     jsr func_cli_putc
     add %sp 3
_endif__start_50:
     jsr func_cli_print_nl
     psh 0
     int $0
.end:
     mov %sp %bp
     pop %bp
     ret
