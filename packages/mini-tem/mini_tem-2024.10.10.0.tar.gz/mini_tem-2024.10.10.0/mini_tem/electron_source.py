import numpy as np
from scipy.constants import c

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron
from mini_tem.utils import find_name

MAX_DZ = c / 2
MAX_DXY = 3e-4 * MAX_DZ
SOURCE_WIDTH = 1e-6


def point_source_xy_function(n_electrons: int):
    """
    Initialize the position vectors for the electrons when they all start exactly at the source tip
    :param n_electrons: Number of electrons to fire
    :return: Positions of the electrons
    """
    return np.zeros((n_electrons, 2))


def small_square_source_xy_function(n_electrons: int):
    """
    Initialize the position vectors for the electrons when they all start in a small square around the source tip
    with a uniform distribution inside the square of width SOURCE_WIDTH
    :param n_electrons: Number of electrons to fire
    :return: Positions of the electrons
    """
    return np.random.uniform(-SOURCE_WIDTH / 2, SOURCE_WIDTH / 2, (n_electrons, 2)).reshape(n_electrons, 2)


def small_source_xy_function(n_electrons: int):
    """
    Initialize the position vectors for the electrons when they all start inside a circle around the source tip
    with a uniform distribution inside the circle
    :param n_electrons: Number of electrons to fire
    :return: Positions of the electrons
    """
    thetas = np.random.uniform(0, 2 * np.pi, n_electrons)
    dxy = np.sqrt(np.random.uniform(0, SOURCE_WIDTH / 2, n_electrons)) * np.sqrt(SOURCE_WIDTH / 2)
    dx = dxy * np.cos(thetas)
    dy = dxy * np.sin(thetas)
    return np.stack([dx, dy], axis=1)


def uniformly_spread_velocity_function(n_electrons: int):
    """
    Initialize the velocity vectors for the electrons when they all start with a uniform velocity
    perpendicular to the optical axis with a maximal speed of MAX_DXY and a z velocity of MAX_DZ
    :param n_electrons: Number of electrons to fire
    :return: Velocities of the electrons
    """
    thetas = np.random.uniform(0, 2 * np.pi, n_electrons)
    dxy = np.sqrt(np.random.uniform(0, MAX_DXY, n_electrons)) * np.sqrt(MAX_DXY)
    dx = dxy * np.cos(thetas)
    dy = dxy * np.sin(thetas)
    return np.stack([dx, dy, np.ones(n_electrons) * MAX_DZ], axis=1)


def parallel_source_velocity_function(n_electrons: int):
    """
    Initialize the velocity vectors for the electrons when they all start with a velocity parallel
    to the optical axis and a maximal speed along z of MAX_DZ
    :param n_electrons: Number of electrons to fire
    :return: Velocities of the electrons
    """
    velocities = np.zeros((n_electrons, 3), dtype=np.float64)
    velocities[:, 2] = MAX_DZ
    return velocities


def circle_source_xy_function(n_electrons: int):
    """
    Initialize the position vectors for the electrons when they all start on a circle at the source tip
    uniformly distributed on the circle
    :param n_electrons: Number of electrons to fire
    :return: Positions of the electrons
    """
    thetas = np.linspace(0, 2 * np.pi, n_electrons, False)
    dxy = np.ones(thetas.shape) * SOURCE_WIDTH / 2
    dx = dxy * np.cos(thetas)
    dy = dxy * np.sin(thetas)
    return np.stack([dx, dy], axis=1)


def circle_source_velocity_function(n_electrons: int):
    """
    Initialize the velocity vectors for the electrons when they all start with a velocity at the horizontal speed MAX_DXY
    along the circle and a speed along z of MAX_DZ
    :param n_electrons: Number of electrons to fire
    :return: Velocities of the electrons
    """
    velocities = np.zeros((n_electrons, 3), dtype=np.float64)
    velocities[:, 2] = MAX_DZ
    return velocities


def ribbon_source_xy_function(n_electrons: int):
    """
    Initialize the position vectors for the electrons when they all start on a ribbon of width SOURCE_WIDTH
    along the x-axis at the source tip
    :param n_electrons:
    :return:
    """
    dxy = np.linspace(-SOURCE_WIDTH / 2, SOURCE_WIDTH / 2, n_electrons)
    dx = dxy
    dy = dxy * 0
    return np.stack([dx, dy], axis=1)


