# Code following from tutorial at:
# https://itnext.io/build-a-zerg-bot-with-pysc2-2-0-295375d2f58e

##Some idiotic setup just to check that devenv is set up correctly.

try:
    from pysc2.agents import base_agent
    from pysc2.env import sc2_env
    from pysc2.lib import actions, features, units
    from absl import app
    import random
    print("Includes OK.")
except:
    print("includes failed.")

# Define agent to play the game
class ZergAgent(base_agent.BaseAgent):

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units if unit.unit_type == unit_type]

    def unit_type_is_selected(self, obs, unit_type):
        # Check single select if the unit selected is correct type
        if(len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
            return True
        # Check multi select if the unit selected is the correct type
        if(len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
            return True
        # If not, then the unit type is not selected
        return False
        
    # Logic for action taken at each step
    def step(self, obs):
        super(ZergAgent, self).step(obs)

        # Fetch all spawning pools
        spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
        # If there is no spawning pool ->
        if len(spawning_pools) == 0:
            print("crash?1")
            # Check if we have a drone selected and if building a spawning pool is available (enough minerals)
            # Build spawning pool and random x and y coordinates within the seen screen. Hopefully a valid position
            if self.unit_type_is_selected(obs, units.Zerg.Drone):
                print("crash?2")
                if (actions.FUNCTIONS.Build_SpawningPool_screen.id in obs.observation.available_actions):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    return actions.FUNCTIONS.Build_SpawningPool_screen("now", (x, y))

            # Find all drones on screen and append to list
            drones = self.get_units_by_type(obs, units.Zerg.Drone)
            # If one or more drones can be found, select one on random
            if len(drones) > 0:
                drone = random.choice(drones)
                # Return the action to ctrl+click select on one of the drones to select all.
                return actions.FUNCTIONS.select_point("select_all_type", (drone.x, drone.y))
        return actions.FUNCTIONS.no_op()

def main(unused_argv):
  agent = ZergAgent()
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