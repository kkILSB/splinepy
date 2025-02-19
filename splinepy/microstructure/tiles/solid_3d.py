import numpy as _np

from splinepy.bezier import Bezier as _Bezier
from splinepy.microstructure.tiles.tile_base import TileBase as _TileBase


class Solid3D(_TileBase):
    """Cubic tile that can be used to create solid reference geometries without microstructure.

    .. raw:: html

        <p><a href="../_static/Solid3D.html">Fullscreen</a>.</p>
        <embed type="text/html" width="100%" height="400" src="../_static/Solid3D.html" />

    """  # noqa: E501

    dim = 3  # hot fix: hide base_tile method that does not work any longer from python 3.13
    _dim = 3
    _para_dim = 3
    _evaluation_points = _np.array([[]])
    _n_info_per_eval_point = 0

    def _closing_tile(
        self,
        parameters=None,
        parameter_sensitivities=None,
        closure=None,
        **kwargs,  # noqa ARG002
    ):
        """Create a closing tile to match with closed surface.

        Parameters
        ----------
        parameters : np.ndarray(0, 0)
          No evaluation points with zero parameters are used. The parameters
          must be a two-dimensional np.array.
        parameter_sensitivities: np.ndarray(0, 0, para_dim)
          No parameter sensitivities are used. The parameter sensitivities must
          be a three-dimensional np.array.
        closure : str
          parametric dimension that needs to be closed.

        Returns
        -------
        list_of_splines : list(splines)
        derivative_list : list / None
        """

        return create_tile(parameters, parameter_sensitivities, closure=None)

    def create_tile(
        self,
        parameters=None,
        parameter_sensitivities=None,
        closure=None,
        **kwargs,  # noqa ARG002
    ):
        """Create a cubic microtile.

        Parameters
        ----------
        parameters : np.array(0, 0)
          No evaluation points with zero parameters is used. The parameters must
          be a two-dimensional np.array.
        parameter_sensitivities: np.ndarray(0, 0, para_dim)
          No parameter sensitivities are used. The parameter sensitivities must
          be a three-dimensional np.array.
        closure : str
          parametric dimension that needs to be closed.
        **kwargs
          Will be passed to _closing_tile if given

        Returns
        -------
        list_of_splines : list(splines)
        derivative_list : list / None
        """

        if closure is not None:
            return self._closing_tile(
                parameters=None,
                parameter_sensitivities=None,
                closure=None,
                **kwargs,
            )

        splines, derivatives = [], []
        for i_derivative in range(3):
            # Constant auxiliary values
            v_one_half = 0.5 if i_derivative == 0 else 0.0

            spline_list, center = [], [v_one_half] * 3

            # Create the center-tile
            center_points = _np.array(
                [
                    [-v_one_half, -v_one_half, -v_one_half],
                    [v_one_half, -v_one_half, -v_one_half],
                    [-v_one_half, v_one_half, -v_one_half],
                    [v_one_half, v_one_half, -v_one_half],
                    [-v_one_half, -v_one_half, v_one_half],
                    [v_one_half, -v_one_half, v_one_half],
                    [-v_one_half, v_one_half, v_one_half],
                    [v_one_half, v_one_half, v_one_half],
                ]
            )
            spline_list.append(
                _Bezier(
                    degrees=[1, 1, 1], control_points=center_points + center
                )
            )

            if i_derivative == 0:
                splines = spline_list.copy()
            else:
                derivatives.append(spline_list)

        return (splines, derivatives)
