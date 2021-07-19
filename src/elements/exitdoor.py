from .levelelement import LevelElement


class ExitDoor(LevelElement):
    """The target location for Block Dude to reach."""

    level_symbol = "X"
    string_symbol = "🌀"


def is_door_element(level_element: LevelElement) -> bool:
    """Determines whether the object is a `ExitDoor` level element or not."""
    return isinstance(level_element, ExitDoor)
