class SelectionSort:
    def __init__(self, tab):
        self.tab = tab

    def swapping(self):
        for i in range(len(self.tab)):
            min_idx = i
            for j in range(i, len(self.tab)):
                if self.tab[min_idx] > self.tab[j]:
                    min_idx = j

            self.tab[i], self.tab[min_idx] = self.tab[min_idx], self.tab[i]

    def shifting(self):
        for i in range(1, len(self.tab)):
            key = self.tab[i]
            j = i - 1
            while j >= 0 and key < self.tab[j]:
                self.tab[j + 1] = self.tab[j]
                j -= 1
            self.tab[j + 1] = key

    def __str__(self):
        return f'{self.tab}'
