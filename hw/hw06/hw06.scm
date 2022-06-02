(define (cddr s) (cdr (cdr s)))

(define (cadr s) 
	(car (cdr s))
)

(define (caddr s) 
	(car (cddr s))
)

(define (ascending? lst) 
	(cond
		((null? lst) #t)
		((= (length lst) 1) #t)
		(else
			(and (>= (cadr lst) (car lst)) (ascending? (cdr lst)))
		)
	)
)

(define (interleave lst1 lst2) 
	(cond
		((null? lst1) lst2)
		((null? lst2) lst1)
		(else
			(append (list (car lst1)) (list (car lst2)) (interleave (cdr lst1) (cdr lst2))) 
		)
	)
)

(define (my-filter func lst) 
	(cond
		((null? lst) nil)
		(else
			(cond
				((func (car lst)) 
					(cons (car lst) (my-filter func (cdr lst)))
				)
				(else
					(my-filter func (cdr lst))
				)
			)
		)
	)
)

""" post-order更容易 元素car一个个加入进去，删除的是已有list里重复的 """
(define (no-repeats lst) 
	(cond
		((null? lst) nil)
		(else
			(cons (car lst) 
				(no-repeats 
					(my-filter 
						(lambda (x) (not (= x (car lst)))) 
						(cdr lst)
					)
				)
			)
		)
	)
)


