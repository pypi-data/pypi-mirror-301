"""Module containing the shoulder joints."""
from __future__ import annotations

from sympy import Matrix, cos, sin
from sympy.physics.mechanics import (
    PinJoint,
    Point,
    ReferenceFrame,
    SphericalJoint,
    System,
    Torque,
    dynamicsymbols,
)

from symbrim.core import Attachment, LoadGroupBase
from symbrim.rider.base_connections import LeftShoulderBase, RightShoulderBase

__all__ = ["SphericalLeftShoulder", "SphericalRightShoulder",
           "FlexAddLeftShoulder", "FlexAddRightShoulder",
           "FlexRotLeftShoulder", "FlexRotRightShoulder",
           "SphericalShoulderTorque", "SphericalShoulderSpringDamper"]


class SphericalShoulderMixin:
    """Spherical joint between the pelvis and the leg."""

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the objects."""
        return {
            **super().descriptions,
            self.q[0]: "Flexion angle of the shoulder.",
            self.q[1]: "Adduction angle of the shoulder.",
            self.q[2]: "Endorotation angle of the shoulder.",
            self.u[0]: "Flexion angular velocity of the shoulder.",
            self.u[1]: "Adduction angular velocity of the shoulder.",
            self.u[2]: "Rotation angular velocity of the shoulder.",
        }

    def _define_objects(self) -> None:
        """Define the objects."""
        super()._define_objects()
        self.q = Matrix(
            dynamicsymbols(self._add_prefix("q_flexion, q_adduction, q_rotation")))
        self.u = Matrix(
            dynamicsymbols(self._add_prefix("u_flexion, u_adduction, u_rotation")))
        self._system = System.from_newtonian(self.torso.body)


class SphericalLeftShoulder(SphericalShoulderMixin, LeftShoulderBase):
    """Spherical joint between the pelvis and the left leg."""

    def _define_kinematics(self) -> None:
        """Define the kinematics."""
        super()._define_kinematics()
        self.system.add_joints(
            SphericalJoint(
                self._add_prefix("joint"), self.torso.body, self.arm.shoulder, self.q,
                self.u, self.torso.left_shoulder_point, self.arm.shoulder_interpoint,
                self.torso.left_shoulder_frame, self.arm.shoulder_interframe,
                rot_type="BODY", amounts=(self.q[0], -self.q[1], self.q[2]),
                rot_order="YXZ")
        )


class SphericalRightShoulder(SphericalShoulderMixin, RightShoulderBase):
    """Spherical joint between the pelvis and the right leg."""

    def _define_kinematics(self) -> None:
        """Define the kinematics."""
        super()._define_kinematics()
        self.system.add_joints(
            SphericalJoint(
                self._add_prefix("joint"), self.torso.body, self.arm.shoulder, self.q,
                self.u, self.torso.right_shoulder_point, self.arm.shoulder_interpoint,
                self.torso.right_shoulder_frame, self.arm.shoulder_interframe,
                rot_type="BODY", amounts=(self.q[0], self.q[1], -self.q[2]),
                rot_order="YXZ")
        )


class FlexRotShoulderMixin:
    """Shoulder joint mixin with flexion and rotation."""

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the objects."""
        return {
            **super().descriptions,
            self.q[0]: "Flexion angle of the shoulder.",
            self.q[1]: "Endorotation angle of the shoulder.",
            self.u[0]: "Flexion angular velocity of the shoulder.",
            self.u[1]: "Rotation angular velocity of the shoulder.",
        }

    def _define_objects(self) -> None:
        """Define the objects."""
        super()._define_objects()
        self.q = Matrix(dynamicsymbols(self._add_prefix("q_flexion, q_rotation")))
        self.u = Matrix(dynamicsymbols(self._add_prefix("u_flexion, u_rotation")))
        self._system = System.from_newtonian(self.torso.body)
        self._intermediate = Attachment(ReferenceFrame(self._add_prefix("int_frame")),
                                        Point(self._add_prefix("int_point")))


