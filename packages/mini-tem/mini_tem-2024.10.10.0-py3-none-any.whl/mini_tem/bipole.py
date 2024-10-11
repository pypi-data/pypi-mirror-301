import numpy as np

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron


class Bipole(Component):
    power = 0
    theta_direction = 0

    def __init__(self, z: float, deflection_power: float, theta_direction: float, name: str = "unknown bipole") -> None:
        """
        Create a bipole
        :param z: z position of the bipole in meters
        :param deflection_power: deflection power of the bipole in volts
        :param theta_direction: direction of the bipole in radians
        :param name: name of the bipole
        """
        self.name = name
        self.set_z(z)
        self.set_power(deflection_power)
        self.set_theta_direction(theta_direction)

        z_field = ComponentField('z', self.z, 'm', lambda h: self.set_z(h))
        power_field = ComponentField('power', self.power, 'V', lambda p: self.set_power(p))
        theta_direction_field = ComponentField('theta', np.rad2deg(self.theta_direction), 'deg', lambda t: self.set_theta_direction(np.deg2rad(t)))

        self.fields = [z_field, power_field, theta_direction_field]

    def __str__(self):
        return f'Bipole {self.name}\n\tposition: {self.z}\n\t' \
               f'power: {self.power}\n\ttheta: {self.theta_direction}'

    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the bipole on the electrons by changing their velocities based on the deflection power
        :param positions: positions of the electrons
        :param velocities: velocities of the electrons
        """
        if not self.enabled:
            return
        velocities[:, 0] += self.power * np.cos(self.theta_direction)
        velocities[:, 1] += self.power * np.sin(self.theta_direction)

    def apply_on_electron(self, electron: Electron) -> None:
        """
        Apply the bipole on the electron by changing its velocity
        :param electron: electron to apply the bipole on
        """
        if not self.enabled:
            return
        v_xy = self.power * np.array([np.cos(self.theta_direction), np.sin(self.theta_direction)])
        v_xyz = np.append(v_xy, 0)
        electron.accelerate(v_xyz)

    def set_z(self, z: float) -> None:
        """
        Set the z position of the bipole
        :param z: z position of the bipole in m.s-1
        """
        self.z = z

    def set_power(self, power: float) -> None:
        """
        Set the deflection power of the bipole
        :param power: power of the bipole in m.s-1
        :return:
        """
        self.power = power

    def set_theta_direction(self, theta_direction: float) -> None:
        """
        Set the direction of the bipole
        :param theta_direction: direction of the bipole in radians
        :return:
        """
        self.theta_direction = theta_direction

    def to_json(self) -> dict:
        """
        Convert the bipole to a json object
        :return: the json object of the bipole
        """
        return {
            'type': 'bipole',
            'z': self.z,
            'power': self.power,
            'theta': self.theta_direction,
            'name': self.name,
            "enabled": self.enabled,
            "height": self.height,
        }

    @staticmethod
    def from_json(json: dict) -> 'Bipole':
        """
        Create a bipole from a json object
        :param json: bipole as a json object
        :return: the bipole
        """
        bipole = Bipole(json['z'], json['power'], json['theta'], json['name'])
        bipole.enabled = json['enabled']
        bipole.height = json['height']
        return bipole
