from agent.agent_fa_q import FAQAgent
from agent.func_aprox import MLP
from env.slg_env import SLGEnv
from env.state_handler import ResourceOnly
from env.terminal_handler import LevelCondition
from env.time_handler import CountActionTime
from env.reward_handler import StepTimeRelated
from env.utility import init_logger
import tensorflow as tf


def main():
    l = init_logger('MLPQAgent')
    sess = tf.Session()
    sh = ResourceOnly()
    th = LevelCondition(3)
    time_h = CountActionTime(60 * 60 * 24 * 5)
    rh = StepTimeRelated(time_h)
    env = SLGEnv(sh, th, rh, time_h)
    agent = FAQAgent(env, 'MLPQAgent', MLP, sess)
    agent.train(1000000, 20, 10, 10000)


if __name__ == '__main__':
    main()
