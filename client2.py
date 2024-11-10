import socket
import numpy as np
from datetime import datetime, timedelta
import time

def gerar_temperaturas( hora, clima_aleatorio):
    temperatura_media_dia = 25 
    temperatura_media_noite = 15 
    temperatura_media_manha = 20 
    variação_dia = 2 
    variação_noite = 2

    inicio = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    horario_atual = inicio + timedelta( hours=hora)
    
    if hora >= 10 and hora <= 16:  # Período do dia (6h às 18h)
        temperatura = temperatura_media_dia + np.random.normal(0, variação_dia)

    elif (hora > 7 and hora <10) or (hora > 16 and hora <20):  
        temperatura = temperatura_media_manha + np.random.normal(0, variação_dia)

    else:
        temperatura = temperatura_media_noite + np.random.normal(0, variação_noite)
        
    temp_final = temperatura + clima_aleatorio
    mens = f'{str(horario_atual)},{str(round(temp_final,1))}'
    return mens

def client():
  """Envia uma mensagem para o servidor.

  Args:
    message: A mensagem a ser enviada.
  """

  host = '127.0.1.1'  # Endereço IP do servidor
  port = 65444     # Porta do servidor
  n = 0
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  
    s.connect((host, port))
    while True:
      clima_aleatorio = np.random.normal(0,3)
      for h in range(0,24):

        message = gerar_temperaturas(h, clima_aleatorio)

        if message is None:
          print("Erro: mensagem é None.")
          break
        
        s.sendall(message.encode('utf-8'))
        data = s.recv(1024)

        print('Enviado:', data.decode('utf-8'))
        time.sleep(2)
      break

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(hostname)
print(ip_address)


client()
