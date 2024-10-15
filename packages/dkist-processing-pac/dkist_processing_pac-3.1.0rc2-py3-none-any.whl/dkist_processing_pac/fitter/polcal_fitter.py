"""Machinery to collect data and parameter objects and spawn fits for each FOV point."""
import copy
import logging
import time

import lmfit
import numpy as np
from lmfit import Parameters

from dkist_processing_pac.fitter.fitter_parameters import NdParameterArray
from dkist_processing_pac.fitter.fitter_parameters import PolcalDresserParameters
from dkist_processing_pac.fitter.fitting_core import compare_I
from dkist_processing_pac.input_data.dresser import Dresser
from dkist_processing_pac.optics.calibration_unit import CalibrationUnit
from dkist_processing_pac.optics.telescope import Telescope

logger = logging.getLogger(__name__)


class FitObjects:
    """Container for all the objects necessary for a polcal fit.

    Namely the Dresser (input data), Calibration Unit and Telescope optical models, and a set of fitting parameters
    """

    def __init__(self, dresser: Dresser, fit_mode: str, init_set: str):
        self.dresser = dresser
        self.fit_mode = fit_mode
        self.init_set = init_set
        self.calibration_unit = CalibrationUnit(dresser)
        self.telescope = Telescope(dresser)
        self.full_parameters = PolcalDresserParameters(
            dresser=dresser, fit_mode=fit_mode, init_set=init_set
        )

        # Initialize CU and Telescope objects with global starting guesses. The point-specific initialization on the CM
        # happens inside run_fits
        initialization_parameters = self.init_parameters.first_parameters
        pardict = initialization_parameters.valuesdict()
        self.calibration_unit.load_pars_from_dict(pardict)
        self.telescope.load_pars_from_dict(pardict)

    @property
    def init_parameters(self) -> NdParameterArray:
        """Return just the starting parameters."""
        return self.full_parameters.init_params

    @property
    def fit_parameters(self) -> NdParameterArray:
        """Return the final fit parameters."""
        return self.full_parameters.fit_params

    @property
    def demoulation_matrices(self) -> np.ndarray:
        """Return the demodulation matrices from the final fit parameters."""
        return self.full_parameters.demodulation_matrices


