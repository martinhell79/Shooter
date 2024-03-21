## Description

Shooter is a simple computer game where players can test their aiming and shooting skills. The game features flying objects that move across the screen, and your objective is to shoot these objects by aiming with your mouse and clicking to fire. 

## Features

- Flying objects with varying speeds and scores.
- Real-time scoring system.
- Highscore tracking.
- Customizable game settings.

## Gameplay

- Move your mouse to aim at the flying objects.
- Click the mouse to shoot and destroy the vulnerabilities.
- Shoot the clock to add extra time.
- Don't shoot the friendly airplanes.
- Earn points based on how quickly they are shot and the speed of the objects.
- Try to achieve the highest score possible and beat your own records.
- Press ESC at any time to quit the game.

## Installation

1. Clone the repository or download the game files.
2. Ensure you have Python 3 installed.
3. Install dependencies using `pip install -r requirements.txt`.
4. Run the game using `python game.py`.

## Customization

You can customize the game by modifying the following settings:

- In `constants.py` you can modify size and speed of objects if you are not happy with the defaults.
- If no name/email is entered, Anonymous will be used instead. In `constants.py` there is a varaible `MAX_PLAYS_PER_EMAIL` that is used to limit the number of plays for a unique email. This variable does not apply to anonymous play.
- If you want to change which screen the game is started on, you can change the variable `chosen_screen` in `game_setup.py`. 0 is default but you can change it to 1 or 2 depending on which screen you want to run it on. However, note that if you use a lightgun, that might calibrate on the primary screen so it would then be better to change the primary screen on your computer's settings and keep the `chosen_screen = 0` value.
  
## Highscores

- The game keeps track of the highscores. Try to make it to the leaderboard!
- Highscores are saved in `highscores.txt`. Empty this file if you want to reset highscores and remove all play history.

## Using a lightgun

Though independent of the implementation, here are some notes that could be useful if you use the AimTrak lightgun to play the game. 

- Figure out what distance from the screen is best to have a smooth experience.
- Unplug other peripherals that are not needed. We sometimes experienced some problems when other peripherals were connected.
- Though not officially written on the webpage for the gun, Mac computers worked well with the gun out of the box.
- If gun starts acting weird and freezes, just unplug and plug it in again.
- Make sure the receiver is firmly placed on the TV/monitor and is pointing in the right direction.

## License

This project is licensed under the [MIT License](LICENSE.md).
