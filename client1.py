import socket
import numpy as np
from datetime import datetime, timedelta
import time

def gerar_energia_com_horario(hora, energia_aleatoria):
    energia_media_dia = 3.96
    energia_media_tarde = 5.28
    energia_media_noite = 0.8
    variacao_dia = 1
    variacao_noite = 0.2

    inicio = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    horario_atual = inicio + timedelta( hours=hora)

    # Gerar temperatura e horário
    if hora >7 and hora <= 17: # Período do meio do dia
        energia_atual = energia_media_dia + np.random.normal(0, variacao_dia)

    elif (hora >= 17 and hora < 22):  # Período da manhâ
        energia_atual = energia_media_tarde + np.random.normal(0, variacao_dia)

    else:  # Período da noite
        energia_atual = energia_media_noite + np.random.normal(0, variacao_noite)

       

    energia_final = np.abs(energia_atual + energia_aleatoria)
    mens = f'{str(horario_atual)},{str(round(energia_final,1))}'
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
      for h in range(0,24):
        clima_aleatorio = np.random.normal(0,1)

        message = gerar_energia_com_horario(h, clima_aleatorio)

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
