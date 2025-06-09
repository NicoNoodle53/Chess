import pygame
#initialize pygame
pygame.init()


def main():
    current_turn = "white"
    screen_width = 480
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chessboard")

    #colors
    white =(240, 217, 181)
    black = (181, 136, 99)
    highlight_color = (255, 255, 0) # Yellow for highlight
    possible_move_color = (0, 255, 0) # Green for possible moves (or blend with yellow)
    highlight_thickness = 5

    #load pieceimages
    piece_images = {
        'p': pygame.image.load('Chess/assets/black_pawn.png'),
        'r': pygame.image.load('Chess/assets/black_rook.png'),
        'n': pygame.image.load('Chess/assets/black_knight.png'),
        'b': pygame.image.load('Chess/assets/black_bishop.png'),
        'q': pygame.image.load('Chess/assets/black_queen.png'),
        'k': pygame.image.load('Chess/assets/black_king.png'),
        'P': pygame.image.load('Chess/assets/white_pawn.png'),
        'R': pygame.image.load('Chess/assets/white_rook.png'),
        'N': pygame.image.load('Chess/assets/white_knight.png'),
        'B': pygame.image.load('Chess/assets/white_bishop.png'),
        'Q': pygame.image.load('Chess/assets/white_queen.png'),
        'K': pygame.image.load('Chess/assets/white_king.png')
    }

    # set up board
    board = [
        ['r' ,'n' ,'b' ,'q' ,'k' ,'b' ,'n' ,'r'], #Rank 8
        ['p' ,'p' ,'p' ,'p' ,'p' ,'p' ,'p' ,'p'], #Rank 7
        [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' '], #Rank 6
        [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' '], #Rank 5
        [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' '], #Rank 4
        [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' '], #Rank 3
        ['P' ,'P' ,'P' ,'P' ,'P' ,'P' ,'P' ,'P'], #Rank 2
        ['R' ,'N' ,'B' ,'Q' ,'K' ,'B' ,'N' ,'R']  #Rank 1
    ]

    square_size = screen_width // 8
    for key, img in piece_images.items():
        piece_images[key] = pygame.transform.scale(img, (square_size, square_size))

    # --- Castling flags ---
    # These flags track if the king or rooks have moved from their initial positions.
    # A moved king or rook prevents castling.
    has_moved = {
        'white_king': False,
        'white_rook_kingside': False, # (7, 7)
        'white_rook_queenside': False, # (7, 0)
        'black_king': False,
        'black_rook_kingside': False, # (0, 7)
        'black_rook_queenside': False, # (0, 0)
    }

    current_turn = 'white' # 'white' or 'black'
    selected_piece_pos = None # (row, col) of the currently selected piece
    possible_moves_for_selected = [] # List of (row, col) tuples for legal moves
    running = True
    selected_piece_pos = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                clicked_col = mouse_x // square_size
                clicked_row = mouse_y // square_size
                clicked_square_coords = (clicked_row, clicked_col)

                print(f"Clicked on row: {clicked_row}, column: {clicked_col}")

                piece_on_clicked_square = board[clicked_row][clicked_col]
                piece_color_on_clicked_square = get_piece_color(piece_on_clicked_square)

                if selected_piece_pos is None:
                    # No piece currently selected. Try to select one.
                    if piece_on_clicked_square != ' ' and piece_color_on_clicked_square == current_turn:
                        selected_piece_pos = clicked_square_coords
                        print(f"Selected {piece_on_clicked_square} at {selected_piece_pos}")

                        # Calculate and store possible moves for the selected piece
                        piece_type = piece_on_clicked_square.lower() # 'p', 'r', 'b', etc.
                        if piece_type == 'p':
                            possible_moves_for_selected = get_pawn_moves(clicked_row, clicked_col, board, current_turn)
                        elif piece_type == 'r':
                            possible_moves_for_selected = get_rook_moves(clicked_row, clicked_col, board, current_turn)
                        elif piece_type == 'n':
                            possible_moves_for_selected = get_knight_moves(clicked_row, clicked_col, board, current_turn)
                        elif piece_type == 'b':
                            possible_moves_for_selected = get_bishop_moves(clicked_row, clicked_col, board, current_turn)
                        elif piece_type == 'q':
                            possible_moves_for_selected = get_queen_moves(clicked_row, clicked_col, board, current_turn)
                        elif piece_type == 'k':
                            # Pass 'has_moved' to the king moves function
                            possible_moves_for_selected = get_king_moves(clicked_row, clicked_col, board, current_turn, has_moved)
                        print(f"Possible moves: {possible_moves_for_selected}")
                    else:
                        # Clicked on an empty square or an opponent's piece when nothing selected
                        print("No piece to select or not your turn.")

                else:
                    # A piece is already selected. This click is either a move or a deselection.
                    start_row, start_col = selected_piece_pos
                    piece_to_move = board[start_row][start_col] # Get the piece that was originally selected

                    if clicked_square_coords == selected_piece_pos:
                        # Clicked on the same square as the selected piece, deselect it
                        selected_piece_pos = None
                        possible_moves_for_selected = [] # Clear possible moves
                        print("Deselected piece.")
                    elif clicked_square_coords in possible_moves_for_selected:
                        # VALID MOVE: The clicked square is one of the calculated possible moves
                        end_row, end_col = clicked_square_coords

                        # --- Handle Castling Move Execution ---
                        is_castling_move = False
                        # Check if it's a king move of two squares horizontally
                        if piece_to_move.lower() == 'k' and abs(start_col - end_col) == 2:
                            # It's a castling attempt
                            is_castling_move = True

                            # Determine which side castling
                            if end_col == start_col + 2: # Kingside castling (e.g., e1 to g1)
                                rook_start_col = 7
                                rook_end_col = 5
                                if current_turn == 'white':
                                    has_moved['white_rook_kingside'] = True
                                else:
                                    has_moved['black_rook_kingside'] = True
                            elif end_col == start_col - 2: # Queenside castling (e.g., e1 to c1)
                                rook_start_col = 0
                                rook_end_col = 3
                                if current_turn == 'white':
                                    has_moved['white_rook_queenside'] = True
                                else:
                                    has_moved['black_rook_queenside'] = True

                            # Move the rook
                            board[start_row][rook_end_col] = board[start_row][rook_start_col]
                            board[start_row][rook_start_col] = ' '


                        # Execute the king's move (or regular piece move)
                        board[end_row][end_col] = piece_to_move
                        board[start_row][start_col] = ' '

                        # Update has_moved flags for the king
                        if piece_to_move == 'K':
                            has_moved['white_king'] = True
                        elif piece_to_move == 'k':
                            has_moved['black_king'] = True
                        # Update has_moved flags for rooks if they moved via regular move
                        # This prevents castling after a rook has moved manually
                        elif piece_to_move == 'R':
                            if (start_row, start_col) == (7, 7): has_moved['white_rook_kingside'] = True
                            if (start_row, start_col) == (7, 0): has_moved['white_rook_queenside'] = True
                        elif piece_to_move == 'r':
                            if (start_row, start_col) == (0, 7): has_moved['black_rook_kingside'] = True
                            if (start_row, start_col) == (0, 0): has_moved['black_rook_queenside'] = True


                        selected_piece_pos = None  # Deselect after successful move
                        possible_moves_for_selected = [] # Clear possible moves

                        if is_castling_move:
                             print(f"Castled {current_turn} king from {(start_row, start_col)} to {(end_row, end_col)}")
                        else:
                            print(f"Moved {piece_to_move} from {(start_row, start_col)} to {(end_row, end_col)}")

                        # Switch turns
                        current_turn = 'black' if current_turn == 'white' else 'white'
                        print(f"It's now {current_turn}'s turn.")
                    elif piece_color_on_clicked_square == current_turn:
                        # Clicked on another *one of your own* pieces (while one was selected)
                        # Switch selection to the new piece
                        selected_piece_pos = clicked_square_coords
                        print(f"Switched selection to {piece_on_clicked_square} at {selected_piece_pos}")

                        # Recalculate possible moves for the newly selected piece
                        piece_type = piece_on_clicked_square.lower()
                        if piece_type == 'p':
                            possible_moves_for_selected = get_pawn_moves(clicked_row, clicked_col, board, current_turn)
                        elif piece_type == 'r':
                            possible_moves_for_selected = get_rook_moves(clicked_row, clicked_col, board, current_turn)
                        elif piece_type == 'n':
                            possible_moves_for_selected = get_knight_moves(clicked_row, clicked_col, board, current_turn)
                        elif piece_type == 'b':
                            possible_moves_for_selected = get_bishop_moves(clicked_row, clicked_col, board, current_turn)
                        elif piece_type == 'q':
                            possible_moves_for_selected = get_queen_moves(clicked_row, clicked_col, board, current_turn)
                        elif piece_type == 'k':
                            # Pass 'has_moved' to the king moves function
                            possible_moves_for_selected = get_king_moves(clicked_row, clicked_col, board, current_turn, has_moved)
                        print(f"Possible moves: {possible_moves_for_selected}")
                    else:
                        # Clicked on an invalid square (opponent's piece not a target, or empty square not in possible moves)
                        print("Invalid move or clicked opponent's piece.")
                        # Keep the piece selected, or deselect? Usually deselect for simplicity
                        selected_piece_pos = None
                        possible_moves_for_selected = []


        # --- DRAWING BOARD, PIECES, AND HIGHLIGHTS ---
        screen.fill(white) # Fill background to clear previous frame

        for row in range(8):
            for col in range(8):
                # Draw board squares
                color = white if (row + col) % 2 == 0 else black
                pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

                # Draw pieces
                piece_symbol = board[row][col]
                if piece_symbol != ' ':
                    screen.blit(piece_images[piece_symbol], (col * square_size, row * square_size))

        # Highlight the selected piece's square
        if selected_piece_pos:
            selected_row, selected_col = selected_piece_pos
            highlight_rect = get_highlight_rect(selected_row, selected_col, square_size)
            pygame.draw.rect(screen, highlight_color, highlight_rect, highlight_thickness)

        # Highlight possible move squares
        for move_row, move_col in possible_moves_for_selected:
            # You could draw a different highlight color or a circle
            move_rect = get_highlight_rect(move_row, move_col, square_size)
            pygame.draw.rect(screen, possible_move_color, move_rect, highlight_thickness)
            # Or draw a circle in the middle:
            # center_x = move_col * square_size + square_size // 2
            # center_y = move_row * square_size + square_size // 2
            # pygame.draw.circle(screen, possible_move_color, (center_x, center_y), square_size // 4)


        pygame.display.flip()

    pygame.quit()


