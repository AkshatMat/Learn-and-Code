class DivisorCounter:
    def __init__(self, limit):
        self.limit = limit
        self.divisor_counts = [0] * (limit + 2) 
        self._precompute()

    def _precompute(self):
        self.divisor_counts = [0] * (self.limit + 2)
        
        for i in range(1, self.limit + 2):
            for j in range(i, self.limit + 2, i):
                self.divisor_counts[j] += 1

    def get(self, n):
        if n < 1 or n > self.limit + 1:
            raise ValueError("Number out of precomputed range")
        return self.divisor_counts[n]