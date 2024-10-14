import os


class Backtrack:
    """
    - 回溯类
    - 原子化操作的实现类
    """
    old: list
    new: list

    def __init__(self, _old=None, _new=None, _folder=None):
        self.old = _old
        self.new = _new
        self.folder = _folder

    def add_new(self, new):
        self.new.append(new)

    def add_old(self, old):
        self.old.append(old)

    def rename_backtrack(self):
        i = len(self.old) - 2
        for j in reversed(range(len(self.old) - 1)):
            os.rename(self.new[i], self.old[j])
            i -= 1


