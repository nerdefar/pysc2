from keras.models import Sequential
from keras.layers import Dense, Activation
from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random




# Build network
def build_network():
    model = Sequential()
    model.add(Dense(32, input_dim=784))
    model.add(Activation('relu'))
    return model
#Compile it
def compile_model(model):
    model.compile(optimizer=RMSprop(epsilon=0.1, rho=0.99), loss='categorical_crossentropy', metrics=['accuracy'])
    return model
# Train it.
def train_model(model, data, labels, epoch, batch_size):
    model.fit(data, labels, epochs, batch_size)


class LearningAgent(base_agent.BaseAgent):
    def __init__(self):
        super(LearningAgent, self).__init__()

    def step(self, obs):
        super(LearningAgent, self).step(obs)
        return actions.FUNCTIONS.no_op()





# Run agent
def main(unused_argv):
    agent = LearningAgent()
    try:
        while True:
            # Set up SC2 env with map, player 1 as agent, player 2 as bot.
            # Feature dimensions sets pixel size for screen and minimap for bot to use
            # step_mul defines game steps before action to be taken, 16 ~= 150 APM
            # Game steps per episode used to set "max time" for a game, 0 = run forever or till finished.
            # Visualize makes for easier debug and observation of bot
            with sc2_env.SC2Env(
                map_name="Simple64",
                players=[sc2_env.Agent(sc2_env.Race.zerg),
                         sc2_env.Bot(sc2_env.Race.random,
                                     sc2_env.Difficulty.very_easy)],
                agent_interface_format=features.AgentInterfaceFormat(
                    feature_dimensions=features.Dimensions(screen=84, minimap=64),
                    use_feature_units=True),
                step_mul=16,
                game_steps_per_episode=0,
                visualize=True) as env:
        
                agent.setup(env.observation_spec(), env.action_spec())
                
                timesteps = env.reset()
                agent.reset()
                
                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)
      
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    app.run(main)