import sys
import hmac
import hashlib
import secrets
import random
from prettytable import PrettyTable


class TableRules:

    def __init__(self, count_moves):
        self.table_of_moves = []
        row = ['draw'] + count_moves // 2 * ['lose'] + count_moves // 2 * ['win']
        for i in range(count_moves):
            self.table_of_moves.append([sys.argv[i]] + row)
            row.insert(0, row.pop())

    def create_help_table(self):
        self.help_table = PrettyTable()
        self.help_table.field_names = ['Move'] + sys.argv
        self.help_table.add_rows(self.table_of_moves)


class MovePC:

    def __init__(self, count_moves):
        self.move = random.randint(1, count_moves)
        self.key = secrets.token_hex()
        self.hmac = hmac.new(self.key.encode(), str(self.move).encode(), hashlib.sha3_256)


def main():


    def create_main_menu():
        menu = 'Main menu:\n' \
               '1 - play\n' \
               "0 - exit\n" \
               "? - help"
        return menu

    def create_play_menu():
        menu = 'Game:\n'
        for i, el in enumerate(sys.argv):
            menu += str(i + 1) + ' - ' + el + '\n'
        menu += "0 - go to the main menu\n" \
                "? - help"
        return menu

    def create_menu_choice():
        print('1 - Yes, continue to play')
        print('0 - No, go to main menu')
        symbol = input()
        while symbol != '0' and symbol != '1':
            print('There is no such item on the menu. Re-enter')
            symbol = input()
        return symbol


    def create_table_menu():
        if not hasattr(TableRules, "help_table"):
            table.create_help_table()
        return table.help_table

    def create_player_selection():
        symbol = input()
        while not ((len(symbol) <= count_moves // 10 + 1 and symbol.isdigit()) or symbol == '?'):
            print('There is no such item on the menu. Re-enter')
            symbol = input()
        return symbol

    def play():
        move_pc = MovePC(count_moves)
        print(create_play_menu())
        print('HMAC\n' + move_pc.hmac.hexdigest())
        print("Enter the move number or\nthe rank '?' to bring up the help table")
        symbol = create_player_selection()
        output_line = ''
        if symbol == '0':
            output_line = create_main_menu()
        elif symbol == '?':
            output_line = create_table_menu()
        elif 0 < int(symbol) <= count_moves:
            output_line = f"Your move: {sys.argv[int(symbol) - 1]}\n" \
                          f"Computer move: {sys.argv[move_pc.move - 1]}\n"
            output_line += pick_winner(int(symbol), move_pc.move, table.table_of_moves)
            output_line += ('HMAC Key\n' + move_pc.key)
            return output_line
        return output_line

    def pick_winner(move_player, move_pc, table_of_moves):
        if table_of_moves[move_player - 1][move_pc] == "draw":
            return "You draw!\n"
        return "You win!\n" if table_of_moves[move_player - 1][move_pc] == "win" else "You lose!\n"

    sys.argv.pop(0)
    count_moves = len(sys.argv)

    if count_moves < 3:
        print("The count of moves must be more than 3")
        print("It`s right:\nrock paper scissors\n"
              "Or:\nstone scissors paper lizard Spock\n"
              "It isn`t right:\nrock paper")
        return
    elif count_moves % 2 == 0:
        print("The count of moves must be odd.")
        print("It`s right:\nrock paper scissors\n"
              "Or:\nstone scissors paper lizard Spock\n"
              "It isn`t right:\nrock paper")
        return
    elif len(set(sys.argv)) < count_moves:
        print("Moves must not be repeated.")
        print("It`s right:\nrock paper scissors\n"
              "It isn`t right:\nrock rock paper")
        return


    table = TableRules(count_moves)
    print(create_main_menu())
    symbol = create_player_selection()
    print("Enter the number in the menu to go, or\nthe rank '?' to bring up the help table")

    while symbol != '0':
        if symbol == '1':
            print(play())
            print("Do you want to repeat?")
            symbol = create_menu_choice()
        elif symbol == '?':
            print(create_table_menu())
            print("Enter any string to return to main menu")
            symbol = input()
            symbol = '0'
        if symbol == "0":
            print(create_main_menu())
            symbol = create_player_selection()



main()
