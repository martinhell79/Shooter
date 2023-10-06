import time
import constants as const

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
    def __init__(self, x, y, image, velocity, speed):
        super().__init__(x, y, image)
        self.velocity = velocity
        self.total_time = None  # Calculate this based on velocity and screen size
        # Calculate start and end score based on speed
        self.start_score = 100 + (speed - const.MIN_SPEED_FLYING_OBJECT) * (100 / (const.MAX_SPEED_FLYING_OBJECT - const.MIN_SPEED_FLYING_OBJECT))
        self.end_score = 20 + (speed - const.MIN_SPEED_FLYING_OBJECT) * (20 / (const.MAX_SPEED_FLYING_OBJECT - const.MIN_SPEED_FLYING_OBJECT))

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
        score_text = font.render(f"{int(current_score)}", True, const.WHITE)
        screen.blit(score_text, (int(self.x) - 25, int(self.y)))

    def update(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt


class NonFlyingObject(BaseObject):
    def __init__(self, x, y, image, lifespan):
        super().__init__(x, y, image)
        self.lifespan = lifespan
        self.time_remaining = lifespan

    def draw(self, screen, font, current_time):
        # Calculate time remaining for the non-flying object
        time_elapsed = current_time - self.timestamp
        self.time_remaining = max(0, self.lifespan - time_elapsed)

        # Draw the object's image at its current position
        screen.blit(self.image, (int(self.x), int(self.y)))

        # Display the remaining lifespan of the object
        lifespan_text = font.render(f"Time Remaining: {int(self.time_remaining)}", True, (255, 255, 255))
        screen.blit(lifespan_text, (int(self.x) - 25, int(self.y) - 20))

        # Optionally, you can add interaction logic here

    def update(self, dt):
        # Implement update logic for non-flying objects
        pass


class AnimationObject:
    def __init__(self, x, y, images, x_offset = 0, y_offset = 0):
        self.x = x - int(x_offset)
        self.y = y - int(y_offset)
        self.images = images
        self.current_frame = 0
    
    def draw(self, screen) -> bool:
        # Draw the next frame of the animation
        if self.current_frame >= len(self.images):
            return True
        
        image = self.images[self.current_frame]
        screen.blit(image, (self.x, self.y))
        self.current_frame += 1
        return False
