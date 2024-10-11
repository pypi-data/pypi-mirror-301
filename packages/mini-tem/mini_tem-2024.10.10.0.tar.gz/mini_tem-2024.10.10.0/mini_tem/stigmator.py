import numpy as np

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron


class Stigmator(Component):
    """
    Class representing a stigmator
    """
    x_factor = 1
    y_factor = 1
    true_x_factor = 1
    true_y_factor = 1
    thetas = np.array([0, np.pi / 2])

    def __init__(self, z: float, x_factor: float, y_factor: float, theta_x: float = 0, theta_y: float = np.pi / 2,
                 name: str = "unknown stigmator"):
        """
        Create a stigmator
        :param z: z position of the center of the stigmator in meters
        :param x_factor: x factor of the stigmator
        :param y_factor: y factor of the stigmator
        :param theta_x rotation of the stigmator x component along the z-axis
        :param theta_y rotation of the stigmator y component along the z-axis
        :param name: name of the stigmator
        """
        self.name = name
        self.set_z(z)
        self.set_x_factor(x_factor)
        self.set_y_factor(y_factor)
        self.set_thetas(theta_x, theta_y)

        z_field = ComponentField('z', self.z, 'm', lambda h: self.set_z(h))
        x_factor_field = ComponentField('x factor', self.x_factor, '', lambda x: self.set_x_factor(x))
        y_factor_field = ComponentField('y factor', self.y_factor, '', lambda y: self.set_y_factor(y))
        theta_x_field = ComponentField(
            'theta_x', np.rad2deg(self.thetas[0]), '°', lambda tx: self.set_thetas(np.deg2rad(tx), float(self.thetas[1]))
        )
        theta_y_field = ComponentField(
            'theta_y', np.rad2deg(self.thetas[1]), '°', lambda ty: self.set_thetas(float(self.thetas[0]), np.deg2rad(ty))
        )

        self.fields = [x_factor_field, y_factor_field, z_field, theta_x_field, theta_y_field]

    def __str__(self):
        return f'Stigmator {self.name}\n\tposition: {self.z}\n\tx factor: {self.x_factor}\n\ty factor: {self.y_factor}'

    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the stigmator on a set of electrons
        :param positions: positions of the electrons
        :param velocities: velocities of the electrons
        :return:
        """
        if not self.enabled:
            return
        velocities[:, 0] *= self.true_x_factor
        velocities[:, 1] *= self.true_y_factor

    def apply_on_electron(self, electron: Electron) -> None:
        """
        Apply the stigmator on an electron by changing its velocity
        :param electron: electron to apply the stigmator on
        :return:
        """
        if not self.enabled:
            return
        electron.velocity[0] *= self.true_x_factor
        electron.velocity[1] *= self.true_y_factor

    @staticmethod
    def from_json(json: dict) -> 'Stigmator':
        """
        Create a stigmator from a json object
        :param json: json object
        :return: stigmator
        """
        stigmator = Stigmator(json["z"], json["x_factor"], json["y_factor"], json["thetas"][0], json["thetas"][1],
                              json["name"])
        stigmator.enabled = json["enabled"]
        stigmator.compute_true_factors()
        return stigmator

    def to_json(self) -> dict:
        """
        Convert the stigmator to a json object
        :return: the stigmator as a json object
        """
        return {
            "type": "stigmator",
            "name": self.name,
            "z": self.z,
            "x_factor": self.x_factor,
            "y_factor": self.y_factor,
            "thetas": self.thetas,
            "enabled": self.enabled
        }

    @property
    def theta_x(self):
        """
        X rotation of the stigmator along the z-axis
        :return: x rotation of the stigmator along the z-axis
        """
        return self.thetas[0]

    @property
    def theta_y(self):
        """
        Y rotation of the stigmator along the z-axis
        :return: y rotation of the stigmator along the z-axis
        """
        return self.thetas[1]

    def set_z(self, z: float) -> None:
        """
        Set the z position of the stigmator
        :param z: z position of the stigmator in meters
        :return:
        """
        self.z = z

    def set_x_factor(self, x_factor: float) -> None:
        """
        Set the x factor of the stigmator
        :param x_factor: x factor of the stigmator
        :return:
        """
        self.x_factor = x_factor
        self.compute_true_factors()

    def set_y_factor(self, y_factor: float) -> None:
        """
        Set the y factor of the stigmator
        :param y_factor: y factor of the stigmator
        :return:
        """
        self.y_factor = y_factor
        self.compute_true_factors()

    def set_thetas(self, theta_x: float, theta_y: float) -> None:
        """
        Set the rotation of the stigmator along the z-axis
        :param theta_x: rotation of the stigmator x-axis along the z-axis
        :param theta_y: rotation of the stigmator y-axis along the z-axis
        :return:
        """
        self.thetas[0] = theta_x
        self.thetas[1] = theta_y
        self.compute_true_factors()

    def compute_true_factors(self) -> None:
        """
        Compute the true factors of the stigmator (taking into account the rotation)
        :return:
        """
        self.true_x_factor = self.x_factor * np.cos(self.thetas[0]) + self.y_factor * np.sin(self.thetas[0])
        self.true_y_factor = self.x_factor * np.cos(self.thetas[1]) + self.y_factor * np.sin(self.thetas[1])