def ribbon_source_velocity_function(n_electrons: int):
    """
    Initialize the velocity vectors for the electrons when they start with a velocity ranging from -MAX_DXY to MAX_DXY
    along the x-axis and a speed along z of MAX_DZ
    :param n_electrons:
    :return:
    """
    velocities = np.zeros((n_electrons, 3), dtype=np.float64)
    vx = np.linspace(-MAX_DXY, MAX_DXY, n_electrons)
    velocities[:, 0] = vx
    velocities[:, 2] = MAX_DZ
    return velocities


xy_functions_list = [point_source_xy_function, small_source_xy_function, small_square_source_xy_function,
                     circle_source_xy_function, ribbon_source_xy_function]
velocity_functions_list = [uniformly_spread_velocity_function, parallel_source_velocity_function,
                            circle_source_velocity_function, ribbon_source_velocity_function]


class ElectronSource(Component):
    """
    Electron source of the TEM, generates electrons with a given position and velocity
    """
    ev = 300000

    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        pass

    def apply_on_electron(self, electron: Electron) -> None:
        pass

    def __init__(self, z: float, xy_function: callable=small_source_xy_function, velocity_function: callable=uniformly_spread_velocity_function) -> None:
        """
        Initialize the electron source
        :param z: z position of the source in meters
        :param xy_function: function to generate the x and y positions of the electrons
        :param velocity_function: function to generate the velocities of the electrons
        """
        self.velocities = None
        self.positions = None
        self.electrons = None
        self.z = z
        self.xy_function = xy_function
        self.velocity_function = velocity_function
        self.name = "electron_source"

        xy_function_field = ComponentField(
            "xy function",
            xy_functions_list.index(xy_function),
            '',
            lambda i: self.set_xy_function(xy_functions_list[int(np.clip(i, 0, len(xy_functions_list) - 1))])
        )
        velocity_function_field = ComponentField(
            "velocity function",
            velocity_functions_list.index(velocity_function),
            '',
            lambda i: self.set_velocity_function(
                velocity_functions_list[int(np.clip(i, 0, len(xy_functions_list) - 1))])
        )
        self.fields = [xy_function_field, velocity_function_field]

    def init_positions_velocities(self, n_electrons: int) -> (np.array, np.array):
        """
        Initialize the positions and velocities of the electrons without creating the electrons
        :param n_electrons: Number of electrons to fire
        :return: Positions and velocities
        """
        self.positions = np.zeros((n_electrons, 3), dtype=np.float64)
        self.velocities = np.zeros((n_electrons, 3), dtype=np.float64)
        self.positions[:, :2] = self.xy_function(n_electrons)
        self.velocities = self.velocity_function(n_electrons)
        self.positions[:, 2] = self.z
        return self.positions.copy(), self.velocities.copy()

    def get_positions_velocities(self, n_electrons: int=None) -> (np.array, np.array):
        """
        Gives the positions and velocities of the electrons fired from the source
        :param n_electrons: Number of electrons to fire
        :return: Positions and velocities
        """
        if self.positions is None or (n_electrons is not None and self.positions.shape[0] != n_electrons):
            return self.init_positions_velocities(n_electrons=n_electrons)
        else:
            return self.positions.copy(), self.velocities.copy()

    def set_xy_function(self, function: callable or int) -> None:
        """
        Set the function to generate the x and y positions of the electrons
        :param function: function to generate the x and y positions of the electrons
        :return:
        """
        if isinstance(function, int):
            function = xy_functions_list[function]
        self.xy_function = function
        self.positions = None
        self.velocities = None

    def set_velocity_function(self, function: callable or int) -> None:
        """
        Set the function to generate the velocities of the electrons
        :param function: function to generate the velocities of the electrons
        :return:
        """
        if isinstance(function, int):
            function = velocity_functions_list[function]
        self.velocity_function = function
        self.positions = None
        self.velocities = None

    def to_json(self) -> dict:
        """
        Convert the source to a json object
        :return: the json object of the source
        """
        return {
            "z": self.z,
            "xy_function": self.xy_function.__name__,
            "velocity_function": self.velocity_function.__name__
        }

    @staticmethod
    def from_json(json: dict) -> 'ElectronSource':
        """
        Create a source from a json object
        :param json: source as a json object
        :return: the source
        """
        return ElectronSource(
            json["z"],
            find_name(xy_functions_list, json["xy_function"]),
            find_name(velocity_functions_list, json["velocity_function"])
        )
