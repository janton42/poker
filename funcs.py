import random

from classes import Table, Hand, Player, AIPlayer
from vars import names, hierarchy


def make_new_table(player_name):
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
    new_table.set_blind_action_position()
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
