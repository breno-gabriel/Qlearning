import connection as cn
import random
import numpy as np

#? Conectando com a porta.
s = cn.connect(2037)

#? A Q-Table, contendo os valoes da função Q usamos a biblioteca numpy para ler o 'resultado.txt' como uma matriz
q_table = np.loadtxt("resultado.txt")

#¢ 1. conversões --

def convert_action_number(action: int) -> str:

    if action == 0:

        return "left"

    elif action == 1:

        return "right"

    elif action == 2:

        return "jump"

def convert_number_action(action: str) -> int:

    if action == "left":

        return 0

    elif action == "right":

        return 1

    elif action == "jump":

        return 2

#¢ 1. --

#¢ 2. mecanismos de aprendizado --
#? Seleciona melhor ação para um determinado estado, a que o agente irá tomar

def better_action(state: int) -> int:

    return np.argmax(q_table[state])

#? A função Bellman é a função de valor de um estado, que é a soma da recompensa imediata e o valor máximo do próximo estado (iterativamente aprimorada) com um desconto gamma

def bellman_equation(r, s_prime, gamma):

    max_q_prime = np.max(q_table[s_prime])
    points = r + gamma * max_q_prime
    return points

# Atualizando a q_table

def update(oldState, action, newState, reward):

    action = convert_number_action(action)

    value = bellman_equation(reward, newState, gamma)
    q_table[oldState, action] += alpha * (value - q_table[oldState, action])

#¢ 2. --

#¢ 3. variáveis --

curr_state = 0

#! HIPERPARÂMETROS --
alpha = 0.01  #! Taxa de aprendizado, atualmente em 0.01 para evitar que sobrescrições bruscas sejam feitas na q_table durante a demonstração
gamma = 0.95  #! Peso das recompensas futuras, fator de desconto na equação
epsilon = 0.01  #! Isso faz parte do epsilon greedy strategy. Atualmente em 0.01 para evitar ações aleatórias
#! --

#¢ 3. --

# ANCHOR #!main --

while True:

    print(
        "=========================== Running the project =============================================================="
    )

    #! epsilon greedy strategy (o agente decidirá se irá explorar o ambiente ou buscar por uma estratégia já conhecida)
    random_number = random.random()
    if random_number < epsilon:

        #! Aqui o agente busca explorar o ambiente.

        action = convert_action_number(random.randint(0, 2))

    else:

        #! Aqui o agente busca pela estratégia que ele já conhece.

        action = convert_action_number(better_action(curr_state))

    print(action)

    state, reward = cn.get_state_reward(s, action)

    print(state)
    print(reward)

    #! Encontrando linha da q_table referente ao NewState
    newState = (int(state, 2))

    update(curr_state, action, newState, reward)
    curr_state = newState

    np.savetxt("resultado.txt", q_table, fmt="%f")
