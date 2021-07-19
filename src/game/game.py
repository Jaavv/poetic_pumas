from blessed.keyboard import Keystroke
from blessed import Terminal

from pathlib import Path

# from .movement import Movement

from .element_data import ElementData
from .input_handler import InputHandler
from .level import Level
from .level import create_level_from_file
from .renderer import Renderer
from .soundboard import Soundboard
from .vector2D import Vector2D
from ..elements.exitdoor import ExitDoor


class GameState:
    """Overall game state.

    Contains all necessary information about the game information and processes
    user input actions.
    """

    def __init__(self, level: Level, renderer: Renderer):
        self.level = level
        self.renderer = renderer
        self.input_handler = InputHandler()
        self.soundboard = Soundboard()
        self.element_data = ElementData(level=self.level, soundboard=self.soundboard)
        self.current_level = 1
        self.win = False
        self.level_dict = {
            1: "level-1.txt",
            2: "level-2.txt",
            3: "level-3.txt",
            4: "level-4.txt",
            5: "level-5.txt",
            6: "level-6.txt",
            7: "level-7.txt",
            8: "level-8.txt",
            9: "level-9.txt",
            10: "level-10.txt",
            11: "level-11.txt",
            12: "level-12.txt",
        }

    def game_state(self) -> None:
        """Checks near MAIN_CHARACTER position for exit door element"""
        exit_checks = [
            self.level.active_element.position + Vector2D(-1, 0),
            self.level.active_element.position + Vector2D(-1, -1),
            self.level.active_element.position + Vector2D(1, -1),
            self.level.active_element.position + Vector2D(1, 0),
            self.level.active_element.position + Vector2D(-1, 1),
            self.level.active_element.position + Vector2D(1, 1),
        ]

        if self.current_level == 0:
            self.current_level = 1
        else:
            for check in exit_checks:
                if isinstance(self.level.get_element_at_position(check), ExitDoor):
                    if self.current_level == 11:
                        return True
                    else:
                        self.current_level += 1
                        self.set_level()

    def set_level(self) -> None:
        self.level = create_level_from_file(
            level_file_name=self.level_dict[self.current_level],
            levels_directory=Path(__file__).parent.parent / Path("resources/levels"))
        self.renderer.terminal.move_xy(0, 0)
        for columns in range(self.renderer.terminal.width):
            for row in range(self.renderer.terminal.height):
                print(f"{self.renderer.terminal.normal} ")
        self.renderer = Renderer(terminal=Terminal(), level=self.level)
        self.element_data = ElementData(level=self.level, soundboard=self.soundboard)
        

    def process_input(self, keystroke: Keystroke) -> None:
        """Takes the active element of the level and applies the input onto it."""
        # Package up data into a neat object

        self.input_handler.handle_input(keystroke, data=self.element_data)

    def update(self, keystroke: Keystroke) -> None:
        """Process the game on every looped update call.

        Args:
            keystroke (Keystroke): user input on keyboard
        """

        print(f"{self.renderer.terminal.move_xy(0, 0)} {keystroke}")
        self.process_input(keystroke)
        self.game_state()
        self.renderer.render_level()




