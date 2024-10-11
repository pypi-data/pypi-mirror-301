import numpy as np

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron


class Tilter(Component):
    """
    Class representing a tilter
    """
    power = 0
    theta = 0

    def __init__(self, z: float, deflection_power: float, theta_direction: float, name: str = "unknown tilter") -> None:
        """
        Create a tilter
        :param z: z position of the tilter in meters
        :param deflection_power: deflection power of the tilter in m.s-2
        :param theta_direction: direction of the tilter in radians
        :param name: name of the tilter
        """
        self.name = name
        self.set_z(z)
        self.set_power(deflection_power)
        self.set_theta_direction(theta_direction)

        z_field = ComponentField('z', self.z, 'm', lambda h: self.set_z(h))
        power_field = ComponentField('power', self.power, 'V', lambda p: self.set_power(p))
        theta_field = ComponentField(
            'theta', np.rad2deg(self.theta), '°', lambda t: self.set_theta_direction(np.deg2rad(t))
        )

        self.fields = [z_field, power_field, theta_field]

    def __str__(self):
        return f'Tilter {self.name}\n\tposition: {self.z}\n\t' \
               f'power: {self.power}\n\ttheta: {self.theta}'

    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the tilter on the electrons by changing their velocities based on the deflection power
        :param positions: positions of the electrons
        :param velocities: velocities of the electrons
        :return:
        """
        if not self.enabled:
            return
        # velocities are augmented of power along the
        velocities[:, 0] += self.power * np.cos(self.theta)
        velocities[:, 1] += self.power * np.sin(self.theta)

    def apply_on_electron(self, electron: Electron) -> None:
        """
        Apply the tilter on the electron by changing its velocity
        :param electron: electron to apply the tilter on
        :return:
        """
        if not self.enabled:
            return
        v_xy = self.power * np.array([np.cos(self.theta), np.sin(self.theta)])
        v_xyz = np.append(v_xy, 0)
        electron.accelerate(v_xyz)

    def set_z(self, z: float) -> None:
        """
        Set the z position of the tilter
        :param z: z position of the tilter in m
        :return:
        """
        self.z = z

    def set_power(self, power: float) -> None:
        """
        Set the deflection power of the tilter
        :param power: power of the tilter in m.s-1
        :return:
        """
        self.power = power

    def set_theta_direction(self, theta_direction: float) -> None:
        """
        Set the direction of the tilter
        :param theta_direction: direction of the tilter in radians
        :return:
        """
        self.theta = theta_direction

    def to_json(self) -> dict:
        """
        Convert the tilter to a json object
        :return: the json object of the tilter
        """
        return {
            'type': 'tilter',
            'z': self.z,
            'power': self.power,
            'theta': self.theta,
            'name': self.name,
            "enabled": self.enabled,
            "height": self.height,
        }

    @staticmethod
    def from_json(json: dict) -> 'Tilter':
        """
        Create a tilter from a json object
        :param json: tilter as a json object
        :return: the tilter
        """
        tilter = Tilter(json['z'], json['power'], json['theta'], json['name'])
        tilter.enabled = json['enabled']
        tilter.height = json['height']
        return tilter
