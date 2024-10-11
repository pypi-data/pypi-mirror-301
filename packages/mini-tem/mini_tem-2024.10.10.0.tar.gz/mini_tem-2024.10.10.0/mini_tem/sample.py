import numpy as np

from mini_tem.component import Component
from mini_tem.component_field import ComponentField
from mini_tem.electron import Electron
from mini_tem.utils import find_name

ROD_REPULSION_POWER = -2e-3

# write cemes using rods
cemes_shape = [
    # C
    [[-2.5, -1], [0, 1], 2],
    [[-2.5, -1], [1, 0], 0.5],
    [[-2.5, 1], [1, 0], 0.5],
    # E
    [[-1.5, -1], [0, 1], 2],
    [[-1.5, -1], [1, 0], 0.5],
    [[-1.5, 0], [1, 0], 0.5],
    [[-1.5, 1], [1, 0], 0.5],
    # M
    [[-0.5, -1], [0, 1], 2],
    [[0.5, -1], [0, 1], 2],
    [[0, 0.5], [1, 1], np.sqrt(0.5)],
    [[0, 0.5], [-1, 1], np.sqrt(0.5)],
    # E
    [[1, -1], [0, 1], 2],
    [[1, -1], [1, 0], 0.5],
    [[1, 0], [1, 0], 0.5],
    [[1, 1], [1, 0], 0.5],
    # S
    [[2, -1], [1, 0], 0.5],
    [[2.5, -1], [0, 1], 1],
    [[2, 0], [1, 0], 0.5],
    [[2, 0], [0, 1], 1],
    [[2, 1], [1, 0], 0.5],
]


def default_shape_function(sample_position: np.array, electron_positions: np.array, electron_velocities: np.array,
                           scale: float, tilt: np.array = np.array([0, 0])) -> None:
    """
    Default shape function for the sample, it is an arrow pointing to the right
    :param sample_position: position of the sample in m
    :param electron_positions: positions of the electrons
    :param electron_velocities: velocities of the electrons
    :param scale: scale of the sample
    :param tilt: tilt of the sample (not supported)
    :return: 
    """
    tilt += 0
    arrow_shaft_width = 0.2 * scale
    arrow_shaft_length = 1 * scale
    arrow_head_width = 0.4 * scale
    arrow_head_length = 0.4 * scale
    dx = electron_positions[:, 0] - sample_position[0]
    dy = electron_positions[:, 1] - sample_position[1]

    arrow_shaft_indexes = np.where(
        (-(arrow_shaft_length + arrow_head_length) < dx)
        * (dx < -arrow_head_length)
        * (-arrow_shaft_width / 2 < dy)
        * (dy < arrow_shaft_width / 2)
    )

    arrow_head_indexes = np.where(
        (-arrow_head_length < dx)
        * (dx < 0)
        * (arrow_head_width / arrow_head_length * dx < dy)
        * (dy < arrow_head_width / -arrow_head_length * dx)
    )

    electron_velocities[arrow_shaft_indexes, 2] = 0
    electron_velocities[arrow_head_indexes, 2] = 0

def normalize_array(v: np.array) -> np.array:
    """
    Normalize an array of vectors
    :param v: the array of vectors to be normalized
    :return: array of normalized vectors
    """
    norm =  np.linalg.norm(v, axis=1)[:, np.newaxis]
    return v / norm


def array_dist(closest_approach_rod: np.array, points: np.array) -> np.array:
    """
    Compute the distance between an array of points and an array of closest approach points on a rod
    :param closest_approach_rod: points on the rods closest to the point with the same index
    :param points: points to compute the distance to
    :return: array of distances between the points and the closest approach points
    """
    dist = np.sqrt(np.sum((closest_approach_rod - points) ** 2, axis=1))
    return dist


