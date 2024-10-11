import numpy as np


def find_name(object_list: list, name: str):
    """
    Find an object in a list by its name
    :param object_list: list of objects
    :param name: name of the object to find
    :return: the object if found, None otherwise
    """
    for item in object_list:
        if item.__name__ == name:
            return item
    return None


def z_step(positions: np.array, velocities: np.array, dz: float) -> None:
    """
    Move the electrons by dz along the z axis and update their positions and velocities
    :param positions: positions of the electrons
    :param velocities: velocities of the electrons
    :param dz: step along the z axis
    :return:
    """
    stopped_electrons = velocities[:, 2] == 0
    velocities[stopped_electrons] = 0
    positions[~stopped_electrons, 2] += dz
    positions[~stopped_electrons, :2] += velocities[~stopped_electrons, :2] * dz
