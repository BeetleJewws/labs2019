def pomogite (n, array)

  def help( array,n, result)
    if n == 1
      result
    else
      temp = result.flat_map{|el| array.map{|el2| [el].flatten(1) + [el2]}}
      help( array,n-1, temp.reject{|x|x[-1] == x[-2]})
    end
  end

  help( array,n, array)

end


array = [1, "hehe", [1,2]]

puts pomogite(3,array).inspect