def before_or_after(dist_r_to_c0: np.array, dist_r_to_c_end: np.array, l: float) -> (np.array, np.array):
    """
    Find if the closest approach point is before or after the rod ends for an arbitrary number of electrons
    :param dist_r_to_c0: distance between the closest approach point and the rod start
    :param dist_r_to_c_end: distance between the closest approach point and the rod end
    :param l: length of the rod
    :return: boolean array for whether the closest approach point is before the rod start, after the rod end
    """
    before_c0 = (dist_r_to_c_end > l) * (dist_r_to_c_end > dist_r_to_c0)
    after_c_end = (dist_r_to_c0 > l) * (dist_r_to_c_end < dist_r_to_c0)
    return before_c0, after_c_end


def electron_vector_to_rod(c0: np.array, dc: np.array, l: np.array, r: np.array, p: np.array, v: np.array) -> (
        np.array, np.array):
    """
    Find the vector between the closest points of the electron path and the rod
    as well as if these points are inside the rod or outside for an arbitrary number of electrons
    and rods
    :param c0: Starting point of the rods
    :param dc: Direction vector of the rods
    :param l: Lengths of the rods
    :param r: Radiuses of the rods
    :param p: Starting point of the electrons
    :param v: Direction vector of the electrons
    :return: Vectors between the closest points of the electron path and the rod,
    if these points are inside the rod or outside
    """
    nv1 = normalize_array(dc)
    nv2 = normalize_array(v)

    l_mult = np.tile(l, (nv1.shape[1], 1))
    c_end = c0 + l_mult.T * nv1

    cn = normalize_array(np.cross(nv1, nv2))

    p_minus_c0 = p - c0

    dot_nv1 = np.einsum('ij,ij->function', p_minus_c0, nv1)
    dot_cn = np.einsum('ij,ij->function', p_minus_c0, cn)
    dot_nv2 = np.einsum('ij,ij->function', p_minus_c0, nv2)

    rejection_1 = p_minus_c0 - (dot_nv1[:, np.newaxis] * nv1) - (dot_cn[:, np.newaxis] * cn)
    rejection_2 = -p_minus_c0 + (dot_nv2[:, np.newaxis] * nv2) + (dot_cn[:, np.newaxis] * cn)

    dot_nv1_rej = np.einsum('ij,ij->function', nv1, normalize_array(rejection_2))
    dot_nv2_rej = np.einsum('ij,ij->function', nv2, normalize_array(rejection_1))

    closest_approach_traj = p - (nv2.T * np.linalg.norm(rejection_1, axis=1) / dot_nv2_rej).T
    closest_approach_rod = c0 - (nv1.T * np.linalg.norm(rejection_2, axis=1) / dot_nv1_rej).T

    dist_r_to_c0 = array_dist(closest_approach_rod, c0)
    dist_r_to_c_end = array_dist(closest_approach_rod, c_end)
    dist_e_to_r = array_dist(closest_approach_traj, closest_approach_rod)
    dist_e_to_c0 = array_dist(closest_approach_traj, c0)
    dist_e_to_c_end = array_dist(closest_approach_traj, c_end)

    approach_before_c0, approach_after_c_end = before_or_after(dist_r_to_c0, dist_r_to_c_end, l)
    approach_between_c0_c_end = ~(approach_before_c0 | approach_after_c_end)
    approach_outside_rod = ((dist_e_to_r > r) * approach_between_c0_c_end) | (
            (dist_e_to_c0 > r) * (dist_e_to_c_end > r) * ~approach_between_c0_c_end
    )

    vector_e_to_r = closest_approach_rod - closest_approach_traj
    vector_e_to_c0 = c0 - closest_approach_traj
    vector_e_to_c_end = c_end - closest_approach_traj

    electron_vector = (
            vector_e_to_r * np.tile(approach_between_c0_c_end, 3).reshape(-1, 3)
            + vector_e_to_c0 * np.tile(approach_before_c0, 3).reshape(-1, 3)
            + vector_e_to_c_end * np.tile(approach_after_c_end, 3).reshape(-1, 3)
    )

    return electron_vector, approach_outside_rod


