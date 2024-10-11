import json
from os import PathLike

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from mini_tem.aperture import Aperture
from mini_tem.bipole import Bipole
from mini_tem.biprism import Biprism
from mini_tem.component import Component
from mini_tem.deflector import Deflector
from mini_tem.electron_source import ElectronSource, uniformly_spread_velocity_function, \
    small_source_xy_function
from mini_tem.half_thick_lens import HalfThickLens
from mini_tem.lens import Lens
from mini_tem.sample import Sample
from mini_tem.shifter import Shifter
from mini_tem.stigmator import Stigmator
from mini_tem.tilter import Tilter


def set_wobbled_fl(original_fl: float, lens: Lens, maximum_wobble: float, i: int, n: int, linear: bool) -> None:
    """
    Set the focal length of the lens depending on the desired wobble
    :param original_fl: original value of the lens focal length
    :param lens: lens component
    :param maximum_wobble: maximum modification of the focal length in percent
    :param i: how far the new value will be from the original value
    :param n: how far is the maximum wobble
    :param linear: whether the scale is linear or exponential
    :return:
    """
    if i == 0:
        lens.focal_length = original_fl
    else:
        if linear:
            lens.focal_length = original_fl * (1 + maximum_wobble * i / n)
        else:
            sign = 1 if i >= 0 else -1
            lens.focal_length = original_fl * (1 + maximum_wobble / 2 ** abs(n - i) * sign)


def set_wobbled_sp(original_rp: float, half_lens: HalfThickLens, maximum_wobble: float, i: int, n: int, linear: bool) -> None:
    """
    Set the refraction power the thick lens surfaces depending on the desired wobble
    :param original_rp: original value of the lens refraction power
    :param half_lens: half thick lens component
    :param maximum_wobble: maximum modification of the refraction power in percent
    :param i: how far the new value will be from the original value
    :param n: how far is the maximum wobble
    :param linear: whether the scale is linear or exponential
    :return:
    """
    if i == 0:
        half_lens.refraction_power = original_rp
    else:
        if linear:
            half_lens.refraction_power = original_rp * (1 + maximum_wobble * i / n)
        else:
            sign = 1 if i >= 0 else -1
            half_lens.refraction_power = original_rp * (1 + maximum_wobble / 2 ** abs(n - i) * sign)


def set_wobbled_x_factor(original_sp: float, stigmator: Stigmator, maximum_wobble: float, i: int, n: int, linear: bool) -> None:
    """
    Set the x factor of the stigmator depend on the desired wobble
    :param original_sp: original value of the stigmator x factor
    :param stigmator: stigmator component
    :param maximum_wobble: maximum modification of the x factor in percent
    :param i: how far the new value will be from the original value
    :param n: how far is the maximum wobble
    :param linear: whether the scale is linear or exponential
    :return:
    """
    if i == 0:
        stigmator.x_factor = original_sp
    else:
        if linear:
            stigmator.x_factor = original_sp * (1 + maximum_wobble * i / n)
        else:
            sign = 1 if i >= 0 else -1
            stigmator.x_factor = original_sp * (1 + maximum_wobble / 2 ** abs(n - i) * sign)

def set_wobbled_power(original_power: float, deflector_or_tilter: Deflector or Tilter, maximum_wobble: float, i: int, n: int, linear: bool) -> None:
    """
    Set the power of the deflector or tilter depending on the desired wobble
    :param original_power: original value of the deflector or tilter power
    :param deflector_or_tilter: deflector or tilter component
    :param maximum_wobble:  maximum modification of the power in percent
    :param i: how far the new value will be from the original value
    :param n: how far is the maximum wobble
    :param linear: whether the scale is linear or exponential
    :return:
    """
    if i == 0:
        deflector_or_tilter.power = original_power
    else:
        if linear:
            deflector_or_tilter.power = original_power * (1 + maximum_wobble * i / n)
        else:
            sign = 1 if i >= 0 else -1
            deflector_or_tilter.power = original_power * (1 + maximum_wobble / 2 ** abs(n - i) * sign)


