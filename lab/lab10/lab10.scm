(define (over-or-under num1 num2)
    (cond 
          ((< num1 num2) -1)
          ((= num1 num2) 0)
          (else 1)
    )
) 
   
(define (make-adder num) 
    (define (add-num inc)
        (+ num inc)
    )
    add-num
)



(define (composed f g) 
    (define (f-then-g x)
        (f (g x))
    )
    f-then-g
)

(define (square n) (* n n))

(define (pow base exp) 
    """ o(logn)的递归函数 """
    """ base case exp = 1 or 0"""
    (cond
        ((= exp 0) 1)
        ((= exp 1) base)
        (else 
            (cond 
                ((even? exp) 
                    (square (pow base (/ exp 2)))
                )
                (else 
                    (* base 
                        (square (pow base (/ (- exp 1) 2)))
                    )
                )
            )
        )
    )
)