def rod_3d_shape_function(sample_position: np.array, electron_positions: np.array, electron_velocities: np.array,
                          scale: float, tilt: np.array = np.array([0, 0])) -> None:
    """
    Default shape function for the sample, it is an arrow pointing to the right
    :param sample_position: position of the sample in m
    :param electron_positions: positions of the electrons
    :param electron_velocities: velocities of the electrons
    :param scale: scale of the sample
    :param tilt: tilt of the sample (not supported)
    :return: None
    """
    tilt += 0
    width = 0.2 * scale
    length = 1 * scale

    rod_start = np.array([sample_position[0] - length / 2, sample_position[1] - width / 2, sample_position[2] + width])
    rod_starts = np.tile(rod_start, (electron_positions.shape[0], 1))

    rod_direction = np.array([1, 1, 0])
    rod_directions = np.tile(rod_direction, (electron_positions.shape[0], 1))

    lengths = np.tile(length, (electron_positions.shape[0]))
    radiuses = np.tile(width / 2, (electron_positions.shape[0]))

    electron_vectors, electrons_outside = electron_vector_to_rod(
        rod_starts,
        rod_directions,
        lengths,
        radiuses,
        electron_positions,
        electron_velocities
    )

    electron_velocities -= np.clip(np.reciprocal(electron_vectors), -1 / width, 1 / width) * ROD_REPULSION_POWER
    electron_velocities[~electrons_outside, 2] = 0



def cemes_shape_function(sample_position: np.array, electron_positions: np.array, electron_velocities: np.array,
                         scale: float, tilt: np.array = np.array([0, 0])) -> None:
    """
    Default shape function for the sample, it is an arrow pointing to the right
    :param sample_position: position of the sample in m
    :param electron_positions: positions of the electrons
    :param electron_velocities: velocities of the electrons
    :param scale: scale of the sample
    :param tilt: tilt of the sample
    :return: None
    """
    width = 0.2 * scale
    electron_vector_sum = None

    for rod in cemes_shape:
        rod_start = rod[0]
        rod_start = np.array(rod_start)
        rod_start = np.append(rod_start, [-width])
        # rotate rot_start based on tilt around x and y axes
        rod_start = np.array([
            rod_start[0] * np.cos(tilt[1]) - rod_start[2] * np.sin(tilt[1]),
            rod_start[1] * np.cos(tilt[0]) + rod_start[2] * np.sin(tilt[0]),
            rod_start[0] * np.sin(tilt[0]) + rod_start[1] * np.sin(tilt[1]) + rod_start[2] * np.cos(tilt[1]) * np.sin(tilt[0])
        ])
        rod_start = sample_position + rod_start * scale
        rod_direction = rod[1]
        rod_direction = np.array(rod_direction)
        rod_direction = np.append(rod_direction, [0])
        # rotate rod_direction based on tilt around x and y axes
        rod_direction = np.array([
            rod_direction[0] * np.cos(tilt[1]) - rod_direction[2] * np.sin(tilt[1]),
            rod_direction[1] * np.cos(tilt[0]) + rod_direction[2] * np.sin(tilt[0]),
            rod_direction[0] * np.sin(tilt[0]) + rod_direction[1] * np.sin(tilt[1]) + rod_direction[2] * np.cos(tilt[1]) * np.sin(tilt[0])
        ])
        rod_length = rod[2] * scale

        rod_starts = np.tile(rod_start, (electron_positions.shape[0], 1))
        rod_directions = np.tile(rod_direction, (electron_positions.shape[0], 1))

        lengths = np.tile(rod_length, (electron_positions.shape[0]))
        radiuses = np.tile(width / 2, (electron_positions.shape[0]))

        electron_vectors, electrons_outside = electron_vector_to_rod(
            rod_starts,
            rod_directions,
            lengths,
            radiuses,
            electron_positions,
            electron_velocities
        )

        if electron_vector_sum is None:
            electron_vector_sum = normalize_array(electron_vectors) * np.clip(
                1 / np.linalg.norm(electron_vectors, axis=1), -1 / width, 1 / width
            )[:, np.newaxis]
        else:
            electron_vector_sum += normalize_array(electron_vectors) * np.clip(
                1 / np.linalg.norm(electron_vectors, axis=1), -1 / width, 1 / width
            )[:, np.newaxis]
        electron_velocities[~electrons_outside, 2] = 0

    electron_velocities -= electron_vector_sum * ROD_REPULSION_POWER


