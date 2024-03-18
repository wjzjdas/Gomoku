import importlib
import gomoku
importlib.reload(gomoku)


def test_search_max():
    board = gomoku.make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    gomoku.put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    gomoku.put_seq_on_board(board, y, x, d_y, d_x, length, col)
    gomoku.print_board(board)
    if gomoku.search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")


def test_detect_row():
    board = gomoku.make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    gomoku.put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    gomoku.print_board(board)
    if gomoku.detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE 1 for detect_row PASSED")
    else:
        print("TEST CASE 1 for detect_row FAILED")



    board = gomoku.make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 2
    gomoku.put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    gomoku.print_board(board)
    if gomoku.detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE 2 for detect_row PASSED")
    else:
        print("TEST CASE 2 for detect_row FAILED")


if __name__ == '__main__':
    test_search_max()
    test_detect_row()