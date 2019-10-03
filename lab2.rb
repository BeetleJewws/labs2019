class Array

  def thread_controller
    this = self
    array_size = size


    chunks_count = (array_size/10).floor + 1
    chunk_elements = (array_size/chunks_count).floor

    (0..chunks_count).map do |chunk_index|
      start = chunk_index*chunk_elements
      var1 = start + chunk_elements - 1
      var2 = array_size - 1
      stop = chunks_count == chunk_index ? var2 : var1

      Thread.new do
        chunk = this[start..stop]
        Thread.current["res"] = yield chunk
      end
    end.each{|t| t.join}.map{|t| t["res"]}
  end


  def new_all?(&alg)
    thread_controller do |chunk|
      chunk.all?(&alg)
    end.all?{|el| el}
  end

  def new_any?(&alg)
    thread_controller do |chunk|
      chunk.any?(&alg)
    end.any?{|el| el}
  end

  def new_select(&alg)
    thread_controller do |chunk|
      chunk.select(&alg)
    end.flatten(1)
  end

  def new_map(&alg)
    thread_controller do |chunk|
      chunk.map(&alg)
    end.flatten(1)
  end

end
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18]
puts arr.new_map{|x|x+x}.inspect


test = (0..100).map{|x|x}
start = Time.now
test.new_map{|el| sleep(1); el + 1}
puts Time.now - start #9s


test2 = (0..10).map{|x|x}
start2 = Time.now
test2.map{|el| sleep(1); el + 1}
puts Time.now - start2 #11s


# puts arr.new_select{|el| el > 6}.inspect
# puts arr.new_any?{|el| el > 1}
# puts arr.new_all?{|el| el > 1}