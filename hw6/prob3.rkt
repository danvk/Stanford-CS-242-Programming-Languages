#lang racket
(print-as-expression #f)
(provide (all-defined-out))

;================;
; Internal Defns ;
;================;
; create a stack.
(define _stack empty)

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

;===========;
; Problem 3 ;
;===========;
; Task: Implement `attempt` and `assert` using `call/cc`.
; Note: You can define any other helper functions.

(define (attempt l)
  ; We an assume l is non-empty.
  ; Push a pair of the continuation and the other options onto the stack.
  (call/cc (lambda (k)
    (if (empty? (rest l)) #f (stack_push (list k (rest l))))
    (first l)
  ))
)

(define (assert b)
  ; if the condition is true, just evaluate to true.
  ; if the condition is false:
  ; - if the stack is non-empty, go back
  ; - if the stack is empty, return false.
  (if b
    #t
    (if (stack_empty?)
      #f
      (let*
        (
          [pair (stack_pop)]
          [k (first pair)]
          [l (second pair)]
        )
        (if (empty? (rest l)) #f (stack_push (list k (rest l))))
        (k (first l))
      )
    )
  )
)
