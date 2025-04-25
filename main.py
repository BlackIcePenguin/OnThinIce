import pygame as pg
import math

def draw_rect_alpha(surface, color, rect):
    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

# Pygame initial setup
pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption('On Thin Ice')
clock = pg.time.Clock()
framerate = 60
running = True

# Player definition variables
player_loc = pg.Vector2(0, 0)
player_spawn = pg.Vector2(0, 0)
player_x_velocity = 0
player_y_velocity = 0
player_angle = 0 # Keeps track of players direction angle to ensure character faces right way.
player_slide = False
player_state = 0 # 0 is initialization, 1 is alive, 2 is dead, 3 is winning, -1 is passing
slide_x_max = 0 # Keep relative distance consistent
slide_y_max = 0 # Keep relative distance consistent
slide_ticks = 0 # Ensure slides stops in 2 seconds
total_slides = 0 # Keeping score, will report num slides after level clear



# UI variables
menu_state = 1 # 0 returns to player, 1 is main menu, 2 stage select, 3 is pause menu, 4 is win screen, starts at 1
menu_select = 0 # 0,1,2 keeps track of where you are in the menu
stage_select = 0 # Keeps track of which art to load, 0 first level, never gets run until menus are done
font = pg.font.SysFont('Ink Free', 90, bold=True)
death_anim_count = 0 # Counter, makes death time take 1 second total
menu_input_lag = 0 # To keep the menu from feeling impossible to navigate

# Pygame image loads
# NOTE FOR COLORS: MADE IS MSPaint, Color tuples (R, G, B, A)
# Good terrain: light turquoise -> (153, 217, 234, 255)
# Bad terrain: indigo -> (63, 72, 204, 255)
# Win Location: Turquoise -> (0, 162, 232, 255)
player_loc_color = (153, 217, 234, 255)
# Image loadings
home_screen = pg.image.load('OnThinIceTitleScreen.png')
select_screen = pg.image.load('OnThinIceSelectScreen.png')
pause_screen = pg.image.load('OnThinIcePauseMenuCrop.png ')
level_clear = pg.image.load('OnThinIceLevelClear.png')
level_0 = pg.image.load('OnThinIceLevel0.png')
level_1 = pg.image.load('OnThinIceLevel1.png')
level_2 = pg.image.load('OnThinIceLevel2.png')
level_3 = pg.image.load('OnThinIceLevel3.png')
level_end = pg.image.load('OnThinIceLevelEnd.png')
player_still = pg.image.load('OnThinIcePlayerStill.png')
player_move = pg.image.load('OnThinIcePlayerMove.png')

current_stage_image = level_0.convert() # Bit redundant, code does not like not having this

