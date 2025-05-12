def board():
    import pygame

    #initialize pygame
    pygame.init()

    screen_width = 400
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chessboard")
    
    #colors
    white =(240, 217, 181)
    black = (181, 136, 99)
    hightligh = (130,180,150)

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

    selected_square = None

    running = True
    selected_piece_pos = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #implement the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                clicked_col = mouse_x // square_size
                clicked_row = mouse_y // square_size
                selected_square = (clicked_row, clicked_col)

                print(f"cliked on row: {clicked_row}, coulumn: {clicked_col}")

                #check to see if we clicked on a piece
                if selected_piece_pos is None:
                    piece = board[clicked_row][clicked_col]
                    if piece != ' ':
                        selected_piece_pos = (clicked_row, clicked_col)
                        print(f"selected piece at: {selected_piece_pos}")
                else:
                    start_row, start_col = selected_piece_pos
                    end_row, end_col = clicked_row, clicked_col
                        
                    #moves piece if a new square is clicked
                    if(start_row, start_col) != (end_row, end_col):
                        piece_to_move = board[start_row][start_col]
                        board[start_row][start_col] = ' '
                        board[end_row][end_col] = piece_to_move
                        selected_piece_pos = None
                        print(f"Moved{piece_to_move} from {(start_row, start_col)} to {(end_row, end_col)}")
                    else:
                        #clicked on the same square, deselect
                        selected_piece_pos = None
                        print("Deselected piece.")
        #Draw the board
        for row in range(8):
            for col in range(8):
                color = white if (row+col) % 2 == 0 else black
                pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

                piece = board[row][col]
                if piece != ' ':
                    piece_image = pygame.transform.scale(piece_images[piece], (square_size, square_size))
                    screen.blit(piece_image, (col * square_size, row * square_size))
        #highlight the selected square
        if selected_square:
            selected_row, selected_col = selected_square
            highlight_color = (255,255,0)
            highlight_thickness = 3
            highlight_rect = pygame.Rect(
                selected_col * square_size,
                selected_row * square_size,
                square_size,
                square_size
            )
            pygame.draw.rect(screen, highlight_color, highlight_rect, highlight_thickness)
            
            

        pygame.display.flip()

    pygame.quit()


board()