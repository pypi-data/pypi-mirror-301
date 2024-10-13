"""Module containing the hand grip connections."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy import symbols
from sympy.physics.mechanics import (
    LinearDamper,
    LinearPathway,
    LinearSpring,
    Point,
    System,
    dynamicsymbols,
)

from symbrim.brim.base_connections import HandGripsBase
from symbrim.utilities.utilities import check_zero

if TYPE_CHECKING:
    from symbrim.core import Attachment

__all__ = ["HolonomicHandGrips", "SpringDamperHandGrips"]


class HolonomicHandGrips(HandGripsBase):
    """Constrain the hands to the steer using holonomic constraints.

    Explanation
    -----------
    This connection defines the hands as holonomic constraints on the steer. The closed
    loop should be time independent in all directions, otherwise one will introduce
    additional constraints making the resulting system invalid. Some simple checks are
    done to verify that this is not the case. An example where this may occur is when
    the arms cannot move sideways with respect to the steer, while the shoulder width
    and the steer width are different.
    """

    def _define_objects(self) -> None:
        """Define the objects."""
        super()._define_objects()
        self._system = System(self.front_frame.system.frame,
                              self.front_frame.system.fixed_point)

    def _define_constraints(self) -> None:
        """Define the constraints."""

        def attach_hand(hand_point: Point, hand_grip: Attachment) -> None:
            """Attach the hand to the steer."""
            for direction in hand_grip.frame:
                constr = hand_point.pos_from(hand_grip.point).dot(direction)
                if not check_zero(constr):
                    if check_zero(constr.diff(dynamicsymbols._t)):
                        error_msg.append(
                            f"While constraining the the hands to the steer, it was "
                            f"found that the holonomic constraint of a hand along "
                            f"{direction} is not dependent on time. The following "
                            f"equations should be set to zero by redefining symbols "
                            f"before the define_kinematics stage: {constr}")
                    hol_constrs.append(constr)
                    aux_vel = (
                        self.auxiliary_handler.get_auxiliary_velocity(hand_point) -
                        self.auxiliary_handler.get_auxiliary_velocity(hand_grip.point))
                    vel_constrs.append(constr.diff(dynamicsymbols._t) +
                                       aux_vel.dot(direction))

        super()._define_constraints()
        error_msg, hol_constrs, vel_constrs = [], [], []
        if self.left_arm:
            attach_hand(self.left_arm.hand_interpoint, self.front_frame.left_hand_grip)
        if self.right_arm:
            attach_hand(self.right_arm.hand_interpoint,
                        self.front_frame.right_hand_grip)
        if error_msg:
            raise ValueError(error_msg)
        self.system.add_holonomic_constraints(*hol_constrs)
        self.system.velocity_constraints = vel_constrs


class SpringDamperHandGrips(HandGripsBase):
    """Constrain the hands to the steer using spring-dampers."""

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the objects."""
        return {
            **super().descriptions,
            self.symbols["k"]:
                "Spring stiffness of the connection between the steer and the hands.",
            self.symbols["c"]: "Damping coefficient of the connection between the "
                               "steer and the hands.",
        }

    def _define_objects(self) -> None:
        """Define the objects."""
        self.symbols["k"], self.symbols["c"] = symbols(self._add_prefix("k c"))
        self._system = System()

    def _define_loads(self) -> None:
        """Define the loads."""
        super()._define_loads()
        if self.left_arm:
            path_left = LinearPathway(
                self.front_frame.left_hand_grip.point, self.left_arm.hand_interpoint)
            self.system.add_actuators(
                LinearSpring(self.symbols["k"], path_left),
                LinearDamper(self.symbols["c"], path_left)
            )
        if self.right_arm:
            path_right = LinearPathway(
                self.front_frame.right_hand_grip.point, self.right_arm.hand_interpoint)
            self.system.add_actuators(
                LinearSpring(self.symbols["k"], path_right),
                LinearDamper(self.symbols["c"], path_right)
            )
