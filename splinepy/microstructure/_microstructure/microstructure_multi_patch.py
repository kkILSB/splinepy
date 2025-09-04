import gustaf as _gus
import numpy as _np

from splinepy._base import SplinepyBase as _SplinepyBase
from splinepy.bezier import Bezier as _Bezier
from splinepy.microstructure._microstructure.microstructure_single_patch \
        import _MicrostructureSinglePatch
from splinepy.multipatch import Multipatch as _MultiPatch
from splinepy.splinepy_core import PySpline as _PySpline

class _MicrostructureMultiPatch(_SplinepyBase):
    """Helper class to facilitate the construction of microstructures."""

    def __init__(
        self,
        deformation_functions=None,
        tilings=None,
        microtiles=None,
        parametrization_functions=None,
    ):
        """Helper class to facilitate the construction of microstructures for
        multi-patch deformation functions.

        Parameters
        ----------
        deformation_functions : multi-patch 
          Outer function that describes the contour of the microstructured
          geometry
        tilings : (list of) int / list<int>
          microtiles per parametric dimension
        microtiles : (list of) spline / list<spline> / user-object
          Representation of the building block defined in the unit cube
        parametrization_functions : (list of) callables (optional)
          Function to describe spline parameters
        """
        if deformation_functions is not None:
                self.deformation_functions = deformation_functions
        if tilings is not None: self.tilings = tilings
        if microtiles is not None: self.microtiles = microtiles
        if parametrization_functions is not None:
                self.parametrization_functions = parametrization_functions

    @property
    def deformation_functions(self):
        """Deformation functions defining the outer geometry (contour) of the
        microstructure.

        Parameters
        ----------
        None

        Returns
        -------
        deformation_functions : multi-patch
        """
        return getattr(self, "_deformation_functions", None)

    @deformation_functions.setter
    def deformation_functions(self, deformation_functions):
        """Deformation functions setter defining the outer geometry of the
        microstructure. Must be multi-patch.

        Parameters
        ----------
        deformation_functions : multi-patch

        Returns
        -------
        None
        """
        self._set_property(deformation_functions, _MultiPatch, number=0)

    @property
    def tilings(self):
        """Numbers of microtiles per parametric dimension.

        Parameters
        ----------
        None

        Returns
        -------
        tilings : (list of) int / list<int>
        """
        return getattr(self, "_tilings", None)

    @tilings.setter
    def tilings(self, tilings):
        """Setter for the tilings attribute, defining the numbers of microtiles
        per parametric dimension.

        Parameters
        ----------
        tilings : (list of) int / list<int>
          Numbers of tiles for each dimension respectively
        Returns
        -------
        None
        """
        self._set_property(tilings, (int, list), number=1)

    @property
    def microtiles(self):
        """Microtiles is a list of lists of splines.

        Parameters
        ----------
        None

        Returns
        -------
        microtiles : (list of) spline / list<spline> / user-object
          list of arbitrary long lists of splines that define the microtiles
        """
        return getattr(self, "_microtiles", None)

    @microtiles.setter
    def microtiles(self, microtiles):
        """Setter for microtiles.

        Microtiles must be a list of either a spline, a list of splines, or a "
        "class that provides (at least) a `create_tile` function and a `dim` "
        "member.

        Parameters
        ----------
        microtiles : (list of) spline / list<spline> / user-object

        Returns
        -------
        None
        """
        # Check of type is postponed to single-patch as it can be custom class.
        self._set_property(microtiles, None, number=2)

    @property
    def parametrization_functions(self):
        """Functions, that - if required - parametrizes the microtiles.

        In order to use said functions, the Microtiles need to provide a couple
        of attributes:

         - evaluation_points - a list of points defined in the unit cube
           that will be evaluated in the parametrization functions to provide
           the required set of data points
         - para_dim - dimensionality of the parametrization
           functions and number of design variables for said microtiles

        Parameters
        ----------
        None

        Returns
        -------
        parametrization_functions : (list of) callable
          Functions that describes the local tile parameters
        """
        return getattr(self, "_parametrization_functions", None)

    @parametrization_functions.setter
    def parametrization_functions(self, parametrization_functions):
        """Setter for parametrization functions.

        Functions, that - if required - parametrizes the microtiles.

        In order to use said functions, the Microtiles need to provide a couple
        of attributes:

         - evaluation_points - a list of points defined in the unit cube
           that will be evaluated in the parametrization functions to provide
           the required set of data points
         - para_dim - dimensionality of the parametrization
           functions and number of design variables for said microtiles

        Parameters
        ----------
        parametrization_functions : (list of) callable
          Functions that describes the local tile parameters

        Returns
        -------
        None
        """
        self._set_property(parametrization_functions, list, number=3)

    @property
    def parameter_sensitivity_functions(self):
        """Functions, that - if required - determine the parameter sensitivity
        of a set of microtiles.

        In order to use said functions, the Microtiles need to provide a couple
        of attributes:

         - evaluation_points - a list of points defined in the unit cube
           that will be evaluated in the parametrization function to provide
           the required set of data points
         - para_dim - dimensionality of the parametrization
           function and number of design variables for said microtiles
         - parametrization_functions - a function that calculates the microtiles
           parameters based on the position of the tile within the deformation
           functions parametric space

        Parameters
        ----------
        None

        Returns
        -------
        parameter_sensitivity_functions : (list of) callable
          Functions that describes the local tile parameters
        """
        return getattr(self, "_parameter_sensitivity_functions", None)

    @parameter_sensitivity_functions.setter
    def parameter_sensitivity_functions(self, parameter_sensitivity_functions):
        """Setter for parameter sensitivity functions.

        Functions, that - if required - determine the parameter sensitivity
        of a set of microtiles.

        In order to use said functions, the Microtiles need to provide a couple
        of attributes:

         - evaluation_points - a list of points defined in the unit cube
           that will be evaluated in the parametrization function to provide
           the required set of data points
         - para_dim - dimensionality of the parametrization
           function and number of design variables for said microtiles
         - parametrization_functions - a function that calculates the microtiles
           parameters based on the position of the tile within the deformation
           functions parametric space

        Parameters
        ----------
        parameter_sensitivity_functions : (list of) callable
          Functions that describes the local tile parameters

        Returns
        -------
        None
        """
        self._set_property(parameter_sensitivity_functions, list, number=4)

    def create(
        self,
        closing_faces=None,
        knot_span_wise=None,
        macro_sensitivities=None,
        **kwargs,
    ):
        """Create a Microstructure for a multi-patch deformation function.

        Parameters
        ----------
        closing_faces : (list of) string
          If not None, Microtile must provide a function `closing_tile`
          Represents coordinate to be a closed surface {"x", "y", "z"}
        knot_span_wise : (list of) bool
          Insertion per knotspan vs. total number per paradim
        macro_sensitivities: (list of) bool
          Calculate the derivatives of the structure with respect to the outer
          control point variables
        **kwargs
          will be passed to `create_tile` function

        Returns
        -------
        Microstructure : list<spline>
          finished microstructure based on object requirements
        """
        # Check sanity
        deformation_functions, tilings, microtiles = \
                self._deformation_functions, self._tilings, self._microtiles
        if (deformation_functions is None) or (tilings is None) or \
                (microtiles is None):
            self._logi("Current information not sufficient, awaiting further "
                       "assignments!")
            return None

        number_of_patches, parametrization_functions, \
                parameter_sensitivity_functions = \
                        len(deformation_functions.patches), \
                                self._parametrization_functions, \
                                        self._parameter_sensitivity_functions
        CheckForListAndCreateOtherwise = lambda property : property if \
                (isinstance(property, list) and len(property) ==
                        number_of_patches) else [property
                                for _ in range(number_of_patches)]
        def CheckForAmbiguity(property, name):
            if isinstance(property, list) and (len(property) ==
                                               number_of_patches):
                    self._logd("Possible ambiguity detected: " + name + "s is "
                            "a list, whose length equals the number of "
                            "patches. Each item will be interpreted as a " +
                            name + " for a patch. If this is not intended and "
                            "the list shoud instead be repeated for each "
                            "patch, please do this explicitly before setting "
                            "the " + name + "s!")
            return CheckForListAndCreateOtherwise(property)

        tilings = CheckForAmbiguity(tilings, "tiling")
        microtiles = CheckForAmbiguity(microtiles, "microtile")
        parametrization_functions = \
                CheckForListAndCreateOtherwise(parametrization_functions)
        microstructures = [_MicrostructureSinglePatch(patch, tiling, microtile,
                parametrization_function) for patch, tiling, microtile,
                        parametrization_function in
                                zip(deformation_functions.patches, tilings,
                                        microtiles, parametrization_functions)]
        self._microstructures = microstructures
        parameter_sensitivity_functions = \
                CheckForAmbiguity(parameter_sensitivity_functions,
                                  "parameter_sensitivity_function")

        # Use a multipatch object to bundle all information
        for microstructure, parameter_sensitivity_function in \
                zip(microstructures, parameter_sensitivity_functions):
                microstructure._parameter_sensitivity_function = \
                        parameter_sensitivity_function
        closing_faces = CheckForListAndCreateOtherwise(closing_faces)
        knot_span_wise = CheckForListAndCreateOtherwise(knot_span_wise)
        macro_sensitivities = \
                CheckForListAndCreateOtherwise(macro_sensitivities)
        multi_patches = [microstructure.create(closing_face,
                knot_span_wise_microstructure,
                macro_sensitivities_microstructure, **kwargs) for
                microstructure, closing_face, knot_span_wise_microstructure,
                macro_sensitivities_microstructure in zip(microstructures,
                closing_faces, knot_span_wise, macro_sensitivities)]
        multi_patch = _MultiPatch([patch for _multi_patch in multi_patches
                                   for patch in _multi_patch.patches])

        # Add fields if requested
        if macro_sensitivities or not all([parameter_sensitivity_function is
                None for parameter_sensitivity_function in
                        parameter_sensitivity_functions]):
                multi_patch.add_fields([[patch for __multi_patch in multi_patches for patch in (_field.patches if __multi_patch is _multi_patch else [None] * len(__multi_patch.patches))] for _multi_patch in multi_patches for _field in _multi_patch.fields], multi_patch.dim)

        return multi_patch

    def show(self, use_saved=False, **kwargs):
        """
        Shows microstructure. Consists of deformation_functions, microtiles, and
        microstructure. Supported only by vedo.

        Parameters
        ----------
        use_saved : bool
        **kwargs : kwargs
          Will be passed to show function

        Returns
        -------
        plt: vedo.Plotter
        """
        if use_saved:
            if hasattr(self, "_microstructure_created"):
                microstructure = self._microstructure_created
            else:
                raise ValueError("No previously created microstructure saved!")
        else:
            # Create on the fly
            microstructure = self.create(**kwargs)

        # Precompute splines
        microtiles = [microtile.create_tile(**kwargs)
                              for microtile in self.microtiles]

        # turn off control points for clarity
        microstructure.show_options["control_points"] = False

        # Show in vedo
        return _gus.show(
            ["Deformation Function", self._deformation_functions],
            *[["Microtile " + str(index), microtile[0]]
              for index, microtile in enumerate(microtiles)],
            ["Composed Microstructure", microstructure],
            **kwargs,
        )

    def _set_property(self, value, Classes, number):
        property_name, can_be_callable = ("deformation_function", "tiling",
                "microtile", "parametrization_function",
                "parameter_sensitivity_function")[number] + "s", number > 2
        if not (value is None or ((number == 2) or isinstance(value, Classes))
                or (can_be_callable and callable(property))): raise ValueError(
                        "Argument " + property_name + " must be None" + ("," if
                                can_be_callable else " or") + " an instance of "
                                        f"{Classes}" + (", or callable" if
                                                can_be_callable else "") + "!")
        setattr(self, "_" + property_name, value)
