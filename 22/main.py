class Game:
    def __init__(self, players_deck):
        self.players_deck = players_deck
        self.num_players = len(players_deck)

    def is_done(self):
        players_lost = 0
        for player_deck in self.players_deck:
            if len(player_deck) == 0:
                players_lost += 1
        return players_lost == len(self.players_deck) - 1

    def play_turn(self):
        cards_played = [player_deck.pop(0) for player_deck in self.players_deck]
        best_card = max(cards_played)
        for i in range(self.num_players):
            if cards_played[i] == best_card:
                best_player = i
                break
        self.players_deck[best_player].extend(sorted(cards_played, reverse=True))


def main(filename):
    game = read_input(filename)

    while not game.is_done():
        game.play_turn()
    print(game.players_deck)
    print(calculate_winning_score(game))


def read_input(filename):
    with open(filename, "r") as f:
        players = f.read().strip().split("\n\n")
    players = list(map(lambda player: list(map(int, player.split("\n")[1:])), players))
    return Game(players)


def calculate_winning_score(game):
    for player_deck in game.players_deck:
        if player_deck:
            winner_deck = player_deck
            break
    score = 0
    multiplier = len(winner_deck)
    for card in winner_deck:
        score += card * multiplier
        multiplier -= 1
    return score


if __name__ == '__main__':
    filename = "input.txt"
    main(filename)
