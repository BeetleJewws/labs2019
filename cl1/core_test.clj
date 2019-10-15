(ns labi.core-test
  (:require [clojure.test :refer :all])
  (:require [labi.core :refer [check myF]]))

(deftest check-test
  (testing "Filtering")
  (is (= (check [[1 1] [1 2] [1 3]]) [[1 2] [1 3]]))
  )

(deftest myF-test
  (testing "Main")
  (is (= (myF 2 [ 1 2 [3 4]] ) [[1 2] [1 [3 4]] [2 1] [2 [3 4]] [[3 4] 1] [[3 4] 2]]))
  (is (= (myF 2 [ "a" "BC" {}]) [["a" "BC"] ["a" {}] ["BC" "a"] ["BC" {}] [{} "a"] [{} "BC"]]))

  )
