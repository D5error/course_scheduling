from util import *
from .load import *
class generateTimetable:
    def __init__(self):
        self.A, self.B, self.W, self.P, self.S, self.p, self.q = loadConfig()
        print(self.A)


    def run(self, path):
        load.generate_schedule(path, self.A, self.B, self.W, self.P, self.S, self.p, self.q)