def is_valid_square(row,col):
    return 0 <= row < 8 and 0 <= col < 8

def get_pawn_moves(row, col, board, current_player_color):
    moves = []
    piece = board[row][col]

    # Define direction based on color
    direction = -1 if current_player_color == 'white' else 1

    # Forward move (1 square)
    new_row = row + direction
    if is_valid_square(new_row, col) and board[new_row][col] == ' ':
        moves.append((new_row, col))

        # Initial two-square move
        if (current_player_color == 'white' and row == 6) or \
           (current_player_color == 'black' and row == 1):
            new_row_two = row + 2 * direction
            if is_valid_square(new_row_two, col) and board[new_row_two][col] == ' ':
                moves.append((new_row_two, col))

    # Captures (diagonal)
    for dc in [-1, 1]: # -1 for left diagonal, 1 for right diagonal
        capture_row, capture_col = row + direction, col + dc
        if is_valid_square(capture_row, capture_col):
            target_piece = board[capture_row][capture_col]
            if target_piece != ' ' and get_piece_color(target_piece) != current_player_color:
                moves.append((capture_row, capture_col))

    # TODO: Add En Passant and Pawn Promotion logic later
    return moves

def get_rook_moves(row, col, board, current_player_color):
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    for dr, dc in directions:
        for i in range(1, 8): # Iterate through squares in a direction
            new_row, new_col = row + dr * i, col + dc * i

            if not is_valid_square(new_row, new_col):
                break # Off board

            target_piece = board[new_row][new_col]
            target_color = get_piece_color(target_piece)

            if target_piece == ' ': # Empty square
                moves.append((new_row, new_col))
            elif target_color != current_player_color: # Opponent's piece (capture)
                moves.append((new_row, new_col))
                break # Stop after capture, cannot move through opponent's piece
            else: # Your own piece (blocked)
                break
    return moves

