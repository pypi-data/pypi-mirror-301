import numpy as np

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron


class Shifter(Component):
    shift = np.zeros(2)

    def __init__(self, z: float, x_shift: float, y_shift: float, name: str = "unknown shifter") -> None:
        """
        Create a shifter
        :param z: z position of the shifter in meters
        :param x_shift: shift along x-axis in meters
        :param y_shift: shift along y-axis in meters
        :param name: name of the shifter
        """
        self.name = name
        self.set_z(z)
        self.set_shift(x_shift, y_shift)

        z_field = ComponentField('z', self.z, 'm', lambda h: self.set_z(h))
        x_shift_field = ComponentField('x_shift', self.x_shift, 'm', lambda x: self.set_shift(x, self.y_shift))
        y_shift_field = ComponentField('y_shift', self.y_shift, 'm', lambda y: self.set_shift(self.x_shift, y))

        self.fields = [z_field, x_shift_field, y_shift_field]

    def __str__(self):
        return f'Shifter {self.name}\n\tposition: {self.z}\n\t' \
               f'shift: {self.shift}'

    @property
    def x_shift(self) -> float:
        """
        X position of the shifter in meters
        :return: x position of the shifter in meters
        """
        return float(self.shift[0])

    @property
    def y_shift(self) -> float:
        """
        Y position of the shifter in meters
        :return: y position of the shifter in meters
        """
        return float(self.shift[1])

    def apply_on_electron(self, electron: Electron) -> None:
        """
        Apply the shifter on an electron by changing its position
        :param electron: electron to apply the shifter on
        :return:
        """
        if not self.enabled:
            return
        s_xyz = np.append(self.shift, 0)
        electron.position += s_xyz

    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the shifter on the electrons by changing their positions
        :param positions: the positions of the electrons
        :param velocities: velocities of the electrons
        :return:
        """
        if not self.enabled:
            return
        # velocities are augmented of power along the
        positions[:, 0] += self.shift[0]
        positions[:, 1] += self.shift[1]

    def set_z(self, z: float) -> None:
        """
        Set the z position of the shifter
        :param z: z position of the shifter in m
        :return:
        """
        self.z = z

    def set_shift(self, x_shift: float, y_shift: float) -> None:
        """
        Set the shift of the shifter
        :param x_shift: shift along x-axis in meters
        :param y_shift: shift along y-axis in meters
        :return:
        """
        self.shift = np.array([x_shift, y_shift])

    @staticmethod
    def from_json(json: dict) -> 'Shifter':
        """
        Create a shifter from a json object
        :param json: the json object to create the shifter from
        :return: the shifter created from the json object
        """
        return Shifter(json['z'], json['x_shift'], json['y_shift'], json['name'])

    def to_json(self) -> dict:
        """
        Convert the shifter to a json object
        :return: the json object of the shifter
        """
        return {
            'type': 'shifter',
            'z': self.z,
            'x_shift': self.shift[0],
            'y_shift': self.shift[1],
            'name': self.name
        }
