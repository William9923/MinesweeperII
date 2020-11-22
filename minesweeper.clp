(deftemplate not_bomb (slot row) (slot col))
(deftemplate bomb (slot row) (slot col))
(deftemplate value_cell (slot row) (slot col) (slot val))
(deftemplate total_bomb (slot n))

(deffunction bomb_neighbor (?r ?c)
  (return
    (length$
      (find-all-facts
        ((?f bomb))
        ;todo cari skeelilingnya ?f:r-1 >= ?r >= ?f:r+1 ...
        ;skrg return semua bomb di board
        (> ?f:row -1)
      )
    )
  )
)

(deffunction all_bomb ()
  (return
    (length$
      (find-all-facts
        ((?f bomb))
        (> ?f:row -1)
      )
    )
  )
)

(assert (not_bomb (row 0) (col 0)))
(assert (to_check 0 0))
(assert (total_bomb (n 0)))
(assert (value_cell (row 0) (col 0) (val 0)))
(assert (value_cell (row 0) (col 1) (val 0)))
(facts)

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



(run)
(facts)
(exit)
; empty line at the end