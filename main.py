import random
import time

names = ['John', 'Nacho', 'Li Bao', 'Sally', 'Shaniqua', 'Ivan', 'Mkembe', 'Liu Xeng', 'Dmitri', 'Gerardo', 'Mclovin',
         'Snowy', 'Lewis', 'Alice', 'Craig', 'Julian', 'Rodrigo', 'Elvis', 'Lord', 'Alfonso', 'Miguel', 'Ricardo']

hierarchy = {'High Card': 1, 'Pair': 2, 'Two Pair': 3, 'Three of a Kind': 4, 'Straight': 5, 'Flush': 6, 'Full House': 7,
             'Four of a Kind': 8, 'Straight Flush': 9, 'Royal Flush': 10}

player_name = input('Enter your name: ')


def main_game_loop(current_table: object):
    choice = int(input('What would you like to do?\n'
                       '(1) play a hand\n'
                       '(2) change tables (keep your current chip count, reset AI players, seating and dealer '
                       'position)\n'
                       '(3) replenish chips (keep your current seating, AI players, and dealer position, reset your '
                       'chip count to initial value)\n'
                       '(4) reset chips (keep your current seating, AI players, and dealer posotion, '
                       'reset all players\' chip count to inital value\n'
                       '(5) reset everything (keep only your name, reset AI players, seating, dealer position, and all'
                       'players\' chip count to initial value)\n'
                       '(6) quit the game\n\nEnter your choice:\t'))
    if choice == 1:
        hand = Hand(current_table)
        hand.play()
        main_game_loop(current_table)
    elif choice == 2:
        # TODO: Change tables but keep chips
        print('Changing tables...')
    elif choice == 3:
        # TODO: Replenish chips
        print('Replenishing chips...')
    elif choice == 4:
        # TODO: Reset chips
        print('Resetting chips...')
    elif choice == 5:
        new_table = make_new_table()

        main_game_loop(new_table)
    elif choice == 6:
        print('Quitting game...')
        print('обсось')
    else:
        print('Invalid input')
        print('You broke the game... smooth move, Poindexter.')


def make_new_table():
    global player_name
    new_table = Table()
    # Make human player instance
    human = Player(player_name)
    # Add human player to table
    new_table.add_player(human, 'human')
    # Get number of AI players from user
    ai_num = int(input('How many AI players [1-9]? '))
    # Make AI player instances
    ai_player_list = make_ai_players(ai_num)
    # Add AI players to table
    for player in ai_player_list:
        new_table.add_player(player, 'bot')
    new_table.make_seating()
    new_table.set_blind_positions()
    new_table.set_action_position()
    new_table.introduce()
    return new_table


def shorthand(cards: list):
    suit_map = {'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'}
    value_map = {'Ace': 'A', 'Jack': 'J', 'Queen': 'Q', 'King': 'K'}
    return [f"{value_map.get(card['Value'], card['Value'])}{suit_map[card['Suit']]}" for card in cards]


def make_pairs(available_cards):  # TODO: Find pairs of cards with the same rank
    pairs = []
    for card in available_cards:
        rank_to_match = card['Rank']
        for card2 in available_cards:
            if card2['Rank'] == rank_to_match:
                pairs.append([card, card2])

    return pairs


def rank_cards(cards: list):
    return sorted(cards, key=lambda card: card['Rank'], reverse=True)


def name_winner(players: list):  # TODO: Remove - this is in the Hand class
    still_in = [player for player in players if player.dealt_in == True]
    if len(still_in) == 1:
        return still_in[0].name


def shuffle(deck: list):
    max_i = len(deck)
    for i in range(max_i):
        j = random.randint(0, max_i - 1)
        deck[i], deck[j] = deck[j], deck[i]

    return deck


def make_ai_players(num_players: int):
    ai_players = []
    name_list = random.sample(names, num_players)
    for name in name_list:
        ai_players.append(AIPlayer(name))
    return ai_players


