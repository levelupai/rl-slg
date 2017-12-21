import random
import logging
import time
import datetime
from env.slg_env import SLGEnv
from exp_replay import *
from func_aprox import FuncApprox
import numpy as np
import tensorflow as tf
from env.utility import generate_user_name, get_path


class FAQAgent(object):
    def __init__(self, env, logger_name, fa, sess):
        """
        Initialization
        :param env: training environment
        :type env: SLGEnv
        :param logger_name: logger name
        :type logger_name: str
        :param fa: function approximator
        :type fa: class
        :param sess: tensorflow session
        """
        self.env = env
        self.logger = logging.getLogger(logger_name)
        self._sess = sess
        self._fa = fa
        self._setup()

    def _setup(self):
        self._def_params()
        self._def_network()
        self._def_tf_sl()

    def _def_params(self):
        self.gamma = 0.99
        self.target_value = 0
        self._replay_size = 50000
        self._batch_size = 32
        self._max_action_id = 100.0
        self.replay = ExpReplay(self._replay_size)

    def _def_network(self):
        self.target = self._fa(self._sess, "target", (self.env.get_state_len() + 1, 50, 50, 1))
        self.online = self._fa(self._sess, "online", (self.env.get_state_len() + 1, 50, 50, 1))
        self.online.copy_to(self.target)

    def _def_tf_sl(self):
        init = tf.global_variables_initializer()
        self._save_path = get_path('saved_networks/SLG-mlp')
        self._saver = tf.train.Saver()
        self._sess.graph.finalize()
        checkpoint = tf.train.get_checkpoint_state(self._save_path)
        if checkpoint and checkpoint.model_checkpoint_path:
            self._saver.restore(self._sess, checkpoint.model_checkpoint_path)
            self.logger.info("Successfully loaded: %s" % checkpoint.model_checkpoint_path)
        else:
            self._sess.run(init)

    def train(self, episodes, update_times, update_iter, save_iter):
        """
        Train agent multiple episode. One episode will terminate when terminal condition reaches.
        :param episodes: number of episodes
        :param update_times: value update taken in one episode
        :param update_iter: update target network after number of iteration
        :param save_iter: save network per number of iterations
        """
        for _ in range(1, episodes + 1):
            self.run(0)
            if self.is_train:
                self.value_update(update_times)
            if _ % update_iter == 0:
                self.online.run_copy()
            if _ % save_iter == 0:
                self._saver.save(self._sess, self._save_path, global_step=_)

    def run(self, update_times):
        """
        Single episode of agent
        """
        self.logger.info('Episode start')
        while not self.env.setup(generate_user_name()):
            pass
        self.logger.info('  User name: %s' % self.env.user_name)
        self.logger.info('  User id: %s' % self.env.user_id)
        self.env.add_cash(1000000)
        self.prev_state = self.env.get_state()
        self.cur_state = self.env.get_state()
        self.action_list = self.env.action_generator()
        self.action = 0
        while not self.env.is_terminal():
            # Choose A from S using policy
            self.logger.debug('  State: %s' % self.cur_state)
            self.logger.debug('  Raw State: %s' % self.env.get_raw_state())
            self.logger.info('  Action list: %s' % [a.data for a in self.action_list])
            self.action = self.action_policy()

            # Take action A
            if self.action.cmd == 'ReqBuild' or self.action.cmd == 'ReqBuildUpdate':
                self.logger.info('  Selected action: %s, Build id: %s' % (self.action.data, self.action.build_id))
            else:
                self.logger.info('  Selected action command: %s, data: %s' % (self.action.cmd, self.action.data))
            self.env.send_action(self.action)
            self.env.update_time(self.action)

            # Observe R, S'
            self.prev_state = self.cur_state
            self.cur_state = self.env.get_state()
            self.action_list = self.env.action_generator()
            self.reward = self.get_reward()
            self.logger.debug('  Reward: %s' % self.reward)

            self.add_replay(self.prev_state, [self.action.id / self._max_action_id], self.reward, self.cur_state,
                            self.action_list)

            # Q(S,A) = Q(S,A) + \alpha [R + \gamma \max_a Q(S',a) - Q(S,A)]
            # Target value = R + \gamma \max_a Q(S',a)
            q_max = self.target_policy(self.cur_state, self.action_list)
            self.target_value = self.reward + self.gamma * q_max
            if self.is_train:
                self.value_update(update_times)

        self.logger.info('Episode finished')

    def add_replay(self, s, a, r, s_, a_):
        """
        Add experience to replay memory.
        """
        self.replay.add((s, a, r, s_, a_))

    def get_reward(self):
        return self.env.reward_function(self.prev_state, self.cur_state, self.action)

    def value_update(self, times):
        """
        Update value function
        :param times: update value several times
        """
        for _ in range(times):
            batch = self.replay.batch(self._batch_size)
            x = np.zeros((self._batch_size, self.env.get_state_len() + 1), dtype=np.float32)
            y = np.zeros((self._batch_size, 1), dtype=np.float32)
            for i in range(len(batch)):
                s, a, r, s_, a_ = batch[i]
                _x = s + a / self._max_action_id
                # Q(S,A) = Q(S,A) + \alpha [R + \gamma \max_a Q(S',a) - Q(S,A)]
                # Target value = R + \gamma \max_a Q(S',a)
                q_max = self.target_policy(s_, a_)
                _y = r + self.gamma * q_max
                x[i, ...] = _x
                y[i, ...] = _y
            self.online.train((x, y))

    def action_policy(self, s, a):
        """
        Action policy for agent, epsilon-greedy
        :return: selected action
        """
        if not self.is_train or random.random() <= self.epsilon:
            return a[random.randint(0, len(a) - 1)]
        q_value = []
        for action in a:
            aid = action.id / self._max_action_id
            n_input = s + [aid]
            q_value.append(self.target.eval([n_input]))
        action_index = np.argmax(q_value)
        return self.action_list[action_index]

    def target_policy(self, s_, a_):
        """
        Target policy for agent, which is greedy
        :return: max q value in next state
        :rtype: float
        """
        if not self.is_train:
            return 0
        q_value = []
        for action in a_:
            aid = action.id / self._max_action_id
            n_input = s_ + [aid]
            q_value.append(self.target.eval([n_input]))
        q_max = max(q_value)
        return q_max

    @property
    def is_train(self):
        return len(self.replay) > self._batch_size * 10

    @property
    def epsilon(self):
        return 0.01
