from agent.agent_fa_q import FAQAgent
from agent.func_aprox import MLP
from env.slg_env import SLGEnv
from env.state_handler import ResourceOnly
from env.terminal_handler import LevelCondition
from env.time_handler import CountActionTime
from env.reward_handler import TotalTimeRelated
from env.utility import init_logger


def main():
    l = init_logger('QUKAgent')
    goal_time = 468000
    sh = ResourceOnly()
    th = LevelCondition(3)
    time_h = CountActionTime(60 * 60 * 24 * 6)
    rh = TotalTimeRelated(time_h, goal_time)
    env = SLGEnv(sh, th, rh, time_h)
    fa = MLP((len(sh) + 1, 20, 20, 1))
    agent = FAQAgent(env, 'QUKAgent', fa)
    agent.train(10000, 20, 1000)


if __name__ == '__main__':
    main()
