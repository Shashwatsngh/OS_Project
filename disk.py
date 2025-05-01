# disk.py
class DiskScheduler:
    @staticmethod
    def fcfs(requests, start):
        time = start
        path = [time]
        for r in requests:
            path.append(r)
            time = r
        return path

    @staticmethod
    def scan(requests, start, end):
        left = sorted([r for r in requests if r < start])
        right = sorted([r for r in requests if r >= start])
        path = [start] + right + [end] + left[::-1]
        return path

