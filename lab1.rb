def pomogite (n, array)

  def help( array,n, result)
    if n == 1
      result
    else
      temp=result.flat_map{|el|array.select{|t|t != el[-1]}.map{|el2|el+[el2]}}
      help(array,n-1,temp)
    end
  end
  help( array,n, array)
end


array = [1, "hehe", [1,2]]

puts pomogite(3,array).inspect


# aba
# abc
# abd
# aca
# acb
# acd
# ada
# adb
# adc