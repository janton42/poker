import time
import random

from classes import Table, Hand, Player, AIPlayer
from vars import names


def make_ai_players(num_players: int):
    ai_players = []
    name_list = random.sample(names, num_players)
    for name in name_list:
        ai_players.append(AIPlayer(name))
    return ai_players


def make_new_table(player_name):
    new_table = Table()
    # Make human player instance
    human = Player(player_name)
    # Add human player to table
    new_table.add_player(human, 'human')
    # Get number of AI players from user
    ai_num = random.randrange(1, 9)
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

def main_game_loop(current_table: object):
    choice = int(input('What would you like to do?\n'
                       '(1) play a hand\n'
                       '(2) reset \n'
                       '(3) quit the game\n\n\n\n\nEnter your choice:\t'))
    if choice == 1:
        hand = Hand(current_table)
        hand.play()
        main_game_loop(current_table)
    elif choice == 2:
        # TODO: Give sub options on what to reset (chips only, AI players, human player name, everything)
        reset = int(input('What would you like to reset?\n'
                          '(1) your chips\n'
                          '(2) the AI players (change tables)\n'
                          '(3) everything\n\n\n\n\nenter your choice:\t'))
        if reset == 1:
            # TODO: Reset player chips
            pass
        elif reset == 2:
            # TODO: Reset AI players
            pass
        elif reset == 3:
            # TODO: Start over
            pass

        print('Reseting...')
    elif choice == 3:
        print('Quitting game...')
        print('обсось')
    else:
        print('Invalid input')
        print('You broke the game... smooth move, Poindexter.')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('\n' * 50)
    print('Welcome to Texas Hold\'em\n')
    print('*' * 50)
    player_name = input('Enter your name: ')
    # Initialize the first table
    table = make_new_table(player_name)
    # Main game loop - this is where the magic happens
    main_game_loop(table)
