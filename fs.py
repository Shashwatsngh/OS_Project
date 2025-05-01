# fs.py
class FileSystem:
    @staticmethod
    def contiguous(disk_size, files):
        disk = [None]*disk_size
        allocation = {}
        for fid, size in enumerate(files):
            for i in range(disk_size - size + 1):
                if all(x is None for x in disk[i:i+size]):
                    for j in range(i, i+size): disk[j] = fid
                    allocation[fid] = ('contig', i, size)
                    break
        return disk, allocation

    @staticmethod
    def linked(disk_size, files):
        disk = [None]*disk_size
        allocation = {}
        free = [i for i in range(disk_size)]
        for fid, size in enumerate(files):
            if len(free) < size: break
            chain = []
            for _ in range(size):
                block = free.pop(0)
                disk[block] = fid
                chain.append(block)
            allocation[fid] = ('linked', chain)
        return disk, allocation

