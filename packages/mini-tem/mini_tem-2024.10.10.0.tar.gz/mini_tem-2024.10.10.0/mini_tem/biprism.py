import numpy as np

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron


class Biprism(Component):
    theta = None
    power = None
    width = None
    position = None
    sin_push_angle = None
    cos_push_angle = None
    push_angle = None
    sin_theta = None
    cos_theta = None

    def __init__(self, z: float, deflection_power: float = 0, name: str = "unknown biprism", x: float = 0, y: float = 0,
                 theta: float = 0, width: float = 0) -> None:
        """
        Create a biprism with a given deflection function
        :param z: z position of the biprism in meters
        :param deflection_power: power of the deflection
        :param name: name of the biprism
        :param x: x position of the biprism in meters
        :param y: y position of the biprism in meters
        :param theta: angle of the biprism in radians
        :param width: width of the biprism in meters
        """
        self.set_power(deflection_power)
        self.name = name
        self.set_theta(theta)
        self.set_width(width)
        self.set_position(np.array([x, y, z]))

        power_field = ComponentField('power', self.power, '', lambda power: self.set_power(power))
        theta_field = ComponentField('theta', np.rad2deg(self.theta), '°', lambda v: self.set_theta(np.deg2rad(v)))
        width_field = ComponentField('width', self.width, 'm', lambda v: self.set_width(v))
        x_field = ComponentField('x', self.position[0], 'm', lambda v: self.set_position([v, self.position[1], self.position[2]]))
        y_field = ComponentField('y', self.position[1], 'm', lambda v: self.set_position([self.position[0], v, self.position[2]]))
        z_field = ComponentField('z', self.position[2], 'm', lambda v: self.set_position([self.position[0], self.position[1], v]))

        self.fields = [power_field, theta_field, width_field, x_field, y_field, z_field]

    def __str__(self):
        return f'Biprism {self.name}\n\tposition: {self.position}\n\t' \
               f'theta: {self.theta}\n\twidth: {self.width}\n\tpower: {self.power}'

    @property
    def x(self):
        """
        X position of the biprism in meters
        """
        return self.position[0]

    @property
    def y(self):
        """
        Y position of the biprism in meters
        """
        return self.position[1]

    @property
    def z(self):
        """
        Z position of the biprism in meters
        """
        return self.position[2]

    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the biprism on the electrons by changing their velocities based on the deflection power
        :param positions: positions of the electrons
        :param velocities: velocities of the electrons
        """
        if not self.enabled:
            return

        vx, vy, indices_over_biprism = self.line_to_points_vector(positions[:, 0], positions[:, 1])
        directions = np.ones(len(positions)) * -1
        directions[indices_over_biprism] = 1
        velocities[:, :2] += self.power * directions[:, np.newaxis] * np.array(
            [self.cos_push_angle, self.sin_push_angle])
        stopped_index = np.where(np.linalg.norm(np.stack([vx, vy], axis=1), axis=1) < self.width / 2)
        velocities[stopped_index] = 0

    def apply_on_electron(self, electron: Electron) -> None:
        """
        Apply the biprism on the electron by changing its velocity based on the deflection power
        :param electron: electron to apply the biprism on
        """
        if not self.enabled:
            return
        vx, vy, over_biprism = self.line_to_points_vector(electron.position[0], electron.position[1])
        direction = 1 if over_biprism else -1
        electron.velocity[:2] += self.power * direction * np.array([self.cos_push_angle, self.sin_push_angle])
        if np.linalg.norm(np.array([vx, vy])) < self.width / 2:
            electron.velocity[2] = 0

    def line_to_points_vector(self, points_x: float or np.array, points_y: float or np.array) -> (np.array, np.array, np.array):
        """
        Compute the vector of the shortest lines from the biprism to the points as well as the distance of the points to the line
        :param points_x: points x coordinates
        :param points_y: points y coordinates
        :return:
        """
        dx = points_x - self.position[0]
        dy = points_y - self.position[1]
        rotated_y = self.position[1] - dx * self.sin_theta + dy * self.cos_theta

        proj_rotated_x = self.position[0] + dx * self.cos_theta + dy * self.sin_theta
        proj_rotated_y = np.ones_like(proj_rotated_x) * self.position[1]
        proj_reverted_x = self.position[0] + \
                          (proj_rotated_x - self.position[0]) * self.cos_theta - \
                          (proj_rotated_y - self.position[1]) * self.sin_theta
        proj_reverted_y = self.position[1] + \
                          (proj_rotated_x - self.position[0]) * self.sin_theta + \
                          (proj_rotated_y - self.position[1]) * self.cos_theta
        vx = points_x - proj_reverted_x
        vy = points_y - proj_reverted_y
        return vx, vy, rotated_y > self.position[1]

    def set_power(self, power: float) -> None:
        """
        Set the deflection power of the biprism
        :param power: power of the biprism in m.s-1
        :return:
        """
        self.power = power

    def set_width(self, width: float) -> None:
        """
        Set the width of the biprism
        :param width: width of the biprism in meters
        :return:
        """
        self.width = width

    def set_position(self, position: np.array) -> None:
        """
        Set the position of the biprism
        :param position: [x, y, z] position of the biprism in meters
        :return:
        """
        self.position = position

    def set_theta(self, theta: float) -> None:
        """
        Set the angle of the biprism inside the column
        :param theta: angle of the biprism in radians
        :return:
        """
        self.theta = theta
        self.cos_theta = np.cos(theta)
        self.sin_theta = np.sin(theta)
        # Push angle is the angle of the push force which is rotated by 90 degrees from the angle of the biprism
        self.push_angle = self.theta + np.pi / 2
        self.cos_push_angle = np.cos(self.push_angle)
        self.sin_push_angle = np.sin(self.push_angle)

    def to_json(self) -> dict:
        """
        Convert the biprism to a json object
        :return: the json object of the biprism
        """
        return {
            'type': 'biprism',
            'name': self.name,
            'position': self.position.tolist(),
            'theta': self.theta,
            'width': self.width,
            'power': self.power,
            'enabled': self.enabled,
            'height': self.height
        }

    @staticmethod
    def from_json(json: dict) -> 'Biprism':
        """
        Create a biprism from a json object
        :param json: biprism as a json object
        :return: the biprism
        """
        bp = Biprism(json['position'][2], json['power'], json['name'], json['position'][0], json['position'][1],
                       json['theta'], json['width'])
        bp.enabled = json['enabled']
        bp.height = json['height']
        return bp
