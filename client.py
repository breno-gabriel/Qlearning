import connection as cn 
import random 
import numpy as np

# Conectando com a porta. 
s = cn.connect(2037)

# usamos a biblioteca numpy para ler o 'resultado.txt' como uma matriz
q_table = np.loadtxt('resultado.txt')

# Funções uteis. 
def bellman_equation( r, s_prime, gamma):
    
    max_q_prime = np.max(q_table[s_prime])
    points = r + gamma * max_q_prime
    return points

def convert_action_number(action : int) -> str:

    if (action == 0): 

        return "left"
    
    elif (action == 1): 

        return "right"
    
    elif (action == 2): 

        return "jump"
    
def better_action(state : int) -> str:

    if q_table[state, 0] > q_table[state, 1] and q_table[state, 0] > q_table[state, 2]:
        return 0
    elif q_table[state, 1] > q_table[state, 0] and q_table[state, 1] > q_table[state, 2]:
        return 1
    else:
        return 2

curr_state = 0
curr_reward = -14

alfa = 0.1 # Taxa aprendizado (no nosso caso, o agente aprende de forma lenta, porém estável). 
gamma = 0.9 # Peso das recompensas futuras (no nosso caso, o agente planeja a longo prazo e considera recompensas futuras mais importantes)
episilon = 0 # Isso faz parte do epsilon greedy strategy. 

while (True): 

    print('=========================== Runnig the project ==============================================================')

    # epsilon greedy strategy (o agente decidirá se irá explorar o ambiente ou buscar por uma estratégia já conhecida)
    random_number = random.random()
    if random_number < episilon: 

        # Aqui o agente busca explorar o ambiente. 

        action = convert_action_number(random.randint(0, 2))

    else: 

        #Aqui o agente busca pela estratégia que ele já conhece. 

        action = convert_action_number(better_action(curr_state))

    print(action)

    state, reward = cn.get_state_reward(s, action)

    print(reward)

    np.savetxt('resultado.txt', q_table, fmt="%f")  