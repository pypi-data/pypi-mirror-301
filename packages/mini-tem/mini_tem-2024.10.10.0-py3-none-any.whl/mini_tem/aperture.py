import numpy as np

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron


class Aperture(Component):

    def __init__(self, z: float, diameter: float, name: str = "unknown aperture", x: float = 0, y: float = 0) -> None:
        """
        Create an aperture with a given diameter
        :param z: z position of the aperture in meters
        :param diameter: diameter of the aperture in meters
        :param name: name of the aperture
        :param x: x position of the aperture in meters
        :param y: y position of the aperture in meters
        """
        self.name = name
        self.diameter = diameter
        self.position = np.array([x, y, z])

        self.diameter_field = ComponentField('diameter', self.diameter, 'm', lambda d: self.set_diameter(d))
        self.x_field = ComponentField('x', float(self.position[0]), 'm',
                                      lambda v: self.set_position(v, float(self.position[1]), float(self.position[2])))
        self.y_field = ComponentField('y', float(self.position[1]), 'm',
                                      lambda v: self.set_position(float(self.position[0]), v, float(self.position[2])))
        self.z_field = ComponentField('z', float(self.position[2]), 'm',
                                      lambda v: self.set_position(float(self.position[0]), float(self.position[1]), v))

        self.fields = [self.diameter_field, self.x_field, self.y_field, self.z_field]

    def __str__(self):
        return f'Aperture {self.name}\n\tdiameter: {self.diameter}\n\tposition: {self.position}'

    @property
    def x(self):
        """
         X position of the aperture in meters
        """
        return self.position[0]

    @property
    def y(self):
        """
        Y position of the aperture in meters
        """
        return self.position[1]


    @property
    def z(self):
        """
        Z position of the aperture in meters
        """
        return self.position[2]


    def is_electron_inside(self, electron: Electron) -> bool:
        """
        Check if an electron is inside the aperture
        :param electron: electron to check
        :return: True if the electron is inside the aperture, False otherwise
        """
        return np.linalg.norm(electron.position - self.position) < self.diameter / 2


    def nullify_speed_by_position(self, positions: np.array, velocities: np.array) -> None:
        """
        Nullify the speed of the electrons that are outside the aperture
        :param positions: array of positions of the electrons
        :param velocities: array of velocities of the electrons
        """
        outside_aperture_indexes = np.where(
            np.linalg.norm(positions[:, :2] - self.position[:2], axis=1) > self.diameter / 2)
        velocities[outside_aperture_indexes, 2] = 0


    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the aperture on a list of electrons
        :param positions: array of positions of the electrons
        :param velocities: array of velocities of the electrons
        """
        if not self.enabled:
            return
        self.nullify_speed_by_position(positions, velocities)


    def apply_on_electron(self, electron: Electron) -> None:
        """
        Apply the aperture on a single electron by nullifying its speed if it is outside the aperture
        :param electron: electron on which the aperture is applied
        """
        if not self.enabled:
            return
        if not self.is_electron_inside(electron):
            electron.velocity = 0

    def set_diameter(self, diameter: float) -> None:
        """
        Set the diameter of the aperture
        """
        self.diameter = diameter

    def set_position(self, x: float, y: float, z:float) -> None:
        """
        Set the position of the aperture
        """
        self.position = np.array([x, y, z])

    def to_json(self) -> dict:
        """
        Return the aperture as a json object
        """
        return {
            "type": "aperture",
            "name": self.name,
            "diameter": self.diameter,
            "position": self.position.tolist(),
            "enabled": self.enabled,
            "height": self.height,
        }

    @staticmethod
    def from_json(json: dict) -> 'Aperture':
        """
        Create an aperture from a json object
        """
        ap = Aperture(json["position"][2], json["diameter"], json["name"], json["position"][0], json["position"][1])
        ap.enabled = json["enabled"]
        ap.height = json["height"]
        return ap
