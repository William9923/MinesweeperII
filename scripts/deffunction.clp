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