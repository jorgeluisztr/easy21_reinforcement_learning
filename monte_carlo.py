import numpy as np
from environment import easy21

def epsilon_greedy(Nsa, Qsa, playersum, dealerobs):
    e = 100 / (100 + np.sum(Nsa[playersum -1, dealerobs -1, :]))
    if np.random.uniform(0, 1) > e:
        action = np.argmax(Qsa[playersum-1, dealerobs-1])
    else:
        action = np.random.choice([0, 1])
    return action

def monte_carlo(limit_stop):
    Qsa = np.zeros([21, 10, 2])
    Nsa = np.zeros([21, 10, 2])
    for i in range(limit_stop):
        episode = easy21()
        playersum, dealerobs = episode.state()
        history = []
        while not episode.end_game:
            action = epsilon_greedy(Nsa, Qsa, playersum, dealerobs)
            Nsa[playersum - 1, dealerobs - 1, action] += 1
            state, reward = episode.turn(action)
            history.append(([playersum, dealerobs], action, reward))
            playersum, dealerobs = state
        Gt = 0
        for j, (State, Action, Reward) in enumerate(reversed(history)):
            playersum, dealerobs = State
            alpha = 1/Nsa[playersum - 1, dealerobs - 1, Action]
            Gt = Gt + Reward
            Qsa[playersum-1, dealerobs-1, Action] += alpha*(Gt - Qsa[playersum-1, dealerobs-1, Action])
    return Qsa
