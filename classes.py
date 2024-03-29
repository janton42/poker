import random
import time

from funcs import shorthand, make_pairs, name_winner, shuffle

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

    def set_blind_action_position(self):
        if self.big_blind_position + 1 > len(self.seating) - 1:
            self.action_position = 0
        else:
            self.action_position = self.big_blind_position + 1

    def set_action_position(self):
        if self.dealer_position + 1 > len(self.seating) - 1:
            self.action_position = 0
        else:
            self.action_position = self.dealer_position + 1

    def show_seating(self):
        for player in self.seating:
            # Get the player's name and chips
            player_info = f'{player.name}\t{player.chips}'
            # Show or hide cards, depending on whether the player is still in the hand, if it's a showdown, and if
            # the player is an AI
            if player.dealt_in:
                if len(player.hand) > 0:
                    if player.human:
                        player_info += f'\t {shorthand(player.hand)}' + '(you)'
                    else:
                        if self.showdown:
                            player_info += f'\t {shorthand(player.hand)}'
                        else:
                            player_info += f'\t ["***", "***"]'
                else:
                    player_info += f'\t ["No Cards"]'
                if self.action_position == self.seating.index(player):
                    player_info += ' (Action)'
            else:
                player_info += f'\t ["Folded"]'

            # Show the dealer, small blind, and big blind positions
            if self.dealer_position == self.seating.index(player) and self.big_blind_position == self.seating.index(
                    player):
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

    def show_overview(self, header_1, header_2, board):
        print('\n' * 50)
        print(f'*' * 50)
        print(header_1[0])
        print(header_1[1])
        print(header_1[2])
        print(f'*' * 50)
        print(header_2[0])
        print(header_2[1])
        print(f'*' * 50)
        self.show_seating()
        print('*\n' * (10 - len(self.seating)))
        print(f'*' * 50)
        print(board[0])
        print(board[1])
        print(f'*' * 50)
        print('\n' * 9)

    def introduce(self):
        # This will be at the top of the terminal, if the terminal spans the full height of the screen, and 10 rows are
        # used at the bottom of the terminal screen for options or other information.
        # heading_1
        line_1 = f"This is a {self.name} table."
        line_2 = f"The blinds are {self.small_blind} and {self.big_blind}."
        line_3 = f''
        header_1 = [line_1, line_2, line_3]
        # heading_2
        line_1 = f''
        line_2 = f''
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
        self.show_overview(header_1, header_2, board)

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
        self.pot = 0
        self.bet_to_call = 0
        self.table = table
        self.players = self.table.seating
        self.dealer = ''
        self.small_blind = ''
        self.big_blind = ''
        self.action = ''
        self.winner = ''
        self.rounds_bet = []

        # Clear collect cards from players, clear the table, and shuffle deck
        self.table.reset_board()
        for player in self.players:
            player.hand.clear()
        random.shuffle(self.deck)
        self.table.showdown = False
        self.table.set_blind_action_position()

    def rank_cards(self, cards: list):
        return sorted(cards, key=lambda card: card['Rank'], reverse=True)

    def deal_pocket(self):
        print('Dealing Pocket Cards')
        # Refactor using sample()
        table_rounds = 0
        while table_rounds < 2:
            for player in self.players:
                if player.dealt_in:
                    player.hand.append(self.deck.pop())
            table_rounds += 1

        for player in self.players:
            # Order players' respective pocket cards by rank
            player.hand = self.rank_cards(player.hand)
            # Set blind player names and have them ante up with their blind amounts.
            if self.players.index(player) == self.table.small_blind_position:
                self.small_blind = player.name
                player.bet(self.table.small_blind, self, 'blind')
            elif self.players.index(player) == self.table.big_blind_position:
                self.big_blind = player.name
                player.bet(self.table.big_blind, self, 'blind')
            elif self.players.index(player) == self.table.action_position:
                self.action = player.name

        line_1 = f'{self.small_blind} put in the small blind (pot + 5)'
        line_2 = f' {self.big_blind} put it the big blind (pot + 10).'
        line_3 = f'Blinds are in.'
        header_1 = [line_1, line_2, line_3]
        # heading_2
        line_1 = f'Pot: {self.pot}'
        line_2 = f'Bet to call: {self.bet_to_call}'
        header_2 = [line_1, line_2]
        # board
        line_1 = f'The board is:'
        if len(self.table.board['Flop']) == 0 and len(self.table.board['Turn']) == 0 and len(
                self.table.board['River']) == 0:
            line_2 = f'There are no cards on the table.'
        else:
            line_2 = f'Ya done fucked up; reset the game, jackass!'
        board = [line_1, line_2]
        # Display current status
        self.table.show_overview(header_1, header_2, board)
        print('\n' * 6)
        time.sleep(5)

    def deal_flop(self):
        table_rounds = 0
        self.bet_to_call = 0
        while table_rounds < 4:
            self.table.board['Flop'].append(self.deck.pop())
            table_rounds += 1

    def deal_turn(self):
        table_rounds = 0
        self.bet_to_call = 0
        while table_rounds < 2:
            self.table.board['Turn'].append(self.deck.pop())
            table_rounds += 1

    def deal_river(self):
        table_rounds = 0
        self.bet_to_call = 0
        while table_rounds < 2:
            self.table.board['River'].append(self.deck.pop())
            table_rounds += 1

    def count_active_players(self):
        active_players = 0
        for player in self.players:
            if player.dealt_in:
                active_players += 1
        return active_players

    def betting_round(self, initial_bet: int, round_title: str, last_bet_pos: int):
        no_bet_no_raise = True
        # If not the pre-flop round, action is to the left of dealer
        if round_title != 'pre-Flop':
            self.table.set_action_position()
        # else:
        #     self.table.set_blind_action_position()
        betting_action = self.table.action_position

        bets = 0
        while True:
            if round_title in self.rounds_bet:
                if bets == last_bet_pos - 1:
                    # if not no_bet_no_raise:
                    #     self.betting_round(self.bet_to_call, round_title, betting_action)
                    break
            elif bets == len(self.players):
                if not no_bet_no_raise:
                    self.betting_round(self.bet_to_call, round_title, betting_action)
                break
            bets += 1
            player = self.players[betting_action]
            self.table.action_position = betting_action
            self.action = player.name
            line_1 = f'This is the {round_title} betting round.'
            line_2 = f'No bet, no raise: {no_bet_no_raise}'
            line_3 = f"Bet to call: {self.bet_to_call}"
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
                cards = shorthand(
                    self.table.board["Flop"][1:] + self.table.board["Turn"][1:] + self.table.board["River"][1:])
            line_2 = f'{cards}'
            board = [line_1, line_2]
            # Display current status

            self.table.show_overview(header_1, header_2, board)
            turn_outcome = ['i', 'out of the hand']
            if player.dealt_in:
                if player.human:
                    turn_outcome = player.turn(self.bet_to_call, self)
                else:
                    turn_outcome = player.take_turn(self.bet_to_call, self)

            if betting_action + 1 == len(self.players):
                betting_action = 0
            else:
                betting_action += 1
            if turn_outcome[0] == 'bet' or turn_outcome == 'raise':
                no_bet_no_raise = False
            # self.table.action_position = betting_action
            line_1 = f'This is the {round_title} betting round.'
            line_2 = f'No bet, no raise: {no_bet_no_raise}'
            line_3 = f"New amount to call: {self.bet_to_call}"
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
            self.table.show_overview(header_1, header_2, board)

            self.table.action_position = betting_action
            print('\n' * 6)
            time.sleep(5)

    def determine_winner(self):  # TODO: Make this more sophisticated
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
        if len(self.table.board['Flop']) == 0 and len(self.table.board['Turn']) == 0 and len(
                self.table.board['River']) == 0:
            line_2 = f'There are no cards on the table.'
        else:
            line_2 = f'{shorthand(self.table.board["Flop"][1:] + self.table.board["Turn"][1:] + self.table.board["River"][1:])}'
        board = [line_1, line_2]
        # Display current status
        self.table.show_overview(header_1, header_2, board)
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
        self.betting_round(self.table.big_blind, 'pre-Flop', self.table.big_blind_position)
        self.reset_last_bets()
        self.deal_flop()
        self.betting_round(0, 'flop', self.table.action_position)
        self.reset_last_bets()
        self.deal_turn()
        self.betting_round(0, 'turn', self.table.action_position)
        self.deal_river()
        self.betting_round(0, 'river', self.table.action_position)
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

    def rank_cards(self, cards: list):
        return sorted(cards, key=lambda card: card['Rank'], reverse=True)

    def print_name(self):
        print(self.name)

    def print_info(self):
        print(f"Name: {self.name}, Chips: {self.chips}")

    def show_hand(self):
        print(f'{self.hand[0]} {self.hand[1]}')

    def make_best_hand(self, community_cards):
        best_pocket = self.hand[0]
        sorted_community = self.rank_cards(community_cards)
        lowest_community = sorted_community[-1]
        if best_pocket['Rank'] > lowest_community['Rank']:
            high_card = [best_pocket]
        else:
            high_card = [sorted_community[0]]
        high_card = shorthand(high_card)
        available = self.hand + community_cards
        available = self.rank_cards(available)
        pairs = make_pairs(available)
        print(f'{self.name} says:')
        if len(pairs) == 1:
            print(f'\tI have a pair of {pairs[0]["Value"]}s')
        elif len(pairs) == 2:
            print(f'\tI have two pair - {pairs[0]["Value"]}s and {pairs[2]["Value"]}s')
        else:
            print(f'\tI have {high_card[0].split(" ")[0]} high')
        print(shorthand(self.hand))

    def bet(self, amount: int, current_hand: object, bet_type: str):
        self.chips -= amount
        self.last_bet = amount
        current_hand.pot += amount
        if bet_type != 'call':
            current_hand.bet_to_call = amount
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
            decision = 'fold'
            amount = 0
            self.fold()
        elif decision == '2':
            decision = 'check'
            amount = 0
        elif decision == '3':
            amount = int(input('How much would you like to bet? '))
            decision = 'bet'
            self.bet(amount, current_hand, decision)
        elif decision == '4':
            decision = 'raise'
            amount = int(input('How much would you like to raise? '))
            self.bet(amount, current_hand, decision)
        elif decision == '5':
            decision = 'call'
            amount = current_bet - self.last_bet
            self.bet(amount, current_hand, decision)
        turn_action = (decision, amount)
        print(f'{self.name} says:{decision} {amount}')

        return turn_action

class AIPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.human = False

    def think(self):  # TODO: Make this more sophisticated
        contemplation = random.randint(1,2)
        print(f'{self.name} is only a machine, but it is thinking...')
        print('\n' * 5)
        time.sleep(contemplation)

        return contemplation

    def take_turn(self, current_bet: int, current_hand: object):
        # Think it over, consider options, calculate odds
        winning_odds = self.think()
        amount = 0
        # Make the decision # TODO: Make this more sophisticated
        if current_bet == 0:
            decision = '2' # Check
        elif current_bet > self.chips * .3:
            decision = '1' # Fold
        elif winning_odds > 11:
            decision = '5' # Raise
        elif winning_odds > 11:
            decision = '3' # Bet
        elif winning_odds > 6:
            decision = '4' # Call
        else:
            decision = '4' # Call

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
            if self.chips == 0:
                amount = 0
            elif self.chips < 10:
                amount = 1
            else:
                amount = random.randint(1, 10)
            self.bet(amount, current_hand, decision)
        elif decision == '4':  # Call
            decision = 'call'

            amount = current_bet - self.last_bet
            self.bet(amount, current_hand, decision)
        elif decision == '5':  # Raise
            decision = 'raise'
            if current_bet > self.chips:
                amount = self.chips
            elif self.chips == 0:
                amount = 0
            elif self.chips < 10:
                amount = 1
            else:
                amount = random.randint(1, 10)
            self.bet(amount, current_hand, decision)
        turn_action = (decision, amount)
        # Return the decision and amount
        return turn_action