class FlexRotLeftShoulder(FlexRotShoulderMixin, LeftShoulderBase):
    """Left shoulder joint with flexion and rotation."""

    def _define_kinematics(self) -> None:
        """Define the kinematics."""
        super()._define_kinematics()
        self.system.add_joints(
            PinJoint(
                self._add_prefix("flexion_joint"), self.torso.body,
                self._intermediate.to_valid_joint_arg(), self.q[0],
                self.u[0], self.torso.left_shoulder_point, self._intermediate.point,
                self.torso.left_shoulder_frame, self._intermediate.frame,
                joint_axis=self.torso.y),
            PinJoint(
                self._add_prefix("rotation_joint"),
                self._intermediate.to_valid_joint_arg(), self.arm.shoulder, self.q[1],
                self.u[1], self._intermediate.point, self.arm.shoulder_interpoint,
                self._intermediate.frame, self.arm.shoulder_interframe,
                joint_axis=self._intermediate.frame.z)
        )


class FlexRotRightShoulder(FlexRotShoulderMixin, RightShoulderBase):
    """Right shoulder joint with flexion and rotation."""

    def _define_kinematics(self) -> None:
        """Define the kinematics."""
        super()._define_kinematics()
        self.system.add_joints(
            PinJoint(
                self._add_prefix("flexion_joint"), self.torso.body,
                self._intermediate.to_valid_joint_arg(), self.q[0],
                self.u[0], self.torso.right_shoulder_point, self._intermediate.point,
                self.torso.right_shoulder_frame, self._intermediate.frame,
                joint_axis=self.torso.y),
            PinJoint(
                self._add_prefix("rotation_joint"),
                self._intermediate.to_valid_joint_arg(), self.arm.shoulder, self.q[1],
                self.u[1], self._intermediate.point, self.arm.shoulder_interpoint,
                self._intermediate.frame, self.arm.shoulder_interframe,
                joint_axis=-self._intermediate.frame.z)
        )


class FlexAddShoulderMixin:
    """Shoulder joint mixin with flexion and adduction."""

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the objects."""
        return {
            **super().descriptions,
            self.q[0]: "Flexion angle of the shoulder.",
            self.q[1]: "Adduction angle of the shoulder.",
            self.u[0]: "Flexion angular velocity of the shoulder.",
            self.u[1]: "Adduction angular velocity of the shoulder.",
        }

    def _define_objects(self) -> None:
        """Define the objects."""
        super()._define_objects()
        self.q = Matrix(dynamicsymbols(self._add_prefix("q_flexion, q_adduction")))
        self.u = Matrix(dynamicsymbols(self._add_prefix("u_flexion, u_adduction")))
        self._system = System.from_newtonian(self.torso.body)
        self._intermediate = Attachment(ReferenceFrame(self._add_prefix("int_frame")),
                                        Point(self._add_prefix("int_point")))


class FlexAddLeftShoulder(FlexAddShoulderMixin, LeftShoulderBase):
    """Left shoulder joint with flexion and adduction."""

    def _define_kinematics(self) -> None:
        """Define the kinematics."""
        super()._define_kinematics()
        self.system.add_joints(
            PinJoint(
                self._add_prefix("flexion_joint"), self.torso.body,
                self._intermediate.to_valid_joint_arg(), self.q[0],
                self.u[0], self.torso.left_shoulder_point, self._intermediate.point,
                self.torso.left_shoulder_frame, self._intermediate.frame,
                joint_axis=self.torso.y),
            PinJoint(
                self._add_prefix("adduction_joint"),
                self._intermediate.to_valid_joint_arg(), self.arm.shoulder, self.q[1],
                self.u[1], self._intermediate.point, self.arm.shoulder_interpoint,
                self._intermediate.frame, self.arm.shoulder_interframe,
                joint_axis=-self._intermediate.frame.x)
        )


class FlexAddRightShoulder(FlexAddShoulderMixin, RightShoulderBase):
    """Right shoulder joint with flexion and adduction."""

    def _define_kinematics(self) -> None:
        """Define the kinematics."""
        super()._define_kinematics()
        self.system.add_joints(
            PinJoint(
                self._add_prefix("flexion_joint"), self.torso.body,
                self._intermediate.to_valid_joint_arg(), self.q[0],
                self.u[0], self.torso.right_shoulder_point, self._intermediate.point,
                self.torso.right_shoulder_frame, self._intermediate.frame,
                joint_axis=self.torso.y),
            PinJoint(
                self._add_prefix("adduction_joint"),
                self._intermediate.to_valid_joint_arg(), self.arm.shoulder, self.q[1],
                self.u[1], self._intermediate.point, self.arm.shoulder_interpoint,
                self._intermediate.frame, self.arm.shoulder_interframe,
                joint_axis=self._intermediate.frame.x)
        )


class SphericalShoulderTorque(LoadGroupBase):
    """Torque for the spherical shoulder joints."""

    parent: SphericalLeftShoulder | SphericalRightShoulder
    required_parent_type = (SphericalLeftShoulder, SphericalRightShoulder)

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the objects."""
        return {
            **super().descriptions,
            self.symbols["T_flexion"]: f"Flexion torque of shoulder: {self.parent}.",
            self.symbols["T_adduction"]:
                f"Adduction torque of shoulder: {self.parent}.",
            self.symbols["T_rotation"]:
                f"Endorotation torque of shoulder: {self.parent}.",
        }

    def _define_objects(self) -> None:
        """Define the objects."""
        self.symbols.update({name: dynamicsymbols(self._add_prefix(name)) for name in (
            "T_flexion", "T_adduction", "T_rotation")})

    def _define_loads(self) -> None:
        """Define the loads."""
        shoulder = self.parent.system.joints[0]
        adduction_axis = (cos(shoulder.coordinates[0]) * shoulder.parent_interframe.x -
                          sin(shoulder.coordinates[0]) * shoulder.parent_interframe.z)
        if isinstance(self.parent, RightShoulderBase):
            rot_dir = -1
        else:
            adduction_axis *= -1
            rot_dir = 1
        torque = (self.symbols["T_flexion"] * shoulder.parent_interframe.y +
                  self.symbols["T_adduction"] * adduction_axis +
                  self.symbols["T_rotation"] * rot_dir * shoulder.child_interframe.z)
        self.parent.system.add_loads(
            Torque(shoulder.child_interframe, torque),
            Torque(shoulder.parent_interframe, -torque)
        )