def get_bishop_moves(row, col, board, current_player_color):
    moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)] # Diagonals

    for dr, dc in directions:
        for i in range(1, 8):
            new_row, new_col = row + dr * i, col + dc * i

            if not is_valid_square(new_row, new_col):
                break

            target_piece = board[new_row][new_col]
            target_color = get_piece_color(target_piece)

            if target_piece == ' ':
                moves.append((new_row, new_col))
            elif target_color != current_player_color:
                moves.append((new_row, new_col))
                break
            else:
                break
    return moves

def get_queen_moves(row, col, board, current_player_color):
    # Queen moves are a combination of Rook and Bishop moves
    return get_rook_moves(row, col, board, current_player_color) + \
           get_bishop_moves(row, col, board, current_player_color)

def get_knight_moves(row, col, board, current_player_color):
    moves = []
    # All 8 possible L-shaped moves for a knight
    knight_offsets = [
        (2, 1), (2, -1), (-2, 1), (-2, -1), # Vertical 2, Horizontal 1
        (1, 2), (1, -2), (-1, 2), (-1, -2)  # Vertical 1, Horizontal 2
    ]

    for dr, dc in knight_offsets:
        new_row, new_col = row + dr, col + dc

        if is_valid_square(new_row, new_col):
            target_piece = board[new_row][new_col]
            target_color = get_piece_color(target_piece)

            if target_piece == ' ' or target_color != current_player_color:
                moves.append((new_row, new_col))
    return moves