class PolcalFitter:
    """Object that brings together data (Dresser), optic models (CM and TM), and fit parameters (PolcalDresserParameters) to run fits."""

    def __init__(
        self,
        *,
        local_dresser: Dresser,
        global_dresser: Dresser,
        fit_mode: str,
        init_set: str,
        fit_TM: bool = False,
        threads: int = 1,
        super_name: str = "",
        inherit_global_vary_in_local_fit: bool = False,
        _dont_fit: bool = False,
        suppress_local_starting_values: bool = False,
        **fit_kwargs,
    ):

        self.fit_mode = fit_mode
        self.init_set = init_set
        self.fits_have_run = False
        self.fit_TM = fit_TM

        self.check_dressers(local_dresser, global_dresser)

        logger.info("Setting up global fit objects...")
        self.global_objects = FitObjects(
            dresser=global_dresser, fit_mode=fit_mode, init_set=init_set
        )

        logger.info("Setting up local fit objects...")
        self.local_objects = FitObjects(dresser=local_dresser, fit_mode=fit_mode, init_set=init_set)

        # At this point the CU, telescope, and parameters objects have been set up and seeded with initial
        # guesses.

        if not _dont_fit:
            t1 = time.time()
            logger.info("Fitting global CU parameters")
            self.run_fits(
                fit_container=self.global_objects,
                threads=threads,
                super_name=super_name,
                **fit_kwargs,
            )

            global_fit_pars = self.global_objects.fit_parameters.first_parameters
            self.validate_global_fit(global_fit_pars)

            logger.info("Applying global CU parameters in local fits")
            if not inherit_global_vary_in_local_fit:
                logger.info("Global CU parameters will be fixed in local fits.")
            self.local_objects.full_parameters.apply_global_CU_params(
                global_fit_pars, inherit_global_vary=inherit_global_vary_in_local_fit
            )

            logger.info("Fitting local modulation matrices")
            self.run_fits(
                fit_container=self.local_objects,
                threads=threads,
                super_name=super_name,
                suppress_point_starting_values=suppress_local_starting_values,
                **fit_kwargs,
            )
            logger.info(f"Done fitting in {time.time() - t1:.1f} s.")
            self.fits_have_run = True

    @property
    def demodulation_matrices(self) -> np.ndarray:
        """Return the best-fit demodulation matrices if fits have been run, otherwise raise an error."""
        if not self.fits_have_run:
            raise ValueError("Cannot access demodulation matrices until fits have been run")

        return self.local_objects.demoulation_matrices

    @property
    def fit_parameters(self) -> NdParameterArray:
        """Return the best-fit parameters."""
        if not self.fits_have_run:
            raise ValueError("Cannot access best-fit parameters until fits have been run")

        return self.local_objects.fit_parameters

    def run_fits(
        self,
        *,
        fit_container: FitObjects,
        suppress_point_starting_values: bool = False,
        threads: int = 1,
        super_name: str = "",
        **fit_kwargs,
    ) -> None:
        """Start a minimizer for each FOV point and record the results.

        This is also where the non-CU parameters are initialized for each FOV point. This happens prior to fitting.
        """
        use_M12 = fit_container.full_parameters.switches["use_M12"]
        fov_shape = fit_container.dresser.shape
        fov_indices = tuple(i - 1 for i in fov_shape)
        num_fits = np.prod(fov_shape)
        self.print_starting_values(fit_container.init_parameters.first_parameters, global_pars=True)
        for i in range(num_fits):
            # These lines ensure that all FOV points have the same CU and TM starting parameters.
            # If we don't deepcopy then each point will start off at the best-fit of the previous point, which is not
            # strictly wrong, just not how we do it.
            point_TM = copy.deepcopy(fit_container.telescope)
            point_CM = copy.deepcopy(fit_container.calibration_unit)

            # Get the correct SoCC out of the Dresser (heyo!)
            idx = np.unravel_index(i, fov_shape)
            logger.info(f"Fitting point {idx} / {fov_indices}")
            I_cal, I_unc = fit_container.dresser[idx]

            # Initialize sensible starting values for non-CU parameters
            fit_container.full_parameters.initialize_single_point_parameters(
                idx, CM=point_CM, TM=point_TM
            )
            params_to_fit = fit_container.init_parameters[idx]
            if not suppress_point_starting_values:
                self.print_starting_values(params_to_fit, global_pars=False)

            # We use a single array object to contain the modulation matrix so a new object is created during each
            # fit iteration
            modmat = np.zeros((I_cal.shape[0], 4), dtype=np.float64)

            t1 = time.time()
            mini = lmfit.Minimizer(
                compare_I,
                params_to_fit,
                fcn_args=(I_cal, I_unc, point_TM, point_CM, modmat),
                fcn_kws={"use_M12": use_M12},
            )
            try:
                fit_out = mini.minimize(method="leastsq", params=params_to_fit, **fit_kwargs)
                fit_params = fit_out.params
                logger.info(
                    f"minimization completed in {time.time() - t1:4.2f} s. Chisq = {fit_out.chisqr:8.2e}, redchi = {fit_out.redchi:8.2e}"
                )
            except Exception as e:
                fit_params = params_to_fit.copy()
                for parameter in fit_params.values():
                    parameter.set(value=np.nan)
                logger.info(f"fit failed in {time.time() - t1:4.2f} s. Setting fit values to NaN.")
                logger.info(f"Error was '{e}'")

            # Save the best-fit parameters
            fit_container.fit_parameters[idx] = fit_params

    @staticmethod
    def check_dressers(local_dresser: Dresser, global_dresser: Dresser) -> None:
        """
        Check that the input Dressers conform to base expectations.

        Namely, the global Dresser only has a single point and neither Dresser has NaN values in its `I_clear` property.
        """
        if np.prod(global_dresser.shape) != 1:
            raise ValueError(
                f"Global dresser is expected to only have a single point. Provided dresser has shape {global_dresser.shape}"
            )

        for dresser, name in zip(
            [local_dresser, global_dresser], ["Local dresser", "Global dresser"]
        ):
            if np.sum(np.isnan(dresser.I_clear)) > 0:
                raise ValueError(f"{name} has NaNs in its I_clear: {global_dresser.I_clear}")

    @staticmethod
    def validate_global_fit(global_fit_pars: Parameters) -> None:
        """Check that there are no NaN values in the global fit parameters."""
        for par_value in global_fit_pars.valuesdict().values():
            if np.isnan(par_value):
                raise ValueError(
                    f"NaN values detected in global fit: {global_fit_pars.valuesdict()}"
                )

    @staticmethod
    def print_starting_values(params: Parameters, global_pars: bool = True) -> None:
        """Print out free and fixed parameter values.

        If `global_pars` is True then only parameters pertaining to all FOV points will be printed. If it is False then
        *only* parameters pertaining to FOV points will be printed.
        """
        fixed_pars = dict()
        free_pars = dict()

        for name, par in params.items():
            if ("I_sys" in name or "modmat" in name) is global_pars:
                continue
            if par.vary:
                free_pars[name] = par.value
            else:
                fixed_pars[name] = par.value

        logger.info(f"{'Global' if global_pars else 'Local'} fixed parameters:")
        if len(fixed_pars) == 0:
            logger.info("\tNone")
        for p, v in fixed_pars.items():
            logger.info(f"\t{p} = {v:0.5f}")

        logger.info(f"{'Global' if global_pars else 'Local'} free parameters:")
        if len(free_pars) == 0:
            logger.info("\tNone")
        for p, v in free_pars.items():
            logger.info(f"\t{p} = {v:0.5f}")