while running:
    # Decrement input lag
    if menu_input_lag > 0:
        menu_input_lag -= 1

    # event runs
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    # ------------------------------------------------------------------------------------
    # Screen Initialization, setting up necessary values for initial start
    match menu_state:
        case 1: # Main Menu
            player_state = -1 # Keeps player logic from running
            screen.blit(home_screen, (0,0))
            # Selector State
            match menu_select: # Visual clarity, rest is all backend
                case 0:
                    # Yellow, (255, 255, 0, 20)
                    draw_rect_alpha(screen, (255, 255, 0, 80), (78, 588, 195, 95))
                case 1:
                    draw_rect_alpha(screen, (255, 255, 0, 80), (289, 588, 195, 95))
                case 2:
                    draw_rect_alpha(screen, (255, 255, 0, 80), (500, 588, 195, 95))
            keys = pg.key.get_pressed()  # Read when player input
            if keys[pg.K_a] and menu_input_lag == 0:
                menu_input_lag = 10
                if menu_select == 0:
                    menu_select = 2
                else:
                    menu_select -= 1
            elif keys[pg.K_d] and menu_input_lag == 0:
                menu_input_lag = 10
                if menu_select == 2:
                    menu_select = 0
                else:
                    menu_select += 1
            if keys[pg.K_SPACE] and menu_input_lag == 0:
                match menu_select:
                    case 0:
                        player_state = 0 # Starts level startup case
                        menu_state = 0 # Disables menu case
                        stage_select = 0 # Loads first level
                        pass
                    case 1:
                        menu_input_lag = 10
                        menu_state = 2
                        menu_select = 0
                    case 2:
                        break # Kills the loop
        #------------------------------------------------------------------------------------
        case 2:
            player_state = -1  # Keeps player logic from running
            screen.blit(select_screen, (0, 538))
         # Selector State
            match menu_select:  # Visual clarity, rest is all backend
                case 0:
                    # Yellow, (255, 255, 0, 20)
                    draw_rect_alpha(screen, (255, 255, 0, 80), (78, 588, 195, 95))
                case 1:
                    draw_rect_alpha(screen, (255, 255, 0, 80), (289, 588, 195, 95))
                case 2:
                    draw_rect_alpha(screen, (255, 255, 0, 80), (500, 588, 195, 95))
                case 3:
                    draw_rect_alpha(screen, (255, 255, 0, 80), (711, 588, 195, 95))
                case 4:
                    draw_rect_alpha(screen, (255, 255, 0, 80), (922, 588, 195, 95))
            keys = pg.key.get_pressed()  # Read when player input
            if keys[pg.K_a] and menu_input_lag == 0:
                menu_input_lag = 10
                if menu_select == 0:
                    menu_select = 4
                else:
                    menu_select -= 1
            elif keys[pg.K_d] and menu_input_lag == 0:
                menu_input_lag = 10
                if menu_select == 4:
                    menu_select = 0
                else:
                    menu_select += 1
            if keys[pg.K_SPACE] and menu_input_lag == 0:
                if menu_select == 4:
                    # Just for back case, goes to main menu
                    menu_state = 1
                    menu_select = 0
                    menu_input_lag = 10
                else:
                    # Sets the level
                    stage_select = menu_select
                    # Reset menu, initializes player
                    menu_state = 0
                    menu_select = 0
                    player_state = 0
        # ------------------------------------------------------------------------------------
        case 3:
            # Pause Menu
            player_state = -1  # Keeps player logic from running
            screen.blit(pause_screen, (0, 0))
            # Selector State
            match menu_select:  # Visual clarity, rest is all backend
                case 0:
                    # Yellow, (255, 255, 0, 20)
                    draw_rect_alpha(screen, (255, 255, 0, 80), (32, 270, 195, 95))
                case 1:
                    draw_rect_alpha(screen, (255, 255, 0, 80), (32, 420, 195, 95))
                case 2:
                    draw_rect_alpha(screen, (255, 255, 0, 80), (32, 570, 195, 95))
            keys = pg.key.get_pressed()  # Read when player input
            if keys[pg.K_w] and menu_input_lag == 0:
                menu_input_lag = 10
                if menu_select == 0:
                    menu_select = 2
                else:
                    menu_select -= 1
            elif keys[pg.K_s] and menu_input_lag == 0:
                menu_input_lag = 10
                if menu_select == 2:
                    menu_select = 0
                else:
                    menu_select += 1
            if keys[pg.K_ESCAPE] and menu_input_lag == 0:
                menu_input_lag = 10
                player_state = 1
                menu_state = 0
            if keys[pg.K_SPACE] and menu_input_lag == 0:
                match menu_select:
                    case 0:
                        # Unpauses the game
                        player_state = 1
                        menu_state = 0
                        pass
                    case 1:
                        # Restart and kill the player
                        player_state = 2
                        menu_state = 0
                    case 2:
                        menu_input_lag = 10 # Ensures player does not instantly restart after going to main menu
                        menu_state = 1 # Goes back to title screen
                        menu_select = 0 # Sets to play, not having this causes the quit to kill the game
        # ------------------------------------------------------------------------------------
        case 4:
            # Level Clear Menu Popup
            player_state = -1  # Keeps player logic from running
            screen.blit(level_clear, (1020, 0))
            win_text = font.render(f"{total_slides}", True, (255, 255, 255, 255))
            screen.blit(win_text, (1120, 85))
            # Selector State
            match menu_select:  # Visual clarity, rest is all backend
                case 0:
                    # Yellow, (255, 255, 0, 20)
                    draw_rect_alpha(screen, (255, 255, 0, 80), (1052, 270, 195, 95))
                case 1:
                    draw_rect_alpha(screen, (255, 255, 0, 80), (1052, 420, 195, 95))
                case 2:
                    draw_rect_alpha(screen, (255, 255, 0, 80), (1052, 570, 195, 95))
            keys = pg.key.get_pressed()  # Read when player input
            if keys[pg.K_w] and menu_input_lag == 0:
                menu_input_lag = 10
                if menu_select == 0:
                    menu_select = 2
                else:
                    menu_select -= 1
            elif keys[pg.K_s] and menu_input_lag == 0:
                menu_input_lag = 10
                if menu_select == 2:
                    menu_select = 0
                else:
                    menu_select += 1
            if keys[pg.K_SPACE] and menu_input_lag == 0:
                match menu_select:
                    case 0:
                        # Continues to next level
                        stage_select += 1
                        player_state = 0
                        menu_state = 0
                        pass
                    case 1:
                        # Respawn the player
                        player_state = 2
                        menu_state = 0
                    case 2:
                        menu_input_lag = 10  # Ensures player does not instantly restart after going to main menu
                        menu_state = 1  # Goes back to title screen
                        menu_select = 0  # Sets to play, not having this causes the quit to kill the game
        case 0:  # resuming player function
            pass
    # ------------------------------------------------------------------------------------
    # This function starts the game
    # Player state selector
    match player_state:
        case 0: # Menu state
            match stage_select:
                case 0:
                    current_stage_image = level_0.convert()
                    player_spawn = (130, 364)
                    player_state = 2  # Kills player, as load screen variant
                case 1:
                    current_stage_image = level_1.convert()
                    player_spawn = (104, 92)
                    player_state = 2  # Kills player, as load screen variant
                case 2:
                    current_stage_image = level_2.convert()
                    player_spawn = (1190, 100)
                    player_state = 2  # Kills player, as load screen variant
                case 3:
                    current_stage_image = level_3.convert()
                    player_spawn = (580, 46)
                    player_state = 2  # Kills player, as load screen variant
                case 4: # This is win screen
                    current_stage_image = level_end.convert()
                    player_spawn = (520, 46)
                    player_state = 2
                case -1:
                    pass
        # ------------------------------------------------------------------------------------
        case 1: # Active gameplay, player has movement control
            screen.blit(current_stage_image, (0, 0))
            # game render components
            # Player Controller
            # Player renderer
            if player_x_velocity == 0 and player_y_velocity == 0:
                # Keeps track of last angle direction, so facing right way when stopped
                player_still_rotate = pg.transform.rotate(player_still, player_angle)
                player_still_center = player_still_rotate.get_rect(center=player_loc)
                screen.blit(player_still_rotate, player_still_center) # So location is centered on image
            else:
                # To ensure angle gets correct, not having it threw the angle off when stopping sometimes
                if abs(player_x_velocity) >= 0.1 or abs(player_y_velocity) >= 0.1:
                    player_angle = math.degrees(math.atan2(-player_y_velocity, player_x_velocity))
                # Rotates the moving penguin and keeps it centered
                player_move_rotate = pg.transform.rotate(player_move, player_angle)
                player_move_center = player_move_rotate.get_rect(center=player_loc)
                screen.blit(player_move_rotate, player_move_center)
            # User inputs
            keys = pg.key.get_pressed()  # Read when player input
            # Directional inputs, add velocity
            if keys[pg.K_w] and player_y_velocity <= 0 and player_slide == False:
                player_y_velocity += -0.1
            elif keys[pg.K_s] and player_y_velocity >= 0 and player_slide == False:
                player_y_velocity += 0.1
            if keys[pg.K_d] and player_x_velocity >= 0 and player_slide == False:
                player_x_velocity += 0.1
            elif keys[pg.K_a] and player_x_velocity <= 0 and player_slide == False:
                player_x_velocity += -0.1
            if keys[pg.K_SPACE] and player_slide == False and (abs(player_x_velocity) + abs(player_y_velocity) > 0):
                player_slide = True
                total_slides += 1
            if keys[pg.K_ESCAPE] and menu_input_lag == 0:
                menu_input_lag = 10
                menu_state = 3
        # ------------------------------------------------------------------------------------
            # Slide logic, activates once space is pressed
            if player_slide:
                if slide_x_max == 0 and slide_y_max == 0:
                    # For initialization, always ensures maximal moved distance is defined by speed
                    slide_x_max = player_x_velocity
                    slide_y_max = player_y_velocity
                    slide_ticks = 0
                elif slide_ticks >= 2 * framerate:
                    # Removes slide state once movement stops,
                    player_slide = False
                    slide_x_max = 0
                    slide_y_max = 0
                    player_x_velocity = 0
                    player_y_velocity = 0
                else:
                    # Primary slide logic, ensure slide will stop after two seconds
                    player_x_velocity -= slide_x_max / (2 * framerate)
                    player_y_velocity -= slide_y_max / (2 * framerate)
                    slide_ticks += 1
        # ------------------------------------------------------------------------------------
            # Movement logic
            player_loc.x += player_x_velocity
            player_loc.y += player_y_velocity

            # Test collision, check if player location pixel is "alive"
            player_loc_color = current_stage_image.get_at((round(player_loc.x), round(player_loc.y)))
            if player_loc_color == (0, 162, 232, 255):
                player_state = -1 # Suspend player logic
                menu_state = 4 # Player wins
            elif player_loc_color == (63, 72, 204, 255):
                player_state = 2 # Player dies

            # Debug Writing, used for test cases only
            #slides_text = font.render(f"Number of Slides: {total_slides}", True, (255, 255, 255))  # White color
            #screen.blit(slides_text, (10, 10))  # Draw at top-left corner
            #collision_text = font.render(f"Player alive: {player_state}", True, (255, 255, 255))  # White color
            #screen.blit(collision_text, (240, 10))  # Draw at top-left corner
            #color_text = font.render(f"Color Location: {player_loc_color}", True, (255, 255, 255))
            #screen.blit(color_text, (580, 10))
        # ------------------------------------------------------------------------------------
        case 2: # Player died, show death screen
            death_anim_count += 1
            if death_anim_count <= framerate:
                pg.draw.circle(screen, (63, 72, 204, 255), player_loc, ((1280/(0.5*framerate))*death_anim_count))
            elif framerate < death_anim_count <= 2 * framerate:
                screen.blit(current_stage_image, (0, 0))
                pg.draw.circle(screen, (63, 72, 204, 255), player_spawn, ((1280 / (0.5 * framerate)) * (2*framerate - death_anim_count)))
            else:
                player_loc.x = player_spawn[0] # Full flush reset
                player_loc.y = player_spawn[1]
                player_x_velocity = 0
                player_y_velocity = 0
                death_anim_count = 0
                total_slides = 0
                slide_ticks = 0
                slide_x_max = 0
                slide_y_max = 0
                player_slide = False
                player_state = 1  # Activates player alive logic
        # ------------------------------------------------------------------------------------
        case -1: # Speed up running, since no need to check this is player cannot be active
            pass

    pg.display.flip()

    clock.tick(framerate)

pg.quit()