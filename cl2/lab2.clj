(ns labi.lab2
  (:import (java.util.logging XMLFormatter)))


(defn check-step
  [start, finish, step]
  (if (< (- finish step) start) (- finish start) step))

(defn calc
  [x0, x1, fun]
  (* (* (+ (fun x1) (fun x0))0.5) (- x1 x0)))

(def core
  (memoize
    (fn [fun, step, start, finish]
      (println start, finish)
      (if (= start finish)
        0
        (+ (calc (- finish step) finish fun)
        (core fun step start (- finish (check-step start finish step))))
        ))))




(println (core (fn [el] (* el el)) 1. 0. 10.))
(println (core (fn [el] (* el el)) 1. 0. 10.))




