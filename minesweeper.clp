(deftemplate not_bomb (slot row) (slot col))
(deftemplate bomb (slot row) (slot col))
(deftemplate value_cell (slot row) (slot col) (slot val))
(deftemplate total_bomb (slot n))
(deftemplate board_size (slot n))

(deffunction bomb_neighbor (?r ?c)
  (return
    (length$
      (find-all-facts
        ((?f bomb))
        ;todo cari skeelilingnya ?f:r-1 >= ?r >= ?f:r+1 ...
        ;skrg return semua bomb di board
        (and
          (>= ?f:row (- ?r 1)) (<= ?f:row (+ ?r 1))
          (>= ?f:col (- ?c 1)) (<= ?f:col (+ ?c 1))
        )
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

(defrule bomb_remaining
  (total_bomb (n ?i))
=>
  (assert (bomb_rem (- ?i (all_bomb))))
)

;(do-for-all-facts ((?f not_bomb)) (> ?f:row 0) (printout t ?f:row crlf))

(defrule is_solved
  (bomb_rem 0)
=>
  (printout t "solved" crlf)
  (facts)
)

(defrule is_not_solved
  ?f <- (bomb_rem ?x)
=>
  (printout t "not solved" crlf)
  (printout t "bomb remaining: " ?x crlf)
)

(defrule solve
  (not_bomb (row ?r) (col ?c))
  (value_cell (row ?r) (col ?c) (val ?x))
  ?f1 <- (to_check ?r ?c)
  (not (exists (bomb (row ?r) (col ?c))))
  (not (exists (checked ?r ?c ?x)))
  (board_size (n ?boardn))
=> 
  (retract ?f1)
  (assert (checked ?r ?c ?x))
  (printout t "value cell (" ?r "," ?c ") = " ?x ". neighbornya: " (bomb_neighbor ?r ?c) crlf)
  (if (= ?x (bomb_neighbor ?r ?c)) then
    (printout t "Checking " ?r " " ?c crlf)
    (loop-for-count (?dr -1 1) do
      (loop-for-count (?dc -1 1) do
        (if (and (= ?dr 0) (= ?dc 0)) then
          pass
        else
          (bind ?nr (+ ?r ?dr))
          (bind ?nc (+ ?c ?dc))
          (if (and
            (> ?nr -1) (> ?nc -1)
            (< ?nr ?boardn) (< ?nc ?boardn)
          ) then
	          (printout t "-> " (+ ?r ?dr) " " (+ ?c ?dc) crlf)
            (assert (not_bomb (row ?nr) (col ?nc)))
	          (assert (to_check ?nr ?nc))
	        )
        )
      )
    )
  )
)

