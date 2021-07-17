from __future__ import annotations

from typing import Iterable, Optional, Union

import src.elements as elements
import src.game.element_data as element_data
from src.game.movement import Movement
from src.game.physics import RigidBody
from src.game.vector2D import Vector2D


class Controller:
    """Controller base class for controlling the movement of level elements."""

    def __init__(self):
        pass

    def _move(
        self,
        data: element_data.ElementData,
        direction: Vector2D,
    ) -> None:
        """Moves this level element laterally by some number of spaces given.

        The number of spaces can be positive or negative.
        """
        RigidBody.move_active_element(data, direction)

    def move_up(self, data: element_data.ElementData) -> None:
        """Move this level element upward according to the rules."""
        self._move(data, Movement.UP)

    def move_left(self, data: element_data.ElementData) -> None:
        """Move this level element leftward according to the rules.

        If there are any objects to the left of block dude, he cannot move left.
        """
        self._move(data, Movement.LEFT)

    def move_right(self, data: element_data.ElementData) -> None:
        """Move this level element rightward according to the rules.

        If there are any objects to the left of block dude, he cannot move left.
        """
        self._move(data, Movement.RIGHT)

    def move_down(self, data: element_data.ElementData) -> None:
        """Move this level element rightward according to the rules.

        If there are any objects to the left of block dude, he cannot move left.
        """
        self._move(data, Movement.DOWN)
    
    def interact(self, data: element_data.ElementData) -> None:
        pass


def get_head_of_active(data: element_data.ElementData) -> elements.LevelElement:
    """..."""
    head_position = data.active_element.position + Movement.UP
    return data.level.get_element_at_position(head_position)


def get_lateral_of_active(data: element_data.ElementData) -> elements.LevelElement:
    """..."""
    lateral_position = data.active_element.position + data.active_element.facing
    return data.level.get_element_at_position(lateral_position)


def get_top_lateral_of_active(data: element_data.ElementData) -> elements.LevelElement:
    """..."""
    top_lateral_position = get_lateral_of_active(data).position + Movement.UP
    return data.level.get_element_at_position(top_lateral_position)


def is_block(element: elements.LevelElement) -> bool:
    """Whether the element is a block."""
    return isinstance(element, elements.Block)


def is_space(element: elements.LevelElement) -> bool:
    """Whether the element is a block."""
    return isinstance(element, elements.Space)


def is_clear_for_action(*elements: elements.LevelElement) -> bool:
    """Ensures the area around the character is clear for picking up blocks."""
    return all((is_space(element) for element in elements))


class DoNothingController:
    """The do nothing controller. Useful for doing nothing on a level element."""


class DudeController(Controller):
    """Block Dude controller with its rules."""

    def __init__(self):
        self.carrying: Optional[elements.ControllableLevelElement] = None

    def move(
        self,
        data: element_data.ElementData,
        direction: Vector2D,
    ) -> None:
        # Move the carrying block as well
        top_lateral_element = get_top_lateral_of_active(data)
        lateral_element = get_lateral_of_active(data)

        position = RigidBody.move_element(data, direction, data.active_element)

        if self.carrying and is_clear_for_action(top_lateral_element):
            # Check if we can move
            block_position = RigidBody.move_element(data, direction, self.carrying)

            if (block_position - position).x:
                self.carrying = None

    def move_left(self, data: element_data.ElementData) -> None:
        """Move this level element leftward according to the rules.

        If there are any objects to the left of block dude, he cannot move left.
        """
        self.move(data, Movement.LEFT)

    def move_right(self, data: element_data.ElementData) -> None:
        """Move this level element rightward according to the rules.

        If there are any objects to the left of block dude, he cannot move left.
        """
        self.move(data, Movement.RIGHT)

    def move_up(self, data: element_data.ElementData) -> None:
        """Move this level element upward according to the rules."""
        active_element = data.active_element
        facing = active_element.facing
        lateral_element = get_lateral_of_active(data)
        head_element = get_head_of_active(data)

        if not is_clear_for_action(lateral_element):
            el = data.level.get_element_at_position(head_element.position + Movement.UP)
            if not self.carrying and is_clear_for_action(head_element, el):
                up_and_lateral_position = facing + Movement.UP
                self.move(data, up_and_lateral_position)
            elif self.carrying:
                up_and_lateral_position = facing + Movement.UP
                self.move(data, up_and_lateral_position)

    def box_action(self, data: element_data.ElementData) -> None:
        """The box action as picking up or dropping."""
        lateral_element = get_lateral_of_active(data)
        top_lateral_element = get_top_lateral_of_active(data)
        head_element = get_head_of_active(data)

        if not self.carrying:
            if is_block(lateral_element) and is_clear_for_action(
                top_lateral_element,
                head_element,
            ):
                RigidBody.move_element_to_destination(
                    data, head_element.position, lateral_element
                )
                data.soundboard.play_sfx("pickup_square")
                self.carrying = lateral_element
        else:
            # top lateral position is empty space, drop it
            if is_clear_for_action(top_lateral_element):
                facing = data.active_element.facing
                RigidBody.move_element(data, facing, self.carrying)
                data.soundboard.play_sfx("thud")
                self.carrying = None

    def move_down(self, data: element_data.ElementData) -> None:
        """Move down action from command."""
        self.box_action(data)

    def interact(self, data: element_data.ElementData) -> None:
        if self.carrying:
            return
    
        position = data.level.active_element.position
        below = position + Movement.DOWN
        bottom_element = data.level.get_element_at_position(below)
        if isinstance(bottom_element, elements.TelekinesisPad):
            block = data.level.find_element(elements.TelekinesisBlock)
            data.level.set_active_element(block)


class TelekinesisController(Controller):
    
    def _move(
        self,
        data: element_data.ElementData,
        direction: Vector2D,
    ) -> None:
        """movement function without rigid body so that the cube can float"""
        position = data.level.active_element.position
        lateral_position = position + direction
        lateral_element = data.level.get_element_at_position(lateral_position)
        destination = lateral_position

        if isinstance(lateral_element, elements.Space):
            destination = lateral_position
        else:
            destination = position
        
        data.level.move_element(position, destination)

    def interact(self, data: element_data.ElementData):
        """Gives the controls back to blockdude
        
        Also drops the block before so that it doesn't float
        """
        position = data.level.active_element.position
        below = position + Movement.DOWN
        while isinstance(data.level.get_element_at_position(below),elements.Space):
            below += Movement.DOWN
        
        data.level.move_element(position, below+Movement.UP)  
        dude = data.level.find_element(elements.Dude)
        data.level.set_active_element(dude)