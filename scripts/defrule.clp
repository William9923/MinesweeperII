(defrule bomb_remaining
  (total_bomb (n ?i))
=>
  (assert (bomb_rem (- ?i (all_bomb))))
  (facts)
)

;(do-for-all-facts ((?f not_bomb)) (> ?f:row 0) (printout t ?f:row crlf))

(defrule is_solved
  (bomb_rem 0)
=>
  (printout t "solved" crlf)
  (facts)
  (exit)
)

(defrule solve
  (not_bomb (row ?r) (col ?c))
  (value_cell (row ?r) (col ?c) (val ?x))
  ?f1 <- (to_check ?r ?c)
  (not (exists (bomb (row ?r) (col ?c))))
  (not (exists (checked ?r ?c)))
=> 
  (retract ?f1)
  (assert (checked ?r ?c))
  (if (= ?x (bomb_neighbor ?r ?c)) then
    (printout t "Checking " ?r " " ?c crlf)
    (loop-for-count (?dr -1 1) do
      (loop-for-count (?dc -1 1) do
        (printout t "-> " (+ ?r ?dr) " " (+ ?c ?dc) crlf)
        (if (and (= ?dr 0) (= ?dc 0)) then
          pass
        else
          (bind ?nr (+ ?r ?dr))
          (bind ?nc (+ ?c ?dc))
          ; todo < ukuran board
          (if (and (> ?nr -1) (> ?nc -1)) then
	        (assert (not_bomb (row ?nr) (col ?nc)))
	        (assert (to_check ?nr ?nc))
	      )
        )
      )
    )
  )
)