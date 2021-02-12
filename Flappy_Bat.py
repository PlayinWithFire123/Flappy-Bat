# Importing pygame functions and the random function
import pygame
import random

# Initializing pygame and font
pygame.init()
pygame.font.init()

# These are all of the constants, which are variables that don't change
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 504 + 111
GROUND_Y = 504
BAT_START_X = 418
BAT_START_Y = 200
PIPE_START_X = 1100
PIPE_WIDTH = 96
PIPE_HEIGHT = 594
PIPE_GAP = 158
TERMINAL_VELOCITY = 5.3
GRAVITY = 0.145
FLAP_SPEED = 20 
BAT_JUMP = -4.7
PIPE_SPAWN = 800

# These lines make the window appear and give it the title of "Flappy Bat"
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bat")

# These load in my images and assign them names, as well as scaling up a few images
# and flipping the pipe to make the top pipe
bat_up = pygame.image.load('Bat up.png')
bat_up = pygame.transform.scale(bat_up, (16 * 4, 15 * 4))
bat_down = pygame.image.load('Bat down.png')
bat_down = pygame.transform.scale(bat_down, (16 * 4, 10 * 4))
background = pygame.image.load('Background.png')
pipe_up = pygame.image.load('Pipe.png')
pipe_down = pygame.transform.flip(pipe_up, False, True)
pipe_up = pygame.transform.scale(pipe_up, (PIPE_WIDTH, PIPE_HEIGHT))
pipe_down = pygame.transform.scale(pipe_down, (PIPE_WIDTH, PIPE_HEIGHT))
font = pygame.font.Font('Flappy_Font.ttf', 50)
smallFont = pygame.font.Font('Flappy_Font.ttf', 20)
restart = pygame.image.load('Restart.png')
restart = pygame.transform.scale(restart, (96, 96))
ground = pygame.image.load('Ground.png')

# This is where the audio is loaded, but in repl audio cannot be played,
# so I can turn it on or off
audioSupported = True
if audioSupported:
    wing = pygame.mixer.Sound('wing.wav')
    swoosh = pygame.mixer.Sound('swoosh.wav')
    point = pygame.mixer.Sound('point.wav')
    hit = pygame.mixer.Sound('hit.wav')

# These are variables for my bat, the bat_x variable is not actually necessary
bat_velocity = 0
bat_x = BAT_START_X
bat_y = BAT_START_Y

# These booleans and integers are just more variables for starting the game, 
# counting the score, animating the bat, displaying starting messages,
# and allowing the game to restart
running = True
gameStarted = False
batAlive = True
firstStart = True
frameCount = 1
score = 0
highScore = 0

# This is a function that includes a nested list to set up the creation of the pipes
# including the image, x, y, and hitbox
def newPipe():
    gapStart = random.randint(75, 290)
    return [[pipe_up, pygame.Rect(PIPE_START_X, gapStart + PIPE_GAP, PIPE_WIDTH, PIPE_HEIGHT)],
            [pipe_down, pygame.Rect(PIPE_START_X, gapStart - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)]]

# This creates the first pipe
pipes = newPipe()

