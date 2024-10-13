# mypy: disable-error-code="valid-type"
from typing import Dict, Literal, Optional, Tuple, get_args

import torch
import warp as wp
from jaxtyping import Float


@wp.kernel
def axis_angle_to_matrix_via_quat_kernel(
    axis: wp.array(dtype=wp.vec3),
    angle: wp.array(dtype=wp.float32),
    rot_mat: wp.array(dtype=wp.mat33),
):
    tid = wp.tid()
    rot_mat[tid] = wp.quat_to_matrix(wp.quat_from_axis_angle(axis[tid], angle[tid]))


@wp.kernel
def axis_angle_to_matrix_kernel(
    axis: wp.array(dtype=wp.vec3),
    angle: wp.array(dtype=wp.float32),
    rot_mat: wp.array(dtype=wp.mat33),
):
    tid = wp.tid()

    axis_elem = axis[tid]
    x, y, z = axis_elem[0], axis_elem[1], axis_elem[2]
    s, c = wp.sin(angle[tid]), wp.cos(angle[tid])
    C = 1.0 - c

    xs, ys, zs = x * s, y * s, z * s
    xC, yC, zC = x * C, y * C, z * C
    xyC, yzC, zxC = x * yC, y * zC, z * xC

    rot_mat[tid] = wp.mat33(
        x * xC + c, xyC - zs, zxC + ys, xyC + zs, y * yC + c, yzC - xs, zxC - ys, yzC + xs, z * zC + c
    )


class AxisAngleToMatrix(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx, axis: Float[torch.Tensor, "... 3"], angle: Float[torch.Tensor, "..."]
    ) -> Float[torch.Tensor, "... 3 3"]:
        axis_wp = wp.from_torch(axis.view(-1, 3), dtype=wp.vec3)
        angles_wp = wp.from_torch(angle.view(-1), dtype=wp.float32)
        rot_mat_wp = wp.empty(
            axis_wp.shape,
            dtype=wp.mat33,  # type: ignore
            device=axis_wp.device,
            requires_grad=axis_wp.requires_grad,
        )
        wp.launch(
            kernel=axis_angle_to_matrix_kernel,
            dim=(axis_wp.shape[0],),
            inputs=[axis_wp, angles_wp],
            outputs=[rot_mat_wp],
            device=axis_wp.device,
        )
        if axis.requires_grad or angle.requires_grad:
            ctx.axis_wp = axis_wp
            ctx.angles_wp = angles_wp
            ctx.rot_mat_wp = rot_mat_wp
        return wp.to_torch(rot_mat_wp).view(angle.shape + (3, 3))

    @staticmethod
    def backward(  # type: ignore
        ctx, rot_mat_grad: Float[torch.Tensor, "... 3 3"]
    ) -> Tuple[Optional[Float[torch.Tensor, "... 3"]], Optional[Float[torch.Tensor, "..."]]]:
        ctx.rot_mat_wp.grad = wp.from_torch(rot_mat_grad.contiguous().view(-1, 3, 3), dtype=wp.mat33)
        wp.launch(
            kernel=axis_angle_to_matrix_kernel,
            dim=(ctx.axis_wp.shape[0],),
            inputs=[ctx.axis_wp, ctx.angles_wp],
            outputs=[ctx.rot_mat_wp],
            adj_inputs=[ctx.axis_wp.grad, ctx.angles_wp.grad],
            adj_outputs=[ctx.rot_mat_wp.grad],
            adjoint=True,
            device=ctx.axis_wp.device,
        )
        axis_grad = wp.to_torch(ctx.axis_wp.grad).view(rot_mat_grad.shape[:-1]) if ctx.axis_wp.requires_grad else None
        angle_grad = (
            wp.to_torch(ctx.angles_wp.grad).view(rot_mat_grad.shape[:-2]) if ctx.angles_wp.requires_grad else None
        )
        return axis_grad, angle_grad


def axis_angle_to_matrix(
    axis: Float[torch.Tensor, "... 3"], angle: Float[torch.Tensor, "..."]
) -> Float[torch.Tensor, "... 3 3"]:
    """
    Converts axis angles to rotation matrices using Rodrigues formula.

    Args:
        axis (torch.Tensor): axis, the shape could be [..., 3].
        angle (torch.Tensor): angle, the shape could be [...].

    Returns:
        torch.Tensor: Rotation matrices [..., 3, 3].

    Example:
        >>> axis = torch.tensor([1.0, 0.0, 0.0])
        >>> angle = torch.tensor(0.5)
        >>> axis_angle_to_matrix(axis, angle)
        tensor([[ 1.0000,  0.0000,  0.0000],
                [ 0.0000,  0.8776, -0.4794],
                [ 0.0000,  0.4794,  0.8776]])
    """
    return AxisAngleToMatrix.apply(axis, angle)  # type: ignore


# fmt: off
_AXES = Literal[
    "sxyz", "sxyx", "sxzy", "sxzx", "syzx", "syzy", "syxz", "syxy", "szxy", "szxz", "szyx", "szyz",
    "rzyx", "rxyx", "ryzx", "rxzx", "rxzy", "ryzy", "rzxy", "ryxy", "ryxz", "rzxz", "rxyz", "rzyz"
]
# fmt: on
_AXES_SPEC: Dict[_AXES, wp.vec4i] = {
    axes: wp.vec4i("sr".index(axes[0]), "xyz".index(axes[1]), "xyz".index(axes[2]), "xyz".index(axes[3]))
    for axes in get_args(_AXES)
}


