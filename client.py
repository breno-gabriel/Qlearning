import connection as cn 
import random 
import numpy as np

# Conectando com a porta. 
s = cn.connect(2037)

# usamos a biblioteca numpy para ler o 'resultado.txt' como uma matriz
q_table = np.loadtxt('resultado.txt')

def reset_table():
    
    with open("resultado.txt", "w") as file:
        text = ""
        for n in range(96):
            text = f"{text}0.000000 0.000000 0.000000\n"
            
        file.write(text)
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
    # if q_table[state, 0] > q_table[state, 1] and q_table[state, 0] > q_table[state, 2]:
    #     return 0
    # elif q_table[state, 1] > q_table[state, 0] and q_table[state, 1] > q_table[state, 2]:
    #     return 1
    # else:
    #     return 2
 
# Atualizando a q_table    
def update(oldState, action, newState, reward):
    
    if (action == "left"): 

        action = 0
    
    elif (action == "right"): 

        action = 1
    
    elif (action == "jump"): 

        action = 2
    
    bellman = bellman_equation(reward, newState, gamma)
    q_table[oldState, action] += alfa * (bellman - q_table[oldState, action])
curr_state = 0
curr_reward = -14

alfa = 0.25 # Taxa aprendizado (no nosso caso, o agente aprende de forma lenta, porém estável). 
gamma = 0.8 # Peso das recompensas futuras (no nosso caso, o agente planeja a longo prazo e considera recompensas futuras mais importantes)
episilon = 1 # Isso faz parte do epsilon greedy strategy.     

reset_table()

while (True): 

    print('=========================== Runnig the project ==============================================================')

    # epsilon greedy strategy (o agente decidirá se irá explorar o ambiente ou buscar por uma estratégia já conhecida)
    random_float = random.uniform(0,1) 
    if random_float < episilon: 

        # Aqui o agente busca explorar o ambiente. 

        action = convert_action_number(random.randint(0, 2))
        print("Escolha aleatoria")

    else: 

        #Aqui o agente busca pela estratégia que ele já conhece. 

        action = convert_action_number(better_action(curr_state))
        print("Escolha consciente")

    # Diminuir a exploração aos poucos. 
    episilon = max(episilon * 0.998, 0.4)
    print(action)

    state, reward = cn.get_state_reward(s, action)

    if reward < -100:

        alfa = 0.05
    
    else: 

        alfa = 0.25 

    # if action == "jump" and reward == -100:
    #     reward = -20
    # elif action == "jump":
    #     reward = -5
    print(reward)
    
    # Encontrando linha da q_table referente ao NewState
    newState = (int(state[2:7],2) * 4) + (int(state[7:9], 2) % 4)
    
    update(curr_state, action, newState, reward)
    curr_state = newState

    np.savetxt('resultado.txt', q_table, fmt="%f")  