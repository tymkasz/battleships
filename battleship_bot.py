size = 10

class BotBattleships:
    def __init__(self, size=size, rng=None):
        self.size = size
        self.rng = rng
        self.cannonaded = set()
        self.hit = set()

    def on_board(self, c, r):

        return 1 <= c <= self.rozmiar and 1 <= r <= self.rozmiar
        
    def not_cannonaded(self):

        return [
            (c, r)
            for c in range(1, self.rozmiar + 1)
            for r in range(1, self.rozmiar + 1)
            if (c,r) not in self.cannonaded
        ]

    def candidates_to_finish(self):

        candidates = set()
        for (c, r) in self.cannonaded:
            for dc, dr in ((0,-1), (0,1), (-1,0), (1,0)):
                p = (c + dc, r + dr)
                if self.on_board(p[0], p[1]) and p not in self.cannonaded:
                    candidates.add(p)
        return sorted(candidates)

    def next_hit(self):

        finishing = self.candidates_to_finish()
        if finishing:
            return self.rng.choice(finishing)

        free = self.not_cannonaded()
        if not free:
            return None

        even = [(c,r) for (c,r) in free if (c+r) % 2 == 0]

        return self.rng.choice(even or free)

    def save_result(self, area, answer):
        
        answer = answer.strip().upper()
        if answer not in ("T", "P"):
            raise ValueError(f"Nieznana odpowiedź: {answer!r}, oczekiwano T albo P")
        self.cannonaded.add(area)
        if answer == "T":
            self.hit.add(area)

        
        


    