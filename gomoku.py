#3.a)
def is_sq_in_board(board,y,x):
    if(len(board) > y and y >= 0 and len(board[0]) > x and x >= 0):
        return True
    return False


def is_empty(board): #1st written function
    for a in board:
        for b  in a:
            if(b != " "):
                 return False
    return True
    
def is_bounded(board, y_end, x_end, length, d_y, d_x): #2nd written function
    if(y_end + d_y <= len(board) - 1 
       and y_end + d_y >= 0
       and x_end + d_x <= len(board) - 1 
       and x_end + d_x >= 0
       and y_end - length * d_y  >= 0
       and y_end - length * d_y <= len(board)-1
       and x_end - length * d_x  >= 0
       and x_end - length * d_x <= len(board)-1): #Eliminates out of bound cases
        if (board[y_end + d_y][x_end + d_x] != " " and board[y_end - length * d_y ][x_end - length * d_x ] != " " ): #Stone cannot be placed on both end
            return "CLOSED"
        elif (board[y_end + d_y][x_end + d_x] == " " and board[y_end - length * d_y ][x_end - length * d_x ] == " " ): #Stone can be placed on both end
            return "OPEN"
        else: #Stone can be placed on one end only
            return "SEMIOPEN"
    else: #out of bound (Error 1: Could be semiopen!!!)
        if(y_end + d_y <= len(board) - 1 
       and y_end + d_y >= 0
       and x_end + d_x <= len(board) - 1 
       and x_end + d_x >= 0):
            if board[y_end + d_y][x_end + d_x] == " ":
                return "SEMIOPEN"
            else:
                return "CLOSED"
        elif(y_end - length * d_y  >= 0
       and y_end - length * d_y <= len(board)-1
       and x_end - length * d_x  >= 0
       and x_end - length * d_x <= len(board)-1):
            if board[y_end - length * d_y][x_end - length * d_x] == " ":
                return "SEMIOPEN"
            else:
                return "CLOSED"
        else:
            return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    y_end = y_start + (length-1) * d_y
    x_end = x_start + (length-1) * d_x
    while (y_end <= len(board) - 1 
           and y_end >= 0 
           and x_end <= len(board) - 1 
           and x_end >= 0): #Check for open or semiopen until coordinates are out of bound
        
        is_same_col = True
        for i in range(length):
            if(board[y_start + i*d_y][x_start + i*d_x] != col):
                is_same_col = False
        
        y_start += d_y
        x_start += d_x
        y_end += d_y
        x_end += d_x
        
        if(is_same_col == False):
            continue
        else:
            ans = is_bounded(board,y_end-d_y,x_end-d_x,length,d_y,d_x)
            if(ans == "OPEN"):
                open_seq_count += 1
            elif(ans == "SEMIOPEN"):
                semi_open_seq_count += 1
    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    ####CHANGE ME   
    open_seq_count, semi_open_seq_count = 0, 0
    
    for i in range(len(board)):
        temp = detect_row(board,col,0,i,length,1,0) #all columns
        open_seq_count += temp[0]
        semi_open_seq_count += temp[1]
        temp = detect_row(board,col,i,0,length,0,1) #all rows
        open_seq_count += temp[0]
        semi_open_seq_count += temp[1]
        temp = detect_row(board,col,0,i,length,1,1) #left up down right upper tri
        open_seq_count += temp[0]
        semi_open_seq_count += temp[1]
        if(i != 0):
            temp = detect_row(board,col,i,0,length,1,1) #left up down right lower tri
            open_seq_count += temp[0]
            semi_open_seq_count += temp[1]
        temp = detect_row(board,col,0,i,length,1,-1) #right up down left upper tri
        open_seq_count += temp[0]
        semi_open_seq_count += temp[1]
        if(i != 0):
            temp = detect_row(board,col,i,len(board)-1,length,1,-1) #right up down left lower tri
            open_seq_count += temp[0]
            semi_open_seq_count += temp[1]
        
    return open_seq_count, semi_open_seq_count  

def search_max(board):
    max = 0
    move_y = 0
    move_x = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == " ":
                board[i][j] = "b"
                k = score(board)
                if k > max:
                    max = k
                    move_y = i
                    move_x = j
                board[i][j] = " "
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
    def check_line(line):
        for i in range(len(line) - 4):
            if all(cell == line[i] for cell in line[i:i+5]) and line[i] != ' ':
                return line[i]
        return False

    # Check rows
    for row in board:
        result = check_line(row)
        if result == 'w':
            return "White won"
        elif result == "b":
            return "Black won"

    # Check columns
    for col in range(len(board[0])):
        column = [board[row][col] for row in range(len(board))]
        result = check_line(column)
        if result == 'w':
            return "White won"
        elif result == "b":
            return "Black won"

    # Check diagonals
    for i in range(len(board) - 4):
        for j in range(len(board[0]) - 4):
            diagonal = [board[i + k][j + k] for k in range(5) if i + k < len(board) and j + k < len(board)]
            if(len(diagonal) == 5):
                result = check_line(diagonal)
            else:
                continue
            if result == 'w':
                return "White won"
            elif result == "b":
                return "Black won"

            another_diagonal = [board[i + k][j + 4 - k] for k in range(5) if i + k < len(board) and j + k < len(board)]
            if(len(another_diagonal) == 5):
                result = check_line(another_diagonal)
            else:
                continue
            if result == 'w':
                return "White won"
            elif result == "b":
                return "Black won"

    # Check for a draw
    if is_board_full(board):
        return "Draw"
    else:
        return "Continue playing"

def is_board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True



def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
    

        
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

#3.b)
def is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):
    c = 0
    for i in range(length):
        if(i == 0 and y_start - d_y >= 0 and x_start - d_x >= 0): #Detect if previous index in sequence is out of bound
            if(board[y_start - d_y][x_start - d_x] == col): #6-connected stones is not a win
                return False
        if(i == length-1 and y_start + d_y <= len(board) - 1 and x_start + d_x <= len(board) - 1): #Detect if following index in sequence is out of bound
            if(board[y_start + d_y][x_start + d_x] == col): #6-connected stones is not a win
                return False
        if(y_start < 0 or x_start < 0 or y_start > len(board)-1 or x_start > len(board)-1): #Check for out of bounds in every index
            break
        else:
             if(board[y_start][x_start] == col):
                c += 1
                y_start += d_y
                x_start += d_x
    if(c == length):
        return True
    return False
        
            


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


  
            
if __name__ == '__main__':

    play_gomoku(8)