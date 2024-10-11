from abc import abstractmethod

import numpy as np

from mini_tem.electron import Electron


class Component:
    """
    Component of the TEM
    """
    z = np.inf
    height = 0
    name = "Undefined"
    fields = []
    enabled = True

    @abstractmethod
    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the component on the electrons by changing their velocities and/or position
        :param positions: positions of the electrons
        :param velocities: velocities of the electrons
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def apply_on_electron(self, electron: Electron) -> None:
        raise NotImplementedError

    def toggle(self, state) -> None:
        """
        Enable or disable the component
        :param state: True to enable, False to disable
        :return: None
        """
        self.enabled = state

    @staticmethod
    def from_json(json: dict):
        raise NotImplementedError

    def to_json(self) -> dict:
        raise NotImplementedError
