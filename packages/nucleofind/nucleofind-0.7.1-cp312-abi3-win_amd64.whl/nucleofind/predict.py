#  Copyright (c) 2024 Jordan Dialpuri, Jon Agirre, Kathryn Cowtan, Paul Bond and University of York. All rights reserved

import argparse
import logging
import os
import site
import sys
import time
from glob import glob
from typing import List
import platform
from pathlib import Path

import gemmi
import numpy as np
import onnxruntime as rt
from tqdm import tqdm

from .__version__ import __version__


class Prediction:
    def __init__(self, model_paths: List[Path], use_gpu: bool = False, compute_variance: bool = False,
                 disable_progress_bar: bool = False, compute_entire_cell: bool = False):
        self.model_paths: List[Path] = model_paths
        self.use_gpu: bool = use_gpu
        self.disable_progress_bar: bool = disable_progress_bar
        self.compute_entire_cell: bool = compute_entire_cell

        if use_gpu and platform.system() == "Darwin":
            logging.warning("GPU acceleration was specified but is not supported on MacOS, continuing with CPU only")
            self.use_gpu = False

        self.compute_variance: bool = compute_variance
        self.model_names: List[Path] = [x.stem for x in model_paths]

        self.predicted_map: np.ndarray = None
        self.variance_map: np.ndarray = None

        self.predicted_grids: List[gemmi.FloatGrid] = None
        self.variance_grid: gemmi.FloatGrid = None

        self.na: float = 0
        self.nb: float = 0
        self.nc: float = 0
        self.translation_list: List[List[int]] = []

        self.model = None

        self.interpolated_grid: gemmi.FloatGrid = None
        self.raw_grid: gemmi.FloatGrid = None
        self.map: gemmi.Ccp4Map = None
        self.structure: gemmi.Structure = None
        self.transform: gemmi.Transform = None
        self.box_minimum: gemmi.Position = None

    def make_prediction(self, file_path: str, column_labels: List[str] = ["FWT", "PHWT"],
                        resolution_cutoff: float = None, use_raw_values: bool = False, overlap: float = 16):
        start = time.time()
        try:
            self._load_model()
        except OSError:
            logging.critical(
                "This model is corrupted, perhaps due to an incomplete download. Try downloading it again with "
                "nucleofind-install -m TYPE --reinstall")
            sys.exit()

        if column_labels == [None, None]:
            column_labels = ["FWT", "PHWT"]

        if ".mtz" in file_path:
            if resolution_cutoff:
                resolution_cutoff = float(resolution_cutoff)
            self._load_mtz(file_path, resolution_cutoff, column_labels)
        elif ".map" in file_path:
            self._load_map(file_path)
        else:
            raise RuntimeError("The input file is not a mtz or map.")

        self._interpolate_grid()
        self._calculate_translations(overlap=overlap)
        self._predict(raw_values=use_raw_values, overlap=overlap)

        self.predicted_grids = self._reinterpolate_to_output(self.predicted_map)
        if self.compute_variance:
            self.variance_grids = self._reinterpolate_to_output(self.variance_maps)

        end = time.time()
        delta = end - start
        logging.info(f"Prediction took - {delta:.3f}")

    def save_predicted_map(self, output_path: str):
        for index, grid in enumerate(self.predicted_grids):
            ccp4 = gemmi.Ccp4Map()
            ccp4.grid = grid
            ccp4.update_ccp4_header()
            if '.map' in output_path and len(self.predicted_grids) == 1:
                ccp4.write_ccp4_map(output_path)
                return
            if ".map" in output_path:
                ccp4.write_ccp4_map(output_path.replace(".map", f"_{self.model_names[index]}.map"))
            else:
                ccp4.write_ccp4_map(f"{output_path}_{self.model_names[index]}.map")

    def save_variance_map(self, output_path: str):
        for index, grid in enumerate(self.variance_grids):
            if not self.compute_variance:
                logging.warning("Attempting to output a variance map without specifying compute_variance=True")
                return
            ccp4 = gemmi.Ccp4Map()
            ccp4.grid = grid
            ccp4.update_ccp4_header()
            if ".map" in output_path:
                ccp4.write_ccp4_map(output_path.replace(".map", f"_variance_{self.model_names[index]}.map"))
            else:
                ccp4.write_ccp4_map(f"{output_path}_variance_{self.model_names[index]}.map")

    def save_interpolated_map(self, output_path: str, grid_spacing: float = 0.7):
        logging.info("Saving interpolated map")
        ccp4 = gemmi.Ccp4Map()
        ccp4.grid = self.interpolated_grid
        ccp4.update_ccp4_header()

        ccp4.write_ccp4_map(output_path)

    def save_raw_map(self, output_path: str):
        ccp4 = gemmi.Ccp4Map()
        ccp4.grid = self.raw_grid
        ccp4.update_ccp4_header()

        ccp4.write_ccp4_map(output_path)

    def _load_model(self):
        providers = ['CPUExecutionProvider']
        if self.use_gpu:
            providers.insert(0, 'CUDAExecutionProvider')

        sess_options = rt.SessionOptions()
        sess_options.intra_op_num_threads = 1
        self.models = [rt.InferenceSession(model, providers=providers, sess_options=sess_options) for model in self.model_paths ]


    def _load_map(self, map_path: str, normalise: bool = True):
        self.map: gemmi.Ccp4Map = gemmi.read_ccp4_map(map_path)
        self.raw_grid: gemmi.FloatGrid = self.map.grid

        if normalise:
            self.raw_grid.normalize()

    def _load_mtz(self, mtz_path: str, resolution_cutoff: float, column_names: List[str] = ["FWT", "PHWT"]):
        mtz = gemmi.read_mtz_file(mtz_path)
        logging.info(f"Reading mtz file {mtz_path}")
        res = mtz.resolution_high()
        spacing = 0.7
        sample_rate = res / spacing
        self.raw_grid = mtz.transform_f_phi_to_map(*column_names, sample_rate=sample_rate)
        self.raw_grid.normalize()
        if resolution_cutoff:
            data = np.array(mtz, copy=False)
            mtz.set_data(data[mtz.make_d_array() >= resolution_cutoff])

    def _get_bounding_box(self, grid: gemmi.FloatGrid) -> gemmi.PositionBox:
        logging.debug(f"Spacegroup: {grid.spacegroup}")
        extent = gemmi.find_asu_brick(grid.spacegroup).get_extent()

        logging.debug(f"ASU Brick Minimum: {extent.minimum}")
        logging.debug(f"ASU Brick Maximum: {extent.maximum}")

        if self.compute_entire_cell:
            extent.maximum = gemmi.Fractional(1, 1, 1)
            extent.minimum = gemmi.Fractional(0, 0, 0)

        corners = [
            grid.unit_cell.orthogonalize(fractional)
            for fractional in (
                extent.minimum,
                gemmi.Fractional(extent.maximum[0], extent.minimum[1], extent.minimum[2]),
                gemmi.Fractional(extent.minimum[0], extent.maximum[1], extent.minimum[2]),
                gemmi.Fractional(extent.minimum[0], extent.minimum[1], extent.maximum[2]),
                gemmi.Fractional(extent.maximum[0], extent.maximum[1], extent.minimum[2]),
                gemmi.Fractional(extent.maximum[0], extent.minimum[1], extent.maximum[2]),
                gemmi.Fractional(extent.minimum[0], extent.maximum[1], extent.maximum[2]),
                extent.maximum,
            )
        ]
        min_x = min(corner[0] for corner in corners)
        min_y = min(corner[1] for corner in corners)
        min_z = min(corner[2] for corner in corners)
        max_x = max(corner[0] for corner in corners)
        max_y = max(corner[1] for corner in corners)
        max_z = max(corner[2] for corner in corners)

        box = gemmi.PositionBox()
        box.minimum = gemmi.Position(min_x, min_y, min_z)
        box.maximum = gemmi.Position(max_x, max_y, max_z)
        return box

    def _interpolate_grid(self, grid_spacing: float = 0.7):
        box: gemmi.PositionBox = self._get_bounding_box(self.raw_grid)
        size: gemmi.Position = box.get_size()

        logging.info(f"Raw unit cell is : {self.raw_grid.unit_cell}")
        logging.debug(f"Box size : {size}")

        num_x = int(size.x / grid_spacing)
        num_y = int(size.y / grid_spacing)
        num_z = int(size.z / grid_spacing)

        logging.debug(f"Num x,y,z: {num_x}, {num_y}, {num_z}")

        array = np.zeros((num_x, num_y, num_z), dtype=np.float32)
        scale = gemmi.Mat33(
            [[grid_spacing, 0, 0], [0, grid_spacing, 0], [0, 0, grid_spacing]]
        )

        self.transform: gemmi.Transform = gemmi.Transform(scale, box.minimum)
        self.raw_grid.interpolate_values(array, self.transform)
        cell: gemmi.UnitCell = gemmi.UnitCell(size.x, size.y, size.z, 90, 90, 90)
        self.interpolated_grid = gemmi.FloatGrid(array, cell)

        self.box_minimum = box.minimum

        logging.debug(f"Interpolated grid (numpy) shape: {array.shape}")
        logging.debug(f"Interpolated grid (gemmi) shape: {self.interpolated_grid}")

    def _reinterpolate_to_output(self, grid_to_interp: np.ndarray) -> List[gemmi.FloatGrid]:
        logging.info("Reinterpolating array")
        # Taken from https://github.com/paulsbond/densitydensenet/blob/main/predict.py - Paul Bond

        output_grids = []

        for model_index in range(len(self.models)):
            dummy_structure = gemmi.Structure()
            dummy_structure.cell = self.raw_grid.unit_cell
            dummy_structure.spacegroup_hm = self.raw_grid.spacegroup.hm
            output_grid = gemmi.FloatGrid()
            output_grid.setup_from(dummy_structure, spacing=0.7)

            size_x = grid_to_interp.shape[0] * 0.7
            size_y = grid_to_interp.shape[1] * 0.7
            size_z = grid_to_interp.shape[2] * 0.7

            grid_to_interp[np.isnan(grid_to_interp)] = 0
            array_cell = gemmi.UnitCell(size_x, size_y, size_z, 90, 90, 90)
            array_grid = gemmi.FloatGrid(grid_to_interp[..., model_index], array_cell)

            if self.compute_entire_cell:
                grid_iterable = output_grid
            else:
                grid_iterable = output_grid.masked_asu()

            for point in grid_iterable:
                position = output_grid.point_to_position(point) - self.box_minimum
                point.value = array_grid.interpolate_value(position)

            output_grid.symmetrize_max()
            output_grids.append(output_grid)

        return output_grids

    def _calculate_translations(self, overlap: int = 32):
        logging.info("Calculating translations")
        logging.debug(
            f"Interpolated grid unit cell : {self.interpolated_grid.unit_cell}"
        )
        logging.debug(
            f"Interpolated grid shape : {self.interpolated_grid.array.shape}"
        )
        overlap_na: float = (self.interpolated_grid.array.shape[0] // overlap) + 1
        overlap_nb: float = (self.interpolated_grid.array.shape[1] // overlap) + 1
        overlap_nc: float = (self.interpolated_grid.array.shape[2] // overlap) + 1

        logging.debug(f"overlap na, nb, nc: {overlap_na}, {overlap_nb}, {overlap_nc}")

        for x in range(int(overlap_na)):
            for y in range(int(overlap_nb)):
                for z in range(int(overlap_nc)):
                    self.translation_list.append(
                        [x * overlap, y * overlap, z * overlap]
                    )

        self.na: float = (self.interpolated_grid.array.shape[0] // 32) + 1
        self.nb: float = (self.interpolated_grid.array.shape[1] // 32) + 1
        self.nc: float = (self.interpolated_grid.array.shape[2] // 32) + 1
        logging.debug(f"na, nb, nc: {self.na}, {self.nb}, {self.nc}")

        logging.debug(f"Translation list size: {len(self.translation_list)}")

    def _predict(self, raw_values: bool = False, overlap: int = 32):
        logging.info("Predicting map")

        predicted_map = np.zeros(
            (
                int(32 * self.na) + (32 - overlap), int(32 * self.nb) + (32 - overlap),
                int(32 * self.nc) + (32 - overlap), len(self.models)
            ),
            np.float32,
        )
        count_map = np.zeros(
            (

                int(32 * self.na) + (32 - overlap), int(32 * self.nb) + (32 - overlap),
                int(32 * self.nc) + (32 - overlap), len(self.models)),
            np.float32,
        )

        if self.compute_variance:
            variance_array_map = np.empty(
                (
                    int(32 * self.na) + (32 - overlap),
                    int(32 * self.nb) + (32 - overlap),
                    int(32 * self.nc) + (32 - overlap),
                    len(self.models)
                ), object
            )

            for i in range(variance_array_map.shape[0]):
                for j in range(variance_array_map.shape[1]):
                    for k in range(variance_array_map.shape[2]):
                        for index in range(len(self.models)):
                            variance_array_map[i, j, k, index] = []

        logging.debug(f"Predicted map shape - {predicted_map.shape}")

        for translation in tqdm(self.translation_list, total=len(self.translation_list),
                                miniters=1000 if len(self.translation_list) > 10_000 else 1,
                                disable=self.disable_progress_bar):
            x, y, z = translation

            sub_array = np.array(
                self.interpolated_grid.get_subarray(
                    start=translation, shape=[32, 32, 32]
                )
            ).reshape((1, 32, 32, 32, 1))

            if np.sum(sub_array) == 0:
                predicted_map[x: x + 32, y: y + 32, z: z + 32, :] += np.zeros(32, 32, 32)
                count_map[x: x + 32, y: y + 32, z: z + 32] += 1
                continue

            for model_index, model in enumerate(self.models):
                input_name = model.get_inputs()[0].name
                predicted_sub = np.array(model.run(None, {input_name: sub_array})).squeeze()
                arg_max = np.argmax(predicted_sub, axis=-1)

            # Taken from https://github.com/paulsbond/densitydensenet/blob/main/predict.py
                if raw_values:
                    predicted_map[x: x + 32, y: y + 32, z: z + 32, model_index] += predicted_sub[
                                                                      :, :, :, 1
                                                                      ]
                else:
                    predicted_map[x: x + 32, y: y + 32, z: z + 32, model_index] += arg_max
                    # x = np.append(variance_map[x: x + 32, y: y + 32, z: z + 32], arg_max.reshape(32,32,32,1), axis=-1)

                if self.compute_variance:
                    for i, a in enumerate(range(x, x + 32)):
                        for j, b in enumerate(range(y, y + 32)):
                            for k, c in enumerate(range(z, z + 32)):
                                variance_array_map[a, b, c, model_index].append(arg_max[i, j, k])

                count_map[x: x + 32, y: y + 32, z: z + 32, model_index] += 1

        predicted_map = predicted_map[
                        0:(32 * self.na),
                        0:(32 * self.nb),
                        0:(32 * self.nc),
                        :
                        ]

        count_map = count_map[
                    0:(32 * self.na),
                    0:(32 * self.nb),
                    0:(32 * self.nc),
                    :
                    ]

        logging.debug(f"Predicted map shape: {predicted_map.shape}")
        self.predicted_map = predicted_map / count_map

        if self.compute_variance:
            variance_maps = np.zeros(
                (
                    int(32 * self.na),
                    int(32 * self.nb),
                    int(32 * self.nc),
                    len(self.models)
                ),
                dtype=np.float32)

            for i in range(variance_maps.shape[0]):
                for j in range(variance_maps.shape[1]):
                    for k in range(variance_maps.shape[2]):
                        for model_index in range(len(self.models)):
                            variance_maps[i, j, k, model_index] = np.var(variance_array_map[i, j, k, model_index])
            self.variance_maps = variance_maps


def predict_map(model: str, input: str, output: str, resolution: float = 2.5, intensity: str = "FWT",
                phase: str = "PHWT", overlap: float = 16):
    model_path = find_model(model)
    prediction = Prediction(model_paths=[model_path])
    prediction.make_prediction(input, [intensity, phase], overlap=overlap)
    prediction.save_predicted_map(output)


def run():
    start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "-model", help="Model selection", required=False)
    parser.add_argument("-i", "-input", help="Input mtz", required=True)
    parser.add_argument("-o", "-output", help="Output base path, if multiple models, or output file path if single "
                                              "model", required=True)
    parser.add_argument("-r", "-resolution", nargs='?', help="Resolution cutoff")
    parser.add_argument("-intensity", nargs='?', help="Name of intensity column in MTZ")
    parser.add_argument("-phase", nargs='?', help="Name of phase column in MTZ")
    parser.add_argument("-overlap", nargs='?', help="Amount of overlap to use", const=16, default=16, type=int)
    parser.add_argument("-no-symmetry", action=argparse.BooleanOptionalAction, help="Compute predictions "
                                                                                            "for the entire unit cell")
    parser.add_argument("-variance", action=argparse.BooleanOptionalAction, help="Output variance map")
    parser.add_argument("-raw", action=argparse.BooleanOptionalAction, help="Output raw map (no argmax)")
    parser.add_argument("-gpu", action=argparse.BooleanOptionalAction, help="Use GPU (experimental)")
    parser.add_argument("-debug", action=argparse.BooleanOptionalAction, help="Turn on debug logging")
    parser.add_argument("-silent", action=argparse.BooleanOptionalAction, help="Turn off progress bar")
    parser.add_argument("-model_path", nargs='?', help="Path to model (development)")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = vars(parser.parse_args())

    log_level = logging.WARNING
    if args["debug"]:
        log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level, format="%(asctime)s %(levelname)s - %(message)s"
    )

    if not args["model_path"]:
        if not args["m"]:
            find_model("")
            return 

        if args["m"] == "all":
            models = ["phosphate", "sugar", "base"]
        else:
            models = [s.strip() for s in args["m"].split(",")]

        model_paths = [find_model(model) for model in models]
    else:
        model_paths = [args["model_path"]]

    if not model_paths:
        if not args["m"] or not os.path.exists(args["m"]):
            raise FileNotFoundError("Model path could not be found, check the supplied path")
        # model_paths = args["m"]
    else:
        logging.info(f"Found models: {' '.join(str(model_paths))}, continuing...")

    if not os.path.isfile(args["i"]):
        raise FileNotFoundError(
            f"Input file has not been found, check path\nPath Supplied {args['i']} from {os.getcwd()}")

    if args["raw"] and args["variance"]:
        logging.warning(
            f"Supplying both raw and variance flags does not output a raw variance map, just the variance map.")

    prediction = Prediction(model_paths=model_paths,
                            use_gpu=True if args["gpu"] else False,
                            compute_variance=True if args["variance"] else False,
                            disable_progress_bar=True if args["silent"] else False,
                            compute_entire_cell=True if args["no_symmetry"] else False)

    prediction.make_prediction(args["i"], [args["intensity"], args["phase"]], overlap=args["overlap"],
                               use_raw_values=True if args["raw"] else False)

    if not args["variance"]:
        prediction.save_predicted_map(args["o"])
    else:
        prediction.save_variance_map(args["o"])

    end = time.time()

    logging.info(f"Time taken {end - start:.2f} seconds / {(end - start) / 60:.2f} minutes")


def model_not_found_err():
    print("""
            No models have been found in either site_packages or CCP4/lib/data.
            You can install models using the command:
            nucleofind-install -m phosphate
        """)


def find_all_potential_models():
    model_extension = "*.onnx"

    potential_models = []

    for pkg in site.getsitepackages():
        models = glob(os.path.join(pkg, "nucleofind_models", model_extension))
        potential_models += models

    clibd = os.environ.get('CLIBD', "")
    if not os.path.exists(clibd) and not potential_models:
        print(
            """CCP4 Environment Variable - CLIBD is not found. 
            You can try sourcing it: 
            Ubuntu - source /opt/xtal/ccp4-X.X/bin/ccp4.setup-sh
            MacOS - source /Applications/ccp4-X.X/bin/ccp4.setup-sh
            """
        )
        return

    ccp4_model_path = os.path.join(clibd, "nucleofind_models")
    if not os.path.exists(ccp4_model_path) and not potential_models:
        model_not_found_err()
        return

    potential_models += glob(os.path.join(ccp4_model_path, model_extension))

    if not potential_models:
        model_not_found_err()

    return [Path(x) for x in potential_models]


def find_model(model_selection: str) -> str:
    models = find_all_potential_models()
    if not models:
        print("""No models were found, please use 

    nucleofind-install --all

to install all the models or

    nucleofind-install -m {phosphate,sugar,base}

to install a single model (choose either phosphate, sugar or base)
              """)
        exit()

    if model_selection:
        for model in models:
            filename = model.name
            if model_selection in filename:
                return model

    if len(models) == 1:
        print("Only found ", models[0], "- using that!")
        return models[0]

    print(f"The specified model type '{model_selection}' could not be found, please add one of the following flags")

    filenames = set([x.stem for x in models])
    for name in filenames:
        print(f"-m {name}")

    exit()


if __name__ == "__main__":
    run()
