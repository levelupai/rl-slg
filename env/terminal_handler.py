class TerminalHandler(object):
    def __init__(self):
        pass

    def is_terminal(self, usr_data):
        return True


class LevelCondition(TerminalHandler):
    def __init__(self, level):
        TerminalHandler.__init__(self)
        self.level = level

    def is_terminal(self, usr_data):
        """
        Reach a certain level
        :param usr_data: user data
        :return: whether agent has reached a certain level
        """
        return usr_data['base_info']['level'] == self.level