def show_overview(table, header_1, header_2, board):
    print('\n' * 50)
    print(f'*' * 50)
    print(header_1[0])
    print(header_1[1])
    print(header_1[2])
    print(f'*' * 50)
    print(header_2[0])
    print(header_2[1])
    print(f'*' * 50)
    table.show_seating()
    print('*\n' * (10 - len(table.seating)))
    print(f'*' * 50)
    print(board[0])
    print(board[1])
    print(f'*' * 50)
    print('\n' * 9)


class Table:
    def __init__(self):
        self.name = "Texas Hold'em"
        self.table = {'human': '', 'bots': []}
        self.seating = ''
        self.dealer_position = 0
        self.small_blind_position = 0
        self.big_blind_position = 0
        self.action_position = 0
        self.small_blind = 5
        self.big_blind = 10
        self.board = {'Flop': [], 'Turn': [], 'River': []}
        self.showdown = False

    def add_player(self, player: object, player_type: str):  # TODO: update logic to use player.human attribute
        if player_type == 'human':
            self.table['human'] = player
        elif player_type == 'bot':
            self.table['bots'].append(player)

    def make_seating(self):
        seating = [self.table['human']] + self.table['bots']
        random.shuffle(seating)
        self.seating = seating

    def rotate_dealer(self):
        if self.dealer_position + 1 > len(self.seating) - 1:
            self.dealer_position = 0
        else:
            self.dealer_position += 1

    def set_blind_positions(self):
        if self.dealer_position + 1 > len(self.seating) - 1:
            self.small_blind_position = 0
            self.big_blind_position = 1
        elif self.dealer_position + 2 > len(self.seating) - 1:
            self.small_blind_position = self.dealer_position + 1
            self.big_blind_position = 0
        else:
            self.small_blind_position = self.dealer_position + 1
            self.big_blind_position = self.dealer_position + 2

    def set_action_position(self):
        if self.big_blind_position + 1 > len(self.seating) - 1:
            self.action_position = 0
        else:
            self.action_position = self.big_blind_position + 1

    def show_seating(self):
        for player in self.seating:
            # Get the player's name and chips
            player_info = f'{player.name}\t{player.chips}'
            # Show or hide cards, depending on whether the player is still in the hand, if it's a showdown, and if
            # the player is an AI
            if player.dealt_in:
                if len(player.hand) > 0:
                    if player not in self.table['bots']:  # TODO: Update to check the player.human attribute
                        player_info += f'\t {shorthand(player.hand)}'
                    else:
                        if self.showdown:
                            player_info += f'\t {shorthand(player.hand)}'
                        else:
                            player_info += f'\t ["***", "***"]'
                else:
                    player_info += f'\t ["No Cards"]'
            else:
                player_info += f'\t ["Folded"]'

            # Show the dealer, small blind, and big blind positions
            if self.dealer_position == self.seating.index(player) and self.big_blind_position == self.seating.index(player):
                print(f'{player_info} (Dealer, Big Blind)')
            elif self.dealer_position == self.seating.index(player):
                print(f'{player_info} (Dealer)')
            elif self.small_blind_position == self.seating.index(player):
                print(f'{player_info} (Small Blind)')
            elif self.big_blind_position == self.seating.index(player):
                print(f'{player_info} (Big Blind)')
            else:
                print(f'{player_info}')

    def reset_board(self):
        self.board = {'Flop': [], 'Turn': [], 'River': []}
        for player in self.seating:
            player.dealt_in = True

    def remove_player(self, player: object):
        self.table['bots'].remove(player)

    def introduce(self):
        # This will be at the top of the terminal, if the terminal spans the full height of the screen, and 10 rows are
        # used at the bottom of the terminal screen for options or other information.
        # heading_1
        line_1 = f"This is a {self.name} table."
        line_2 = f"The blinds are {self.small_blind} and {self.big_blind}."
        line_3 = f'Dealer pos: {self.dealer_position}'
        header_1 = [line_1, line_2, line_3]
        # heading_2
        line_1 = f'Small Blind pos: {self.small_blind_position}'
        line_2 = f'Big Blind pos: {self.big_blind_position}'
        header_2 = [line_1, line_2]
        # board
        line_1 = f'The board is:'
        if len(self.board['Flop']) == 0 and len(self.board['Turn']) == 0 and len(self.board['River']) == 0:
            line_2 = f'There are no cards on the table.'
        else:
            line_2 = f'{line_1} {shorthand(self.board["Flop"])} {shorthand(self.board["Turn"])} ' \
                     f'{shorthand(self.board["River"])}'
        board = [line_1, line_2]
        # Display current status
        show_overview(self, header_1, header_2, board)


