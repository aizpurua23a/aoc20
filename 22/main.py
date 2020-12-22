import inspect


class SpaceGame:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            data = file.read().split('\n\n')

        self.decks = []
        for deck in data:
            self.decks.append(list(int(card) for card in deck.split('\n')[1:]))

        self.configs = set()
        self.rounds = 0

    def play_game(self):
        while len(self.decks[0]) != 0 and len(self.decks[1]) != 0:
            self.play_round()
        return self.decks

    def play_round(self):
        if self.decks[0][0] > self.decks[1][0]:
            winner_card = self.decks[0].pop(0)
            loser_card = self.decks[1].pop(0)
            self.decks[0].append(winner_card)
            self.decks[0].append(loser_card)
            return

        if self.decks[1][0] > self.decks[0][0]:
            winner_card = self.decks[1].pop(0)
            loser_card = self.decks[0].pop(0)
            self.decks[1].append(winner_card)
            self.decks[1].append(loser_card)
            return


    def play_recursive_game(self, d0, d1):
        seen_cards = set(self.to_str(d0, d1))

        self.rounds += 1
        if self.rounds % 1000 == 0:
            print('Round: {}, l0: {}, l1: {}'.format(self.rounds, len(d0), len(d1)))

        while d0 and d1:
            c0 = d0.pop(0)
            c1 = d1.pop(0)

            if len(d0) >= c0 and len(d1) >= c1:
                winner, _, _ = self.play_recursive_game(d0[:c0], d1[:c1])
                if winner == 0:
                    d0.append(c0)
                    d0.append(c1)
                else:
                    d1.append(c1)
                    d1.append(c0)
            else:
                if c0 > c1:
                    winner = 0
                else:
                    winner = 1

                if winner == 0:
                    d0.append(c0)
                    d0.append(c1)
                else:
                    d1.append(c1)
                    d1.append(c0)

            if self.to_str(d0, d1) in seen_cards:
                return 0, d0, d1
            else:
                seen_cards.add(self.to_str(d0, d1))

        if len(d0) == 0:
            return 1, d0, d1
        if len(d1) == 0:
            return 0, d0, d1
        raise ValueError('We should not be here')

    @staticmethod
    def to_str(d0, d1):
        return ",".join(str(c0) for c0 in d0) + ":" + ",".join(str(c1) for c1 in d1)


    @classmethod
    def day22_01(cls, filename):
        sg = SpaceGame(filename)
        d0, d1 = sg.play_game()
        if len(d0) == 0:
            d = d1
        else:
            d = d0

        result = 0
        for i in range(-1, -len(d)-1, -1):
            result += -i * d[i]

        return result

    @classmethod
    def day22_02(cls, filename):
        sg = SpaceGame(filename)
        winner, d0, d1 = sg.play_recursive_game(sg.decks[0], sg.decks[1])
        if len(d0) == 0:
            d = d1
        else:
            d = d0

        result = 0
        for i in range(-1, -len(d) - 1, -1):
            result += -i * d[i]

        return result


if __name__ == '__main__':
    print(SpaceGame.day22_01('input.txt'))
    print(SpaceGame.day22_02('input.txt'))