# This is the main gameplay loop
while running:
    # Draws the background into the window and tracks the mouse position
    screen.blit(background, (0, 0))
    mouse = pygame.mouse.get_pos()

    # This makes the bat fall with gravity and limits gravitys 
    # effect by terminal velocity
    if batAlive:
        if gameStarted:
            if bat_velocity < TERMINAL_VELOCITY:
                bat_velocity += GRAVITY

        # This makes it so bat velocity affects the bats y location
        bat_y += bat_velocity

        # This if statement makes it so the game ends when the 
        # bottom of the bat touches the ground
        if bat_y > GROUND_Y - 15 * 4 and batAlive:
            batAlive = False
            if audioSupported:
                hit.play()

        # This makes it so the bat cannot fly over the pipes
        # but does not die when it goes into the sky
        if bat_y < -75:
            bat_y = -75

        # This is a variable I use to move the ground and animate
        # the bat
        frameCount += 1

    # This is the animation for the bat. It uses a math equation to see 
    # whenever the frame count counts 20 more ticks to see when the bat 
    # should be in wings up or wings down
    if (frameCount // FLAP_SPEED) % 2 == 0: 
        screen.blit(bat_up, (bat_x, bat_y))
        flappy_bat_rect = pygame.Rect(bat_x, bat_y, 13 * 4, 10 * 4)
    else:
        screen.blit(bat_down, (bat_x, bat_y + 20))
        flappy_bat_rect = pygame.Rect(bat_x, bat_y + 20, 13 * 4, 10 * 4)

    # This is the brains behind the pipes
    if gameStarted:
        # The booleans make it so the pipes don't spawn exponentially
        spawnPipe = False
        passPipe = False
        # This is where the newPipe function comes in. 
        # This draws a pipe and then moves it left
        for pipe in pipes:
            screen.blit(pipe[0], pipe[1])
            if batAlive:
                pipe[1].x -= 2
            # This spawns in a pipe when a pipe crosses the spawn line called PIPE_SPAWN
            if pipe[1].x == PIPE_SPAWN:
                spawnPipe = True
            # This is for the score and checks whenever a pipe passes the bat
            if pipe[1].x == bat_x:
                passPipe = True
            # This is the collision detection, and detects whenever a pipe hits the bat
            # as well as playing the sound for it
            if pipe[1].colliderect(flappy_bat_rect) and batAlive:
                batAlive = False
                hit.play()

        # This spawns in new pipes
        if spawnPipe and batAlive:
            pipes += newPipe()

        # This increases the score when passPipe is true,
        # plays the point sound, and keeps track of the high score
        if passPipe and batAlive:
            score += 1 
            if audioSupported:
                point.play()
            if score > highScore:
                highScore = score

        # This deletes pipes when they cross the screen
        if pipes[0][1].x < -PIPE_WIDTH:
            del pipes[0]
        
        # This draws in the score counter and the score and high score
        # counters that appear when you die
        if batAlive:
            screen.blit(font.render(str(score), False, (255, 255, 255)), (440, 50))
        else:
            screen.blit(font.render('Score: ' + str(score), False, (255, 255, 255)), (341, 50))
            screen.blit(font.render('Best: ' + str(highScore), False, (255, 255, 255)), (370, 100))
        
    screen.blit(ground, (-(2 * frameCount % 24), GROUND_Y))

    # This loop is for quitting out of the window and jumping up
    for event in pygame.event.get():
        # This if statement makes the game stop running whenever the window is closed
        if event.type == pygame.QUIT:
            running = False
        # This detects whenever the spacebar is pressed and makes the bat jump
        # and play the wing sound
        if event.type == pygame.KEYDOWN:
            if batAlive and event.key == pygame.K_SPACE:
                if audioSupported:
                    wing.play()
                gameStarted = True
                bat_velocity = BAT_JUMP
                firstStart = False

        # This detects whenever the mouse is pressed on the restart button area
        # during when the restart button is up, and restarts the game
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if batAlive == False and 450 - 48 <= mouse[0] <= 450 + 48 and 252 - 48 <= mouse[1] <= 252 + 48: 
                if audioSupported:
                    swoosh.play()
                bat_y = BAT_START_Y
                bat_velocity = 0
                pipes = newPipe()
                gameStarted = False
                batAlive = True
                score = 0 

    # This puts up the text at the start of the game that says 
    # 'Flappy Bat' and 'Press space to start'
    if firstStart:
        screen.blit(font.render('Flappy Bat', False, (255, 255, 255)), (320, 120))
        screen.blit(smallFont.render('Press space to start', False, (255, 255, 255)), (350, 320))

    # This tests when to draw the restart button
    if batAlive == False:
        screen.blit(restart, (450 - 48, 252 - 48)) 
    
    # This is a necessary function for the display to actually work for pygame
    pygame.display.flip()

# This prints your all time high score once you are done playing the game
print('Your high score was', highScore)
