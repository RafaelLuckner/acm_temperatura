import socket
import threading
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Função para receber dados de um cliente específico e armazenar em uma lista
def handle_client(conn, addr, tipo_dado):
    print(f"Conectado com {addr} para {tipo_dado}")
    while True:
        data = conn.recv(1024)
        if not data:
            print(f"Conexão encerrada com {addr} para {tipo_dado}")
            break
        print(f"Recebido de {tipo_dado}: {data.decode('utf-8')}")
        
        # Decodifica a mensagem
        result = data.decode('utf-8')
        partes = result.split(',')
        horario = partes[0]
        valor = float(partes[1])
        
        # Adiciona o dado ao DataFrame e salva no CSV
        df_novo = pd.DataFrame([[horario, valor, tipo_dado]], columns=['Horario', 'Valor', 'Tipo'])
        df_novo['Horario'] = pd.to_datetime(df_novo['Horario'])
        df_novo['Valor'] = pd.to_numeric(df_novo['Valor'])
        
        # Salva o novo dado no CSV, acrescentando sem sobrescrever
        df_novo.to_csv('df_temperatura_energia.csv', mode='a', header=False, index=False)
        
        conn.sendall(data)  # Responde ao cliente para confirmação

    conn.close()

def server():
    host = '127.0.1.1'
    port = 65444

    # Criar o arquivo CSV com cabeçalhos antes de iniciar o servidor
    df_inicial = pd.DataFrame(columns=['Horario', 'Valor', 'Tipo'])
    df_inicial.to_csv('df_temperatura_energia.csv', index=False)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor rodando em {host}:{port}")
        
        # Aceita conexões dos dois clientes
        for tipo_dado in ['Energia', 'Temperatura']:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, tipo_dado))
            client_thread.start()

        # Aguarda o término das threads
        client_thread.join()

def gerar_grafico(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Horario'], df['Energia'], label='Energia', color='blue')
    plt.plot(df['Horario'], df['Temperatura'], label='Temperatura', color='green')
    plt.xlabel('Horário')
    plt.ylabel('Valores')
    plt.title('Temperatura e Consumo de Energia por Hora')
    plt.legend()
    plt.xticks(rotation=45)
    plt.savefig('grafico_temperatura_energia.png', format='png')
    plt.close()


server()
# gerar_grafico(df_fin)
