from agent.example_agent import ExampleAgent
from env.slg_env import SLGEnv
from env.state_handler import ExampleState
from env.terminal_handler import LevelCondition
from env.reward_handler import ExampleReward
from env.time_handler import TimeHandler
from env.utility import init_logger, generate_user_name


def main():
    l = init_logger('ExampleAgent')
    sh = ExampleState()
    th = LevelCondition(2)
    time_h = TimeHandler()
    rh = ExampleReward()
    env = SLGEnv(sh, th, rh, time_h)
    env.setup(generate_user_name())
    agent = ExampleAgent(env)
    agent.run()


if __name__ == '__main__':
    main()