def get_king_moves(row, col, board, current_player_color, has_moved):
    moves = []
    # All 8 squares around the king
    king_offsets = [
        (0, 1), (0, -1), (1, 0), (-1, 0), # Horizontal & Vertical
        (1, 1), (1, -1), (-1, 1), (-1, -1) # Diagonals
    ]

    for dr, dc in king_offsets:
        new_row, new_col = row + dr, col + dc

        if is_valid_square(new_row, new_col):
            target_piece = board[new_row][new_col]
            target_color = get_piece_color(target_piece)

            if target_piece == ' ' or target_color != current_player_color:
                moves.append((new_row, new_col))

    # --- Castling Logic ---
    king_row = row # Original row of the king
    king_col = col # Original column of the king

    # Determine king's original position based on color
    if current_player_color == 'white':
        king_original_row = 7
        king_moved_flag = has_moved['white_king']
        kingside_rook_moved_flag = has_moved['white_rook_kingside']
        queenside_rook_moved_flag = has_moved['white_rook_queenside']
        rook_kingside_char = 'R'
        rook_queenside_char = 'R'
    else: # black
        king_original_row = 0
        king_moved_flag = has_moved['black_king']
        kingside_rook_moved_flag = has_moved['black_rook_kingside']
        queenside_rook_moved_flag = has_moved['black_rook_queenside']
        rook_kingside_char = 'r'
        rook_queenside_char = 'r'

    # Castling is only possible if the king is on its original square
    # and has not moved previously.
    if king_moved_flag or (king_row != king_original_row or king_col != 4): # King must be on its starting square
        return moves # No castling if king has moved or is not on starting square

    # Check if king is currently in check
    if is_in_check(board, current_player_color):
        return moves # Cannot castle if king is in check

    # Kingside Castling
    # Check if kingside rook has moved AND is at its original position
    if not kingside_rook_moved_flag and board[king_original_row][7] == rook_kingside_char:
        # Check if squares between king and rook are empty
        if board[king_original_row][5] == ' ' and board[king_original_row][6] == ' ':
            # Check if king passes through or lands on an attacked square
            # King moves from (original_row, 4) to (original_row, 6)
            # Squares to check: (original_row, 4), (original_row, 5), (original_row, 6)
            can_castle_kingside = True
            for c in range(king_col, king_col + 3): # Check 4, 5, 6 (e.g., e1, f1, g1)
                # Temporarily create a board state for checking if the intermediate squares are attacked
                # This is important for "king does not pass through check" rule.
                temp_board = [row[:] for row in board] # Create a copy of the board
                if c == king_col + 2: # This is the destination square for the king
                    temp_board[king_original_row][c] = temp_board[king_original_row][king_col]
                    temp_board[king_original_row][king_col] = ' '
                elif c == king_col + 1: # This is the square the king passes through
                     temp_board[king_original_row][c] = temp_board[king_original_row][king_col]
                     temp_board[king_original_row][king_col] = ' '

                if is_square_attacked(king_original_row, c, temp_board, get_opposite_color(current_player_color)):
                    can_castle_kingside = False
                    break
            if can_castle_kingside:
                moves.append((king_original_row, 6)) # Add kingside castling move

    # Queenside Castling
    # Check if queenside rook has moved AND is at its original position
    if not queenside_rook_moved_flag and board[king_original_row][0] == rook_queenside_char:
        # Check if squares between king and rook are empty
        if board[king_original_row][1] == ' ' and \
           board[king_original_row][2] == ' ' and \
           board[king_original_row][3] == ' ':
            # Check if king passes through or lands on an attacked square
            # King moves from (original_row, 4) to (original_row, 2)
            # Squares to check: (original_row, 4), (original_row, 3), (original_row, 2)
            can_castle_queenside = True
            for c in range(king_col, king_col - 3, -1): # Check 4, 3, 2 (e.g., e1, d1, c1)
                # Temporarily create a board state for checking if the intermediate squares are attacked
                temp_board = [row[:] for row in board] # Create a copy of the board
                if c == king_col - 2: # This is the destination square for the king
                    temp_board[king_original_row][c] = temp_board[king_original_row][king_col]
                    temp_board[king_original_row][king_col] = ' '
                elif c == king_col - 1: # This is the square the king passes through
                    temp_board[king_original_row][c] = temp_board[king_original_row][king_col]
                    temp_board[king_original_row][king_col] = ' '

                if is_square_attacked(king_original_row, c, temp_board, get_opposite_color(current_player_color)):
                    can_castle_queenside = False
                    break
            if can_castle_queenside:
                moves.append((king_original_row, 2)) # Add queenside castling move
    # --- End Castling Logic ---

    return moves

