def board():
    import pygame

    pygame.init()

    screen_width = 400
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chessboard")
    
    #colors
    white =(240, 217, 181)
    black = (181, 136, 99)

    #load pieceimages
    piece_images = {
        'p': pygame.image.load('Chess/assets/black_pawn.png'),
        'r': pygame.image.load('Chess/assets/black_pawn.png'),
        'n': pygame.image.load('Chess/assets/black_knight.png'),
        'b': pygame.image.load('Chess/assets/black_bishop.png'),
        'q': pygame.image.load('Chess/assets/black_pawn.png'),
        'k': pygame.image.load('Chess/assets/black_pawn.png'),
        'P': pygame.image.load('Chess/assets/black_pawn.png'),
        'R': pygame.image.load('Chess/assets/black_pawn.png'),
        'N': pygame.image.load('Chess/assets/black_pawn.png'),
        'B': pygame.image.load('Chess/assets/black_pawn.png'),
        'Q': pygame.image.load('Chess/assets/black_pawn.png'),
        'K': pygame.image.load('Chess/assets/black_pawn.png')
    }
    

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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                clicked_col = mouse_x // square_size
                clicked_row = mouse_y // square_size

                print(f"cliked on row: {clicked_row}, coulumn: {clicked_col}")

        #Draw the board
        for row in range(8):
            for col in range(8):
                color = white if (row+col) % 2 == 0 else black
                pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

                piece = board[row][col]
                if piece != ' ':
                    piece_image = pygame.transform.scale(piece_images[piece], (square_size, square_size))
                    screen.blit(piece_image, (col * square_size, row * square_size))
    
        pygame.display.flip()

    pygame.quit()


board()