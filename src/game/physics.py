from __future__ import annotations

import src.elements as elements

from . import element_data
from .movement import Movement
from .vector2D import Vector2D


class RigidBody:
    """Imitates rigidbody movements on elements using statis methods. Utilizes Vector2D class"""

    @staticmethod
    def get_drop_position(data: element_data.ElementData, position: Vector2D) -> Vector2D:
        """Applies drop

        :param data: The element data
        :param position: Position of the element
        :return tuple of boolean successful drop and new position
        """
        one_below = position + Movement.DOWN
        while elements.space.is_space_element(
            data.level.get_element_at_position(one_below)
        ) or elements.exitdoor.is_door_element(data.level.get_element_at_position(one_below)):
            one_below.add(Movement.DOWN)

        new_position = one_below + Movement.UP

        return new_position

    @staticmethod
    def move_active_element(
        data: element_data.ElementData, movement: Vector2D
    ) -> Vector2D:
        """
        Apply movement to the active element.

        Applies the given movement to the body
        :param data: the element data
        :param movement: The movement vector
        """
        return RigidBody.move_element(data, movement, data.active_element)

    @staticmethod
    def move_element(
        data: element_data.ElementData, movement: Vector2D, element: elements.LevelElement
    ) -> Vector2D:
        """Apply movement to an element."""
        destination = element.position + movement
        destination_element = data.level.get_element_at_position(destination)

        if elements.space.is_space_element(destination_element) or elements.exitdoor.is_door_element(destination_element):
            data.soundboard.play_sfx("step")
        else:
            destination = element.position
            data.soundboard.play_sfx("bump")

        destination = RigidBody.get_drop_position(data, destination)
        data.level.move_element(element.position, destination)

        return destination

    @staticmethod
    def move_element_to_destination(
        data: element_data.ElementData,
        destination: Vector2D,
        element: elements.LevelElement,
    ) -> Vector2D:
        """Apply movement to an element."""
        destination_element = data.level.get_element_at_position(destination)

        if elements.space.is_space_element(destination_element):
            data.soundboard.play_sfx("step")
        else:
            destination = element.position
            data.soundboard.play_sfx("bump")

        destination = RigidBody.get_drop_position(data, destination)
        data.level.move_element(element.position, destination)

        return destination
