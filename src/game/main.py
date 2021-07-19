import os
import sys
from pathlib import Path

from blessed import Terminal

from .game import GameState
from .level import create_level_from_file
from .renderer import Renderer
from .title import Title

# Timeout speed for inputs
TIMEOUT = 0.1

levels_folder = os.listdir(path="src/resources/levels/")


def clean_exit():
    while 1:
        interpreter = sys.executable
        os.system(f"{interpreter} blockdude.py")
        exit()


def starting_level_from_script_args() -> str:
    """Takes the Python script input to jump to a particular level.

    e.g. `python ./blockdude.py level-5`
    """
    starting_level = "level-1"
    if len(sys.argv) >= 2:
        if f"{sys.argv[1]}.txt" in levels_folder:
            starting_level = str(sys.argv[1])
    return starting_level


def main(terminal: Terminal, level_num: str = None) -> None:
    """Main entry point and loop for the game."""
    # Necessary when running with Docker; Docker's terminal defaults to 8 colors
    terminal.number_of_colors = 1 << 24

    if level_num:
        starting_level = level_num
    else:
        starting_level = starting_level_from_script_args()

    # initalize game vars
    try:
        level = create_level_from_file(
            level_file_name=f"{starting_level}.txt",
            levels_directory=Path(__file__).parent.parent / Path("resources/levels"),
        )
    except FileNotFoundError:
        clean_exit()

    renderer = Renderer(terminal=terminal, level=level)
    gamestate = GameState(level=level, renderer=renderer)

    gamestate.current_level = int(level_num[-1])

    with terminal.cbreak(), terminal.hidden_cursor(), terminal.fullscreen():
        renderer.render_level()

        while True:
            keystroke = terminal.inkey(timeout=TIMEOUT)
            if gamestate.game_state():
                gamestate = None
                renderer = None
                break
            elif keystroke:
                gamestate.update(keystroke)

    if gamestate.current_level == 11:
        end_game = create_level_from_file("./resources/levels/level-99.txt")
        renderer.render_level(end_game)
        end_game = Title()
        end_game.display_logo()
        print(f"{renderer.terminal.move_xy(8, 8)} CONGRATULATIONS, YOU'VE WON THE GAME!")


if __name__ == "__main__":
    main(Terminal())
