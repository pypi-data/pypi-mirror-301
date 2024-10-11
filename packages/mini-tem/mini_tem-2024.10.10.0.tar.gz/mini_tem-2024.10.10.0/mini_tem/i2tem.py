import json
from os import PathLike

import numpy as np

from mini_tem.aperture import Aperture
from mini_tem.biprism import Biprism
from mini_tem.deflector import Deflector
from mini_tem.electron_source import ElectronSource, small_source_xy_function, uniformly_spread_velocity_function
from mini_tem.half_thick_lens import HalfThickLens
from mini_tem.lens import Lens
from mini_tem.minitem import MiniTem
from mini_tem.sample import Sample
from mini_tem.shifter import Shifter
from mini_tem.stigmator import Stigmator
from mini_tem.tilter import Tilter


class I2TEM(MiniTem):
    lenses: dict
    biprisms: dict
    apertures: dict
    aperture_values: dict
    deflectors: dict
    shifters: dict
    tilters: dict
    samples: dict
    stigmators: dict

    def __init__(self, screen_resolution: int=256) -> None:
        """
        Initialize the I2TEM microscope
        :param screen_resolution: Resolution of the screen/camera
        """
        super().__init__(file_name="", screen_resolution_root=screen_resolution)
        self.source = ElectronSource(0, small_source_xy_function, uniformly_spread_velocity_function)
        self.corrector = 0.43345
        self.z_screen = 2.0525 + self.corrector
        self.c1_values = [-5.2, 5.2]
        # self.c1 = Lens(z=0.651507265273, focal_length=0.077965, name="c1")
        self.c1 = Lens(z=0.651507265273, focal_length=0.08, name="c1")

        # self.c2 = Lens(z=0.754902093688, focal_length=0.02248, name="c2")
        self.c2 = Lens(z=0.754902093688, focal_length=0.0113, name="c2")
        self.c3 = Lens(z=0.92594196596, focal_length=0.200, name="c3")
        self.obj1 = HalfThickLens(z=0.998, refraction_power=0.001, name="obj1")
        self.obj2 = Lens(z=0.999, focal_length=0.001, name="obj2")
        # self.i1 = Lens(z=1.24470537431 + self.corrector, focal_length=0.081685, name="i1")
        # self.i2 = Lens(z=1.3722235985 + self.corrector, focal_length=0.079045, name="i2")
        # self.i3 = Lens(z=1.49422359173 + self.corrector, focal_length=0.0873225, name="i3")
        # self.p1 = Lens(z=1.67240424466 + self.corrector, focal_length=0.060815, name="p1")
        # self.p2 = Lens(z=1.78740596186 + self.corrector, focal_length=0.063935, name="p2")
        self.i1 = Lens(z=1.24470537431 + self.corrector, focal_length=0.081685, name="i1")
        self.i2 = Lens(z=1.3722235985 + self.corrector, focal_length=0.06, name="i2")
        self.i3 = Lens(z=1.49422359173 + self.corrector, focal_length=0.04, name="i3")
        self.p1 = Lens(z=1.67240424466 + self.corrector, focal_length=0.025, name="p1")
        self.p2 = Lens(z=1.78740596186 + self.corrector, focal_length=0.025, name="p2")
        # self.p2 = Lens(z=1.78740596186 + self.corrector, focal_length=0.052, name="p2")


        self.bpc = Biprism(z=0.585999975, deflection_power=1e2, name="bpc", x=0, y=0, theta=0, width=1e-7)
        self.bpc.toggle(False)
        self.bp1 = Biprism(z=1.18169995 + self.corrector, deflection_power=1e2, name="bp1", x=0, y=0, theta=0,
                           width=1e-7)
        self.bp1.toggle(False)
        self.bp2 = Biprism(z=1.30969995 + self.corrector, deflection_power=1e2, name="bp2", x=0, y=0, theta=0,
                           width=1e-7)
        self.bp2.toggle(False)
        self.cond_ap_values = [300e-6, 100e-6, 60e-6, 10e-6]
        self.cond_ap = Aperture(z=0.5784, diameter=self.cond_ap_values[0], name="cond_ap", x=0, y=0)
        self.cond_ap.toggle(False)
        self.stem_ap_values = [100e-6, 50e-6, 30e-6, 10e-6]
        self.stem_ap = Aperture(z=0.77376, diameter=self.stem_ap_values[0], name="stem_ap", x=0, y=0)
        self.stem_ap.toggle(False)
        self.obj_ap_values = [50e-6, 20e-6, 10e-6, 5e-6]
        self.obj_ap = Aperture(z=1.0026, diameter=self.obj_ap_values[0], name="obj_ap", x=0, y=0)
        self.obj_ap.toggle(False)
        self.sa_ap_values = [50e-6, 20e-6, 5e-6, 3e-6]
        self.sa_ap = Aperture(z=1.1947, diameter=self.sa_ap_values[0], name="sa_ap", x=0, y=0)
        self.sa_ap.toggle(False)

        # z and category false
        self.gx = Tilter(z=0.1, deflection_power=0, name="ghx", theta_direction=0)
        self.gy = Tilter(z=0.1000001, deflection_power=0, name="ghy", theta_direction=np.pi / 2)
        self.gx.toggle(False)
        self.gy.toggle(False)

        self.bh = Shifter(z=0.8, x_shift=0, y_shift=0, name="bh")
        self.bh.toggle(False)

        self.bt = Deflector(z=0.81, pivot_z=0.1418, theta_x=0, theta_y=0, name="bt")
        self.bt.toggle(False)

        self.cs = Stigmator(z=0.84, x_factor=0.3, y_factor=1, name="cs")
        # self.cs3 = HexaStigmator()

        self.lorentz = Sample(z=0.9518, scale=1e-6, x=0, y=0, name="lorentz")
        self.lorentz.toggle(False)
        self.normal = Sample(z=0.9988, scale=1e-5, x=0, y=0, x_tilt=np.pi/30, name="normal")
        self.normal.set_shape_function(3)
        self.normal.toggle(True)

        self.update_typed_lists()
        self.sort_components()

    def load_file(self, filename: str or PathLike) -> None:
        """
        Load a microscope configuration from a json file
        :param filename: name of the file to load
        :return:
        """
        try:
            load_dict = json.load(open(filename))
        except FileNotFoundError:
            return
        self.from_json(load_dict)
        self.update_typed_lists()
        self.sort_components()

    def save_file(self, filename: str or PathLike) -> None:
        """
        Save the microscope configuration to a json file
        :param filename: name of the file to save
        :return:
        """
        save_dict = self.to_json()
        with open(filename, "w") as f:
            json.dump(save_dict, f, indent=4)

    def update_typed_lists(self) -> None:
        """
        Update the typed lists of the components of the microscope
        :return:
        """
        self.lenses = {
            "c1": self.c1,
            "c2": self.c2,
            "c3": self.c3,
            "obj1": self.obj1,
            "obj2": self.obj2,
            "i1": self.i1,
            "i2": self.i2,
            "i3": self.i3,
            "p1": self.p1,
            "p2": self.p2,
        }
        self.biprisms = {
            "bpc": self.bpc,
            "bp1": self.bp1,
            "bp2": self.bp2,
        }
        self.apertures = {
            "cond_ap": self.cond_ap,
            "stem_ap": self.stem_ap,
            "obj_ap": self.obj_ap,
            "sa_ap": self.sa_ap,
        }
        self.aperture_values = {
            "cond_ap": self.cond_ap_values,
            "stem_ap": self.stem_ap_values,
            "obj_ap": self.obj_ap_values,
            "sa_ap": self.sa_ap_values,
        }
        self.deflectors = {
            "gx": self.gx,
            "gy": self.gy,
        }
        self.shifters = {
            "bh": self.bh,
        }
        self.tilters = {
            "bt": self.bt,
        }
        self.samples = {
            "lorentz": self.lorentz,
            "normal": self.normal,
        }
        self.stigmators = {
            "cs": self.cs,
        }
        self.raw_components = [
            self.source, self.c1, self.c2, self.c3, self.obj1, self.obj2, self.i1, self.i2, self.i3, self.p1, self.p2,
            self.bpc, self.bp1, self.bp2, self.cond_ap, self.stem_ap, self.obj_ap, self.sa_ap,
            self.gx, self.gy, self.bh, self.bt, self.lorentz, self.normal, self.cs
        ]
