from MDP import MDP
from visualization import visualize_values
import matplotlib.pyplot as plt
from IPython import display
import time
import generator

class VI:

    def __init__(self, mdp, discount = 0.9):
        self.refresh(mdp, discount)

    '''
    clear values and policy
    '''
    def refresh(self, mdp, discount):
        self.mdp = mdp
        self.states = mdp.getStates()
        self.actions = mdp.getActions()
        self.transition = mdp.transition
        self.reward = mdp.reward
        self.terminal = mdp.terminal
        self.values = {state: 0 for state in self.states}
        self.policy = {state: None for state in self.states}
        self.discount = discount

    '''
    runs value iteration on self.MDP
    if visualize, will refresh figure after every iteration
    '''
    def iterate(self, iterations=50, visualize=True):
        self.refresh(self.mdp, self.discount)
        for k in range(0, iterations):
            for state in self.states:
                max_val = -float('inf')
                term = self.terminal(state)
                if term:
                    max_val = self.reward(state)
                else:
                    for action in self.actions:
                        new_state = self.transition(state, action)
                        new_val = self.reward(state) + self.discount * self.values[new_state]
                        if new_val > max_val:
                            max_val = new_val
                            self.policy[state] = action
                self.values[state] = max_val
            
            if visualize:
                fig = visualize_values(self.mdp, self.values, self.policy, title='Iteration ' + str(k))
                display.clear_output(wait=True)
                display.display(fig)
                time.sleep(0.1)
        if visualize:
            display.clear_output(wait=True)

        return self.values, self.policy

'''
creates environment with specified reward value, 
lava penalty, and gamma, then runs value iteration
'''
def vi_wrapper(reward, lava, gamma):
    rewards, terminal = generator.make_small_env(reward_value=reward, lava_value=lava)
    mdp = MDP(rewards, terminal)
    vi = VI(mdp, gamma)
    values, policy = vi.iterate(iterations=20, visualize=False)
    fig = visualize_values( mdp, values, policy, \
                            title='Reward: ' + str(reward) + '   Lava: ' + str(lava) + '    Gamma: ' + str(gamma), \
                            vmin=-6, vmax=8 )
    display.display(fig)
    display.clear_output(wait=True)