def set_wobbled_rotation(original_rotation: float, sample: Sample, maximum_wobble: float, i: int, n: int, linear: bool) -> None:
    """
    Set the rotation of the sample depending on the desired wobble
    :param original_rotation: original value of the sample rotation
    :param sample: sample component
    :param maximum_wobble: maximum modification of the rotation in percent
    :param i: how far the new value will be from the original value
    :param n: how far is the maximum wobble
    :param linear: whether the scale is linear or exponential
    :return:
    """
    if i == 0:
        sample.tilt[0] = original_rotation
    else:
        if linear:
            sample.tilt[0] = original_rotation * (1 + maximum_wobble * i / n)
        else:
            sign = 1 if i >= 0 else -1
            sample.tilt[0] = original_rotation * (1 + maximum_wobble / 2 ** abs(n - i) * sign)


class MiniTem:
    """
    A class representing a transmission electron microscope
    """
    source = None
    z_screen = np.inf
    components = []
    raw_components = []

    def __init__(self, default_electron_number: int=100000, file_name: str or PathLike="i2tem.json",
                 screen_size: float=0.1, screen_resolution_root: int=150) -> None:
        """
        Initialize the microscope
        :param default_electron_number: Number of electrons to fire by default
        :param file_name: Name of the file to load the microscope from
        :param screen_size: Size of the screen in meters
        :param screen_resolution_root: Resolution of the screen/camera
        """
        self.screen_resolution_root = screen_resolution_root
        # Load the microscope file
        if not self.load_file(file_name):
            self.default_configuration()

        for component in self.raw_components:
            setattr(self, component.name, component)

        self.sort_components()

        print(f"Loaded {len(self.components)} components.")
        self.default_electron_number = default_electron_number
        self.screen_size = screen_size

    def sort_components(self) -> None:
        """
        Sort the components by their z position
        :return:
        """
        self.raw_components.sort(key=lambda x: x.z)
        self.components = [c for c in self.raw_components if self.source.z <= c.z <= self.z_screen]

    def default_configuration(self) -> None:
        """
        Set the default configuration of the microscope
        :return:
        """
        self.source = ElectronSource(0, small_source_xy_function, uniformly_spread_velocity_function)
        self.z_screen = 2
        l1 = Lens(z=1, focal_length=1, name="l1")
        sample = Sample(z=1.1, scale=1e-5, x=0, y=0, name="sample")
        ap1 = Aperture(z=1.2, diameter=5e-7, name="ap1", x=3e-7, y=0)
        bp1 = Biprism(z=1.5, deflection_power=1e2, name="bp1", x=0, y=0, theta=np.pi / 4, width=1e-7)
        bp2 = Biprism(z=1.6, deflection_power=1e2, name="bp2", x=1e-7, y=0, theta=0, width=1e-7)
        def1 = Tilter(z=1.7, deflection_power=0, theta_direction=0, name="def1")
        self.raw_components = [self.source, l1, sample, ap1, bp1, bp2, def1]

    def launch_electrons(self, n_electrons: int=None, with_history: bool=False,
                         z_max: float=None, force_reinit: bool=False) -> (np.array, np.array, np.array):
        """
        Launch electrons through the microscope
        :param n_electrons: Number of electrons to launch
        :param with_history: Whether to keep the history of the electrons positions and velocities
        :param z_max: Maximum z position of the electrons
        :param force_reinit: Whether to reinitialize the electrons starting positions and velocities
        :return: Positions, velocities and history of the electrons going through the microscope
        """
        if n_electrons is None:
            n_electrons = self.default_electron_number
        # Launch n electrons with energy
        positions, velocities = self.get_positions_velocities(force_reinit, n_electrons)
        z_max = self.z_screen if z_max is None else z_max
        position_history = []
        velocities_history = []
        if with_history:
            self.update_history(position_history, positions, velocities, velocities_history)

        for component in self.components:
            if component == self.source:
                continue
            if component.z > z_max:
                break
            delta_z = component.z - np.max(positions[:, 2])
            if delta_z == 0:
                print("Warning: two components are too close together. (delta_z = 0)")
                break
            positions = self.update_positions(delta_z, position_history, positions, velocities, velocities_history,
                                              with_history)
            component.apply_on_electrons(positions, velocities)

        delta_z = z_max - np.max(positions[:, 2])
        if delta_z > 0:
            positions = self.update_positions(delta_z, position_history, positions, velocities, velocities_history,
                                              with_history)
        return positions, velocities, np.array([position_history, velocities_history])

    def update_positions(self, delta_z: float, position_history: np.array, positions: np.array, velocities: np.array,
                         velocities_history: np.array, with_history: bool) -> np.array:
        """
        Update the positions of the electrons
        :param delta_z: Change in z position
        :param position_history: positions history
        :param positions: last positions of the electrons
        :param velocities: last velocities of the electrons
        :param velocities_history: velocities history
        :param with_history: whether to update the history
        :return: updated positions
        """
        if with_history:
            self.update_history(position_history, positions, velocities, velocities_history)
        with np.errstate(divide='ignore', invalid='ignore'):
            delta_positions = delta_z * velocities / velocities[:, 2, np.newaxis]
        delta_positions[np.isnan(delta_positions) + np.isinf(delta_positions)] = 0
        positions += delta_positions
        if with_history:
            self.update_history(position_history, positions, velocities, velocities_history)
        return positions

    @staticmethod
    def update_history(position_history: np.array, positions: np.array,
                       velocities: np.array, velocities_history: np.array) -> None:
        """
        Update the history of the electrons
        :param position_history: positions history
        :param positions: last positions of the electrons
        :param velocities: last velocities of the electrons
        :param velocities_history: velocities history
        :return:
        """
        position_history.append(positions.copy())
        velocities_history.append(velocities.copy())

    def get_positions_velocities(self, force_reinit: bool, n_electrons: int) -> (np.array, np.array):
        """
        Get the positions and velocities of the electrons
        :param force_reinit: whether to reinitialize the electrons starting positions and velocities
        :param n_electrons: number of electrons
        :return: positions and velocities
        """
        if force_reinit:
            positions, velocities = self.source.init_positions_velocities(n_electrons)
        else:
            positions, velocities = self.source.get_positions_velocities(n_electrons)
        return positions, velocities

    def load_file(self, filename: str or PathLike) -> bool:
        """
        Load a microscope file
        :param filename: the filename
        :return: True if the file was loaded, False otherwise
        """
        try:
            load_dict = json.load(open(filename))
        except FileNotFoundError:
            return False
        self.from_json(load_dict)
        return True

    def from_json(self, load_dict: dict) -> None:
        """
        Load a microscope from a json object
        :param load_dict: the json object
        :return:
        """
        self.source = ElectronSource.from_json(load_dict["source"])
        self.z_screen = load_dict["z_screen"]
        self.raw_components = [self.source]
        for name, component in load_dict["components"].items():
            if component["type"] == "lens":
                self.raw_components.append(Lens.from_json(component))
            elif component["type"] == "sample":
                self.raw_components.append(Sample.from_json(component))
            elif component["type"] == "aperture":
                self.raw_components.append(Aperture.from_json(component))
            elif component["type"] == "biprism":
                self.raw_components.append(Biprism.from_json(component))
            elif component["type"] == "deflector":
                self.raw_components.append(Deflector.from_json(component))
            elif component["type"] == "shifter":
                self.raw_components.append(Shifter.from_json(component))
            elif component["type"] == "tilter":
                self.raw_components.append(Deflector.from_json(component))
            elif component["type"] == "bipole":
                self.raw_components.append(Bipole.from_json(component))
            elif component["type"] == "half_thick_lens":
                half_lens = HalfThickLens.from_json(component)
                second_half_lens = half_lens.second_half
                self.raw_components.append(half_lens)
                self.raw_components.append(second_half_lens)
            setattr(self, name, self.raw_components[-1])
        self.default_electron_number = load_dict["default_electron_number"]
        self.sort_components()
        print(f"Loaded {len(self.components)} components.")

    def save_file(self, filename: str or PathLike) -> None:
        """
        Save the microscope to a json file
        :param filename: the filename
        :return:
        """
        save_dict = self.to_json()
        with open(filename, "w") as f:
            json.dump(save_dict, f, indent=4)

    def to_json(self) -> dict:
        """
        Convert the microscope to a json object
        :return: the json object
        """
        save_dict = {
            "source": self.source.to_json(),
            "z_screen": self.z_screen,
            "components": {c.name: c.to_json() for c in self.raw_components if c != self.source},
            "default_electron_number": self.default_electron_number
        }
        return save_dict

    def generate_image(self, z: float=None, force_reinit: bool=False, side_view: bool=False, theta: float=0,
                       scale_screen: bool=True, color_scale: float=None,
                       screen_resolution: int=None, positions_only: bool=False
                       ) -> (np.array, np.array, float, float, float) or (np.array, float) or np.array:
        """
        Generate an image of the screen or the side view of the column or the positions of the electrons
        :param z: position of the screen of maximum z position of the electrons for the side view
        :param force_reinit: whether to reinitialize the electrons starting positions and velocities
        :param side_view: whether to generate the side view of the column
        :param theta: angle of the screen
        :param scale_screen: whether to scale the screen to the size of the beam or not
        :param color_scale: scaling factor for the color of the screen (i.e. brightness)
        :param screen_resolution: resolution of the screen
        :param positions_only: whether to return only the positions of the electrons or the images
        :return: image of the screen or the side view of the column or the positions of the electrons
        """
        if z is None:
            z = self.z_screen
        positions, velocities, history = self.launch_electrons(
            n_electrons=self.default_electron_number,
            with_history=side_view, z_max=z,
            force_reinit=force_reinit
        )
        if positions_only:
            return positions

        farthest, image, scale = self.display_screen(positions, theta, z, scaled=scale_screen, color_scaled=color_scale,
                                                     screen_resolution=screen_resolution)

        if side_view:
            h_scale, side_view_image, w_scale = self.display_side_view(farthest, history, theta, z, self.source.z)
            return image, side_view_image, scale, w_scale, h_scale
        else:
            return image, scale

    def display_screen(self, positions: np.array, theta: float, z: float, scaled: bool=True,
                       color_scaled: float=None, screen_resolution: int=None) -> (float, np.array, float):
        """
        Display the screen of the microscope
        :param positions: positions of the electrons
        :param theta: angle of the screen
        :param z: position of the screen along the z axis
        :param scaled: whether to scale the screen to the size of the beam or not
        :param color_scaled: scaling factor for the color of the screen (i.e. brightness) None for no scaling
        :param screen_resolution: resolution of the screen
        :return: farthest distance of an electron from the optical axis, screen image, scale of the screen in m
        """
        if screen_resolution is None:
            screen_resolution = [self.screen_resolution_root, self.screen_resolution_root]
        image = np.zeros(screen_resolution)
        farthest = np.max(np.sqrt(positions[:, 0] ** 2 + positions[:, 1] ** 2))
        drs = self.screen_resolution_root // 2
        if farthest == 0 or scaled == False:
            scale = drs / self.screen_size
        else:
            scale = drs / farthest * scaled
        x = ((positions[:, 0] * np.cos(theta) - positions[:, 1] * np.sin(theta)) * scale + drs).astype(int)
        y = ((positions[:, 1] * np.cos(theta) + positions[:, 0] * np.sin(theta)) * scale + drs).astype(int)
        mask = (0 <= x) * (x < self.screen_resolution_root) * (0 <= y) * (y < self.screen_resolution_root) * (
                positions[:, 2] >= z)
        x = x[mask]
        y = y[mask]
        # noinspection PyTypeChecker
        hist, _, _ = np.histogram2d(x=x, y=y, 
                                    bins=self.screen_resolution_root, 
                                    range=[[0, self.screen_resolution_root], [0, self.screen_resolution_root]])
        image[:, :] = hist
        if color_scaled is None:
            image *= 255 / max(1, np.max(image))
        else:
            image = np.clip(image * color_scaled, 0, 255)
        return farthest, image, scale

    def display_side_view(self, farthest: float, history: np.array, theta: float, z: float, source_z: float) -> (float, np.array, float):
        """
        Display the side view of the column
        :param farthest: distance of the farthest electron from the optical axis
        :param history: history of the electrons (positions and velocities)
        :param theta: angle of the screen
        :param z: position of the screen along the z axis
        :param source_z: position of the source along the z axis
        :return: horizontal scale, side view image, vertical scale
        """
        history = np.array(history[:, :, :100])
        # project history x,y by rotating the view along the z axis by theta
        rotation_matrix = np.array([[np.sin(theta), np.cos(theta)],
                                    [np.cos(theta), -np.sin(theta)]])
        rotated_positions_history = np.matmul(history[0, :, :, :2], rotation_matrix)
        w_farthest = np.max(np.abs(np.linalg.norm(history[0, :, :, :2])))
        drs = self.screen_resolution_root // 2
        if w_farthest == 0:
            w_scale = 1
        else:
            w_scale = drs / farthest
        h_scale = 600 / (z - source_z)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlim(-w_farthest, w_farthest)
        ax.set_ylim(source_z - z, 0)
        canvas = FigureCanvasAgg(fig)
        for i in range(rotated_positions_history.shape[1]):
            plt.plot(
                rotated_positions_history[:, i, 0], -history[0, :, i, 2],
                color='green', alpha=0.1
            )
        canvas.draw()  # draw the canvas, cache the renderer
        s, (width, height) = canvas.print_to_buffer()
        side_view_image = np.frombuffer(s, dtype='uint8').reshape((height, width, 4))
        plt.close(fig)
        return h_scale, side_view_image, w_scale

    def wobble(self, parameters: list or Component, number_images: int=15, maximum_wobbles: int=None, 
               scale_screen: bool=False, color_scale: float=None, linear: bool=True
               ) -> np.array:
        """
        Generate a series of images with wobbled parameters
        :param parameters: list of components to wobble
        :param number_images: number of images to generate
        :param maximum_wobbles: maximum wobble for each parameter
        :param scale_screen: whether to scale the screen to the size of the beam or not
        :param color_scale: scaling factor for the color of the screen (i.e. brightness)
        :param linear: whether the wobble scale is linear or exponential
        :return: 3D data cube containing the images with the component wobbled according to the maximum wobble
        """
        if maximum_wobbles is None:
            maximum_wobbles = [0.1] * len(parameters)

        parameters = list(parameters)

        images = []
        original_parameters = []

        if number_images % (2 * len(parameters)) != 1:
            print("Number of images must be equal to 2*p*k + 1 with k an integer.")
            return
        for p in parameters:
            if p not in self.components:
                print(f"Component {p} not found.")
                return
            if isinstance(p, Lens):
                original_parameters.append(p.focal_length)
            if isinstance(p, Deflector) or isinstance(p, Tilter):
                original_parameters.append(p.power)
            if isinstance(p, Shifter):
                print("Shifter wobble not supported yet")
            if isinstance(p, Sample):
                original_parameters.append(p.tilt_x)
            if isinstance(p, HalfThickLens):
                original_parameters.append(p.refraction_power)
            if isinstance(p, Stigmator):
                original_parameters.append(p.x_factor)

        n = number_images // (2 * len(parameters))

        for i in range(-n, n + 1):
            if i == 0:
                self.add_wobbled_image(color_scale, 0, images, 0, linear, maximum_wobbles, n, parameters[0],
                                       original_parameters[0], scale_screen)
            for j, p in enumerate(parameters):
                self.add_wobbled_image(color_scale, i, images, j, linear, maximum_wobbles, n, p, original_parameters[j],
                                       scale_screen)
        images = np.array(images)
        return images

    def add_wobbled_image(self, color_scale: float, i: int, images: np.array, j: int, 
                          linear: bool, maximum_wobbles: list, n: int, p: Component, op, scale_screen: bool
                          ) -> None:
        """
        Add a wobbled image to the list of images
        :param color_scale: scaling factor for the color of the screen (i.e. brightness)
        :param i: index of the wobble
        :param images: data cube containing the images
        :param j: index of the parameter
        :param linear: whether the wobble scale is linear or exponential
        :param maximum_wobbles: maximum wobble for each parameter
        :param n: number of images to generate
        :param p: component to wobble
        :param op: original parameter value
        :param scale_screen: whether to scale the screen to the size of the beam or not
        :return:
        """
        if isinstance(p, Lens):
            set_wobbled_fl(op, p, maximum_wobbles[j], i, n, linear)
        if isinstance(p, Deflector) or isinstance(p, Tilter):
            set_wobbled_power(op, p, maximum_wobbles[j], i, n, linear)
        if isinstance(p, Sample):
            set_wobbled_rotation(op, p, maximum_wobbles[j], i, n, linear)
        if isinstance(p, HalfThickLens):
            set_wobbled_sp(op, p, maximum_wobbles[j], i, n, linear)
        if isinstance(p, Stigmator):
            set_wobbled_x_factor(op, p, maximum_wobbles[j], i, n, linear)
        image, _ = self.generate_image(scale_screen=scale_screen, color_scale=color_scale)
        images.append(image)
        if isinstance(p, Lens):
            set_wobbled_fl(op, p, maximum_wobbles[j], 0, n, linear)
        if isinstance(p, Deflector) or isinstance(p, Tilter):
            set_wobbled_power(op, p, maximum_wobbles[j], 0, n, linear)
        if isinstance(p, Sample):
            set_wobbled_rotation(op, p, maximum_wobbles[j], 0, n, linear)
        if isinstance(p, HalfThickLens):
            set_wobbled_sp(op, p, maximum_wobbles[j], 0, n, linear)
        if isinstance(p, Stigmator):
            set_wobbled_x_factor(op, p, maximum_wobbles[j], 0, n, linear)


