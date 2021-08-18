from helper import title, winning_states
from random import choice
import time
import copy


def display_board(board):
    for el in board:
        print('—————————————')
        print(f'| {el[0]} | {el[1]} | {el[2]} |')
    print('—————————————')


def transform_board(board, mark):
    temp = copy.deepcopy(board)
    for row in temp:
        for col in enumerate(row):
            if col[1] == mark:
                row[col[0]] = True
    return temp


def player_turn(board):
    while True:
        try:
            move = int(input('Enter Board Number 1 - 9: ')) - 1
            if move not in range(9):
                print('Please enter a number from 1 - 9...')
                continue
            elif board[move // 3][move % 3] != ' ':
                print('That box is already taken...')
                continue
        except ValueError:
            print('Please enter a number...')
            continue
        break
    return move


def computer_turn(board):
    # Check if Computer can win
    if (move := check_almost_win(board, 'X')) != None:
        print('computer')
        return move

    # Check if Player can win
    if (move := check_almost_win(board, 'O')) != None:
        print('player')
        return move

    # Check if center or corner is empty
    corners = []
    if board[1][1] == ' ':
        return 4
    if board[0][0] == ' ':
        corners.append(0)
    if board[0][2] == ' ':
        corners.append(2)
    if board[2][0] == ' ':
        corners.append(6)
    if board[2][2] == ' ':
        corners.append(8)
    if corners:
        return choice(corners)

    return choice([board[i].index(' ') + 3 * i for i in range(3) if ' ' in board[i]])


def check_almost_win(board, mark):
    board = transform_board(board, mark)
    transposed_board = list(map(list, zip(*board)))

    for i in range(3):
        if board[i] in winning_states:
            return board[i].index(' ') + i * 3
        if transposed_board[i] in winning_states:
            return 3 * transposed_board[i].index(' ') + i

    if (check_board := [board[0][0], board[1][1], board[2][2]]) in winning_states:
        return [0, 4, 8][check_board.index(' ')]
    if (check_board := [board[0][2], board[1][1], board[0][2]]) in winning_states:
        return [2, 4, 6][check_board.index(' ')]


def check_win(board, mark):
    board = transform_board(board, mark)
    transposed_board = list(map(list, zip(*board)))

    for i in range(3):
        if board[i] == [True, True, True]:
            return True
        if transposed_board[i] == [True, True, True]:
            return True

    if [board[0][0], board[1][1], board[2][2]] == [True, True, True]:
        return True
    if [board[0][2], board[1][1], board[2][0]] == [True, True, True]:
        return True

    return False


def display_computer_turn():
    print('\n\nComputer\'s Turn', end='')
    time.sleep(.5)
    print('.', end='', flush=True)
    time.sleep(.5)
    print('.', end='', flush=True)
    time.sleep(.5)
    print('.', flush=True)
    time.sleep(.5)


if __name__ == "__main__":
    # Initial Board
    print('\n', title, '\n\n')
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    turn = 1
    print('Box Numbers:')
    display_board([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    time.sleep(2)

    display_computer_turn()
    board[choice([0,1,2])][choice([0,1,2])] = 'X'
    display_board(board)

    while turn < 5:
        # Ask user for input (move)
        print('\n\nPlayer\'s Turn...')
        move = player_turn(board)
        board[move // 3][move % 3] = 'O'
        display_board(board)
        if check_win(board, 'O'):
            print('Congratulations, You Win!')
            break
        
        display_computer_turn()
        move = computer_turn(board)
        board[move // 3][move % 3] = 'X'
        display_board(board)
        if check_win(board, 'X'):
            print('Computer wins!')
            break

        turn += 1
    else:
        print('It\'s a tie!')