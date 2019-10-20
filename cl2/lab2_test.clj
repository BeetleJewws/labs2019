(ns labi.lab2-test
  (:require [clojure.test :refer :all])
  (:require [labi.lab2 :refer [core check-step]]))

(deftest check-step-test
  (testing "Checking")
  (is (= (check-step 0 1 2) 1))
  )

(deftest core-test
  (testing "Core")
  (is (> (int(time (core (fn [el] (* el el)) 0.1 0. 100. 0))) (int(time (core (fn [el] (* el el)) 0.1 0. 100. 0)))))
  )
