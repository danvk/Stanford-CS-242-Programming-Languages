#lang racket
(print-as-expression #f)
(provide (all-defined-out))

;========;
; Import ;
;=========
; import `attempt` and `assert`.
(require "prob3.rkt")

; import `get_num`, `filled_at?`, and `has_dup?`.
(require "src/sudoku.rkt")

;==============;
; Helper Funcs ;
;==============;
; return #t, if `state` has no blanks.
; return #f, otherwise.
(define (filled_all? state)
  (for*/and ([row (range 0 9)]
             [col (range 0 9)])
    (filled_at? state (list row col))))

; return the position of any blank in `state`.
; return #f, if `state` has no blanks.
(define (get_blank_pos state)
  (for*/first ([row (range 0 9)]
               [col (range 0 9)]
               #:when (not (filled_at? state (list row col))))
    (list row col)))

; return the new state after writing `num` at `pos` in `state`.
(define (add_num state pos num)
  (if (filled_at? state pos)
    (error (format "trying to overwrite '~a' at (~a,~a)!"
                   num (first pos) (second pos)))
    (append state (list (list (first pos) (second pos) num)))))

; return #t, if every number does not appear twice in every row.
; return #f, otherwise.
(define (valid_row? state)
  (define (get_vals_in_row row)
    (for*/list ([col (range 0 9)])
      (get_num state (list row col))))
  (for*/and ([row (range 0 9)])
    (let* ([vals_in_row (get_vals_in_row row)]
           [nums_in_row (filter number? vals_in_row)])
      (not (has_dup? nums_in_row)))))

; return #t, if every number does not appear twice in every column.
; return #f, otherwise.
(define (valid_col? state)
  (define (get_vals_in_col col)
    (for*/list ([row (range 0 9)])
      (get_num state (list row col))))
  (for*/and ([col (range 0 9)])
    (let* ([vals_in_col (get_vals_in_col col)]
           [nums_in_col (filter number? vals_in_col)])
      (not (has_dup? nums_in_col)))))

; return #t, if every number does not appear twice in every subgrid.
; return #f, otherwise.
(define (valid_subg? state)
  (define (get_vals_in_subg row_i col_i)
    (for*/list ([row_j (range 0 3)]
                [col_j (range 0 3)])
      (let* ([row (+ (* 3 row_i) row_j)]
             [col (+ (* 3 col_i) col_j)])
        (get_num state (list row col)))))
  (for*/and ([row_i (range 0 3)]
             [col_i (range 0 3)])
    (let* ([vals_in_subg (get_vals_in_subg row_i col_i)]
           [nums_in_subg (filter number? vals_in_subg)])
      (not (has_dup? nums_in_subg)))))

;===========;
; Problem 4 ;
;===========;
; Task: Implement `solve` using `attempt` and `assert`.
; Note: You can define any other helper functions.

(define (valid? state)
  (and
    (valid_row? state)
    (valid_col? state)
    (valid_subg? state)))

(define (solve state)
  (let*
    ([blank (get_blank_pos state)])
    (if blank
      ; fill in the blank and recursively solve
      (let*
        ([num (attempt (range 1 10))])
        (assert (valid? state))  ; huge optimization
        (solve (add_num state blank num))
      )
      ; check whether this solution is valid
      (and (assert (valid? state)) state)
    )
  )
)
