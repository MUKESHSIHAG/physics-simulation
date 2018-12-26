import pygame, math, time
from Pendulum import Pendulum, dist, onPath, collide        

if __name__ == "__main__":
    # Define pygame variables
    (width, height) = (640, 480)
    background_colour = (255,255,255)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pendulum")
    running = True
    selected = None

    # Define the stack of pendulums
    pendulum_stack = [Pendulum(0, 250, 40), 
                      Pendulum(0, 300, 40), 
                      Pendulum(0, 350, 40), 
                      Pendulum(0, 400, 40)]

    # Assign an id to each pendulum                   
    for i, p in enumerate(pendulum_stack): 
        p.ID = i

    # Number of pendulums for reference within the game loop
    numPen = len(pendulum_stack)

    while running:
        # draw background and line pendulums hang from
        screen.fill(background_colour)
        pygame.draw.line(screen, (0,0,255), (120, 40),
                         (520, 40), 3)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for p in pendulum_stack:
            # Check for mouse left click
            if pygame.mouse.get_pressed() == (1,0,0):
                (mouseX, mouseY) = pygame.mouse.get_pos()
                a = mouseX - p.pivot_x
                b = mouseY - p.pivot_y

                # If mouse position is within bounds of a pendulum
                # then select that pendulum
                if dist(a, b, p.x, p.y) < 40:
                    if selected == None:
                        selected = p.ID
                        (p.x, p.y) = onPath(a, b, p.length, p.pivot_y)
                        p.v_x = 0
                elif selected == p.ID:
                    (p.x, p.y) = onPath(a, b, p.length, p.pivot_y)
                    p.v_x = 0
                if p.ID < numPen-1:
                    for i in range(p.ID, numPen-1):
                        collide(pendulum_stack[p.ID], pendulum_stack[i+1])
            
            if event.type == pygame.MOUSEBUTTONUP:
                # Deselect pendulum upon mouse release
                if selected == p.ID:
                    p.v_x = 0
                selected = None

            # Check for collisions with adjacent pendulum
            if p.ID < numPen-1:
                for i in range(p.ID, numPen-1):
                    collide(pendulum_stack[p.ID], pendulum_stack[i+1])

            # Pendulum should swing unless it's selected by the user
            if selected != p.ID:         
                p.swing()
            p.draw(screen)

        time.sleep(0.4*0.01)
        pygame.display.flip()

    pygame.quit()
    
