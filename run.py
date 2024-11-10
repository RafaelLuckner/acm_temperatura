import subprocess
import time

# Executa o servidor como subprocesso
server_process = subprocess.Popen(['python', 'server.py'])
time.sleep(2)

# Executa client1 e client2 como subprocessos
process1 = subprocess.Popen(['python', 'client1.py'])
time.sleep(0.5)
process2 = subprocess.Popen(['python', 'client2.py'])

# Executa o dashboard como subprocesso
dashboard_process = subprocess.Popen(['streamlit', 'run', 'dashboard.py'])

# Aguarda os processos finalizarem
process1.wait()
process2.wait()

# Aguardar o dashboard também se terminar (se necessário)
dashboard_process.wait()

server_process.wait()
