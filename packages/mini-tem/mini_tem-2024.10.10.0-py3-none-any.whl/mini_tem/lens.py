import numpy as np

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron
from mini_tem.utils import z_step


class Lens(Component):
    z_center = 0
    focal_length = 0
    width = 0

    def __init__(self, z: float, focal_length: float, name: str = "unknown lens", width: float = 0,
                 current_direction: int=1, x: float = 0, y: float = 0) -> None:
        """
        Create a lens with a given focal length
        :param z: z position of the center of the lens in meters
        :param focal_length: focal length of the lens in meters
        :param name: name of the lens
        :param width: width of the lens in meters
        :param current_direction: direction of the current in the lens
        :param x: x position of the lens in meters
        :param y: y position of the lens in meters
        """
        self.name = name
        self.set_z(z)
        self.x = x
        self.y = y
        self.set_focal_length(focal_length)
        self.set_width(width)
        self.current_direction = current_direction

        z_field = ComponentField('z', self.z_center, 'm', lambda h: self.set_z(h))
        x_field = ComponentField('x', self.x, 'm', lambda h: self.set_x(h))
        y_field = ComponentField('y', self.y, 'm', lambda h: self.set_y(h))
        focal_length_field = ComponentField('focal length', self.focal_length, 'm',
                                            lambda fc: self.set_focal_length(fc))
        width_field = ComponentField('width', self.width, 'm', lambda w: self.set_width(w))

        self.fields = [focal_length_field, width_field, x_field, y_field, z_field]

    def __str__(self):
        return f'Lens {self.name}\n\tposition: {self.z_center}\n\tfocal length: {self.focal_length}'

    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the component on the electrons by changing their velocities and/or position
        :param positions: positions of the electrons
        :param velocities: velocities of the electrons
        :return:
        """
        if not self.enabled:
            return
        # Compute the positions of the electrons until they reach the lens center without changing their courses
        z_step(positions, velocities, self.width/2)
        # Change velocity based on focal length, velocities and positions
        velocities[:, 0] = velocities[:, 0] - ((positions[:, 0] - self.x) / self.focal_length * velocities[:, 2].reshape(-1, 1))
        velocities[:, 1] = velocities[:, 1] - ((positions[:, 1] - self.y) / self.focal_length * velocities[:, 2].reshape(-1, 1))
        # Rotate the positions and velocities vector based on focal length to simulate larmor rotation
        theta = 2 * np.pi / np.sqrt(self.focal_length) / 100 * self.current_direction # 0 #todo remove for rotation
        positions[:, 0], positions[:, 1] = \
            positions[:, 0] * np.cos(theta) + positions[:, 1] * np.sin(theta), \
            positions[:, 0] * (-np.sin(theta)) + positions[:, 1] * np.cos(theta)
        velocities[:, 0], velocities[:, 1] = \
            velocities[:, 0] * np.cos(theta) + velocities[:, 1] * np.sin(theta), \
            velocities[:, 0] * (-np.sin(theta)) + velocities[:, 1] * np.cos(theta)
        # Compute the positions of the electrons until they reach the end of the length without changing their courses
        z_step(positions, velocities, self.width/2)

    def apply_on_electron(self, electron: Electron) -> None:
        if not self.enabled:
            return
        electron.velocity[0] = electron.velocity[0] - ((electron.position[0] - self.x) / self.focal_length * electron.velocity[2])
        electron.velocity[1] = electron.velocity[1] - ((electron.position[1] - self.x) / self.focal_length * electron.velocity[2])
        theta = 1 * 2 * np.pi / self.focal_length / 100 * self.current_direction
        electron.position[0], electron.position[1] = \
            electron.position[0] * np.cos(theta) + electron.position[1] * np.sin(theta), \
            electron.position[0] * -np.sin(theta) + electron.position[1] * np.cos(theta)
        electron.velocity[0], electron.velocity[1] = \
            electron.velocity[0] * np.cos(theta) + electron.velocity[1] * np.sin(theta), \
            electron.velocity[0] * -np.sin(theta) + electron.velocity[1] * np.cos(theta)
        electron.position[2] = electron.position[2] + self.width

    def set_focal_length(self, focal_length: float) -> None:
        """
        Set the focal length of the lens
        :param focal_length: focal length of the lens in meters
        :return:
        """
        self.focal_length = focal_length

    def set_z(self, z: float) -> None:
        """
        Set the z position of the lens
        :param z: z position of the lens in meters
        :return:
        """
        self.z = z - self.width / 2
        self.z_center = z

    def set_x(self, x) -> None:
        """
        Set the x position of the lens
        :param x: x position of the lens in meters
        :return:
        """
        self.x = x

    def set_y(self, y) -> None:
        """
        Set the y position of the lens
        :param y: y position of the lens in meters
        :return:
        """
        self.y = y

    def set_width(self, width: float) -> None:
        """
        Set the width of the lens (along the z axis)
        :param width: width of the lens in meters
        :return:
        """
        self.width = width
        self.z = self.z_center - self.width / 2

    def to_json(self) -> dict:
        """
        Convert the lens to a json object
        :return: the lens as a json object
        """
        return {
            "type": "lens",
            "name": self.name,
            "z": self.z_center,
            "focal_length": self.focal_length,
            "width": self.width,
            "enabled": self.enabled,
            "height": self.height,
        }

    @staticmethod
    def from_json(json: dict)-> 'Lens':
        """
        Create a lens from a json object
        :param json: the json object to create the lens from
        :return: the lens created from the json object
        """
        lens = Lens(json["z"], json["focal_length"], json["name"], json["width"])
        lens.enabled = json["enabled"]
        lens.height = json["height"]
        return lens
