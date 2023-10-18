import time
import constants as const
import pygame

class BaseObject:
    def __init__(self, x, y, image=None):
        self.x = x
        self.y = y
        self.image = image
        self.timestamp = time.time()
        self.start_score = None  # Calculate this based on speed
        self.end_score = None  # Calculate this based on speed

    def draw(self, screen, font, current_time):
        # Common drawing logic for all objects
        pass

    def update(self, dt):
        # Common update logic for all objects
        pass


class FlyingObject(BaseObject):
    def __init__(self, x, y, image, velocity, speed, debug=False):
        super().__init__(x, y, image)
        self.velocity = velocity
        self.total_time = None  # Calculate this based on velocity and screen size
        # Calculate start and end score based on speed
        self.start_score = 100 + (speed - const.MIN_SPEED_FLYING_OBJECT) * (100 / (const.MAX_SPEED_FLYING_OBJECT - const.MIN_SPEED_FLYING_OBJECT))
        self.end_score = 20 + (speed - const.MIN_SPEED_FLYING_OBJECT) * (20 / (const.MAX_SPEED_FLYING_OBJECT - const.MIN_SPEED_FLYING_OBJECT))
        self.debug = debug


        # Calculate intersection point with each edge of the screen
        t_to_left = (0 - x) / velocity[0] if velocity[0] < 0 else float('inf')
        t_to_right = (const.screen_width - x) / velocity[0] if velocity[0] > 0 else float('inf')
        t_to_top = (0 - y) / velocity[1] if velocity[1] < 0 else float('inf')
        t_to_bottom = (const.screen_height - y) / velocity[1] if velocity[1] > 0 else float('inf')

        # Choose the smallest positive t (time to edge)
        t_to_edge = min(t for t in [t_to_left, t_to_right, t_to_top, t_to_bottom] if t > 0)

        # Calculate total_time based on the exact distance to the edge
        self.total_time = t_to_edge

        print(f"Total Time: {self.total_time}")  # Debug print

    def draw(self, screen, font, current_time):
         #see how long the object has been on the screen
        time_elapsed = current_time - self.timestamp  # Should be increasing as time goes on
        
        # Draw circle in new position
        # pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        screen.blit(self.image, (int(self.x), int(self.y)))
        #Compute and display current score for object
        current_score = self.end_score + (self.start_score - self.end_score) * (1 - (time_elapsed / self.total_time))
        if self.debug:
            score_text = font.render(f"{int(current_score)}", True, const.WHITE)
            screen.blit(score_text, (int(self.x) - 25, int(self.y)))

    def update(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt


class CircleObject(BaseObject):
    def __init__(self, x, y, lifespan, debug=False):
        super().__init__(x, y)
        self.radius = 1  # Start as a dot
        self.creation_time = time.time()
        self.debug = debug
        self.lifespan = lifespan
        self.growth_rate = 0.8
        self.elapsed_time = 0

    def draw(self, screen, font, current_time):
        pygame.draw.circle(screen, (255, 131, 250), (int(self.x), int(self.y)), int(self.radius))
        if self.radius >= const.BONUS_CIRCLE_RADIUS:
            circle_text = font.render(f"+3s", True, (255, 255, 255))
            screen.blit(circle_text, (int(self.x) - 20, int(self.y) - 10))
        '''
        # Calculate time remaining for the non-flying object
        time_elapsed = current_time - self.timestamp
        self.time_remaining = max(0, self.lifespan - time_elapsed)

        # Draw the object's image at its current position
        screen.blit(self.image, (int(self.x), int(self.y)))

        if self.debug:
            # Display the remaining lifespan of the object
            lifespan_text = font.render(f"Time Remaining: {int(self.time_remaining)}", True, (255, 255, 255))
            screen.blit(lifespan_text, (int(self.x) - 25, int(self.y) - 20))

        # Optionally, you can add interaction logic here
        '''
    def update(self, dt):
        # Calculate the elapsed time since creation
        self.elapsed_time = time.time() - self.creation_time
        print(f"etime: {self.elapsed_time}")
        # Gradually increase the radius until it reaches max_radius
        if self.radius < const.BONUS_CIRCLE_RADIUS:
            self.radius += self.growth_rate



class AnimationObject:
    def __init__(self, x, y, images, x_offset = 0, y_offset = 0, size_modifier=1):
        self.x = x - int(x_offset)
        self.y = y - int(y_offset)
        self.images = images
        self.current_frame = 0
        self.size_modifier = size_modifier
    
    def draw(self, screen) -> bool:
        # Draw the next frame of the animation
        if self.current_frame >= len(self.images):
            return True
        
        image = self.images[self.current_frame]
        resized_image = pygame.transform.scale(image, (int(image.get_width() * self.size_modifier), int(image.get_height() * self.size_modifier)))
        screen.blit(resized_image, (self.x, self.y))
        self.current_frame += 1
        return False
