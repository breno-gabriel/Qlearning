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
    
    return np.argmax(q_table[state])
 
# Atualizando a q_table    
def update(oldState, action, newState, reward):
    
    if (action == "left"): 

        action = 0
    
    elif (action == "right"): 

        action = 1
    
    elif (action == "jump"): 

        action = 2
    
    value = bellman_equation(reward, newState, gamma)
    q_table[oldState, action] += alfa * (value - q_table[oldState, action])
    
curr_state = 0

alfa = 0.01 # Taxa de aprendizado, atualmente em 0.01 para evitar que sobrescrições bruscas sejam feitas na q_table durante a demonstração 
gamma = 0.95 # Peso das recompensas futuras, fator de desconto na equação
episilon = 0.01 # Isso faz parte do epsilon greedy strategy. Atualmente em 0.01 para evitar ações aleatórias     

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
    
    # Encontrando linha da q_table referente ao NewState
    newState = (int(state[2:7],2) * 4) + (int(state[7:9], 2) % 4)
    
    update(curr_state, action, newState, reward)
    curr_state = newState

    np.savetxt('resultado.txt', q_table, fmt="%f")  