class Hand:
    def __init__(self, table: object):
        self.deck = [{'Suit': 'Spades', 'Value': 'Ace', 'Rank': 14}, {'Suit': 'Spades', 'Value': 'King', 'Rank': 13},
                     {'Suit': 'Spades', 'Value': 'Queen', 'Rank': 12}, {'Suit': 'Spades', 'Value': 'Jack', 'Rank': 11},
                     {'Suit': 'Spades', 'Value': '10', 'Rank': 10}, {'Suit': 'Spades', 'Value': '9', 'Rank': 9},
                     {'Suit': 'Spades', 'Value': '8', 'Rank': 8}, {'Suit': 'Spades', 'Value': '7', 'Rank': 7},
                     {'Suit': 'Spades', 'Value': '6', 'Rank': 6}, {'Suit': 'Spades', 'Value': '5', 'Rank': 5},
                     {'Suit': 'Spades', 'Value': '4', 'Rank': 4}, {'Suit': 'Spades', 'Value': '3', 'Rank': 3},
                     {'Suit': 'Spades', 'Value': '2', 'Rank': 2}, {'Suit': 'Hearts', 'Value': 'Ace', 'Rank': 14},
                     {'Suit': 'Hearts', 'Value': 'King', 'Rank': 13}, {'Suit': 'Hearts', 'Value': 'Queen', 'Rank': 12},
                     {'Suit': 'Hearts', 'Value': 'Jack', 'Rank': 11}, {'Suit': 'Hearts', 'Value': '10', 'Rank': 10},
                     {'Suit': 'Hearts', 'Value': '9', 'Rank': 9}, {'Suit': 'Hearts', 'Value': '8', 'Rank': 8},
                     {'Suit': 'Hearts', 'Value': '7', 'Rank': 7}, {'Suit': 'Hearts', 'Value': '6', 'Rank': 6},
                     {'Suit': 'Hearts', 'Value': '5', 'Rank': 5}, {'Suit': 'Hearts', 'Value': '4', 'Rank': 4},
                     {'Suit': 'Hearts', 'Value': '3', 'Rank': 3}, {'Suit': 'Hearts', 'Value': '2', 'Rank': 2},
                     {'Suit': 'Diamonds', 'Value': 'Ace', 'Rank': 14},
                     {'Suit': 'Diamonds', 'Value': 'King', 'Rank': 13},
                     {'Suit': 'Diamonds', 'Value': 'Queen', 'Rank': 12},
                     {'Suit': 'Diamonds', 'Value': 'Jack', 'Rank': 11},
                     {'Suit': 'Diamonds', 'Value': '10', 'Rank': 10}, {'Suit': 'Diamonds', 'Value': '9', 'Rank': 9},
                     {'Suit': 'Diamonds', 'Value': '8', 'Rank': 8}, {'Suit': 'Diamonds', 'Value': '7', 'Rank': 7},
                     {'Suit': 'Diamonds', 'Value': '6', 'Rank': 6}, {'Suit': 'Diamonds', 'Value': '5', 'Rank': 5},
                     {'Suit': 'Diamonds', 'Value': '4', 'Rank': 4}, {'Suit': 'Diamonds', 'Value': '3', 'Rank': 3},
                     {'Suit': 'Diamonds', 'Value': '2', 'Rank': 2}, {'Suit': 'Clubs', 'Value': 'Ace', 'Rank': 14},
                     {'Suit': 'Clubs', 'Value': 'King', 'Rank': 13}, {'Suit': 'Clubs', 'Value': 'Queen', 'Rank': 12},
                     {'Suit': 'Clubs', 'Value': 'Jack', 'Rank': 11}, {'Suit': 'Clubs', 'Value': '10', 'Rank': 10},
                     {'Suit': 'Clubs', 'Value': '9', 'Rank': 9}, {'Suit': 'Clubs', 'Value': '8', 'Rank': 8},
                     {'Suit': 'Clubs', 'Value': '7', 'Rank': 7}, {'Suit': 'Clubs', 'Value': '6', 'Rank': 6},
                     {'Suit': 'Clubs', 'Value': '5', 'Rank': 5}, {'Suit': 'Clubs', 'Value': '4', 'Rank': 4},
                     {'Suit': 'Clubs', 'Value': '3', 'Rank': 3}, {'Suit': 'Clubs', 'Value': '2', 'Rank': 2}]
        self.round = 0
        self.pot = 0
        self.table = table
        self.players = self.table.seating
        self.dealer = ''
        self.small_blind = ''
        self.big_blind = ''
        self.action = ''
        self.winner = ''

        # Clear collect cards from players, clear the table, and shuffle deck
        self.table.reset_board()
        for player in self.players:
            player.hand.clear()
        random.shuffle(self.deck)
        self.table.showdown = False

    def deal_pocket(self):
        print('Dealing Pocket Cards')
        table_rounds = 0
        while table_rounds < 2:
            for player in self.players:
                if player.dealt_in:
                    player.hand.append(self.deck.pop())
            table_rounds += 1

        for player in self.players:
            # Order players' respective pocket cards by rank
            player.hand = rank_cards(player.hand)
            # Set blind player names and have them ante up with their blind amounts.
            if self.players.index(player) == self.table.small_blind_position:
                self.small_blind = player.name
                player.bet(self.table.small_blind, self)
            elif self.players.index(player) == self.table.big_blind_position:
                self.big_blind = player.name
                player.bet(self.table.big_blind, self)
            elif self.players.index(player) == self.table.action_position:
                self.action = player.name

        line_1 = f'{self.small_blind} put in the small blind (pot + 5)'
        line_2 = f' {self.big_blind} put it the big blind (pot + 10).'
        line_3 = f'Blinds are in.'
        header_1 = [line_1, line_2, line_3]
        # heading_2
        line_1 = f'Pot: {self.pot}'
        line_2 = f''
        header_2 = [line_1, line_2]
        # board
        line_1 = f'The board is:'
        if len(self.table.board['Flop']) == 0 and len(self.table.board['Turn']) == 0 and len(self.table.board['River']) == 0:
            line_2 = f'There are no cards on the table.'
        else:
            line_2 = f'Ya done fucked up; reset the game, jackass!'
        board = [line_1, line_2]
        # Display current status
        show_overview(self.table, header_1, header_2, board)
        print('\n' * 6)
        time.sleep(5)

    def deal_flop(self):
        self.round = 1
        print('Dealing Flop')
        print('Burning one, turning three')
        table_rounds = 0
        while table_rounds < 4:
            self.table.board['Flop'].append(self.deck.pop())
            table_rounds += 1

    def deal_turn(self):
        self.round = 2
        print('Dealing Turn')
        print('Burning one, turning one')
        table_rounds = 0
        while table_rounds < 2:
            self.table.board['Turn'].append(self.deck.pop())
            table_rounds += 1

    def deal_river(self):
        self.round = 3
        print('Dealing River')
        print('Burning one, turning one')
        table_rounds = 0
        while table_rounds < 2:
            self.table.board['River'].append(self.deck.pop())
            table_rounds += 1

    def count_active_players(self):
        active_players = 0
        for player in self.players:
            if player.dealt_in:
                active_players += 1
        return active_players

    def betting_round(self, initial_bet: int, round_title: str):
        betting_action = self.table.action_position
        bets = 0
        while True:
            if bets == len(self.players):
                break
            bets += 1
            player = self.players[betting_action]
            self.action = player.name
            line_1 = f"This is the {round_title} betting round."
            line_2 = f"The blinds are {self.table.small_blind} and {self.table.big_blind}."
            line_3 = f"Bets: {bets} of {len(self.players)}"
            header_1 = [line_1, line_2, line_3]
            # heading_2
            line_1 = f'Pot: {self.pot}'
            line_2 = f'Action is on {self.action}.'
            header_2 = [line_1, line_2]
            # board
            line_1 = f'The board is:'
            cards = 'Empty.'
            if round_title == 'flop':
                cards = shorthand(self.table.board["Flop"][1:])
            elif round_title == 'turn':
                cards = shorthand(self.table.board["Flop"][1:] + self.table.board["Turn"][1:])
            elif round_title == 'river':
                cards = shorthand(self.table.board["Flop"][1:] + self.table.board["Turn"][1:] + self.table.board["River"][1:])
            line_2 = f'{cards}'
            board = [line_1, line_2]
            # Display current status

            show_overview(self.table, header_1, header_2, board)
            if player.dealt_in:
                if player.human:
                    turn_outcome = player.turn(initial_bet, self)
                else:
                    turn_outcome = player.take_turn(initial_bet, self)

            betting_action += 1
            if betting_action == len(self.players):
                betting_action = 0
            line_1 = f"This is the {round_title} betting round."
            line_2 = f"The blinds are {self.table.small_blind} and {self.table.big_blind}."
            line_3 = f"Bets: {bets} of {len(self.players)}"
            header_1 = [line_1, line_2, line_3]
            # heading_2
            line_1 = f'Pot: {self.pot}'
            if turn_outcome[1] == 0:
                line_2 = f'{self.action} {turn_outcome[0]}s.'
            else:
                line_2 = f'{self.action} {turn_outcome[0]}s {turn_outcome[1]}.'
            header_2 = [line_1, line_2]
            # board
            line_1 = f'The board is:'
            line_2 = f'{cards}'
            board = [line_1, line_2]
            # Display current status
            show_overview(self.table, header_1, header_2, board)
            print('\n' * 6)
            time.sleep(5)

    def determine_winner(self):
        if self.winner != '':
            winner = self.winner
        else:
            winner = random.randint(0, len(self.players) - 1)

        for player in self.players:
            if self.players.index(player) == winner:
                player.chips += self.pot
                self.winner = player.name

        return self.winner

    def declare_winner(self):
        self.table.showdown = True
        self.winner = self.determine_winner()
        line_1 = f"This is a {self.table.name} table."
        line_2 = f"The blinds are {self.table.small_blind} and {self.table.big_blind}."
        line_3 = f""
        header_1 = [line_1, line_2, line_3]
        # heading_2
        line_1 = f'Pot: {self.pot}'
        line_2 = f'Winner Winner, Chicken Dinner! {self.winner} won {self.pot}!'
        header_2 = [line_1, line_2]
        # board
        line_1 = f'The board is:'
        if len(self.table.board['Flop']) == 0 and len(self.table.board['Turn']) == 0 and len(self.table.board['River']) == 0:
            line_2 = f'There are no cards on the table.'
        else:
            line_2 = f'{shorthand(self.table.board["Flop"][1:] + self.table.board["Turn"][1:] + self.table.board["River"][1:])}'
        board = [line_1, line_2]
        # Display current status
        show_overview(self.table, header_1, header_2, board)
        self.table.rotate_dealer()
        self.table.set_blind_positions()
        for player in self.players:
            player.hand = []
        return

    def reset_last_bets(self):
        for player in self.players:
            player.last_bet = 0

    def play(self):
        # Deal pocket cards
        # Blinds are added to the pot
        self.deal_pocket()
        # First betting round
        self.betting_round(self.table.big_blind, 'pre-Flop')
        self.reset_last_bets()
        self.deal_flop()
        self.betting_round(0, 'flop')
        self.reset_last_bets()
        self.deal_turn()
        self.betting_round(0, 'turn')
        self.deal_river()
        self.betting_round(0, 'river')
        self.declare_winner()