def scattering_arrow_shape_function(sample_position: np.array, electron_positions: np.array, electron_velocities: np.array,
                           scale: float, tilt: np.array = np.array([0, 0])) -> None:
    """
    Default shape function for the sample, it is an arrow pointing to the right
    :param sample_position: position of the sample in m
    :param electron_positions: positions of the electrons
    :param electron_velocities: velocities of the electrons
    :param scale: scale of the sample
    :param tilt: tilt of the sample (not supported)
    :return: None
    """
    tilt += 0
    arrow_shaft_width = 0.2 * scale
    arrow_shaft_length = 1 * scale
    arrow_head_width = 0.4 * scale
    arrow_head_length = 0.4 * scale
    dx = electron_positions[:, 0] - sample_position[0]
    dy = electron_positions[:, 1] - sample_position[1]

    arrow_shaft_indexes = np.where(
        (-(arrow_shaft_length + arrow_head_length) < dx)
        * (dx < -arrow_head_length)
        * (-arrow_shaft_width / 2 < dy)
        * (dy < arrow_shaft_width / 2)
    )[0]

    arrow_head_indexes = np.where(
        (-arrow_head_length < dx)
        * (dx < 0)
        * (arrow_head_width / arrow_head_length * dx < dy)
        * (dy < arrow_head_width / -arrow_head_length * dx)
    )[0]

    factor = 0.1

    chance_electron_stopped = 0.25
    shaft_filter = np.random.random(arrow_shaft_indexes.shape[0]) > chance_electron_stopped
    head_filter = np.random.random(arrow_head_indexes.shape[0]) > chance_electron_stopped

    std_x, std_y = np.std(electron_velocities[:, 0]), np.std(electron_velocities[:, 1])
    deviation_x, deviation_y = std_x * factor, std_y * factor
    electron_velocities[arrow_shaft_indexes, 0] += np.random.normal(0, deviation_x, (len(arrow_shaft_indexes)))
    electron_velocities[arrow_head_indexes, 0] += np.random.normal(0, deviation_x, (len(arrow_head_indexes)))
    electron_velocities[arrow_shaft_indexes, 1] += np.random.normal(0, deviation_y, (len(arrow_shaft_indexes)))
    electron_velocities[arrow_head_indexes, 1] += np.random.normal(0, deviation_y, (len(arrow_head_indexes)))

    electron_velocities[arrow_shaft_indexes, 2] *= shaft_filter

    electron_velocities[arrow_head_indexes, 2] *= head_filter


shape_functions = [default_shape_function, rod_3d_shape_function, cemes_shape_function, scattering_arrow_shape_function]


