from blessed import Terminal
from src.game.main import main
from src.game.title import Title


class LoadBlockdude:

    def __init__(self):
        self.intro_title = Title()
        self.title_return_code = self.intro_title.title()

        main(Terminal(), self.title_return_code)


if __name__ == "__main__":
    new_game = LoadBlockdude()
