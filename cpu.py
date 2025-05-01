# cpu.py
from collections import deque

class Scheduler:
    @staticmethod
    def fcfs(procs):
        time, gantt = 0, []
        for at, bt, pid in sorted(procs, key=lambda x: x[0]):
            if time < at: time = at
            gantt.append((pid, time, time+bt))
            time += bt
        return gantt

    @staticmethod
    def sjf(procs):
        procs = sorted(procs, key=lambda x: x[0])
        time, gantt, ready, i = 0, [], [], 0
        while i < len(procs) or ready:
            if not ready:
                time = max(time, procs[i][0])
            while i < len(procs) and procs[i][0] <= time:
                ready.append(procs[i]); i+=1
            ready.sort(key=lambda x: x[1])
            at, bt, pid = ready.pop(0)
            gantt.append((pid, time, time+bt))
            time += bt
        return gantt

    @staticmethod
    def rr(procs, q):
        procs = sorted(procs, key=lambda x: x[0])
        queue = deque()
        time, gantt, i = 0, [], 0
        while i < len(procs) or queue:
            if not queue:
                time = max(time, procs[i][0])
            while i < len(procs) and procs[i][0] <= time:
                queue.append([*procs[i]]); i+=1
            at, bt, pid = queue.popleft()
            run = min(q, bt)
            gantt.append((pid, time, time+run))
            time += run; bt -= run
            if bt>0:
                while i < len(procs) and procs[i][0] <= time:
                    queue.append([*procs[i]]); i+=1
                queue.append([at, bt, pid])
        return gantt

