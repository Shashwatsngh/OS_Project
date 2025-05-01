# memory.py
class Allocator:
    @staticmethod
    def first_fit(size, requests):
        mem = [None]*size
        allocations = {}
        for pid, req in enumerate(requests):
            for i in range(size-req+1):
                if all(x is None for x in mem[i:i+req]):
                    for j in range(i, i+req): mem[j] = pid
                    allocations[pid] = (i, req)
                    break
        return mem, allocations

    @staticmethod
    def best_fit(size, requests):
        mem = [None]*size
        allocations = {}
        for pid, req in enumerate(requests):
            best_i, best_len = None, size+1
            i = 0
            while i < size:
                if mem[i] is None:
                    j = i
                    while j < size and mem[j] is None: j+=1
                    length = j - i
                    if req <= length < best_len:
                        best_i, best_len = i, length
                    i = j
                else:
                    i+=1
            if best_i is not None:
                for k in range(best_i, best_i+req): mem[k] = pid
                allocations[pid] = (best_i, req)
        return mem, allocations

