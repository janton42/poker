import random

from vars import names, hierarchy


def shorthand(cards: list):
    suit_map = {'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'}
    value_map = {'Ace': 'A', 'Jack': 'J', 'Queen': 'Q', 'King': 'K'}
    return [f"{value_map.get(card['Value'], card['Value'])}{suit_map[card['Suit']]}" for card in cards]


def make_pairs(available_cards):  # TODO: Find pairs of cards with the same rank
    pairs = []
    for card in available_cards:
        rank_to_match = card['Rank']
        for card2 in available_cards:
            if card2['Rank'] == rank_to_match and card['Suit'] != card2['Suit']:
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