def main():
    i2tem = MiniTem(file_name="")
    i2tem.source = ElectronSource(0, small_source_xy_function, uniformly_spread_velocity_function)
    corrector = 0.43345
    i2tem.z_screen = 2.0525 + corrector
    c1 = Lens(z=0.651507265273, focal_length=0.5, name="c1")
    c2 = Lens(z=0.754902093688, focal_length=0.5, name="c2")
    c3 = Lens(z=0.92594196596, focal_length=0.5, name="c3")
    obj = Lens(z=0.9985300839, focal_length=0.5, name="obj")
    i1 = Lens(z=1.24470537431 + corrector, focal_length=0.5, name="i1")
    i2 = Lens(z=1.3722235985 + corrector, focal_length=0.5, name="i2")
    i3 = Lens(z=1.49422359173 + corrector, focal_length=0.5, name="i3")
    p1 = Lens(z=1.67240424466 + corrector, focal_length=0.5, name="p1")
    p2 = Lens(z=1.78740596186 + corrector, focal_length=0.5, name="p2")

    bpc = Biprism(z=0.585999975, deflection_power=1e2, name="bpc", x=0, y=0, theta=0, width=1e-7)
    bpc.toggle(False)
    bp1 = Biprism(z=1.18169995 + corrector, deflection_power=1e2, name="bp1", x=0, y=0, theta=0, width=1e-7)
    bp1.toggle(False)
    bp2 = Biprism(z=1.30969995 + corrector, deflection_power=1e2, name="bp2", x=0, y=0, theta=0, width=1e-7)
    bp2.toggle(False)

    cond_app = Aperture(z=0.5784, diameter=5e-7, name="cond_app", x=0, y=0)
    cond_app.toggle(False)
    stem_app = Aperture(z=0.77376, diameter=5e-7, name="stem_app", x=0, y=0)
    stem_app.toggle(False)
    obj_app = Aperture(z=1.0026, diameter=5e-7, name="obj_app", x=0, y=0)
    obj_app.toggle(False)
    sa_app = Aperture(z=1.1947, diameter=5e-7, name="sa_app", x=0, y=0)
    sa_app.toggle(False)

    lorentz = Sample(z=0.9518, scale=1e-6, x=0, y=0, name="lorentz")
    lorentz.toggle(False)
    normal = Sample(z=0.9988, scale=1e-6, x=0, y=0, name="normal")

    i2tem.raw_components = [i2tem.source, c1, c2, c3, obj, i1, i2, i3, p1, p2,
                            bpc, bp1, bp2, cond_app, stem_app, obj_app, sa_app, lorentz, normal]
    i2tem.sort_components()
    i2tem.save_file("i2tem.json")
    i2tem.load_file("i2tem.json")


if __name__ == '__main__':
    main()
