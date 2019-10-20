(ns labi.lab2-test
  (:require [clojure.test :refer :all])
  (:require [labi.lab2 :refer [core check-step myFn]]))

(deftest check-step-test
  (testing "Checking")
  (is (= (check-step 0 1 2) 1))
  )

(deftest core-test
  (testing "Core")
  (is (= 9.5 (core myFn 1. 0. 3.)))
  )
