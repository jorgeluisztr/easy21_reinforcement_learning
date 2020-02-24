import numpy as np
from environment import easy21

def epsilon_greedy(Nsa, Qsa, playersum, dealerobs):
    e = 100 / (100 + np.sum(Nsa[playersum -1, dealerobs -1, :]))
    if np.random.uniform(0, 1) > e:
        action = np.argmax(Qsa[playersum-1, dealerobs-1])
    else:
        action = np.random.choice([0, 1])
    return action

def sarsa(limit, lbd, gamma, Qopt=None):
    Qsa = np.zeros([21, 10, 2])
    Nsa = np.zeros([21, 10, 2])
    mse=[]

    for i in range(limit):
        E = np.zeros([21,10,2])
        episode = easy21()
        playersum, dealerobs = episode.state()
        action = epsilon_greedy(Nsa, Qsa, playersum, dealerobs)

        while not episode.end_game:
            Nsa[playersum-1, dealerobs-1, action] += 1
            Qsa[playersum-1,dealerobs-1, action] += 1

            state, reward = episode.turn(action)
            playersum, dealerobs = state

            if episode.end_game:
                delta = reward - Qsa[playersum-1, dealerobs-1, action]
                p = 0

            else:
                p = epsilon_greedy(Nsa,Qsa, playersum, dealerobs)
                delta = reward + gamma * Qsa[playersum -1, dealerobs -1, p] - Qsa[playersum-1,dealerobs-1, action]

            alpha = 1/Nsa[playersum-1, dealerobs-1, action]
            Qsa += (alpha*delta*E)
            E += (gamma*lbd)

            action = p

        if (i%1000==0) and (Qopt != None):
            mse.append((np.sum((Qsa-Qopt)**2)))

    return (Qsa, mse)