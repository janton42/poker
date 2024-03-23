import time

from funcs import make_new_table, shorthand, make_pairs, \
name_winner, shuffle, make_ai_players

from classes import Hand

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
