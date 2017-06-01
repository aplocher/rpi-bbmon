class ProcessManager:
    def __init__(self):
        self._processes = {}
        self.n = 0

    def add(self, process):
        self._processes[self.n] = process
        self.n = self.n + 1

    def hasAnyErrors(self):
        for n in self._processes.keys():
            p = self._processes[n]
            if not p.exitcode is None or not p.is_alive():
                print("ERROR")
                return True

        return False
