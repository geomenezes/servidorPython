import requests
import re

# obter IP pela API do dyndns
req = requests.get('http://checkip.dyndns.org')

# extrair somente o IP da resposta HTTP
ip_addr = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', req.text)[0]

html = """<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Projeto Python</title>
  <link href="style.css" rel="stylesheet" type="text/css" />
</head>

<body>

  <div class="nav">
    <center>
      <img src="python.png">
    </center>
  </div>
  
  <div class="init">
    <h1>Seu endereço IP é: {{IP}}</h1>
  </div>

  <div class="end">
  </div>

</body>

</html>
"""
html = html.replace('{{IP}}', ip_addr)
print(html)