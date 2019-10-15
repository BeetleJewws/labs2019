(ns labi.core)



(require '[clojure.pprint :as pp])

(defn fl [coll]
  ;(into [] (mapcat  #(if (sequential? %) % [%]) coll)))
  (apply concat coll))

(defn check
  [el]
  (filterv (fn [x]  (not= (first (take-last 2 x)) (last (take-last 2 x))))el))

(defn work
  [n , result, basis]
  (if (= (- n 1) 0 )
    result
    (work (- n 1) (check(fl (map (fn [el] (map (fn [el2] (conj el el2)) basis )) result))) basis)))

(defn myF
  [n, result]
  (work (- n 1)  (check(fl (map (fn [el] (map (fn [el2]  (conj [el] el2)) result )) result))) result))


(println "Result:")
(pp/pprint (myF 3 [ 1 ":(" [1 5] [] {}]))
