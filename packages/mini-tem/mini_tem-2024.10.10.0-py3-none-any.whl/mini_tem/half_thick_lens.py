import numpy as np

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron


class HalfThickLens(Component):
    """
    Class representing each half of a thick lens using the refraction power of each interface
    """
    refraction_power = 0

    def __init__(self, z: float, refraction_power: float, second_half=None, name: str = "unknown half lens") -> None:
        """
        Create a lens
        :param z: z position of the center of the lens in meters
        :param refraction_power: refraction power of the interface
        :param name: name of the lens
        :param second_half: second half of the lens
        """
        self.second_half = None
        if second_half is not None:
            self.second_half = second_half

        self.name = name
        self.set_z(z)
        self.set_surface_power(refraction_power)

        z_field = ComponentField('z', self.z, 'm', lambda h: self.set_z(h))
        surface_power_field = ComponentField('surface power', self.refraction_power, 'm', lambda p: self.set_surface_power(p))

        self.fields = [surface_power_field, z_field]

    def __str__(self):
        return f'Lens {self.name}\n\tposition: {self.z}\n\tsurface power: {self.refraction_power}'

    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the lens on the electrons by changing their velocities based on the surface power
        :param positions:
        :param velocities:
        :return:
        """
        if not self.enabled:
            return
        velocities[:, :2] *= self.refraction_power

    def apply_on_electron(self, electron: Electron) -> None:
        """
        Apply the lens on the electron by changing its velocity
        :param electron: electron to apply the lens on
        :return:
        """
        if not self.enabled:
            return
        electron.velocity[:2] *= self.refraction_power

    def set_surface_power(self, refraction_power: float):
        self.refraction_power = refraction_power
        if self.second_half is not None:
            self.second_half.refraction_power = refraction_power

    def set_z(self, z: float) -> None:
        """
        Set the z position of the lens
        :param z: z position of the lens in m
        :return:
        """
        self.z = z

    def to_json(self, force_second_half: bool=False) -> dict:
        """
        Convert the lens to a json object
        :return: the lens as a json object
        """
        if self.second_half:
            return {
                "type": "lens",
                "name": self.name,
                "z": self.z,
                "refraction_power": self.refraction_power,
                "enabled": self.enabled,
                "second_half": self.second_half.to_json()
            }
        return {
            "type": "lens",
            "name": self.name,
            "z": self.z,
            "refraction_power": self.refraction_power,
            "enabled": self.enabled
        }

    @staticmethod
    def from_json(json: dict) -> 'HalfThickLens':
        """
        Create a lens from a json object.
        :param json: json object to create the lens from
        :return: the lens created from the json object
        """
        second_half_json = json["second_half"]
        second_half = HalfThickLens(second_half_json["z"], second_half_json["refraction_power"], name=second_half_json["name"])
        second_half.enabled = second_half_json["enabled"]
        lens = HalfThickLens(json["z"], json["refraction_power"], second_half, json["name"])
        lens.enabled = json["enabled"]
        return lens
