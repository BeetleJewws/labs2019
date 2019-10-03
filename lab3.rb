# 2019-10-01T08:42:12.360203+00:00 app[web.1]: 10.33.38.71 - - [01/Oct/2019:08:42:12 +0000]
# "GET /static/css/fixer-style.css HTTP/1.1" 200 0 "https://rapid-text-annotation-tool.herokuapp.com/interface/workspace/1/edit/"
# "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
#
@regex = /^
(?<date_log>\d{4}-\d{2}-\d{2})
T
(?<time_log>\d{2}:\d{2}:\d{2}\.\d*\+\d{2}:\d{2})
\s
(?<dyno>\w*\[\w*\.\d\])
:\s
(?<client_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
\s-\s-\s\[
(?<date_local>\d{2}\/\w*\/\d{4})
:
(?<time_local>\d{2}:\d{2}:\d{2} \s \+\d{4})
\]\s\"
(?<method> \w*)
\s
(?<file_url>[\w\.\-\~\#\/\:]*)
\s
(?<protocol>[\w\/\.]*)
\"\s
(?<response>\d{3})
\s\d*\s\"
(?<url>[\w\.\-\~\#\:\/]*)
\"\s\"
(?<browser>[\w\/\.]*)
\s\(
(?<os>[\w\s\;\.]*)
\)
/x

filePath = 'C:\Users\BeetleJuice\RubymineProjects\titiled\logs.txt'

data = []
File.open(filePath, 'r') do |f|
  @records = f.readlines.map do |line|
    data << line.match(@regex)
  end
end

puts data.any? {|el| el[:response] == "404"}


