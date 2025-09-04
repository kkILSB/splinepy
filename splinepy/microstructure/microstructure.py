from splinepy._base import SplinepyBase as _SplinepyBase

class Microstructure(_SplinepyBase):
    """Interface class to facilitate the construction of microstructures."""

    def __init__(
        self,
        deformation_function=None,
        tiling=None,
        microtile=None,
        parametrization_function=None,
    ):
        """Interface class to facilitate the construction of microstructures.

        Parameters
        ----------
        deformation_function : single-patch (or multi-patch)
          Outer function that describes the solid analogue of the
          microstructured geometry
        tiling : (list of) int / list<int>
          microtiles per parametric dimension
        microtile : (list of) spline / list<spline> / user-object
          Representation of the building block defined in the unit cell
        parametrization_function : (list of) callables (optional)
          Function to evaluate parameters of the unit cells
        """
        from splinepy.microstructure._microstructure import \
                _MicrostructureMultiPatch, _MicrostructureSinglePatch
        from splinepy.splinepy_core import PySpline as _PySpline

        self._is_single_patch = isinstance(deformation_function, _PySpline)
        self._microstructure = (_MicrostructureSinglePatch if
                self._is_single_patch else
                        _MicrostructureMultiPatch)(deformation_function, tiling,
                                microtile, parametrization_function)

    @property
    def deformation_function(self):
        """Deformation function defining the outer geometry (solid analogue) of
        the microstructure.

        Parameters
        ----------
        None

        Returns
        -------
        deformation_function : single-patch (or multi-patch)
        """
        return self._get_property(number=0, message=None)

    @deformation_function.setter
    def deformation_function(self, deformation_function):
        """Deformation function setter defining the outer geometry of the
        microstructure. Must be single-patch (or multi-patch).

        Parameters
        ----------
        deformation_function : single-patch (or multi-patch)

        Returns
        -------
        None
        """
        get_attribute = lambda number : self._get_property(number, message=None)
        self.__init__(deformation_function, get_attribute(number=1),
                      get_attribute(number=2), get_attribute(number=3))

    @property
    def tiling(self):
        """Number of microtiles per parametric dimension.

        Parameters
        ----------
        None

        Returns
        -------
        tiling : (list of) int / list<int>
        """
        return self._get_property(number=1, message=None)

    @tiling.setter
    def tiling(self, tiling):
        """Setter for the tiling attribute, defining the number of microtiles
        per parametric dimension.

        Parameters
        ----------
        tiling : (list of) int / list<int>
          Number of tiles for each dimension respectively

        Returns
        -------
        None
        """
        self._set_property(number=1, value=tiling, message="Successfully set "
                                   f"tiling to : {self.tiling}")

    @property
    def microtile(self):
        """Microtile is a list of splines.

        Parameters
        ----------
        None

        Returns
        -------
        microtile : (list of) spline / list<spline> / user-object
          arbitrary long list of splines that define the microtile
        """
        return self._get_property(number=2, message="microtile is empty. "
                       "Please check splinepy.microstructure.tiles.show() for "
                       "predefined tile collections.")

    @microtile.setter
    def microtile(self, microtile):
        """Setter for microtile.

        Microtile must be either a spline, a list of splines, or a class that
        provides (at least) a `create_tile` function and a `dim` member
        (potentially a list).

        Parameters
        ----------
        microtile : (list of) spline / list<spline> / user-object

        Returns
        -------
        None
        """
        self._set_property(number=2, value=microtile, message=None)

    @property
    def parametrization_function(self):
        """Function, that - if required - parametrizes the microtiles
        (potentially list).

        In order to use said function, the Microtile needs to provide a couple
        of attributes:

         - evaluation_points - a list of points defined in the unit cube
           that will be evaluated in the parametrization function to provide
           the required set of data points
         - para_dim - dimensionality of the parametrization
           function and number of design variables for said microtile

        Parameters
        ----------
        None

        Returns
        -------
        parametrization_function : (list of) callable
          Function that describes the local tile parameters
        """
        return self._get_property(number=3, message=None)

    @parametrization_function.setter
    def parametrization_function(self, parametrization_function):
        """Setter for parametrization function.
        
        Function, that - if required - parametrizes the microtiles (potentially
        list).

        In order to use said function, the Microtile needs to provide a couple
        of attributes:

         - evaluation_points - a list of points defined in the unit cube
           that will be evaluated in the parametrization function to provide
           the required set of data points
         - para_dim - dimensionality of the parametrization
           function and number of design variables for said microtile

        Parameters
        ----------
        parametrization_function : (list of) callable
          Function that describes the local tile parameters

        Returns
        -------
        None
        """
        self._set_property(number=3, value=parametrization_function,
                           message=None)

    @property
    def parameter_sensitivity_function(self):
        """Function, that - if required - determines the parameter sensitivity
        of a set of microtiles (potentially list).

        In order to use said function, the Microtile needs to provide a couple
        of attributes:

         - evaluation_points - a list of points defined in the unit cube that
           will be evaluated in the parametrization function to provide the
           required set of data points
         - para_dim - dimensionality of the parametrization function and number
           of design variables for said microtile
         - parametrization_function - a function that calculates the microtile
           parameters based on the position of the tile within the deformation
           functions parametric space

        Parameters
        ----------
        None

        Returns
        -------
        parameter_sensitivity_function : (list of) callable
          Function that describes the sensitivities of local tile parameters
        """
        return self._get_property(number=4, message=None)

    @parameter_sensitivity_function.setter
    def parameter_sensitivity_function(self, parameter_sensitivity_function):
        """Setter for parametrization sensitivity function.
        
        Function, that - if required - determines the parameter sensitivity of a
        set of microtiles (potentially list).

        In order to use said function, the Microtile needs to provide a couple
        of attributes:

         - evaluation_points - a list of points defined in the unit cube that
           will be evaluated in the parametrization function to provide the
           required set of data points
         - para_dim - dimensionality of the parametrization function and number
           of design variables for said microtile
         - parametrization_function - a function that calculates the microtile
           parameters based on the position of the tile within the deformation
           functions parametric space

        Parameters
        ----------
        parameter_sensitivity_function : (list of) callable
          Function that describes the sensitivities of local tile parameters

        Returns
        -------
        None
        """
        self._set_property(number=4, value=parameter_sensitivity_function,
                           message=None)

    def create(
        self,
        closing_face=None,
        knot_span_wise=None,
        macro_sensitivities=None,
        **kwargs,
    ):
        """Create a Microstructure for a deformation function.

        Parameters
        ----------
        closing_face : (list of) string
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
        return self._microstructure.create(closing_face, knot_span_wise,
                                           macro_sensitivities, **kwargs)

    def show(self, use_saved=False, **kwargs):
        """
        Shows microstructure. Consists of deformation_function, microtile, and
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
        return self._microstructure.show(use_saved, **kwargs)

    def _get_property_name(self, number):
        return "_" + ("deformation_function", "tiling", "microtile",
                      "parametrization_function",
                      "parameter_sensitivity_function")[number] + ("" if
                              self._is_single_patch else "s")

    def _get_property(self, number, message):
        attribute_name = self._get_property_name(number)
        if hasattr(self._microstructure, attribute_name):
            return getattr(self._microstructure, attribute_name)
        else:
            if message is not None: self._logi(message)
            return None

    def _set_property(self, number, value, message):
        setattr(self._microstructure, self._get_property_name(number), value)
        if message is not None: self._logd(message)
