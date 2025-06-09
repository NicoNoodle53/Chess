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
                            possible_moves_for_selected = get_king_moves(clicked_row, clicked_col, board, current_turn)
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

                        # Execute the move
                        board[end_row][end_col] = piece_to_move
                        board[start_row][start_col] = ' '

                        selected_piece_pos = None  # Deselect after successful move
                        possible_moves_for_selected = [] # Clear possible moves

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
                            possible_moves_for_selected = get_king_moves(clicked_row, clicked_col, board, current_turn)
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

def get_king_moves(row, col, board, current_player_color):
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
    return moves

def get_highlight_rect(row, col, size):
    highlight_rect = pygame.Rect(col * size,row * size, size, size)
    return highlight_rect

def get_piece_color(piece_symbol):
    #Returns 'white', 'black', or None if empty.
    if piece_symbol == ' ':
        return None
    return 'white' if piece_symbol.isupper() else 'black'
        

main()