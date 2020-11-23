(deftemplate not_bomb (slot row) (slot col))
(deftemplate bomb (slot row) (slot col))
(deftemplate value_cell (slot row) (slot col) (slot val))
(deftemplate total_bomb (slot n))
(deftemplate board_size (slot n))
(deftemplate cnt (slot r) (slot c) (slot n))

(deffunction bomb_neighbor (?r ?c)
  ; hitung jumlah bomb yang posisinya di sekitar ?r ?c
  ; r-1 <= f:row <= r+1
  ; c-1 <= f:col <= c+1
  
  (return
    (length$
      (find-all-facts
        ((?f bomb))
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
  (declare (salience -10))
  (total_bomb (n ?i))
=>
  (assert (bomb_rem (- ?i (all_bomb))))
)

;(do-for-all-facts ((?f not_bomb)) (> ?f:row 0) (printout t ?f:row crlf))

(defrule is_solved
  (declare (salience -9))
  (bomb_rem 0)
=>
  (printout t "solved" crlf)
  (facts)
)

(defrule is_not_solved
  (declare (salience -9))
  ?f <- (bomb_rem ?x)
=>
  (printout t "not solved" crlf)
  (printout t "bomb remaining: " ?x crlf)
)

(defrule floodfill
  (declare (salience 100))
  ; trigger
  ?f1 <- (to_open ?r ?c ?x)
  
  ; syarat
  (not (exists (bomb (row ?r) (col ?c))))
  (not (exists (opened ?r ?c)))
  
  ; assign var
  (value_cell (row ?r) (col ?c) (val 0))
  (board_size (n ?boardn))
=> 
  (retract ?f1)
  (assert (opened ?r ?c))
  (printout t "Checking " ?r " " ?c crlf)

  (loop-for-count (?dr -1 1) do
    (loop-for-count (?dc -1 1) do
      (if (not (and (= ?dr 0) (= ?dc 0))) then
        (bind ?nr (+ ?r ?dr))
        (bind ?nc (+ ?c ?dc))
        (if (and
          (>= ?nr 0) (>= ?nc 0)
          (< ?nr ?boardn) (< ?nc ?boardn)
        ) then
          (printout t "-> " (+ ?r ?dr) " " (+ ?c ?dc) crlf)
          (assert (to_check ?nr ?nc))
        )
      )
    )
  )
)

(defrule to_check_is_not_bomb
  (declare (salience -8))
  ?f1 <- (to_check ?r ?c)
  (not (exists (bomb (row ?r) (col ?c))))
  (value_cell (row ?r) (col ?c) (val ?x))
=>
  (retract ?f1)
  (assert (to_open ?r ?c ?x))
  (assert (not_bomb (row ?r) (col ?c)))

  (printout t "value cell (" ?r "," ?c ") = " ?x ". neighbornya: " (bomb_neighbor ?r ?c) crlf)
)

(defrule to_check_is_bomb
  (declare (salience -8))
  ?f1 <- (to_check ?r ?c)
  (exists (bomb (row ?r) (col ?c)))
  (value_cell (row ?r) (col ?c) (val ?x))
=>
  (retract ?f1)
)

(defrule to_flag_bomb
  (declare (salience 98))
  (to_open ?r ?c ?x)
  (board_size (n ?boardn))
=>
  ; for 8 neighbornya: if jumlah yang to_check + opened + bomb + val = 8 maka assert(to_flag(r c))

  (printout t "sus flag " ?r " " ?c crlf)
  ;(facts)
  (assert (cnt (r ?r) (c ?c) (n ?x)))
  (loop-for-count (?dr -1 1) do
    (loop-for-count (?dc -1 1) do
      (if (not (and (= ?dr 0) (= ?dc 0))) then
        (bind ?nr (+ ?r ?dr))
        (bind ?nc (+ ?c ?dc))
        (if (and
          (>= ?nr 0) (>= ?nc 0)
          (< ?nr ?boardn) (< ?nc ?boardn)
        ) then
          (assert (to_increment ?r ?c ?nr ?nc))
        )
      )
    )
  )
)


(defrule to_increment_rule
  ?f2 <- (to_increment ?rr ?cc ?r ?c)
=>
  (retract ?f2)
)

(defrule to_increment_rule
  (declare (salience 5))
  ?f <- (cnt (r ?rr) (c ?cc) (n ?n))
  ?f2 <- (to_increment ?rr ?cc ?r ?c)
  (or
    (exists (to_open ?r ?c ?x2))
    (exists (opened ?r ?c))
    (exists (bomb (row ?r) (col ?c)))
  )
=>
  (retract ?f2)
  (modify ?f (n (+ ?n 1)))
  ;(printout t "asal: " ?rr " " ?cc ". tujuan: " ?r " " ?c " " (+ ?n 1) crlf)
)

(defrule find_bomb_nearby
  (declare (salience 97))
  ?f <- (cnt (r ?r) (c ?c) (n 8))
  
  ; assign var
  (board_size (n ?boardn))
=>
  (printout t "bomb nearby " ?r ?c crlf)
  (loop-for-count (?dr -1 1) do
    (loop-for-count (?dc -1 1) do
      (if (not (and (= ?dr 0) (= ?dc 0))) then
        (bind ?nr (+ ?r ?dr))
        (bind ?nc (+ ?c ?dc))
        (if (and
          (>= ?nr 0) (>= ?nc 0)
          (< ?nr ?boardn) (< ?nc ?boardn)
        ) then
          ;(printout t ?nr ?nc crlf)
          (assert (test_to_flag ?nr ?nc))
        )
      )
    )
  )
)

(defrule to_flag_rule
  (declare (salience -1))
  ?f <- (test_to_flag ?r ?c)
  (not (or
    (exists (to_open ?r ?c ?x2))
    (exists (opened ?r ?c))
    (exists (bomb (row ?r) (col ?c)))
  ))
=>
  (retract ?f)
  (printout t "bomb " ?r ?c crlf)
  (assert(to_flag ?r ?c))
)

(defrule flag_is_bomb
  (declare (salience 95))
  ; trigger
  ?f1 <- (to_flag ?r ?c)
  
  ; syarat
  (not(exists (to_check ?r ?c)))
  (not(exists (opened ?r ?c)))
  (not(exists (bomb (row ?r) (col ?c))))

  ; assign var
  (board_size (n ?boardn))
=>
  (retract ?f1)
  (assert(bomb (row ?r) (col ?c)))
  
  (loop-for-count (?dr -1 1) do
    (loop-for-count (?dc -1 1) do
      (if (not (and (= ?dr 0) (= ?dc 0))) then
        (bind ?nr (+ ?r ?dr))
        (bind ?nc (+ ?c ?dc))
        (if (and
          (>= ?nr 0) (>= ?nc 0)
          (< ?nr ?boardn) (< ?nc ?boardn)
        ) then
          (assert (subtract_neighbor ?nr ?nc))
        )
      )
    )
  )
)

(defrule subtract_neighbor_rule
  ?f <- (subtract_neighbor ?r ?c)
  ?f2 <- (value_cell (row ?r) (col ?c) (val ?x))
=>
  (retract ?f)
  (modify ?f2 (val (- ?x 1)))
)

(defrule flag_is_not_bomb
  ?f1 <- (to_flag ?r ?c)
  (or
    (exists (to_check ?r ?c))
    (exists (opened ?r ?c))
    (exists (bomb (row ?r) (col ?c)))
  )
=>
  (retract(?f1))
)