import numpy as np

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron


class Deflector(Component):
    """
    Deflect the beam around a pivot point so that a parallel and centered beam will pass through the pivot point with
    the desired angle
    """
    pivot_z = 0
    theta = np.zeros(2)

    def __init__(self, z: float, pivot_z: float, theta_x: float, theta_y, name: str = "unknown tilter") -> None:
        """
        Tilt the beam around a pivot point so that a parallel and centered beam will pass through the pivot point with
        the desired angle
        :param z: z position of the shifter in meters
        :param pivot_z: z position of the pivot point in meters
        :param theta_x: tilt of the beam around x-axis in radians
        :param theta_y: tilt of the beam around y-axis in radians
        :param name: name of the shifter
        """
        self.name = name
        self.set_z(z)
        self.set_pivot(pivot_z)
        self.set_theta(theta_x, theta_y)

        z_field = ComponentField('z', self.z, 'm', lambda v: self.set_z(v))
        pivot_z_field = ComponentField('pivot_z', self.pivot_z, 'm', lambda pz: self.set_pivot(pz))
        theta_x_field = ComponentField(
            'theta_x', np.rad2deg(self.theta[0]), '°', lambda tx: self.set_theta(np.deg2rad(tx), float(self.theta[1]))
        )
        theta_y_field = ComponentField(
            'theta_y', np.rad2deg(self.theta[1]), '°', lambda ty: self.set_theta(float(self.theta[0]), np.deg2rad(ty))
        )

        self.fields = [z_field, theta_x_field, theta_y_field, pivot_z_field]

    def __str__(self):
        return f'Deflector {self.name}\n\tz: {self.z}\n\tpivot: {self.pivot_z}\n\t' \
                f'theta: {self.theta}'

    def apply_on_electron(self, electron: Electron) -> None:
        """
        Apply the deflector on the electron by changing its velocity
        :param electron: electron to app²ly the deflector on
        :return: 
        """
        if not self.enabled or electron.position[2] != self.z:
            return
        dxy = np.sin(self.theta) * self.pivot_z
        electron.position[:2] += dxy
        dv_xy = np.sin(self.theta) * electron.velocity[2]
        electron.velocity[:2] += dv_xy

    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the deflector on the electrons by changing their positions and velocities
        :param positions: positions of the electrons
        :param velocities: velocities of the electrons
        :return: 
        """
        if not self.enabled:
            return
        dxy = np.sin(self.theta) * self.pivot_z
        positions[:, 0] += dxy[0]
        positions[:, 1] += dxy[1]
        dv_x = velocities[:, 0] * np.sin(self.theta[0])
        dv_y = velocities[:, 1] * np.sin(self.theta[1])
        velocities[:, 0] += dv_x
        velocities[:, 1] += dv_y

    @property
    def theta_x(self):
        """
        Tilt of the beam around x-axis in radians
        :return: tilt of the beam around x-axis in radians
        """
        return self.theta[0]

    @property
    def theta_y(self):
        """
        Tilt of the beam around y-axis in radians
        :return: tilt of the beam around y-axis in radians
        """
        return self.theta[1]

    def set_z(self, z: float) -> None:
        """
        Set the z position of the deflector
        :param z: z position of the deflector in m
        :return: 
        """
        self.z = z

    def set_pivot(self, pivot_z: float) -> None:
        """
        Set the pivot point of the deflector
        :param pivot_z: z position of the pivot point in m
        :return: 
        """
        self.pivot_z = pivot_z

    def set_theta(self, theta_x: float, theta_y: float) -> None:
        """
        Set the tilt of the beam around x and y-axis
        :param theta_x: tilt of the beam at the pivot point around x-axis in radians
        :param theta_y: tilt of the beam at the pivot point around y-axis in radians
        :return: 
        """
        self.theta = np.array([theta_x, theta_y])

    @staticmethod
    def from_json(json: dict) -> 'Deflector':
        """
        Create a deflector from a json object
        :param json: deflector as a json object
        :return: the deflector
        """
        return Deflector(json['z'], json['pivot_z'], json['theta_x'], json['theta_y'], json['name'])

    def to_json(self) -> dict:
        """
        Convert the deflector to a json object
        :return: the json object of the deflector
        """
        return {
            'type': 'deflector',
            'z': self.z,
            'pivot_z': self.pivot_z,
            'theta_x': self.theta[0],
            'theta_y': self.theta[1],
            'name': self.name
        }

