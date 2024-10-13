"""Module containing the wheel models."""
from __future__ import annotations

import contextlib
from abc import abstractmethod
from typing import TYPE_CHECKING

from sympy import Symbol, symbols
from sympy.physics.mechanics import Point, Vector, inertia

from symbrim.core import ModelBase, NewtonianBodyMixin

with contextlib.suppress(ImportError):
    from bicycleparameters.io import remove_uncertainties

    from symbrim.utilities.parametrize import get_inertia_vals

    if TYPE_CHECKING:
        from bicycleparameters import Bicycle

if TYPE_CHECKING:
    with contextlib.suppress(ImportError):
        from symbrim.utilities.plotting import PlotModel

__all__ = ["WheelBase", "KnifeEdgeWheel", "ToroidalWheel"]


class WheelBase(NewtonianBodyMixin, ModelBase):
    """Wheel base class."""

    @property
    @abstractmethod
    def center(self) -> Point:
        """Point representing the center of the wheel."""

    @property
    @abstractmethod
    def rotation_axis(self) -> Vector:
        """Rotation axis of the wheel."""

    def get_param_values(  # noqa: PLR0912
        self, bicycle_parameters: Bicycle, position: str | None = None
    ) -> dict[Symbol, float]:  # pragma: no cover
        """Get the parameter values of the wheel.

        Parameters
        ----------
        bicycle_parameters : Bicycle
            Bicycle parameters object from the BicycleParameters package.
        position : str, optional
            Position of the wheel, by default None. Options are "front" and "rear".
        """
        params = super().get_param_values(bicycle_parameters)
        if position is None:
            return params
        if position not in ["front", "rear"]:
            raise ValueError("Position must be 'front' or 'rear'.")
        if "Benchmark" in bicycle_parameters.parameters:
            bp = remove_uncertainties(bicycle_parameters.parameters["Benchmark"])
            if position == "front":
                if "mF" in bp:
                    params[self.body.mass] = bp["mF"]
                if "IFxx" in bp and "IFyy" in bp:
                    params.update(get_inertia_vals(self.body, bp["IFxx"], bp["IFyy"]))
            elif position == "rear":
                if "mR" in bp:
                    params[self.body.mass] = bp["mR"]
                if "IRxx" in bp and "IRyy" in bp:
                    params.update(get_inertia_vals(self.body, bp["IRxx"], bp["IRyy"]))
        if "Measured" in bicycle_parameters.parameters:
            bp = remove_uncertainties(bicycle_parameters.parameters["Measured"])
            if position == "front":
                if "mF" in bp:
                    params[self.body.mass] = bp["mF"]
            elif position == "rear" and "mR" in bp:
                params[self.body.mass] = bp["mR"]
        return params


class KnifeEdgeWheel(WheelBase):
    """Knife edge wheel."""

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the attributes of the wheel."""
        return {
            **super().descriptions,
            self.radius: self.radius.__doc__,
        }

    @property
    def radius(self) -> Symbol:
        """Radius of the wheel."""
        return self.symbols["r"]

    def _define_objects(self) -> None:
        """Define the objects of the wheel."""
        super()._define_objects()
        self.body.central_inertia = inertia(self.body.frame,
                                            *symbols(self._add_prefix("ixx iyy ixx")))
        self.symbols["r"] = Symbol(self._add_prefix("r"))

    @property
    def center(self) -> Point:
        """Point representing the center of the wheel."""
        return self.body.masscenter

    @property
    def rotation_axis(self) -> Vector:
        """Rotation axis of the wheel."""
        return self.body.y

    def get_param_values(self, bicycle_parameters: Bicycle,
                         position: str | None = None
                         ) -> dict[Symbol, float]:  # pragma: no cover
        """Get the parameter values of the wheel.

        Parameters
        ----------
        bicycle_parameters : Bicycle
            Bicycle parameters object from the BicycleParameters package.
        position : str, optional
            Position of the wheel, by default None. Options are "front" and "rear".
        """
        params = super().get_param_values(bicycle_parameters, position)
        if position is None:
            return params
        bp = remove_uncertainties(bicycle_parameters.parameters.get(
            "Benchmark", bicycle_parameters.parameters.get("Measured")))
        if position == "front":
            params[self.radius] = bp["rF"]
        elif position == "rear":
            params[self.radius] = bp["rR"]
        return params

    def set_plot_objects(self, plot_object: PlotModel) -> None:
        """Set the symmeplot plot objects."""
        super().set_plot_objects(plot_object)
        plot_object.get_plot_object(self.body).attach_circle(
            self.center, self.radius, self.rotation_axis, facecolor="none",
            edgecolor="k")


class ToroidalWheel(WheelBase):
    """Toroidal shaped wheel."""

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the attributes of the wheel."""
        return {
            **super().descriptions,
            self.radius: self.radius.__doc__,
            self.transverse_radius: self.transverse_radius.__doc__
        }

    @property
    def radius(self) -> Symbol:
        """Radius of the wheel."""
        return self.symbols["r"]

    @property
    def transverse_radius(self) -> Symbol:
        """Transverse radius of curvature of the crown of the wheel."""
        return self.symbols["tr"]

    def _define_objects(self) -> None:
        """Define the objects of the wheel."""
        super()._define_objects()
        self.body.central_inertia = inertia(self.body.frame,
                                            *symbols(self._add_prefix("ixx iyy ixx")))
        self.symbols["r"] = Symbol(self._add_prefix("r"))
        self.symbols["tr"] = Symbol(self._add_prefix("tr"))

    @property
    def center(self) -> Point:
        """Point representing the center of the wheel."""
        return self.body.masscenter

    @property
    def rotation_axis(self) -> Vector:
        """Rotation axis of the wheel."""
        return self.body.y
