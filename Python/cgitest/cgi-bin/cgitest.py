# -*- coding: utf-8 -*-

import cgi
import cgitb; cgitb.enable()
import sys                
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#print('Content-type: text/html\n'.encode('utf-8'))
html_body = """
<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf8">
  <style>
   h1 {
    font-size: 3em;
   }
  </style>
 </head>

 <body>
  <h1>%s</h1>
 </body>

</html>
"""


form = cgi.FieldStorage()
#text = form.getvalue('text','')
text = (form['text'].value)
           
print(html_body % (text))

#.encode('utf-8')