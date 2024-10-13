"""Module containing the hip joints."""
from __future__ import annotations

from sympy import Matrix, cos, sin
from sympy.physics.mechanics import (
    PinJoint,
    SphericalJoint,
    System,
    Torque,
    dynamicsymbols,
)

from symbrim.core import LoadGroupBase
from symbrim.rider.base_connections import LeftHipBase, RightHipBase

__all__ = ["SphericalLeftHip", "SphericalRightHip", "PinRightHip", "PinLeftHip",
           "SphericalHipTorque", "SphericalHipSpringDamper"]


class SphericalHipMixin:
    """Spherical joint between the pelvis and the leg."""

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the objects."""
        return {
            **super().descriptions,
            self.q[0]: "Flexion angle of the hip.",
            self.q[1]: "Adduction angle of the hip.",
            self.q[2]: "Endorotation angle of the hip.",
            self.u[0]: "Flexion angular velocity of the hip.",
            self.u[1]: "Adduction angular velocity of the hip.",
            self.u[2]: "Endorotation angular velocity of the hip.",
        }

    def _define_objects(self) -> None:
        """Define the objects."""
        super()._define_objects()
        self.q = Matrix(
            dynamicsymbols(self._add_prefix("q_flexion, q_adduction, q_rotation")))
        self.u = Matrix(
            dynamicsymbols(self._add_prefix("u_flexion, u_adduction, u_rotation")))
        self._system = System.from_newtonian(self.pelvis.body)


class SphericalLeftHip(SphericalHipMixin, LeftHipBase):
    """Spherical joint between the pelvis and the left leg."""

    def _define_kinematics(self) -> None:
        """Define the kinematics."""
        super()._define_kinematics()
        self.system.add_joints(
            SphericalJoint(
                self._add_prefix("joint"), self.pelvis.body, self.leg.hip, self.q,
                self.u, self.pelvis.left_hip_point, self.leg.hip_interpoint,
                self.pelvis.frame, self.leg.hip_interframe, rot_type="BODY",
                amounts=(self.q[0], -self.q[1], self.q[2]), rot_order="YXZ")
        )


class SphericalRightHip(SphericalHipMixin, RightHipBase):
    """Spherical joint between the pelvis and the right leg."""

    def _define_kinematics(self) -> None:
        """Define the kinematics."""
        super()._define_kinematics()
        self.system.add_joints(
            SphericalJoint(
                self._add_prefix("joint"), self.pelvis.body, self.leg.hip, self.q,
                self.u, self.pelvis.right_hip_point, self.leg.hip_interpoint,
                self.pelvis.frame, self.leg.hip_interframe, rot_type="BODY",
                amounts=(self.q[0], self.q[1], -self.q[2]), rot_order="YXZ")
        )


class PinHipMixin:
    """Pin joint between the pelvis and the leg."""

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the objects."""
        return {
            **super().descriptions,
            self.q[0]: "Flexion angle of the hip.",
            self.u[0]: "Flexion angular velocity of the hip.",
        }

    def _define_objects(self) -> None:
        """Define the objects."""
        super()._define_objects()
        self.q = Matrix([dynamicsymbols(self._add_prefix("q_flexion"))])
        self.u = Matrix([dynamicsymbols(self._add_prefix("u_flexion"))])
        self._system = System.from_newtonian(self.pelvis.body)

    def _define_kinematics(self) -> None:
        """Define the kinematics."""
        super()._define_kinematics()
        self.system.add_joints(
            PinJoint(
                self._add_prefix("joint"), self.pelvis.body, self.leg.hip, self.q,
                self.u, self.pelvis.left_hip_point, self.leg.hip_interpoint,
                self.pelvis.frame, self.leg.hip_interframe,
                joint_axis=self.pelvis.y)
        )


class PinLeftHip(PinHipMixin, LeftHipBase):
    """Pin joint between the pelvis and the left leg."""


class PinRightHip(PinHipMixin, RightHipBase):
    """Pin joint between the pelvis and the right leg."""


class SphericalHipTorque(LoadGroupBase):
    """Torque for the spherical hip joints."""

    parent: SphericalLeftHip | SphericalRightHip
    required_parent_type = (SphericalLeftHip, SphericalRightHip)

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the objects."""
        return {
            **super().descriptions,
            self.symbols["T_flexion"]: "Flexion torque of the hip.",
            self.symbols["T_adduction"]: "Adduction torque of the hip.",
            self.symbols["T_rotation"]: "Endorotation torque of the hip.",
        }

    def _define_objects(self) -> None:
        """Define the objects."""
        self.symbols.update({name: dynamicsymbols(self._add_prefix(name)) for name in (
            "T_flexion", "T_adduction", "T_rotation")})

    def _define_loads(self) -> None:
        """Define the loads."""
        hip = self.parent.system.joints[0]
        adduction_axis = (cos(hip.coordinates[0]) * hip.parent_interframe.x -
                          sin(hip.coordinates[0]) * hip.parent_interframe.z)
        if isinstance(self.parent, RightHipBase):
            rot_dir = -1
        else:
            adduction_axis *= -1
            rot_dir = 1
        torque = (self.symbols["T_flexion"] * hip.parent_interframe.y +
                  self.symbols["T_adduction"] * adduction_axis +
                  self.symbols["T_rotation"] * rot_dir * hip.child_interframe.z)
        self.parent.system.add_loads(
            Torque(hip.child_interframe, torque),
            Torque(hip.parent_interframe, -torque)
        )


class SphericalHipSpringDamper(LoadGroupBase):
    """Spring damper for the spherical hip joints."""

    parent: SphericalLeftHip | SphericalRightHip
    required_parent_type = (SphericalLeftHip, SphericalRightHip)

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the objects."""
        desc = {**super().descriptions}
        for tp in ("flexion", "adduction", "rotation"):
            desc.update({
                self.symbols[f"k_{tp}"]:
                    f"{tp.capitalize()} stiffness of hip: {self.parent}.",
                self.symbols[f"c_{tp}"]:
                    f"{tp.capitalize()} damping of hip: {self.parent}.",
                self.symbols[f"q_ref_{tp}"]:
                    f"{tp.capitalize()} reference angle of hip: {self.parent}.",
            })
        return desc

    def _define_objects(self) -> None:
        """Define the objects."""
        for tp in ("flexion", "adduction", "rotation"):
            self.symbols.update({name: dynamicsymbols(self._add_prefix(name))
                                 for name in (f"k_{tp}", f"c_{tp}", f"q_ref_{tp}")})

    def _define_loads(self) -> None:
        """Define the loads."""
        hip = self.parent.system.joints[0]
        adduction_axis = (cos(hip.coordinates[0]) * hip.parent_interframe.x -
                          sin(hip.coordinates[0]) * hip.parent_interframe.z)
        if isinstance(self.parent, RightHipBase):
            rot_dir = -1
        else:
            adduction_axis *= -1
            rot_dir = 1
        torques = []
        for i, tp in enumerate(("flexion", "adduction", "rotation")):
            torques.append(-self.symbols[f"k_{tp}"] * (
                    hip.coordinates[i] - self.symbols[f"q_ref_{tp}"]) -
                           self.symbols[f"c_{tp}"] * hip.speeds[i])
        torque = (torques[0] * hip.parent_interframe.y +
                  torques[1] * adduction_axis +
                  torques[2] * rot_dir * hip.child_interframe.z)
        self.parent.system.add_loads(
            Torque(hip.child_interframe, torque),
            Torque(hip.parent_interframe, -torque)
        )