@wp.func
def _euler_angle_to_matrix(angle: wp.float32, axis: wp.int32) -> wp.mat33:
    c, s = wp.cos(angle), wp.sin(angle)
    if axis == 0:
        return wp.mat33(1.0, 0.0, 0.0, 0.0, c, -s, 0.0, s, c)
    elif axis == 1:
        return wp.mat33(c, 0.0, s, 0.0, 1.0, 0.0, -s, 0.0, c)
    else:
        return wp.mat33(c, -s, 0.0, s, c, 0.0, 0.0, 0.0, 1.0)


@wp.kernel
def euler_angles_to_matrix_kernel(
    euler_angles: wp.array(dtype=wp.vec3), axes: wp.vec4i, rot_mat: wp.array(dtype=wp.mat33)
):
    tid = wp.tid()
    euler_angles_elem = euler_angles[tid]

    if axes[0] == 0:  # static/extrinsic rotation
        rot_mat[tid] = wp.mul(
            wp.mul(
                _euler_angle_to_matrix(euler_angles_elem[2], axes[3]),
                _euler_angle_to_matrix(euler_angles_elem[1], axes[2]),
            ),
            _euler_angle_to_matrix(euler_angles_elem[0], axes[1]),
        )
    else:  # rotating/intrinsic rotation
        rot_mat[tid] = wp.mul(
            wp.mul(
                _euler_angle_to_matrix(euler_angles_elem[0], axes[1]),
                _euler_angle_to_matrix(euler_angles_elem[1], axes[2]),
            ),
            _euler_angle_to_matrix(euler_angles_elem[2], axes[3]),
        )


class EulerAnglesToMatrix(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx, euler_angles: Float[torch.Tensor, "... 3"], axes: _AXES = "sxyz"
    ) -> Float[torch.Tensor, "... 3 3"]:
        axes = axes.lower()  # type: ignore
        if len(axes) == 3:
            axes = f"s{axes}"  # type: ignore
        if axes not in _AXES_SPEC:
            raise ValueError(f"Invalid axes: {axes}")

        euler_angles_wp = wp.from_torch(euler_angles.view(-1, 3).contiguous(), dtype=wp.vec3)
        rot_mat_wp = wp.from_torch(
            torch.empty(
                euler_angles.shape + (3,),
                dtype=euler_angles.dtype,
                device=euler_angles.device,
                requires_grad=euler_angles.requires_grad,
            ).view(-1, 3, 3),
            dtype=wp.mat33,
        )
        axes_spec = _AXES_SPEC[axes]

        wp.launch(
            kernel=euler_angles_to_matrix_kernel,
            dim=(euler_angles_wp.shape[0],),
            inputs=[euler_angles_wp, axes_spec],
            outputs=[rot_mat_wp],
            device=euler_angles_wp.device,
        )
        if euler_angles.requires_grad:
            ctx.euler_angles_wp = euler_angles_wp
            ctx.rot_mat_wp = rot_mat_wp
            ctx.axes_spec = axes_spec
        return wp.to_torch(rot_mat_wp).view(euler_angles.shape + (3,))

    @staticmethod
    def backward(  # type: ignore
        ctx, rot_mat_grad: Float[torch.Tensor, "... 3 3"]
    ) -> Tuple[Optional[Float[torch.Tensor, "... 3"]], None]:
        ctx.rot_mat_wp.grad = wp.from_torch(rot_mat_grad.contiguous().view(-1, 3, 3), dtype=wp.mat33)
        wp.launch(
            kernel=euler_angles_to_matrix_kernel,
            dim=(ctx.euler_angles_wp.shape[0],),
            inputs=[ctx.euler_angles_wp, ctx.axes_spec],
            outputs=[ctx.rot_mat_wp],
            adj_inputs=[ctx.euler_angles_wp.grad, ctx.axes_spec],
            adj_outputs=[ctx.rot_mat_wp.grad],
            adjoint=True,
            device=ctx.euler_angles_wp.device,
        )
        return wp.to_torch(ctx.euler_angles_wp.grad).view(rot_mat_grad.shape[:-1]), None


def euler_angles_to_matrix(
    euler_angles: Float[torch.Tensor, "... 3"], axes: _AXES = "sxyz"
) -> Float[torch.Tensor, "... 3 3"]:
    """Converts Euler angles to rotation matrices.

    Args:
        euler_angles (torch.Tensor): Euler angles, the shape could be [..., 3].
        axes (str): Axis specification; one of 24 axis sequences as string or encoded tuple - e.g. `sxyz (the default). It's recommended to use the full name of the axes, e.g. "sxyz" instead of "xyz", but if 3 characters are provided, it will be prefixed with "s".

    Returns:
        torch.Tensor: Rotation matrices [..., 3, 3].

    Example:
        >>> euler_angles = torch.tensor([1.0, 0.5, 2.0])
        >>> euler_angles_to_matrix(euler_angles, axes="sxyz")
        tensor([[-0.3652, -0.6592,  0.6574],
                [ 0.7980,  0.1420,  0.5857],
                [-0.4794,  0.7385,  0.4742]])
        >>> euler_angles_to_matrix(euler_angles, axes="rxyz")
        tensor([[-0.3652, -0.7980,  0.4794],
                [ 0.3234, -0.5917, -0.7385],
                [ 0.8729, -0.1146,  0.4742]])
    """
    return EulerAnglesToMatrix.apply(euler_angles, axes)  # type: ignore


__all__ = ["axis_angle_to_matrix"]
