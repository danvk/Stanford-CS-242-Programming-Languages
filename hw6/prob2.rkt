#lang racket
(print-as-expression #f)
(provide (all-defined-out))

;========;
; Import ;
;========;
; import `throw` and `try_except`.
(require "prob1.rkt")

;===========;
; Problem 2 ;
;===========;
; Task: Implement `eval` using `throw` and `try_except`.
; Note: You can define any other helper functions.

(define (eval_help e)
  (if
    (number? e)
    e
    (let* (
      [op (first e)]
      [a (eval_help (second e))]
      [b (eval_help (third e))])
      (cond
        [(equal? op "+") (+ a b)]
        [(equal? op "-") (- a b)]
        [(equal? op "*") (* a b)]
        [(equal? op "/") (if (equal? b 0) (throw "DivZero") (/ a b))]
        [else (throw "OpError")]
      )
    )
  )
)

(define (eval e)
  (try_except
    (lambda () (eval_help e))
    (lambda (msg) msg)
  )
)
