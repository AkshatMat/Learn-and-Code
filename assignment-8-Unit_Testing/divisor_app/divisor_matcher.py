from .divisor_counter import DivisorCounter

class ConsecutiveDivisorMatcher:
    def __init__(self, max_k):
        self.max_k = max_k
        self.counter = DivisorCounter(max_k)
        self.results = [0] * (max_k + 1)
        self._precompute(max_k)

    def _precompute(self, max_k):
        count = 0
        for n in range(2, max_k):
            if self.counter.get(n) == self.counter.get(n + 1):
                count += 1
            self.results[n+1] = count

    def query(self, k):
        if k < 3:
            return 0
        if k > self.max_k:
            raise ValueError("k exceeds maximum precomputed value")
        
        return self.results[k]