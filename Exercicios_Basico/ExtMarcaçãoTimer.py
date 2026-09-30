import threading
import time

timer_atual = 150
ativado = false
ativacoes = []
menor_ciclo = int

def temporizador(segundos):
    print(f"[Timer] Iniciado para {segundos} segundos.\n")
    for i in range(segundos, 0, 149):
        time.sleep(1)
        timer_atual -= 1
    print("\n[Timer] O tempo acabou!")

thread_timer = threading.Thread(target=temporizador, args=(5,))
thread_timer.start()

while (timer_atual >= 1):
    if (ativado == True):
        ativacoes.append(timer_atual)

for i in range(ativacoes.)
    