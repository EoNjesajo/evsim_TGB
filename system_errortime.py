import time

class SystemErrorTime():

    def __init__(self):
        self.start = 0.0
        self.end = 0.0
        self.result = 0.0

    def start_time(self):
        self.start = time.time()
        print(f"시작시간 : {self.start}")
        return self.start

    def time_interval(self):
        self.end = time.time()
        self.result = self.end - self.start
        print(f"반환시간 : {self.end}")
        print(f"소요시간 : {self.result}\n")
        return self.result