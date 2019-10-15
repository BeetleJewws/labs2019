class Array
  def thread_controller
    this = self
    array_size = size

    i=0
    q = Queue.new
    this.map {|x| q<<[x,i]; i=i+1}

    (0..2).map do |i|
      Thread.new do
        res = []
        while not q.empty?
          el = q.pop
          chunk = el[0]
          index = el[1]
          temp = yield chunk
          res << [temp,index]
          if temp == false
            q.clear
          end
        end
        Thread.current["res"] = res
      end
    end.each{|t| t.join}.map{|t| t["res"]}.flatten(1).sort_by{ |x| x[1] }.map {|el| el[0] }.flatten(1)
  end


  def new_all?(&alg)
    thread_controller do |chunk|
      [chunk].all?(&alg)
    end.all?{|el| el}
  end

  def new_any?(&alg)
    thread_controller do |chunk|
      [chunk].any?(&alg)
    end.any?{|el| el}
  end

  def new_select(&alg)
    thread_controller do |chunk|
      [chunk].select(&alg)
    end
  end

  def new_map(&alg)
    thread_controller do |chunk|
      [chunk].map(&alg)
    end
  end
end

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18]
puts arr.new_map{|x|x+x}.inspect
puts arr.new_select{|x|x>3}.inspect
puts arr.new_all?{|x|x<3}


