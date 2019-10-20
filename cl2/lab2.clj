(ns labi.lab2)


(defn check-step
  [start, finish, step]
  (if (< (- finish step) start) (- finish start) step))

(defn core [fun, step, start, finish, result]
  (if (= start finish)
    (println result)
    (memoize (core
               fun
               step
               start
               (- finish (check-step start finish step))
               (+ (* (/ (+ (fun finish) (fun (- finish (check-step start finish step))))2) (- finish (- finish (check-step start finish step)))) result)
               ))))


(time (core (fn [el] (* el el)) 0.1 0. 100. 0))
(time (core (fn [el] (* el el)) 0.1 0. 101. 0))
(time (core (fn [el] (* el el)) 0.1 0. 102. 0))
(time (core (fn [el] (* el el)) 0.1 0. 103. 0))