class SphericalShoulderSpringDamper(LoadGroupBase):
    """Spherical for the spherical shoulder joints."""

    parent: SphericalLeftShoulder | SphericalRightShoulder
    required_parent_type = (SphericalLeftShoulder, SphericalRightShoulder)

    @property
    def descriptions(self) -> dict[object, str]:
        """Descriptions of the objects."""
        desc = {**super().descriptions}
        for tp in ("flexion", "adduction", "rotation"):
            desc.update({
                self.symbols[f"k_{tp}"]:
                    f"{tp.capitalize()} stiffness of shoulder: {self.parent}.",
                self.symbols[f"c_{tp}"]:
                    f"{tp.capitalize()} damping of:shoulder {self.parent}.",
                self.symbols[f"q_ref_{tp}"]:
                    f"{tp.capitalize()} reference angle of shoulder: {self.parent}.",
            })
        return desc

    def _define_objects(self) -> None:
        """Define the objects."""
        for tp in ("flexion", "adduction", "rotation"):
            self.symbols.update({name: dynamicsymbols(self._add_prefix(name))
                                 for name in (f"k_{tp}", f"c_{tp}", f"q_ref_{tp}")})

    def _define_loads(self) -> None:
        """Define the loads."""
        shoulder = self.parent.system.joints[0]
        adduction_axis = (cos(shoulder.coordinates[0]) * shoulder.parent_interframe.x -
                          sin(shoulder.coordinates[0]) * shoulder.parent_interframe.z)
        if isinstance(self.parent, RightShoulderBase):
            rot_dir = -1
        else:
            adduction_axis *= -1
            rot_dir = 1
        torques = []
        for i, tp in enumerate(("flexion", "adduction", "rotation")):
            torques.append(-self.symbols[f"k_{tp}"] * (
                    shoulder.coordinates[i] - self.symbols[f"q_ref_{tp}"]) -
                           self.symbols[f"c_{tp}"] * shoulder.speeds[i])
        torque = (torques[0] * shoulder.parent_interframe.y +
                  torques[1] * adduction_axis +
                  torques[2] * rot_dir * shoulder.child_interframe.z)
        self.parent.system.add_loads(
            Torque(shoulder.child_interframe, torque),
            Torque(shoulder.parent_interframe, -torque)
        )