def get_highlight_rect(row, col, size):
    highlight_rect = pygame.Rect(col * size,row * size, size, size)
    return highlight_rect

def get_piece_color(piece_symbol):
    #Returns 'white', 'black', or None if empty.
    if piece_symbol == ' ':
        return None
    return 'white' if piece_symbol.isupper() else 'black'

def get_opposite_color(color):
    return 'black' if color == 'white' else 'white'


# --- NEW FUNCTIONS FOR CHECK AND ATTACKED SQUARES (as provided before, but highlighting changes) ---
def find_king_position(board, color):
    king_char = 'K' if color == 'white' else 'k'
    for r in range(8):
        for c in range(8):
            if board[r][c] == king_char:
                return (r, c)
    return None # Should not happen in a valid game

def is_square_attacked(row, col, board, attacking_color):
    # 'attacking_color' is the color of the pieces that might be attacking the square (e.g., if checking for white king's safety, attacking_color would be 'black')
    opponent_color = 'black' if attacking_color == 'white' else 'white' # This is actually `attacking_color` itself for the checks below

    # Check for pawn attacks
    pawn_direction = 1 if attacking_color == 'white' else -1 # Pawns move "down" for white, "up" for black to attack
    pawn_char = 'P' if attacking_color == 'white' else 'p'
    if is_valid_square(row + pawn_direction, col - 1) and board[row + pawn_direction][col - 1] == pawn_char:
        return True
    if is_valid_square(row + pawn_direction, col + 1) and board[row + pawn_direction][col + 1] == pawn_char:
        return True

    # Check for knight attacks
    knight_offsets = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    knight_char = 'N' if attacking_color == 'white' else 'n'
    for dr, dc in knight_offsets:
        target_row, target_col = row + dr, col + dc
        if is_valid_square(target_row, target_col) and board[target_row][target_col] == knight_char:
            return True

    # Check for rook/queen (horizontal/vertical) attacks
    rook_queen_chars = ['R', 'Q'] if attacking_color == 'white' else ['r', 'q']
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        for i in range(1, 8):
            target_row, target_col = row + dr * i, col + dc * i
            if not is_valid_square(target_row, target_col):
                break
            target_piece = board[target_row][target_col]
            if target_piece != ' ':
                if target_piece in rook_queen_chars:
                    return True
                else: # Blocked by another piece, friendly or enemy
                    break
    # Check for bishop/queen (diagonal) attacks
    bishop_queen_chars = ['B', 'Q'] if attacking_color == 'white' else ['b', 'q']
    for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        for i in range(1, 8):
            target_row, target_col = row + dr * i, col + dc * i
            if not is_valid_square(target_row, target_col):
                break
            target_piece = board[target_row][target_col]
            if target_piece != ' ':
                if target_piece in bishop_queen_chars:
                    return True
                else: # Blocked
                    break

    # Check for king attacks (important for immediate vicinity)
    king_char = 'K' if attacking_color == 'white' else 'k'
    for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        target_row, target_col = row + dr, col + dc
        if is_valid_square(target_row, target_col) and board[target_row][target_col] == king_char:
            return True

    return False

def is_in_check(board, king_color):
    king_pos = find_king_position(board, king_color)
    if king_pos is None:
        return False # Should not happen

    # The color of the pieces that would be attacking the king
    attacking_color = get_opposite_color(king_color)
    return is_square_attacked(king_pos[0], king_pos[1], board, attacking_color)


main()