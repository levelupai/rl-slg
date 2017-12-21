import datetime


class TimeHandler(object):
    def __init__(self, total_time_limit=0):
        self.total_time_limit = total_time_limit
        self.start_time = 0
        self.idle_time = 0
        self.last_idle_time = 0
        self.total_idle_time = 0
        self.total_build_time = 0
        self.total_step = 0

    def clear_up(self):
        self.start_time = datetime.datetime.now()
        self.idle_time = 0
        self.last_idle_time = 0
        self.total_idle_time = 0
        self.total_build_time = 0
        self.total_step = 0

    @property
    def total_time(self):
        return self.total_idle_time + self.total_build_time

    def update_time(self, action):
        pass


class CountActionTime(TimeHandler):
    def __init__(self, total_time_limit=0):
        TimeHandler.__init__(self, total_time_limit)

    def update_time(self, action):
        self.total_step += 1
        if action.cmd == "FastForward":
            self.idle_time += action.data['minute'] * 60
        else:
            self.total_idle_time += self.idle_time
            self.last_idle_time = self.idle_time
            self.idle_time = 0
            self.total_build_time += action.time
