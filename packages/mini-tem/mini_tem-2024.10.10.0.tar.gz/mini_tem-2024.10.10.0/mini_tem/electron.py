import numpy as np


class Electron:
    def __init__(self) -> None:
        """
        Create an electron with a position and velocity
        """
        self.position = np.array([0, 0, 0])
        self.velocity = np.array([0, 0, 0])

    def step(self, dt: float) -> None:
        """
        Step the electron forward in time by dt
        :param dt: time in seconds
        :return: None
        """
        self.position += self.velocity * dt

    def z_step(self, dz: float or np.array) -> None:
        """
        Step the electron forward in z by dz
        :param dz: distance in meters
        :return: None
        """
        dt = dz / self.velocity[2]
        self.step(dt)

    def accelerate(self, acceleration: np.array) -> None:
        """
        Accelerate the electron by adding the acceleration to the velocity
        :param acceleration: acceleration in m.s-2
        :return: None
        """
        self.velocity += acceleration

    @property
    def is_stopped(self) -> bool:
        """
        Check if the electron is stopped
        :return: True if the electron is stopped, False otherwise
        """
        return self.velocity[2] == 0

    def __copy__(self):
        new_electron = Electron()
        new_electron.position = self.position.copy()
        new_electron.velocity = self.velocity.copy()
        return new_electron

    def __str__(self):
        return f'Electron\n\tposition: {self.position}\n\tvelocity: {self.velocity}'