class Player:
    def __init__(self, name):
        self.name = name
        self.initial_chips = 1000
        self.hand = []
        self.chips = self.initial_chips
        self.dealt_in = True
        self.last_bet = 0
        self.human = True

    def print_name(self):
        print(self.name)

    def print_info(self):
        print(f"Name: {self.name}, Chips: {self.chips}")

    def show_hand(self):
        print(f'{self.hand[0]} {self.hand[1]}')

    def make_best_hand(self, community_cards):
        best_pocket = self.hand[0]
        sorted_community = rank_cards(community_cards)
        lowest_community = sorted_community[-1]
        if best_pocket['Rank'] > lowest_community['Rank']:
            high_card = [best_pocket]
        else:
            high_card = [sorted_community[0]]
        high_card = shorthand(high_card)
        available = self.hand + community_cards
        available = rank_cards(available)
        pairs = make_pairs(available)
        print(f'{self.name} says:')
        if len(pairs) == 2:
            print(f'\tI have a pair of {pairs[0]["Value"]}s')
        elif len(pairs) == 4:
            print(f'\tI have two pair - {pairs[0]["Value"]}s and {pairs[2]["Value"]}s')
        else:
            print(f'\tI have {high_card[0].split(" ")[0]} high')
        print(shorthand(self.hand))

    def bet(self, amount: int, current_hand: object):
        self.chips -= amount
        self.last_bet = amount
        current_hand.pot += amount
        return amount

    def fold(self):
        self.dealt_in = False
        return self.dealt_in

    def deal_me_in(self):
        self.dealt_in = True
        return self.dealt_in

    def turn(self, current_bet: int, current_hand: object):
        amount = 0
        decision = input('What would you like to do?\n'
                         '(1) Fold\n'
                         '(2) Check\n'
                         '(3) Bet\n'
                         '(4) Raise\n'
                         '(5) Call\n\n'
                         'Enter your choice: ')
        if decision == '1':
            amount = 0
            self.fold()
        elif decision == '2':
            amount = 0
        elif decision == '3':
            amount = int(input('How much would you like to bet? '))
            decision = 'bet'
            self.bet(amount, current_hand)
        elif decision == '4':
            amount = int(input('How much would you like to raise? '))
            self.bet(amount, current_hand)
        elif decision == '5':
            amount = current_bet - self.last_bet
            self.bet(amount, current_hand)
        turn_action = (decision, amount)
        print(f'{self.name} says:{decision} {amount}')

        return turn_action


class AIPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.human = False


    def think(self):  # TODO: Make this more sophisticated
        contemplation = random.randint(3, 10)
        print(f'{self.name} is only a machine, but it is thinking...')
        print('\n' * 5)
        time.sleep(contemplation)

    def take_turn(self, current_bet: int, current_hand: object):
        # Think it over, consider options, calculate odds
        self.think()
        amount = 0
        # Make the decision # TODO: Make this more sophisticated
        decision = '3'

        # Set the amount based on decision
        if decision == '1':  # Fold
            decision = 'fold'
            amount = 0
            self.fold()
        elif decision == '2':  # Check
            decision = 'check'
            amount = 0
        elif decision == '3':  # Bet
            decision = 'bet'
            amount = random.randint(1, self.chips)
            self.bet(amount, current_hand)
        elif decision == '4':  # Call
            decision = 'call'
            amount = random.randint(self.chips - current_bet, self.chips)
            self.bet(amount, current_hand)
        elif decision == '5':  # Raise
            decision = 'raise'
            if current_bet > self.chips:
                amount = self.chips
            else:
                amount = current_bet + random.randint(1, self.chips - current_bet)
            self.bet(amount, current_hand)
        turn_action = (decision, amount)
        # Return the decision and amount
        return turn_action


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Initialize the first table
    table = make_new_table()
    # Main game loop - this is where the magic happens
    main_game_loop(table)
