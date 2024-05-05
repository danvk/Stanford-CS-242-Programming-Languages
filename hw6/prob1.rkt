#lang racket
(print-as-expression #f)
(provide (all-defined-out))

;================;
; Internal Defns ;
;================;
; create a stack.
(define _stack empty)

; store a top-level continuation.
(define _exit null)
(call/cc (lambda (k) (set! _exit k)))

;==============;
; Helper Funcs ;
;==============;
; return #t if the stack is empty, and #f otherwise.
(define (stack_empty?)
  (empty? _stack))

; push `e` to the stack, and return nothing.
(define (stack_push e)
  (set! _stack (append (list e) _stack)))

; pop the topmost element from the stack, and return the element.
(define (stack_pop)
  (if (stack_empty?)
    (error "trying to pop from the empty stack!")
    (let* ([top (first _stack)])
      (set! _stack (rest _stack))
      top)))

; exit to the top-level, and return nothing.
(define (exit) (_exit))

;===========;
; Problem 1 ;
;===========;
; Task: Implement `throw` and `try_except` using `call/cc`.
; Note: You can define any other helper functions.

(define (throw msg)
  ; If an exception is thrown by throw outside try f
  ; (i.e., either inside except f or outside (try except ...)),
  ; you should print out an error message ThrowError and exit to the top-level.
  (if (stack_empty?)
    ((let* () (printf "ThrowError\n") (exit)))
    (let*
      ([pair (stack_pop)]
       [k (first pair)]
       [except_f (second pair)])
      (k (except_f msg))
    )
  )
)

(define (try_except try_f except_f)
  ; "push the current continuation k and except_f to the stack"
  (call/cc (lambda (k) (let* ()
    (stack_push (list k except_f))
    (let* ([result (try_f)])
      (stack_pop)
      (k result)
    )
  ))))