class Sample(Component):
    """
    Class representing a sample in the TEM simulation
    """
    scale = 1
    position = np.array([0, 0, 0])
    tilt = np.array([0, 0])

    def __init__(self, z: float, scale: float = 1,
                 x: float = 0, y: float = 0,
                 x_tilt: float = 0, y_tilt: float = 0,
                 name: str = "unknown sample"):
        """
        Create a sample
        :param z: z position of the sample in meters
        :param scale: scale of the sample in meters
        :param x: x position of the sample in meters
        :param y: y position of the sample in meters
        :param name: name of the sample
        """
        self.name = name
        self.set_position(np.array([x, y, z]))
        self.shape_function = shape_functions[2]
        self.set_scale(scale)
        self.set_tilt(np.array([x_tilt, y_tilt]))

        scale_field = ComponentField("scale", scale, 'm', lambda s: self.set_scale(s))
        x_field = ComponentField("x", x, 'm',
                                 lambda px: self.set_position(np.array([px, self.position[1], self.position[2]])))
        y_field = ComponentField("y", y, 'm',
                                 lambda py: self.set_position(np.array([self.position[0], py, self.position[2]])))
        z_field = ComponentField("z", z, 'm',
                                 lambda pz: self.set_position(np.array([self.position[0], self.position[1], pz])))
        shape_function_field = ComponentField("shape function", shape_functions.index(self.shape_function), '',
                                              lambda i: self.set_shape_function(int(i)))
        tilt_x_field = ComponentField("tilt x", x_tilt, '°', lambda px: self.set_tilt(np.array([np.deg2rad(px), self.tilt[1]])))
        tilt_y_field = ComponentField("tilt y", y_tilt, '°', lambda py: self.set_tilt(np.array([self.tilt[0], np.deg2rad(py)])))

        self.fields = [scale_field, x_field, y_field, shape_function_field, tilt_x_field, tilt_y_field,
                       z_field, shape_function_field]

    def __str__(self):
        return f'Sample {self.name}\n\tposition: {self.position}\n\tscale: {self.scale}, ' \
               f'tilt: {self.tilt}, shape: {self.shape_function.__name__}'

    def apply_on_electrons(self, positions: np.array, velocities: np.array) -> None:
        """
        Apply the sample on the electrons
        :param positions: positions of the electrons
        :param velocities: velocities of the electrons
        :return: None
        """
        if not self.enabled:
            return
        self.shape_function(self.position, positions, velocities, self.scale, self.tilt)

    def apply_on_electron(self, electron: Electron) -> None:
        """
        Apply the sample on the electron by changing its position and velocity
        :param electron: electron to apply the sample on
        :return: None
        """
        if not self.enabled:
            return
        self.shape_function(self.position, np.array([electron.position]), np.array([electron.velocity]), self.scale,
                            self.tilt)

    @property
    def x(self):
        """
        X position of the sample in meters
        :return: x position of the sample
        """
        return self.position[0]

    @property
    def y(self):
        """
        Y position of the sample in meters
        :return: y position of the sample
        """
        return self.position[1]

    @property
    def z(self):
        """
        Z position of the sample in meters
        :return: z position of the sample
        """
        return self.position[2]

    @property
    def tilt_x(self):
        """
        X tilt of the sample in radians
        :return: x tilt of the sample
        """
        return self.tilt[0]

    @property
    def tilt_y(self):
        """
        Y tilt of the sample in radians
        :return: y tilt of the sample
        """
        return self.tilt[1]

    def set_position(self, position: np.array) -> None:
        """
        Set the position of the sample
        :param position: position of the sample in meters (x, y, z)
        :return:
        """
        self.position = position

    def set_scale(self, scale: float) -> None:
        """
        Set the scale of the sample
        :param scale: scale of the sample in meters
        :return:
        """
        self.scale = scale

    def to_json(self) -> dict:
        """
        Convert the sample to a json object
        :return: the json object of the sample
        """
        return {
            'type': 'sample',
            'name': self.name,
            'position': self.position.tolist(),
            'scale': self.scale,
            'enabled': self.enabled,
            'shape_function': self.shape_function.__name__,
            'height': self.height,
            'tilt': self.tilt.tolist(),
        }

    @staticmethod
    def from_json(json: dict) -> 'Sample':
        """
        Create a sample from a json object
        :param json: sample as a json object
        :return: the sample
        """
        sample = Sample(z=json['position'][2], scale=json['scale'],
                        x=json['position'][0], y=json['position'][1],
                        x_tilt=json['tilt'][0], y_tilt=json['tilt'][1],
                        name=json['name'])
        sample.shape_function = shape_functions[find_name(shape_functions, json['shape_function'])]
        sample.enabled = json['enabled']
        sample.height = json['height']
        return sample

    def set_shape_function(self, shape_function: int or callable) -> None:
        """
        Set the shape function of the sample
        :param shape_function: shape function or index of the shape function
        :return:
        """
        if isinstance(shape_function, int):
            self.shape_function = shape_functions[shape_function]
        else:
            self.shape_function = shape_function

    def set_tilt(self, tilt: np.array) -> None:
        """
        Set the tilt of the sample
        :param tilt: tilt of the sample (x, y) in radians
        :return:
        """
        self.tilt = tilt
