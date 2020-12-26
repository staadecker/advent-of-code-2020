class Game:
    def __init__(self, players_deck):
        self.players_deck = players_deck
        self.num_players = len(players_deck)
        self.previous_turns = set()
        self.winner = None
        self.num_cards = sum(map(len, self.players_deck))

    def is_done(self):
        return self.winner is not None

    def encode_state(self):
        return tuple(map(tuple, self.players_deck))

    def play_turn(self):
        # Infinite loop check
        state = self.encode_state()
        if state in self.previous_turns:
            self.winner = 0
            return
        self.previous_turns.add(state)

        # Draw cards
        cards_played = [player_deck.pop(0) for player_deck in self.players_deck]

        # Check is_recursive
        is_recursive = True
        for i, card_played in enumerate(cards_played):
            if len(self.players_deck[i]) < card_played:
                is_recursive = False
                break

        # Play recursive game
        if is_recursive:
            new_decks = [player_deck[:cards_played[i]] for i, player_deck in enumerate(self.players_deck)]
            recursive_game = Game(new_decks)
            recursive_game.play()
            round_winner = recursive_game.winner
        else:
            best_card = max(cards_played)
            for player in range(self.num_players):
                if cards_played[player] == best_card:
                    round_winner = player
                    break

        # Make round winner be first card
        if round_winner == 1:
            cards_played = cards_played[::-1]

        self.players_deck[round_winner].extend(cards_played)

        # Winner check
        if len(self.players_deck[round_winner]) == self.num_cards:
            self.winner = round_winner

    def play(self):
        while not self.is_done():
            self.play_turn()


def main(filename):
    game = read_input(filename)
    game.play()
    print(game.winner)
    print(game.players_deck)
    print(calculate_winning_score(game))


def read_input(filename):
    with open(filename, "r") as f:
        players = f.read().strip().split("\n\n")
    players = list(map(lambda player: list(map(int, player.split("\n")[1:])), players))
    return Game(players)


def calculate_winning_score(game):
    score = 0
    winner_deck = game.players_deck[game.winner]
    multiplier = len(winner_deck)
    for card in winner_deck:
        score += card * multiplier
        multiplier -= 1
    return score


if __name__ == '__main__':
    filename = "input.txt"
    main(filename)
