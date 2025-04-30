def board():
    import pygame

    pygame.init()

    screen_width = 400
    screen_height = 480
    
    

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