(ns labi.lab3)


(defn myFn
  [x]
  (* x x))

(defn finish
  [x]
  (int (Math/floor (/ x 0.5))))

(defn calc
  [x0, x1, fun]
  (print ".")
  (* (* (+ (fun x1) (fun x0)) 1/2) (- x1 x0)))

(defn core
  ([x0, x1, fun] (lazy-seq (cons (calc x0 x1 fun) (core x1 (+ x1(- x1 x0)) fun)))))



(def seq (core 0 0.5 myFn))

(println (reduce + (take (finish 2.5) seq)))
(println (reduce + (take (finish 3.0) seq)))




