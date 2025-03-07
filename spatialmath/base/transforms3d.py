# Part of Spatial Math Toolbox for Python
# Copyright (c) 2000 Peter Corke
# MIT Licence, see details in top-level file: LICENCE

"""
These functions create and manipulate 3D rotation matrices and rigid-body
transformations as 3x3 SO(3) matrices and 4x4 SE(3) matrices respectively.
These matrices are represented as 2D NumPy arrays.

Vector arguments are what numpy refers to as ``array_like`` and can be a list,
tuple, numpy array, numpy row vector or numpy column vector.

"""

# pylint: disable=invalid-name

import sys
import math
import numpy as np
import scipy as sp
from collections.abc import Iterable

from spatialmath import base as smb
from spatialmath.base import symbolic as sym

_eps = np.finfo(np.float64).eps

# ---------------------------------------------------------------------------------------#


def rotx(theta, unit="rad"):
    """
    Create SO(3) rotation about X-axis

    :param theta: rotation angle about X-axis
    :type theta: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :return: SO(3) rotation matrix
    :rtype: ndarray(3,3)

    - ``rotx(θ)`` is an SO(3) rotation matrix (3x3) representing a rotation
      of θ radians about the x-axis
    - ``rotx(θ, "deg")`` as above but θ is in degrees

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> rotx(0.3)
        >>> rotx(45, 'deg')

    :seealso: :func:`~trotx`
    :SymPy: supported
    """

    theta = smb.getunit(theta, unit)
    ct = smb.sym.cos(theta)
    st = smb.sym.sin(theta)
    # fmt: off
    R = np.array([
        [1, 0, 0],
        [0, ct, -st],
        [0, st, ct]])
    # fmt: on
    return R


# ---------------------------------------------------------------------------------------#
def roty(theta, unit="rad"):
    """
    Create SO(3) rotation about Y-axis

    :param theta: rotation angle about Y-axis
    :type theta: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :return: SO(3) rotation matrix
    :rtype: ndarray(3,3)

    - ``roty(θ)`` is an SO(3) rotation matrix (3x3) representing a rotation
      of θ radians about the y-axis
    - ``roty(θ, "deg")`` as above but θ is in degrees

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> roty(0.3)
        >>> roty(45, 'deg')

    :seealso: :func:`~troty`
    :SymPy: supported
    """

    theta = smb.getunit(theta, unit)
    ct = smb.sym.cos(theta)
    st = smb.sym.sin(theta)
    # fmt: off
    return np.array([
        [ct, 0, st],
        [0, 1, 0],
        [-st, 0, ct]])
    # fmt: on


# ---------------------------------------------------------------------------------------#
def rotz(theta, unit="rad"):
    """
    Create SO(3) rotation about Z-axis

    :param theta: rotation angle about Z-axis
    :type theta: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :return: SO(3) rotation matrix
    :rtype: ndarray(3,3)

    - ``rotz(θ)`` is an SO(3) rotation matrix (3x3) representing a rotation
      of θ radians about the z-axis
    - ``rotz(θ, "deg")`` as above but θ is in degrees

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> rotz(0.3)
        >>> rotz(45, 'deg')

    :seealso: :func:`~yrotz`
    :SymPy: supported
    """
    theta = smb.getunit(theta, unit)
    ct = smb.sym.cos(theta)
    st = smb.sym.sin(theta)
    # fmt: off
    return np.array([
        [ct, -st, 0],
        [st, ct, 0],
        [0, 0, 1]])
    # fmt: on


# ---------------------------------------------------------------------------------------#
def trotx(theta, unit="rad", t=None):
    """
    Create SE(3) pure rotation about X-axis

    :param theta: rotation angle about X-axis
    :type theta: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :param t: 3D translation vector, defaults to [0,0,0]
    :type t: array_like(3)
    :return: SE(3) transformation matrix
    :rtype: ndarray(4,4)

    - ``trotx(θ)`` is a homogeneous transformation (4x4) representing a rotation
      of θ radians about the x-axis.
    - ``trotx(θ, 'deg')`` as above but θ is in degrees
    - ``trotx(θ, 'rad', t=[x,y,z])`` as above with translation of [x,y,z]

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> trotx(0.3)
        >>> trotx(45, 'deg', t=[1,2,3])

    :seealso: :func:`~rotx`
    :SymPy: supported
    """
    T = smb.r2t(rotx(theta, unit))
    if t is not None:
        T[:3, 3] = smb.getvector(t, 3, "array")
    return T


# ---------------------------------------------------------------------------------------#
def troty(theta, unit="rad", t=None):
    """
    Create SE(3) pure rotation about Y-axis

    :param theta: rotation angle about Y-axis
    :type theta: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :param t: 3D translation vector, defaults to [0,0,0]
    :type t: array_like(3)
    :return: SE(3) transformation matrix
    :rtype: ndarray(4,4)

    - ``troty(θ)`` is a homogeneous transformation (4x4) representing a rotation
      of θ radians about the y-axis.
    - ``troty(θ, 'deg')`` as above but θ is in degrees
    - ``troty(θ, 'rad', t=[x,y,z])`` as above with translation of [x,y,z]

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> troty(0.3)
        >>> troty(45, 'deg', t=[1,2,3])

    :seealso: :func:`~roty`
    :SymPy: supported
    """
    T = smb.r2t(roty(theta, unit))
    if t is not None:
        T[:3, 3] = smb.getvector(t, 3, "array")
    return T


# ---------------------------------------------------------------------------------------#
def trotz(theta, unit="rad", t=None):
    """
    Create SE(3) pure rotation about Z-axis

    :param theta: rotation angle about Z-axis
    :type theta: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :param t: 3D translation vector, defaults to [0,0,0]
    :type t: array_like(3)
    :return: SE(3) transformation matrix
    :rtype: ndarray(4,4)

    - ``trotz(θ)`` is a homogeneous transformation (4x4) representing a rotation
      of θ radians about the z-axis.
    - ``trotz(θ, 'deg')`` as above but θ is in degrees
    - ``trotz(θ, 'rad', t=[x,y,z])`` as above with translation of [x,y,z]

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> trotz(0.3)
        >>> trotz(45, 'deg', t=[1,2,3])

    :seealso: :func:`~rotz`
    :SymPy: supported
    """
    T = smb.r2t(rotz(theta, unit))
    if t is not None:
        T[:3, 3] = smb.getvector(t, 3, "array")
    return T


# ---------------------------------------------------------------------------------------#


def transl(x, y=None, z=None):
    """
    Create SE(3) pure translation, or extract translation from SE(3) matrix


    **Create a translational SE(3) matrix**

    :param x: translation along X-axis
    :type x: float
    :param y: translation along Y-axis
    :type y: float
    :param z: translation along Z-axis
    :type z: float
    :return: SE(3) transformation matrix
    :rtype: numpy(4,4)
    :raises ValueError: bad argument

    - ``T = transl( X, Y, Z )`` is an SE(3) homogeneous transform (4x4)
      representing a pure translation of X, Y and Z.
    - ``T = transl( V )`` as above but the translation is given by a 3-element
      list, dict, or a numpy array, row or column vector.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> import numpy as np
        >>> transl(3, 4, 5)
        >>> transl([3, 4, 5])
        >>> transl(np.array([3, 4, 5]))

    **Extract the translational part of an SE(3) matrix**

    :param x: SE(3) transformation matrix
    :type x: numpy(4,4)
    :return: translation elements of SE(2) matrix
    :rtype: ndarray(3)
    :raises ValueError: bad argument

    - ``t = transl(T)`` is the translational part of a homogeneous transform T as a
      3-element numpy array.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> import numpy as np
        >>> T = np.array([[1, 0, 0, 3], [0, 1, 0, 4], [0, 0, 1, 5], [0, 0, 0, 1]])
        >>> transl(T)

    .. note:: This function is compatible with the MATLAB version of the
        Toolbox.  It is unusual/weird in doing two completely different things
        inside the one function.
    :seealso: :func:`~spatialmath.smb.transforms2d.transl2`
    :SymPy: supported
    """

    if smb.isscalar(x) and y is not None and z is not None:
        t = np.r_[x, y, z]
    elif smb.isvector(x, 3):
        t = smb.getvector(x, 3, out="array")
    elif smb.ismatrix(x, (4, 4)):
        # SE(3) -> R3
        return x[:3, 3]
    else:
        raise ValueError("bad argument")

    if t.dtype != "O":
        t = t.astype("float64")

    T = np.identity(4, dtype=t.dtype)
    T[:3, 3] = t
    return T


def ishom(T, check=False, tol=100):
    """
    Test if matrix belongs to SE(3)

    :param T: SE(3) matrix to test
    :type T: numpy(4,4)
    :param check: check validity of rotation submatrix
    :type check: bool
    :return: whether matrix is an SE(3) homogeneous transformation matrix
    :rtype: bool

    - ``ishom(T)`` is True if the argument ``T`` is of dimension 4x4
    - ``ishom(T, check=True)`` as above, but also checks orthogonality of the
      rotation sub-matrix and validitity of the bottom row.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> import numpy as np
        >>> T = np.array([[1, 0, 0, 3], [0, 1, 0, 4], [0, 0, 1, 5], [0, 0, 0, 1]])
        >>> ishom(T)
        >>> T = np.array([[1, 1, 0, 3], [0, 1, 0, 4], [0, 0, 1, 5], [0, 0, 0, 1]]) # invalid SE(3)
        >>> ishom(T)  # a quick check says it is an SE(3)
        >>> ishom(T, check=True) # but if we check more carefully...
        >>> R = np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
        >>> ishom(R)

    :seealso: :func:`~spatialmath.smb.transformsNd.isR` :func:`~isrot` :func:`~spatialmath.smb.transforms2d.ishom2`
    """
    return (
        isinstance(T, np.ndarray)
        and T.shape == (4, 4)
        and (
            not check
            or (
                smb.isR(T[:3, :3], tol=tol)
                and np.all(T[3, :] == np.array([0, 0, 0, 1]))
            )
        )
    )


def isrot(R, check=False, tol=100):
    """
    Test if matrix belongs to SO(3)

    :param R: SO(3) matrix to test
    :type R: numpy(3,3)
    :param check: check validity of rotation submatrix
    :type check: bool
    :return: whether matrix is an SO(3) rotation matrix
    :rtype: bool

    - ``isrot(R)`` is True if the argument ``R`` is of dimension 3x3
    - ``isrot(R, check=True)`` as above, but also checks orthogonality of the
      rotation matrix.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> import numpy as np
        >>> T = np.array([[1, 0, 0, 3], [0, 1, 0, 4], [0, 0, 1, 5], [0, 0, 0, 1]])
        >>> isrot(T)
        >>> R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        >>> isrot(R)
        >>> R = R = np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]]) # invalid SO(3)
        >>> isrot(R)  # a quick check says it is an SO(3)
        >>> isrot(R, check=True) # but if we check more carefully...

    :seealso: :func:`~spatialmath.smb.transformsNd.isR` :func:`~spatialmath.smb.transforms2d.isrot2`,  :func:`~ishom`
    """
    return (
        isinstance(R, np.ndarray)
        and R.shape == (3, 3)
        and (not check or smb.isR(R, tol=tol))
    )


# ---------------------------------------------------------------------------------------#
def rpy2r(roll, pitch=None, yaw=None, *, unit="rad", order="zyx"):
    """
    Create an SO(3) rotation matrix from roll-pitch-yaw angles

    :param roll: roll angle
    :type roll: float
    :param pitch: pitch angle
    :type pitch: float
    :param yaw: yaw angle
    :type yaw: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :param order: rotation order: 'zyx' [default], 'xyz', or 'yxz'
    :type order: str
    :return: SO(3) rotation matrix
    :rtype: ndarray(3,3)
    :raises ValueError: bad argument

    - ``rpy2r(⍺, β, γ)`` is an SO(3) orthonormal rotation matrix (3x3)
      equivalent to the specified roll (⍺), pitch (β), yaw (γ) angles angles.
      These correspond to successive rotations about the axes specified by
      ``order``:

        - 'zyx' [default], rotate by γ about the z-axis, then by β about the new
          y-axis, then by ⍺ about the new x-axis.  Convention for a mobile robot
          with x-axis forward and y-axis sideways.
        - 'xyz', rotate by γ about the x-axis, then by β about the new y-axis,
          then by ⍺ about the new z-axis. Convention for a robot gripper with
          z-axis forward and y-axis between the gripper fingers.
        - 'yxz', rotate by γ about the y-axis, then by β about the new x-axis,
          then by ⍺ about the new z-axis. Convention for a camera with z-axis
          parallel to the optic axis and x-axis parallel to the pixel rows.

    - ``rpy2r(RPY)`` as above but the roll, pitch, yaw angles are taken
      from ``RPY`` which is a 3-vector with values (⍺, β, γ).

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> rpy2r(0.1, 0.2, 0.3)
        >>> rpy2r([0.1, 0.2, 0.3])
        >>> rpy2r([10, 20, 30], unit='deg')

    :seealso: :func:`~eul2r` :func:`~rpy2tr` :func:`~tr2rpy`
    """

    if smb.isscalar(roll):
        angles = [roll, pitch, yaw]
    else:
        angles = smb.getvector(roll, 3)

    angles = smb.getunit(angles, unit)

    if order in ("xyz", "arm"):
        R = rotx(angles[2]) @ roty(angles[1]) @ rotz(angles[0])
    elif order in ("zyx", "vehicle"):
        R = rotz(angles[2]) @ roty(angles[1]) @ rotx(angles[0])
    elif order in ("yxz", "camera"):
        R = roty(angles[2]) @ rotx(angles[1]) @ rotz(angles[0])
    else:
        raise ValueError("Invalid angle order")

    return R


# ---------------------------------------------------------------------------------------#
def rpy2tr(roll, pitch=None, yaw=None, unit="rad", order="zyx"):
    """
    Create an SE(3) rotation matrix from roll-pitch-yaw angles

    :param roll: roll angle
    :type roll: float
    :param pitch: pitch angle
    :type pitch: float
    :param yaw: yaw angle
    :type yaw: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :param order: rotation order: 'zyx' [default], 'xyz', or 'yxz'
    :type order: str
    :return: SE(3) transformation matrix
    :rtype: ndarray(4,4)

    - ``rpy2tr(⍺, β, γ)`` is an SE(3) matrix (4x4) equivalent to the specified
      roll (⍺), pitch (β), yaw (γ) angles angles. These correspond to successive
      rotations about the axes specified by ``order``:

        - 'zyx' [default], rotate by γ about the z-axis, then by β about the new
          y-axis, then by ⍺ about the new x-axis.  Convention for a mobile robot
          with x-axis forward and y-axis sideways.
        - 'xyz', rotate by γ about the x-axis, then by β about the new y-axis,
          then by ⍺ about the new z-axis. Convention for a robot gripper with
          z-axis forward and y-axis between the gripper fingers.
        - 'yxz', rotate by γ about the y-axis, then by β about the new x-axis,
          then by ⍺ about the new z-axis. Convention for a camera with z-axis
          parallel to the optic axis and x-axis parallel to the pixel rows.

    - ``rpy2tr(RPY)`` as above but the roll, pitch, yaw angles are taken
      from ``RPY`` which is a 3-vector with values (⍺, β, γ).

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> rpy2tr(0.1, 0.2, 0.3)
        >>> rpy2tr([0.1, 0.2, 0.3])
        >>> rpy2tr([10, 20, 30], unit='deg')

    .. note:: By default, the translational component is zero but it can be
        set to a non-zero value.

    :seealso: :func:`~eul2tr` :func:`~rpy2r` :func:`~tr2rpy`
    """

    R = rpy2r(roll, pitch, yaw, order=order, unit=unit)
    return smb.r2t(R)


# ---------------------------------------------------------------------------------------#


def eul2r(phi, theta=None, psi=None, unit="rad"):
    """
    Create an SO(3) rotation matrix from Euler angles

    :param phi: Z-axis rotation
    :type phi: float
    :param theta: Y-axis rotation
    :type theta: float
    :param psi: Z-axis rotation
    :type psi: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :return: SO(3) rotation matrix
    :rtype: ndarray(3,3)

    - ``R = eul2r(φ, θ, ψ)`` is an SO(3) orthonornal rotation
      matrix equivalent to the specified Euler angles.  These correspond
      to rotations about the Z, Y, Z axes respectively.
    - ``R = eul2r(EUL)`` as above but the Euler angles are taken from
      ``EUL`` which is a 3-vector with values (φ θ ψ).

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> eul2r(0.1, 0.2, 0.3)
        >>> eul2r([0.1, 0.2, 0.3])
        >>> eul2r([10, 20, 30], unit='deg')

    :seealso: :func:`~rpy2r` :func:`~eul2tr` :func:`~tr2eul`

    :SymPy: supported
    """

    if np.isscalar(phi):
        angles = [phi, theta, psi]
    else:
        angles = smb.getvector(phi, 3)

    angles = smb.getunit(angles, unit)

    return rotz(angles[0]) @ roty(angles[1]) @ rotz(angles[2])


# ---------------------------------------------------------------------------------------#
def eul2tr(phi, theta=None, psi=None, unit="rad"):
    """
    Create an SE(3) pure rotation matrix from Euler angles

    :param phi: Z-axis rotation
    :type phi: float
    :param theta: Y-axis rotation
    :type theta: float
    :param psi: Z-axis rotation
    :type psi: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :return: SE(3) transformation matrix
    :rtype: ndarray(4,4)

    - ``R = eul2tr(PHI, θ, PSI)`` is an SE(3) homogeneous transformation
      matrix equivalent to the specified Euler angles.  These correspond
      to rotations about the Z, Y, Z axes respectively.
    - ``R = eul2tr(EUL)`` as above but the Euler angles are taken from
      ``EUL`` which is a 3-vector with values
      (PHI θ PSI).


    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> eul2tr(0.1, 0.2, 0.3)
        >>> eul2tr([0.1, 0.2, 0.3])
        >>> eul2tr([10, 20, 30], unit='deg')

    .. note:: By default, the translational component is zero but it can be
        set to a non-zero value.

    :seealso: :func:`~rpy2tr` :func:`~eul2r` :func:`~tr2eul`

    :SymPy: supported
    """

    R = eul2r(phi, theta, psi, unit=unit)
    return smb.r2t(R)


# ---------------------------------------------------------------------------------------#


def angvec2r(theta, v, unit="rad"):
    """
    Create an SO(3) rotation matrix from rotation angle and axis

    :param theta: rotation
    :type theta: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :param v: 3D rotation axis
    :type v: array_like(3)
    :return: SO(3) rotation matrix
    :rtype: ndarray(3,3)
    :raises ValueError: bad arguments

    ``angvec2r(θ, V)`` is an SO(3) orthonormal rotation matrix
    equivalent to a rotation of ``θ`` about the vector ``V``.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> angvec2r(0.3, [1, 0, 0])  # rotx(0.3)
        >>> angvec2r(0, [1, 0, 0])    # rotx(0)

    .. note::

        - If ``θ == 0`` then return identity matrix.
        - If ``θ ~= 0`` then ``V`` must have a finite length.

    :seealso: :func:`~angvec2tr` :func:`~tr2angvec`

    :SymPy: not supported
    """
    if not np.isscalar(theta) or not smb.isvector(v, 3):
        raise ValueError("Arguments must be theta and vector")

    if np.linalg.norm(v) < 10 * _eps:
        return np.eye(3)

    theta = smb.getunit(theta, unit)

    # Rodrigue's equation

    sk = smb.skew(smb.unitvec(v))
    R = np.eye(3) + math.sin(theta) * sk + (1.0 - math.cos(theta)) * sk @ sk
    return R


# ---------------------------------------------------------------------------------------#
def angvec2tr(theta, v, unit="rad"):
    """
    Create an SE(3) pure rotation from rotation angle and axis

    :param theta: rotation
    :type theta: float
    :param unit: angular units: 'rad' [default], or 'deg'
    :type unit: str
    :param v: 3D rotation axis
    :type v: : array_like(3)
    :return: SE(3) transformation matrix
    :rtype: ndarray(4,4)

    ``angvec2tr(θ, V)`` is an SE(3) homogeneous transformation matrix
    equivalent to a rotation of ``θ`` about the vector ``V``.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> angvec2tr(0.3, [1, 0, 0])  # rtotx(0.3)

    .. note::

        - If ``θ == 0`` then return identity matrix.
        - If ``θ ~= 0`` then ``V`` must have a finite length.
        - The translational part is zero.

    :seealso: :func:`~angvec2r` :func:`~tr2angvec`

    :SymPy: not supported
    """
    return smb.r2t(angvec2r(theta, v, unit=unit))


# ---------------------------------------------------------------------------------------#


def exp2r(w):
    r"""
    Create an SO(3) rotation matrix from exponential coordinates

    :param w: exponential coordinate vector
    :type w: array_like(3)
    :return: SO(3) rotation matrix
    :rtype: ndarray(3,3)
    :raises ValueError: bad arguments

    ``exp2r(w)`` is an SO(3) orthonormal rotation matrix
    equivalent to a rotation of :math:`\| w \|` about the vector :math:`\hat{w}`.

    If ``w`` is zero then result is the identity matrix.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> eulervec2r([0.3, 0, 0])  # rotx(0.3)
        >>> angvec2r([0, 0, 0])      # rotx(0)

    .. note:: Exponential coordinates are also known as an Euler vector

    :seealso: :func:`~angvec2r` :func:`~tr2angvec`

    :SymPy: not supported
    """
    if not smb.isvector(w, 3):
        raise ValueError("Arguments must be a 3-vector")

    v, theta = smb.unitvec_norm(w)

    if theta is None:
        return np.eye(3)

    # Rodrigue's equation

    sk = smb.skew(v)
    R = np.eye(3) + math.sin(theta) * sk + (1.0 - math.cos(theta)) * sk @ sk
    return R


def exp2tr(w):
    r"""
    Create an SE(3) pure rotation matrix from exponential coordinates

    :param w: exponential coordinate vector
    :type w: array_like(3)
    :return: SO(3) rotation matrix
    :rtype: ndarray(3,3)
    :raises ValueError: bad arguments

    ``exp2r(w)`` is an SO(3) orthonormal rotation matrix
    equivalent to a rotation of :math:`\| w \|` about the vector :math:`\hat{w}`.

    If ``w`` is zero then result is the identity matrix.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> eulervec2r([0.3, 0, 0])  # rotx(0.3)
        >>> angvec2r([0, 0, 0])      # rotx(0)

    .. note:: Exponential coordinates are also known as an Euler vector

    :seealso: :func:`~angvec2r` :func:`~tr2angvec`

    :SymPy: not supported
    """
    if not smb.isvector(w, 3):
        raise ValueError("Arguments must be a 3-vector")

    v, theta = smb.unitvec_norm(w)

    if theta is None:
        return np.eye(4)

    # Rodrigue's equation

    sk = smb.skew(v)
    R = np.eye(3) + math.sin(theta) * sk + (1.0 - math.cos(theta)) * sk @ sk
    return smb.r2t(R)


# ---------------------------------------------------------------------------------------#
def oa2r(o, a=None):
    """
    Create SO(3) rotation matrix from two vectors

    :param o: 3D vector parallel to Y- axis
    :type o: array_like(3)
    :param a: 3D vector parallel to the Z-axis
    :type o: array_like(3)
    :return: SO(3) rotation matrix
    :rtype: ndarray(3,3)

    ``T = oa2tr(O, A)`` is an SO(3) orthonormal rotation matrix for a frame
    defined in terms of vectors parallel to its Y- and Z-axes with respect to a
    reference frame.  In robotics these axes are respectively called the
    orientation and approach vectors defined such that R = [N O A] and N = O x
    A.

    Steps:

        1. N' = O x A
        2. O' = A x N
        3. normalize N', O', A
        4. stack horizontally into rotation matrix

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> oa2r([0, 1, 0], [0, 0, -1])  # Y := Y, Z := -Z

    .. note::

        - The A vector is the only guaranteed to have the same direction in the
          resulting rotation matrix
        - O and A do not have to be unit-length, they are normalized
        - O and A do not have to be orthogonal, so long as they are not parallel
        - The vectors O and A are parallel to the Y- and Z-axes of the
          equivalent coordinate frame.

    :seealso: :func:`~oa2tr`

    :SymPy: not supported
    """
    o = smb.getvector(o, 3, out="array")
    a = smb.getvector(a, 3, out="array")
    n = np.cross(o, a)
    o = np.cross(a, n)
    R = np.stack((smb.unitvec(n), smb.unitvec(o), smb.unitvec(a)), axis=1)
    return R


# ---------------------------------------------------------------------------------------#
def oa2tr(o, a=None):
    """
    Create SE(3) pure rotation from two vectors

    :param o: 3D vector parallel to Y- axis
    :type o: array_like(3)
    :param a: 3D vector parallel to the Z-axis
    :type o: array_like(3)
    :return: SE(3) transformation matrix
    :rtype: ndarray(4,4)

    ``T = oa2tr(O, A)`` is an SE(3) homogeneous transformation matrix for a
    frame defined in terms of vectors parallel to its Y- and Z-axes with respect
    to a reference frame.  In robotics these axes are respectively called the
    orientation and approach vectors defined such that R = [N O A] and N = O x
    A.

    Steps:

        1. N' = O x A
        2. O' = A x N
        3. normalize N', O', A
        4. stack horizontally into rotation matrix

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> oa2tr([0, 1, 0], [0, 0, -1])  # Y := Y, Z := -Z

    .. note:

        - The A vector is the only guaranteed to have the same direction in the
          resulting rotation matrix
        - O and A do not have to be unit-length, they are normalized
        - O and A do not have to be orthogonal, so long as they are not parallel
        - The translational part is zero.
        - The vectors O and A are parallel to the Y- and Z-axes of the
          equivalent coordinate frame.

    :seealso: :func:`~oa2r`

    :SymPy: not supported
    """
    return smb.r2t(oa2r(o, a))


# ------------------------------------------------------------------------------------------------------------------- #
def tr2angvec(T, unit="rad", check=False):
    r"""
    Convert SO(3) or SE(3) to angle and rotation vector

    :param R: SE(3) or SO(3) matrix
    :type R: ndarray(4,4) or ndarray(3,3)
    :param unit: 'rad' or 'deg'
    :type unit: str
    :param check: check that rotation matrix is valid
    :type check: bool
    :return: :math:`(\theta, {\bf v})`
    :rtype: float, ndarray(3)
    :raises ValueError: bad arguments

    ``(v, θ) = tr2angvec(R)`` is a rotation angle and a vector about which the
    rotation acts that corresponds to the rotation part of ``R``.

    By default the angle is in radians but can be changed setting `unit='deg'`.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> T = troty(45, 'deg')
        >>> v, theta = tr2angvec(T)
        >>> print(v, theta)

    .. note::

        - If the input is SE(3) the translation component is ignored.

    :seealso: :func:`~angvec2r` :func:`~angvec2tr` :func:`~tr2rpy` :func:`~tr2eul`
    """

    if smb.ismatrix(T, (4, 4)):
        R = smb.t2r(T)
    else:
        R = T
    if not isrot(R, check=check):
        raise ValueError("argument is not SO(3)")

    v = smb.vex(trlog(R))

    if smb.iszerovec(v):
        theta = 0
        v = np.r_[0, 0, 0]
    else:
        theta = smb.norm(v)
        v = smb.unitvec(v)

    if unit == "deg":
        theta *= 180 / math.pi

    return (theta, v)


# ------------------------------------------------------------------------------------------------------------------- #
def tr2eul(T, unit="rad", flip=False, check=False):
    r"""
    Convert SO(3) or SE(3) to ZYX Euler angles

    :param R: SE(3) or SO(3) matrix
    :type R: ndarray(4,4) or ndarray(3,3)
    :param unit: 'rad' or 'deg'
    :type unit: str
    :param flip: choose first Euler angle to be in quadrant 2 or 3
    :type flip: bool
    :param check: check that rotation matrix is valid
    :type check: bool
    :return: ZYZ Euler angles
    :rtype: ndarray(3)

    ``tr2eul(R)`` are the Euler angles corresponding to
    the rotation part of ``R``.

    The 3 angles :math:`[\phi, \theta, \psi]` correspond to sequential rotations
    about the Z, Y and Z axes respectively.

    By default the angles are in radians but can be changed setting `unit='deg'`.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> T = eul2tr(0.2, 0.3, 0.5)
        >>> print(T)
        >>> tr2eul(T)

    .. note::

        - There is a singularity for the case where :math:`\theta=0` in which
          case we arbitrarily set :math:`\phi = 0` and :math:`\phi` is set to
          :math:`\phi+\psi`.
        - If the input is SE(3) the translation component is ignored.

    :seealso: :func:`~eul2r` :func:`~eul2tr` :func:`~tr2rpy` :func:`~tr2angvec`
    :SymPy: not supported

    """

    if smb.ismatrix(T, (4, 4)):
        R = smb.t2r(T)
    else:
        R = T
    if not isrot(R, check=check):
        raise ValueError("argument is not SO(3)")

    eul = np.zeros((3,))
    if abs(R[0, 2]) < 10 * _eps and abs(R[1, 2]) < 10 * _eps:
        eul[0] = 0
        sp = 0
        cp = 1
        eul[1] = math.atan2(cp * R[0, 2] + sp * R[1, 2], R[2, 2])
        eul[2] = math.atan2(-sp * R[0, 0] + cp * R[1, 0], -sp * R[0, 1] + cp * R[1, 1])
    else:
        if flip:
            eul[0] = math.atan2(-R[1, 2], -R[0, 2])
        else:
            eul[0] = math.atan2(R[1, 2], R[0, 2])
        sp = math.sin(eul[0])
        cp = math.cos(eul[0])
        eul[1] = math.atan2(cp * R[0, 2] + sp * R[1, 2], R[2, 2])
        eul[2] = math.atan2(-sp * R[0, 0] + cp * R[1, 0], -sp * R[0, 1] + cp * R[1, 1])

    if unit == "deg":
        eul *= 180 / math.pi

    return eul


# ------------------------------------------------------------------------------------------------------------------- #


def tr2rpy(T, unit="rad", order="zyx", check=False):
    r"""
    Convert SO(3) or SE(3) to roll-pitch-yaw angles

    :param R: SE(3) or SO(3) matrix
    :type R: ndarray(4,4) or ndarray(3,3)
    :param unit: 'rad' or 'deg'
    :type unit: str
    :param order: 'xyz', 'zyx' or 'yxz' [default 'zyx']
    :type order: str
    :param check: check that rotation matrix is valid
    :type check: bool
    :return: Roll-pitch-yaw angles
    :rtype: ndarray(3)
    :raises ValueError: bad arguments

    ``tr2rpy(R)`` are the roll-pitch-yaw angles corresponding to
    the rotation part of ``R``.

    The 3 angles RPY = :math:`[\theta_R, \theta_P, \theta_Y]` correspond to
    sequential rotations about the Z, Y and X axes respectively.  The axis order
    sequence can be changed by setting:

    - ``order='xyz'``  for sequential rotations about X, Y, Z axes
    - ``order='yxz'``  for sequential rotations about Y, X, Z axes

    By default the angles are in radians but can be changed setting
    ``unit='deg'``.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> T = rpy2tr(0.2, 0.3, 0.5)
        >>> print(T)
        >>> tr2rpy(T)

    .. note::

        - There is a singularity for the case where :math:`\theta_P = \pi/2` in
          which case we arbitrarily set :math:`\theta_R=0` and
          :math:`\theta_Y = \theta_R + \theta_Y`.
        - If the input is SE(3) the translation component is ignored.

    :seealso: :func:`~rpy2r` :func:`~rpy2tr` :func:`~tr2eul`,
              :func:`~tr2angvec`
    :SymPy: not supported
    """

    if smb.ismatrix(T, (4, 4)):
        R = smb.t2r(T)
    else:
        R = T
    if not isrot(R, check=check):
        raise ValueError("not a valid SO(3) matrix")

    rpy = np.zeros((3,))
    if order in ("xyz", "arm"):

        # XYZ order
        if abs(abs(R[0, 2]) - 1) < 10 * _eps:  # when |R13| == 1
            # singularity
            rpy[0] = 0  # roll is zero
            if R[0, 2] > 0:
                rpy[2] = math.atan2(R[2, 1], R[1, 1])  # R+Y
            else:
                rpy[2] = -math.atan2(R[1, 0], R[2, 0])  # R-Y
            rpy[1] = math.asin(np.clip(R[0, 2], -1.0, 1.0))
        else:
            rpy[0] = -math.atan2(R[0, 1], R[0, 0])
            rpy[2] = -math.atan2(R[1, 2], R[2, 2])

            k = np.argmax(np.abs([R[0, 0], R[0, 1], R[1, 2], R[2, 2]]))
            if k == 0:
                rpy[1] = math.atan(R[0, 2] * math.cos(rpy[0]) / R[0, 0])
            elif k == 1:
                rpy[1] = -math.atan(R[0, 2] * math.sin(rpy[0]) / R[0, 1])
            elif k == 2:
                rpy[1] = -math.atan(R[0, 2] * math.sin(rpy[2]) / R[1, 2])
            elif k == 3:
                rpy[1] = math.atan(R[0, 2] * math.cos(rpy[2]) / R[2, 2])

    elif order in ("zyx", "vehicle"):

        # old ZYX order (as per Paul book)
        if abs(abs(R[2, 0]) - 1) < 10 * _eps:  # when |R31| == 1
            # singularity
            rpy[0] = 0  # roll is zero
            if R[2, 0] < 0:
                rpy[2] = -math.atan2(R[0, 1], R[0, 2])  # R-Y
            else:
                rpy[2] = math.atan2(-R[0, 1], -R[0, 2])  # R+Y
            rpy[1] = -math.asin(np.clip(R[2, 0], -1.0, 1.0))
        else:
            rpy[0] = math.atan2(R[2, 1], R[2, 2])  # R
            rpy[2] = math.atan2(R[1, 0], R[0, 0])  # Y

            k = np.argmax(np.abs([R[0, 0], R[1, 0], R[2, 1], R[2, 2]]))
            if k == 0:
                rpy[1] = -math.atan(R[2, 0] * math.cos(rpy[2]) / R[0, 0])
            elif k == 1:
                rpy[1] = -math.atan(R[2, 0] * math.sin(rpy[2]) / R[1, 0])
            elif k == 2:
                rpy[1] = -math.atan(R[2, 0] * math.sin(rpy[0]) / R[2, 1])
            elif k == 3:
                rpy[1] = -math.atan(R[2, 0] * math.cos(rpy[0]) / R[2, 2])

    elif order in ("yxz", "camera"):

        if abs(abs(R[1, 2]) - 1) < 10 * _eps:  # when |R23| == 1
            # singularity
            rpy[0] = 0
            if R[1, 2] < 0:
                rpy[2] = -math.atan2(R[2, 0], R[0, 0])  # R-Y
            else:
                rpy[2] = math.atan2(-R[2, 0], -R[2, 1])  # R+Y
            rpy[1] = -math.asin(np.clip(R[1, 2], -1.0, 1.0))  # P
        else:
            rpy[0] = math.atan2(R[1, 0], R[1, 1])
            rpy[2] = math.atan2(R[0, 2], R[2, 2])

            k = np.argmax(np.abs([R[1, 0], R[1, 1], R[0, 2], R[2, 2]]))
            if k == 0:
                rpy[1] = -math.atan(R[1, 2] * math.sin(rpy[0]) / R[1, 0])
            elif k == 1:
                rpy[1] = -math.atan(R[1, 2] * math.cos(rpy[0]) / R[1, 1])
            elif k == 2:
                rpy[1] = -math.atan(R[1, 2] * math.sin(rpy[2]) / R[0, 2])
            elif k == 3:
                rpy[1] = -math.atan(R[1, 2] * math.cos(rpy[2]) / R[2, 2])

    else:
        raise ValueError("Invalid order")

    if unit == "deg":
        rpy *= 180 / math.pi

    return rpy


# ---------------------------------------------------------------------------------------#
def trlog(T, check=True, twist=False):
    """
    Logarithm of SO(3) or SE(3) matrix

    :param R: SE(3) or SO(3) matrix
    :type R: ndarray(4,4) or ndarray(3,3)
    :param check: check that matrix is valid
    :type check: bool
    :param twist: return a twist vector instead of matrix [default]
    :type twist: bool
    :return: logarithm
    :rtype: ndarray(4,4) or ndarray(3,3)
    :raises ValueError: bad argument

    An efficient closed-form solution of the matrix logarithm for arguments that
    are SO(3) or SE(3).

    - ``trlog(R)`` is the logarithm of the passed rotation matrix ``R`` which
      will be 3x3 skew-symmetric matrix.  The equivalent vector from ``vex()``
      is parallel to rotation axis and its norm is the amount of rotation about
      that axis.
    - ``trlog(T)`` is the logarithm of the passed homogeneous transformation
      matrix ``T`` which will be 4x4 augumented skew-symmetric matrix. The
      equivalent vector from ``vexa()`` is the twist vector (6x1) comprising [v
      w].

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> trlog(trotx(0.3))
        >>> trlog(trotx(0.3), twist=True)
        >>> trlog(rotx(0.3))
        >>> trlog(rotx(0.3), twist=True)

    :seealso: :func:`~trexp` :func:`~spatialmath.smb.transformsNd.vex` :func:`~spatialmath.smb.transformsNd.vexa`
    """

    if ishom(T, check=check):
        # SE(3) matrix

        if smb.iseye(T):
            # is identity matrix
            if twist:
                return np.zeros((6,))
            else:
                return np.zeros((4, 4))
        else:
            [R, t] = smb.tr2rt(T)

            if smb.iseye(R):
                # rotation matrix is identity
                if twist:
                    return np.r_[t, 0, 0, 0]
                else:
                    return smb.Ab2M(np.zeros((3, 3)), t)
            else:
                S = trlog(R, check=False)  # recurse
                w = smb.vex(S)
                theta = smb.norm(w)
                Ginv = (
                    np.eye(3)
                    - S / 2
                    + (1 / theta - 1 / math.tan(theta / 2) / 2) / theta * S @ S
                )
                v = Ginv @ t
                if twist:
                    return np.r_[v, w]
                else:
                    return smb.Ab2M(S, v)

    elif isrot(T, check=check):
        # deal with rotation matrix
        R = T
        if smb.iseye(R):
            # matrix is identity
            if twist:
                return np.zeros((3,))
            else:
                return np.zeros((3, 3))
        elif abs(np.trace(R) + 1) < 100 * _eps:
            # check for trace = -1
            #   rotation by +/- pi, +/- 3pi etc.
            diagonal = R.diagonal()
            k = diagonal.argmax()
            mx = diagonal[k]
            I = np.eye(3)
            col = R[:, k] + I[:, k]
            w = col / np.sqrt(2 * (1 + mx))
            theta = math.pi
            if twist:
                return w * theta
            else:
                return smb.skew(w * theta)
        else:
            # general case
            theta = math.acos((np.trace(R) - 1) / 2)
            skw = (R - R.T) / 2 / math.sin(theta)
            if twist:
                return smb.vex(skw * theta)
            else:
                return skw * theta
    else:
        raise ValueError("Expect SO(3) or SE(3) matrix")


# ---------------------------------------------------------------------------------------#


def trexp(S, theta=None, check=True):
    """
    Exponential of se(3) or so(3) matrix

    :param S: se(3), so(3) matrix or equivalent twist vector
    :type T: ndarray(4,4) or ndarray(6); or ndarray(3,3) or ndarray(3)
    :param θ: motion
    :type θ: float
    :return: matrix exponential in SE(3) or SO(3)
    :rtype: ndarray(4,4) or ndarray(3,3)
    :raises ValueError: bad arguments

    An efficient closed-form solution of the matrix exponential for arguments
    that are so(3) or se(3).

    For so(3) the results is an SO(3) rotation matrix:

    - ``trexp(Ω)`` is the matrix exponential of the so(3) element ``Ω`` which is
      a 3x3 skew-symmetric matrix.
    - ``trexp(Ω, θ)`` as above but for an so(3) motion of Ωθ, where ``Ω`` is
      unit-norm skew-symmetric matrix representing a rotation axis and a
      rotation magnitude given by ``θ``.
    - ``trexp(ω)`` is the matrix exponential of the so(3) element ``ω``
      expressed as a 3-vector.
    - ``trexp(ω, θ)`` as above but for an so(3) motion of ωθ where ``ω`` is a
      unit-norm vector representing a rotation axis and a rotation magnitude
      given by ``θ``. ``ω`` is expressed as a 3-vector.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> trexp(skew([1, 2, 3]))
        >>> trexp(skew([1, 0, 0]), 2)  # revolute unit twist
        >>> trexp([1, 2, 3])
        >>> trexp([1, 0, 0], 2)  # revolute unit twist

    For se(3) the results is an SE(3) homogeneous transformation matrix:

    - ``trexp(Σ)`` is the matrix exponential of the se(3) element ``Σ`` which is
      a 4x4 augmented skew-symmetric matrix.
    - ``trexp(Σ, θ)`` as above but for an se(3) motion of Σθ, where ``Σ`` must
      represent a unit-twist, ie. the rotational component is a unit-norm
      skew-symmetric matrix.
    - ``trexp(S)`` is the matrix exponential of the se(3) element ``S``
      represented as a 6-vector which can be considered a screw motion.
    - ``trexp(S, θ)`` as above but for an se(3) motion of Sθ, where ``S`` must
      represent a unit-twist, ie. the rotational component is a unit-norm
      skew-symmetric matrix.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> trexp(skewa([1, 2, 3, 4, 5, 6]))
        >>> trexp(skewa([1, 0, 0, 0, 0, 0]), 2)  # prismatic unit twist
        >>> trexp([1, 2, 3, 4, 5, 6])
        >>> trexp([1, 0, 0, 0, 0, 0], 2)

    :seealso: :func:`~trlog :func:`~spatialmath.smb.transforms2d.trexp2`
    """

    if smb.ismatrix(S, (4, 4)) or smb.isvector(S, 6):
        # se(3) case
        if smb.ismatrix(S, (4, 4)):
            # augmentented skew matrix
            if check and not smb.isskewa(S):
                raise ValueError("argument must be a valid se(3) element")
            tw = smb.vexa(S)
        else:
            # 6 vector
            tw = smb.getvector(S)

        if smb.iszerovec(tw):
            return np.eye(4)

        if theta is None:
            (tw, theta) = smb.unittwist_norm(tw)
        else:
            if theta == 0:
                return np.eye(4)
            elif not smb.isunittwist(tw):
                raise ValueError("If theta is specified S must be a unit twist")

        # tw is a unit twist, th is its magnitude
        t = tw[0:3]
        w = tw[3:6]

        R = smb.rodrigues(w, theta)

        skw = smb.skew(w)
        V = (
            np.eye(3) * theta
            + (1.0 - math.cos(theta)) * skw
            + (theta - math.sin(theta)) * skw @ skw
        )

        return smb.rt2tr(R, V @ t)

    elif smb.ismatrix(S, (3, 3)) or smb.isvector(S, 3):
        # so(3) case
        if smb.ismatrix(S, (3, 3)):
            # skew symmetric matrix
            if check and not smb.isskew(S):
                raise ValueError("argument must be a valid so(3) element")
            w = smb.vex(S)
        else:
            # 3 vector
            w = smb.getvector(S)

        if theta is not None and not smb.isunitvec(w):
            raise ValueError("If theta is specified S must be a unit twist")

        # do Rodrigues' formula for rotation
        return smb.rodrigues(w, theta)
    else:
        raise ValueError(" First argument must be SO(3), 3-vector, SE(3) or 6-vector")


def trnorm(T):
    r"""
    Normalize an SO(3) or SE(3) matrix

    :param R: SE(3) or SO(3) matrix
    :type R: ndarray(4,4) or ndarray(3,3)
    :param T1: second SE(3) matrix
    :return: normalized SE(3) or SO(3) matrix
    :rtype: ndarray(4,4) or ndarray(3,3)
    :raises ValueError: bad arguments

    - ``trnorm(R)`` is guaranteed to be a proper orthogonal matrix rotation
      matrix (3x3) which is *close* to the input matrix R (3x3).
    - ``trnorm(T)`` as above but the rotational submatrix of the homogeneous
      transformation T (4x4) is normalised while the translational part is
      unchanged.

    The steps in normalization are:

    #. If :math:`\mathbf{R} = [n, o, a]`
    #. Form unit vectors :math:`\hat{o}, \hat{a}` from  :math:`o, a` respectively
    #. Form the normal vector :math:`\hat{n} = \hat{o} \times \hat{a}`
    #. Recompute :math:`\hat{o} = \hat{a} \times \hat{n}` to ensure that :math:`\hat{o}, \hat{a}` are orthogonal
    #. Form the normalized SO(3) matrix :math:`\mathbf{R} = [\hat{n}, \hat{o}, \hat{a}]`

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> from numpy import linalg
        >>> T = troty(45, 'deg', t=[3, 4, 5])
        >>> linalg.det(T[:3,:3]) - 1 # is a valid SO(3)
        >>> T = T @ T @ T @ T @ T @ T @ T @ T @ T @ T @ T @ T @ T
        >>> linalg.det(T[:3,:3]) - 1  # not quite a valid SO(3) anymore
        >>> T = trnorm(T)
        >>> linalg.det(T[:3,:3]) - 1  # once more a valid SO(3)

    .. note::

        - Only the direction of a-vector (the z-axis) is unchanged.
        - Used to prevent finite word length arithmetic causing transforms to
          become 'unnormalized', ie. determinant :math:`\ne 1`.
    """

    if not ishom(T) and not isrot(T):
        raise ValueError("expecting SO(3) or SE(3)")

    o = T[:3, 1]
    a = T[:3, 2]

    n = np.cross(o, a)  # N = O x A
    o = np.cross(a, n)  # (a)];
    R = np.stack((smb.unitvec(n), smb.unitvec(o), smb.unitvec(a)), axis=1)

    if ishom(T):
        return smb.rt2tr(R, T[:3, 3])
    else:
        return R


def trinterp(start, end, s=None):
    """
    Interpolate SE(3) matrices

    :param start: initial SE(3) or SO(3) matrix value when s=0, if None then identity is used
    :type start: ndarray(4,4) or ndarray(3,3)
    :param end: final SE(3) or SO(3) matrix, value when s=1
    :type end: ndarray(4,4) or ndarray(3,3)
    :param s: interpolation coefficient, range 0 to 1
    :type s: float
    :return: interpolated SE(3) or SO(3) matrix value
    :rtype: ndarray(4,4) or ndarray(3,3)
    :raises ValueError: bad arguments

    - ``trinterp(None, T, S)`` is a homogeneous transform (4x4) interpolated
      between identity when S=0 and T (4x4) when S=1.
    - ``trinterp(T0, T1, S)`` as above but interpolated
      between T0 (4x4) when S=0 and T1 (4x4) when S=1.
    - ``trinterp(None, R, S)`` is a rotation matrix (3x3) interpolated
      between identity when S=0 and R (3x3) when S=1.
    - ``trinterp(R0, R1, S)`` as above but interpolated
      between R0 (3x3) when S=0 and R1 (3x3) when S=1.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> T1 = transl(1, 2, 3)
        >>> T2 = transl(4, 5, 6)
        >>> trinterp(T1, T2, 0)
        >>> trinterp(T1, T2, 1)
        >>> trinterp(T1, T2, 0.5)
        >>> trinterp(None, T2, 0)
        >>> trinterp(None, T2, 1)
        >>> trinterp(None, T2, 0.5)

    .. note:: Rotation is interpolated using quaternion spherical linear interpolation (slerp).

    :seealso: :func:`spatialmath.smb.quaternions.qlerp` :func:`~spatialmath.smb.transforms3d.trinterp2`
    """

    if not 0 <= s <= 1:
        raise ValueError("s outside interval [0,1]")

    if smb.ismatrix(end, (3, 3)):
        # SO(3) case

        if start is None:
            # 	TRINTERP(T, s)
            q0 = smb.r2q(smb.t2r(end))
            qr = smb.qslerp(smb.eye(), q0, s)
        else:
            # 	TRINTERP(T0, T1, s)
            q0 = smb.r2q(smb.t2r(start))
            q1 = smb.r2q(smb.t2r(end))
            qr = smb.qslerp(q0, q1, s)

        return smb.q2r(qr)

    elif smb.ismatrix(end, (4, 4)):
        # SE(3) case
        if start is None:
            # 	TRINTERP(T, s)
            q0 = smb.r2q(smb.t2r(end))
            p0 = transl(end)

            qr = smb.qslerp(smb.qeye(), q0, s)
            pr = s * p0
        else:
            # 	TRINTERP(T0, T1, s)
            q0 = smb.r2q(smb.t2r(start))
            q1 = smb.r2q(smb.t2r(end))

            p0 = transl(start)
            p1 = transl(end)

            qr = smb.qslerp(q0, q1, s)
            pr = p0 * (1 - s) + s * p1

        return smb.rt2tr(smb.q2r(qr), pr)
    else:
        return ValueError("Argument must be SO(3) or SE(3)")


def delta2tr(d):
    r"""
    Convert differential motion to SE(3)

    :param Δ: differential motion as a 6-vector
    :type Δ: array_like(6)
    :return: SE(3) matrix
    :rtype: ndarray(4,4)

    ``delta2tr(Δ)`` is an SE(3) matrix representing differential
    motion :math:`\Delta = [\delta_x, \delta_y, \delta_z, \theta_x, \theta_y, \theta_z]`.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> delta2tr([0.001, 0, 0, 0, 0.002, 0])

    :Reference: Robotics, Vision & Control: Second Edition, P. Corke, Springer 2016; p67.

    :seealso: :func:`~tr2delta`
    :SymPy: supported
    """

    return np.eye(4, 4) + smb.skewa(d)


def trinv(T):
    r"""
    Invert an SE(3) matrix

    :param T: SE(3) matrix
    :type T: ndarray(4,4)
    :return: inverse of SE(3) matrix
    :rtype: ndarray(4,4)
    :raises ValueError: bad arguments

    Computes an efficient inverse of an SE(3) matrix:

    :math:`\begin{pmatrix} {\bf R} & t \\ 0\,0\,0 & 1 \end{pmatrix}^{-1} =  \begin{pmatrix} {\bf R}^T & -{\bf R}^T t \\ 0\,0\, 0 & 1 \end{pmatrix}`

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> T = trotx(0.3, t=[4,5,6])
        >>> trinv(T)
        >>> T @ trinv(T)

    :SymPy: supported
    """
    if not ishom(T):
        raise ValueError("expecting SE(3) matrix")
    # inline this code for speed, don't use tr2rt and rt2tr
    R = T[:3, :3]
    t = T[:3, 3]
    Ti = np.zeros((4, 4), dtype=T.dtype)
    Ti[:3, :3] = R.T
    Ti[:3, 3] = -R.T @ t
    Ti[3, 3] = 1
    return Ti


def tr2delta(T0, T1=None):
    r"""
    Difference of SE(3) matrices as differential motion

    :param T0: first SE(3) matrix
    :type T0: ndarray(4,4)
    :param T1: second SE(3) matrix
    :type T1: ndarray(4,4)
    :return: Differential motion as a 6-vector
    :rtype:ndarray(6)
    :raises ValueError: bad arguments

    - ``tr2delta(T0, T1)`` is the differential motion Δ (6x1) corresponding to
      infinitessimal motion (in the T0 frame) from pose T0 to T1 which are SE(3)
      matrices.

    - ``tr2delta(T)`` as above but the motion is from the world frame to the
      pose represented by T.

    The vector :math:`\Delta = [\delta_x, \delta_y, \delta_z, \theta_x,
    \theta_y, \theta_z` represents infinitessimal translation and rotation, and
    is an approximation to the instantaneous spatial velocity multiplied by time
    step.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> T1 = trotx(0.3, t=[4,5,6])
        >>> T2 = trotx(0.31, t=[4,5.02,6])
        >>> tr2delta(T1, T2)

    .. note::

        - Δ is only an approximation to the motion T, and assumes
          that T0 ~ T1 or T ~ eye(4,4).
        - Can be considered as an approximation to the effect of spatial velocity over a
          a time interval, average spatial velocity multiplied by time.

    :Reference: Robotics, Vision & Control: Second Edition, P. Corke, Springer 2016; p67.

    :seealso: :func:`~delta2tr`
    :SymPy: supported
    """

    if T1 is None:
        # tr2delta(T)

        if not ishom(T0):
            raise ValueError("expecting SE(3) matrix")
        Td = T0

    else:
        #  incremental transformation from T0 to T1 in the T0 frame
        Td = trinv(T0) @ T1

    return np.r_[transl(Td), smb.vex(smb.t2r(Td) - np.eye(3))]


def tr2jac(T):
    r"""
    SE(3) Jacobian matrix

    :param T: SE(3) matrix
    :type T: ndarray(4,4)
    :return: Jacobian matrix
    :rtype: ndarray(6,6)

    Computes an Jacobian matrix that maps spatial velocity between two frames
    defined by an SE(3) matrix.

    ``tr2jac(T)`` is a Jacobian matrix (6x6) that maps spatial velocity or
    differential motion from frame {B} to frame {A} where the pose of {B}
    elative to {A} is represented by the homogeneous transform T = :math:`{}^A
    {\bf T}_B`.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> T = trotx(0.3, t=[4,5,6])
        >>> tr2jac(T)

    :Reference: Robotics, Vision & Control: Second Edition, P. Corke, Springer 2016; p65.
    :SymPy: supported
    """

    if not ishom(T):
        raise ValueError("expecting an SE(3) matrix")

    Z = np.zeros((3, 3), dtype=T.dtype)
    R = smb.t2r(T)
    return np.block([[R, Z], [Z, R]])


def eul2jac(angles):
    """
    Euler angle rate Jacobian

    :param angles: Euler angles (φ, θ, ψ)
    :type angles: array_like(3)
    :return: Jacobian matrix
    :rtype: ndarray(3,3)

    - ``eul2jac(φ, θ, ψ)`` is a Jacobian matrix (3x3) that maps ZYZ Euler angle
      rates to angular velocity at the operating point specified by the Euler
      angles φ, ϴ, ψ.
    - ``eul2jac(𝚪)`` as above but the Euler angles are taken from ``𝚪`` which
      is a 3-vector with values (φ θ ψ).

    Example:

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> eul2jac(0.1, 0.2, 0.3)

    .. note::
        - Used in the creation of an analytical Jacobian.
        - Angles in radians, rates in radians/sec.

    Reference::
    - Robotics, Vision & Control: Second Edition, P. Corke, Springer 2016; p232-3.

    :SymPy: supported

    :seealso: :func:`angvelxform` :func:`rpy2jac` :func:`exp2jac`
    """

    if len(angles) == 1:
        angles = angles[0]

    phi = angles[0]
    theta = angles[1]

    ctheta = smb.sym.cos(theta)
    stheta = smb.sym.sin(theta)
    cphi = smb.sym.cos(phi)
    sphi = smb.sym.sin(phi)

    # fmt: off
    return np.array([
            [ 0, -sphi, cphi * stheta],
            [ 0,  cphi, sphi * stheta],
            [ 1,     0, ctheta ]
        ])
    # fmt: on


def rpy2jac(angles, order="zyx"):
    """
    Jacobian from RPY angle rates to angular velocity

    :param angles: roll-pitch-yaw angles (⍺, β, γ)
    :param order: angle sequence, defaults to 'zyx'
    :type order: str, optional
    :param order: rotation order: 'zyx' [default], 'xyz', or 'yxz'
    :type order: str
    :return: Jacobian matrix
    :rtype: ndarray(3,3)

    - ``rpy2jac(⍺, β, γ)`` is a Jacobian matrix (3x3) that maps roll-pitch-yaw
      angle rates to angular velocity at the operating point (⍺, β, γ). These
      correspond to successive rotations about the axes specified by ``order``:

        - 'zyx' [default], rotate by γ about the z-axis, then by β about the new
          y-axis, then by ⍺ about the new x-axis.  Convention for a mobile robot
          with x-axis forward and y-axis sideways.
        - 'xyz', rotate by γ about the x-axis, then by β about the new y-axis,
          then by ⍺ about the new z-axis. Convention for a robot gripper with
          z-axis forward and y-axis between the gripper fingers.
        - 'yxz', rotate by γ about the y-axis, then by β about the new x-axis,
          then by ⍺ about the new z-axis. Convention for a camera with z-axis
          parallel to the optic axis and x-axis parallel to the pixel rows.

    - ``rpy2jac(𝚪)`` as above but the roll, pitch, yaw angles are taken
      from ``𝚪`` which is a 3-vector with values (⍺, β, γ).

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> rpy2jac(0.1, 0.2, 0.3)

    .. note::
        - Used in the creation of an analytical Jacobian.
        - Angles in radians, rates in radians/sec.

    Reference::
    - Robotics, Vision & Control: Second Edition, P. Corke, Springer 2016; p232-3.

    :SymPy: supported

    :seealso: :func:`rotvelxform` :func:`eul2jac` :func:`exp2jac`
    """

    pitch = angles[1]
    yaw = angles[2]

    cp = smb.sym.cos(pitch)
    sp = smb.sym.sin(pitch)
    cy = smb.sym.cos(yaw)
    sy = smb.sym.sin(yaw)

    if order == "xyz":
        # fmt: off
        J = np.array([	
            [ sp,       0,   1], 
            [-cp * sy,  cy,  0],
            [ cp * cy,  sy,  0]
        ])
        # fmt: on
    elif order == "zyx":
        # fmt: off
        J = np.array([	 
                [ cp * cy, -sy, 0],
                [ cp * sy,  cy, 0],
                [-sp,       0,  1],
            ])
        # fmt: on
    elif order == "yxz":
        # fmt: off
        J = np.array([	
                [ cp * sy,  cy, 0],
                [-sp,       0,  1],
                [ cp * cy, -sy, 0]
            ])
        # fmt: on
    return J


def exp2jac(v):
    """
    Jacobian from exponential coordinate rates to angular velocity

    :param v: Exponential coordinates
    :type v: array_like(3)
    :return: Jacobian matrix
    :rtype: ndarray(3,3)

    - ``exp2jac(v)`` is a Jacobian matrix (3x3) that maps exponential coordinate
      rates to angular velocity at the operating point ``v``.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> expjac(0.3 * np.r_[1, 0, 0])

    .. note::
        - Used in the creation of an analytical Jacobian.

    Reference::

        - A compact formula for the derivative of a 3-D rotation in
          exponential coordinate
          Guillermo Gallego, Anthony Yezzi
          https://arxiv.org/pdf/1312.0788v1.pdf
        - Robot Dynamics Lecture Notes
          Robotic Systems Lab, ETH Zurich, 2018
          https://ethz.ch/content/dam/ethz/special-interest/mavt/robotics-n-intelligent-systems/rsl-dam/documents/RobotDynamics2018/RD_HS2018script.pdf

    :SymPy: supported

    :seealso: :func:`rotvelxform` :func:`eul2jac` :func:`rpy2jac`
    """

    vn, theta = smb.unitvec_norm(v)
    if theta is None:
        return np.eye(3)

    # R = trexp(v)
    # z = np.eye(3,3) - R
    # # build the derivative columnwise
    # A = []
    # for i in range(3):
    #     # (III.7)
    #     dRdvi = vn[i] * smb.skew(vn) + smb.skew(np.cross(vn, z[:,i])) / theta
    #     x = smb.vex(dRdvi)
    #     A.append(x)
    # return np.c_[A].T

    # from ETH paper
    theta = smb.norm(v)
    sk = smb.skew(v)

    # (2.106)
    E = (
        np.eye(3)
        + sk * (1 - np.cos(theta)) / theta**2
        + sk @ sk * (theta - np.sin(theta)) / theta**3
    )
    return E


def r2x(R, representation="rpy/xyz"):
    r"""
    Convert SO(3) matrix to angular representation

    :param R: SO(3) rotation matrix
    :type R: ndarray(3,3)
    :param representation: rotational representation, defaults to "rpy/xyz"
    :type representation: str, optional
    :return: angular representation
    :rtype: ndarray(3)

    Convert an SO(3) rotation matrix to a minimal rotational representation
    :math:`\vec{\Gamma} \in \mathbb{R}^3`.

    ============================  ========================================
    ``representation``            Rotational representation
    ============================  ========================================
    ``"rpy/xyz"`` ``"arm"``       RPY angular rates in XYZ order (default)
    ``"rpy/zyx"`` ``"vehicle"``   RPY angular rates in XYZ order
    ``"rpy/yxz"`` ``"camera"``    RPY angular rates in YXZ order
    ``"eul"``                     Euler angular rates in ZYZ order
    ``"exp"``                     exponential coordinate rates
    ============================  ========================================

    :SymPy: supported

    :seealso: :func:`x2r` :func:`tr2rpy` :func:`tr2eul` :func:`trlog`
    """
    if representation == "eul":
        r = tr2eul(R)
    elif representation.startswith("rpy/"):
        r = tr2rpy(R, order=representation[4:])
    elif representation in ("arm", "vehicle", "camera"):
        r = tr2rpy(R, order=representation)
    elif representation == "exp":
        r = trlog(R, twist=True)
    else:
        raise ValueError(f"unknown representation: {representation}")
    return r


def x2r(r, representation="rpy/xyz"):
    r"""
    Convert angular representation to SO(3) matrix

    :param r: angular representation
    :type r: array_like(3)
    :param representation: rotational representation, defaults to "rpy/xyz"
    :type representation: str, optional
    :return: SO(3) rotation matrix
    :rtype: ndarray(3,3)

    Convert a minimal rotational representation :math:`\vec{\Gamma} \in
    \mathbb{R}^3` to an SO(3) rotation matrix.

    ============================  ========================================
    ``representation``            Rotational representation
    ============================  ========================================
    ``"rpy/xyz"`` ``"arm"``       RPY angular rates in XYZ order (default)
    ``"rpy/zyx"`` ``"vehicle"``   RPY angular rates in XYZ order
    ``"rpy/yxz"`` ``"camera"``    RPY angular rates in YXZ order
    ``"eul"``                     Euler angular rates in ZYZ order
    ``"exp"``                     exponential coordinate rates
    ============================  ========================================

    :SymPy: supported

    :seealso: :func:`r2x` :func:`rpy2r` :func:`eul2r` :func:`trexp`
    """
    if representation == "eul":
        R = eul2r(r)
    elif representation.startswith("rpy/"):
        R = rpy2r(r, order=representation[4:])
    elif representation in ("arm", "vehicle", "camera"):
        R = rpy2r(r, order=representation)
    elif representation == "exp":
        R = trexp(r)
    else:
        raise ValueError(f"unknown representation: {representation}")
    return R


def tr2x(T, representation="rpy/xyz"):
    r"""
    Convert SE(3) to an analytic representation

    :param T: pose as an SE(3) matrix
    :type T: ndarray(4,4)
    :param representation: angular representation to use, defaults to "rpy/xyz"
    :type representation: str, optional
    :return: analytic vector representation
    :rtype: ndarray(6)

    Convert an SE(3) matrix into an equivalent vector representation
    :math:`\vec{x}  = (\vec{t},\vec{r}) \in \mathbb{R}^6` where rotation
    :math:`\vec{r} \in \mathbb{R}^3` is encoded in a minimal representation.

    ============================  ========================================
    ``representation``            Rotational representation
    ============================  ========================================
    ``"rpy/xyz"`` ``"arm"``       RPY angular rates in XYZ order (default)
    ``"rpy/zyx"`` ``"vehicle"``   RPY angular rates in XYZ order
    ``"rpy/yxz"`` ``"camera"``    RPY angular rates in YXZ order
    ``"eul"``                     Euler angular rates in ZYZ order
    ``"exp"``                     exponential coordinate rates
    ============================  ========================================

    :SymPy: supported

    :seealso: :func:`r2x`
    """
    t = transl(T)
    R = smb.t2r(T)
    r = r2x(R, representation=representation)
    return np.r_[t, r]


def x2tr(x, representation="rpy/xyz"):
    r"""
    Convert analytic representation to SE(3)

    :param x: analytic vector representation
    :type x: array_like(6)
    :param representation: angular representation to use, defaults to "rpy/xyz"
    :type representation: str, optional
    :return: pose as an SE(3) matrix
    :rtype: ndarray(4,4)

    Convert a vector representation of pose :math:`\vec{x} = (\vec{t},\vec{r})
    \in \mathbb{R}^6` to SE(3), where rotation :math:`\vec{r} \in \mathbb{R}^3` is encoded
    in a minimal representation to an equivalent SE(3) matrix.

    ============================  ========================================
    ``representation``            Rotational representation
    ============================  ========================================
    ``"rpy/xyz"`` ``"arm"``       RPY angular rates in XYZ order (default)
    ``"rpy/zyx"`` ``"vehicle"``   RPY angular rates in XYZ order
    ``"rpy/yxz"`` ``"camera"``    RPY angular rates in YXZ order
    ``"eul"``                     Euler angular rates in ZYZ order
    ``"exp"``                     exponential coordinate rates
    ============================  ========================================

    :SymPy: supported

    :seealso: :func:`r2x`
    """
    t = x[:3]
    R = x2r(x[3:], representation=representation)

    return smb.rt2tr(R, t)


def rot2jac(R, representation="rpy/xyz"):
    """
    DEPRECATED, use :func:`rotvelxform` instead
    """
    raise DeprecationWarning("use rotvelxform instead")


def angvelxform(𝚪, inverse=False, full=True, representation="rpy/xyz"):
    """
    DEPRECATED, use :func:`rotvelxform` instead
    """
    raise DeprecationWarning("use rotvelxform instead")


def angvelxform_dot(𝚪, 𝚪d, full=True, representation="rpy/xyz"):
    """
    DEPRECATED, use :func:`rotvelxform` instead
    """
    raise DeprecationWarning("use rotvelxform_inv_dot instead")


def rotvelxform(𝚪, inverse=False, full=False, representation="rpy/xyz"):
    r"""
    Rotational velocity transformation

    :param 𝚪: angular representation or rotation matrix
    :type 𝚪: array_like(3) or ndarray(3,3)
    :param representation: defaults to 'rpy/xyz'
    :type representation: str, optional
    :param inverse: compute mapping from analytical rates to angular velocity
    :type inverse: bool
    :param full: return 6x6 transform for spatial velocity
    :type full: bool
    :return: rotation rate transformation matrix
    :rtype: ndarray(3,3) or ndarray(6,6)

    Computes the transformation from analytical rates
    :math:`\dvec{x}` where the rotational part is expressed as the rate of change in
    some angular representation to spatial velocity :math:`\omega`, where
    rotation rate is expressed as angular velocity.

    .. math::
         \vec{\omega} = \mat{A}(\Gamma) \dvec{x}

    where :math:`\mat{A}` is a 3x3 matrix and :math:`\Gamma \in
    \mathbb{R}^3` is a minimal angular representation.

    :math:`\mat{A}(\Gamma)` is a function of the rotational representation
    which can be specified by the parameter ``𝚪`` as a 1D array, or by
    an SO(3) rotation matrix which will be converted to the ``representation``.

    ============================  ========================================
    ``representation``            Rotational representation
    ============================  ========================================
    ``"rpy/xyz"`` ``"arm"``       RPY angular rates in XYZ order (default)
    ``"rpy/zyx"`` ``"vehicle"``   RPY angular rates in XYZ order
    ``"rpy/yxz"`` ``"camera"``    RPY angular rates in YXZ order
    ``"eul"``                     Euler angular rates in ZYZ order
    ``"exp"``                     exponential coordinate rates
    ============================  ========================================

    If ``inverse==True`` return :math:`\mat{A}^{-1}` computed using
    a closed-form solution rather than matrix inverse.

    If ``full=True`` a block diagonal 6x6 matrix is returned which transforms analytic
    velocity to spatial velocity.

    .. note:: Similar to :func:`eul2jac` :func:`rpy2jac` :func:`exp2jac`
        with ``full=False``.

    The analytical Jacobian is

    .. math::

        \mat{J}_a(q) = \mat{A}^{-1}(\Gamma)\, \mat{J}(q)

    where :math:`\mat{A}` is computed with ``inverse==True`` and ``full=True``.

    Reference:

       - ``symbolic/angvelxform.ipynb`` in this Toolbox
       - Robot Dynamics Lecture Notes, Robotic Systems Lab, ETH Zurich, 2018
         https://ethz.ch/content/dam/ethz/special-interest/mavt/robotics-n-intelligent-systems/rsl-dam/documents/RobotDynamics2018/RD_HS2018script.pdf

    :SymPy: supported

    :seealso: :func:`rotvelxform` :func:`eul2jac` :func:`rpy2r` :func:`exp2jac`
    """

    if smb.isrot(𝚪):
        # passed a rotation matrix
        # convert to the representation
        𝚪 = r2x(𝚪, representation=representation)

    if sym.issymbol(𝚪):
        C = sym.cos
        S = sym.sin
        T = sym.tan
    else:
        C = math.cos
        S = math.sin
        T = math.tan

    if representation in ("rpy/xyz", "arm"):
        alpha, beta, gamma = 𝚪
        # autogenerated by symbolic/angvelxform.ipynb
        if not inverse:
            # analytical rates -> angular velocity
            # fmt: off
            A = np.array([
                [ S(beta),          0,        1], 
                [-S(gamma)*C(beta), C(gamma), 0], 
                [ C(beta)*C(gamma), S(gamma), 0]
                ])
            # fmt: on
        else:
            # angular velocity -> analytical rates
            # fmt: off
            A = np.array([
                [0, -S(gamma)/C(beta),  C(gamma)/C(beta)], 
                [0,  C(gamma),          S(gamma)], 
                [1,  S(gamma)*T(beta), -C(gamma)*T(beta)]
                ])
            # fmt: on

    elif representation in ("rpy/zyx", "vehicle"):
        alpha, beta, gamma = 𝚪
        # autogenerated by symbolic/angvelxform.ipynb
        if not inverse:
            # analytical rates -> angular velocity
            # fmt: off
            A = np.array([
                [C(beta)*C(gamma), -S(gamma), 0], 
                [S(gamma)*C(beta),  C(gamma), 0], 
                [-S(beta),          0,        1]
                ])
            # fmt: on
        else:
            # angular velocity -> analytical rates
            # fmt: off
            A = np.array([
                [C(gamma)/C(beta), S(gamma)/C(beta), 0],
                [-S(gamma),        C(gamma),         0],
                [C(gamma)*T(beta), S(gamma)*T(beta), 1]
                ])
            # fmt: on

    elif representation in ("rpy/yxz", "camera"):
        alpha, beta, gamma = 𝚪
        # autogenerated by symbolic/angvelxform.ipynb
        if not inverse:
            # analytical rates -> angular velocity
            # fmt: off
            A = np.array([
                [ S(gamma)*C(beta),  C(gamma), 0],
                [-S(beta),           0,        1],
                [ C(beta)*C(gamma), -S(gamma), 0]
            ])
            # fmt: on
        else:
            # angular velocity -> analytical rates
            # fmt: off
            A = np.array([
                [S(gamma)/C(beta), 0,  C(gamma)/C(beta)], 
                [C(gamma),         0, -S(gamma)],
                [S(gamma)*T(beta), 1,  C(gamma)*T(beta)]
                ])
            # fmt: on

    elif representation == "eul":
        phi, theta, psi = 𝚪
        # autogenerated by symbolic/angvelxform.ipynb
        if not inverse:
            # analytical rates -> angular velocity
            # fmt: off
            A = np.array([
                [0, -S(phi), S(theta)*C(phi)], 
                [0,  C(phi), S(phi)*S(theta)], 
                [1,  0,      C(theta)]
                ])
            # fmt: on
        else:
            # angular velocity -> analytical rates
            # fmt: off
            A = np.array([
                [-C(phi)/T(theta), -S(phi)/T(theta),  1], 
                [-S(phi),           C(phi),           0], 
                [ C(phi)/S(theta),  S(phi)/S(theta),  0]
                ])
            # fmt: on

    elif representation == "exp":
        # from ETHZ class notes
        sk = smb.skew(𝚪)
        theta = smb.norm(𝚪)
        if not inverse:
            # analytical rates -> angular velocity
            # (2.106)
            A = (
                np.eye(3)
                + sk * (1 - C(theta)) / theta**2
                + sk @ sk * (theta - S(theta)) / theta**3
            )
        else:
            # angular velocity -> analytical rates
            # (2.107)
            A = (
                np.eye(3)
                - sk / 2
                + sk @ sk / theta**2 * (1 - (theta / 2) * (S(theta) / (1 - C(theta))))
            )

    if full:
        return sp.linalg.block_diag(np.eye(3, 3), A)
    else:
        return A


def rotvelxform_inv_dot(𝚪, 𝚪d, full=False, representation="rpy/xyz"):
    r"""
    Derivative of angular velocity transformation

    :param 𝚪: angular representation
    :type 𝚪: ndarray(3)
    :param 𝚪d: angular representation rate
    :type 𝚪d: ndarray(3)
    :param representation: defaults to 'rpy/xyz'
    :type representation: str, optional
    :param full: return 6x6 transform for spatial velocity
    :type full: bool
    :return: derivative of inverse angular velocity transformation matrix
    :rtype: ndarray(6,6) or ndarray(3,3)

    The angular rate transformation matrix :math:`\mat{A} \in \mathbb{R}^{6 \times 6}` is such that

    .. math::

        \dvec{x} = \mat{A}^{-1}(\Gamma) \vec{\nu}

    where :math:`\dvec{x} \in \mathbb{R}^6` is analytic velocity :math:`(\vec{v}, \dvec{\Gamma})`,
    :math:`\vec{\nu} \in \mathbb{R}^6` is spatial velocity :math:`(\vec{v}, \vec{\omega})`, and
    :math:`\vec{\Gamma} \in \mathbb{R}^3` is a minimal rotational
    representation.

    The relationship between spatial and analytic acceleration is

    .. math::

        \ddvec{x} = \dmat{A}^{-1}(\Gamma, \dot{\Gamma) \vec{\nu} + \mat{A}^{-1}(\Gamma) \dvec{\nu}

    and :math:`\dmat{A}^{-1}(\Gamma, \dot{\Gamma)` is computed by this function.


    ============================  ========================================
    ``representation``            Rotational representation
    ============================  ========================================
    ``"rpy/xyz"`` ``"arm"``      RPY angular rates in XYZ order (default)
    ``"rpy/zyx"`` ``"vehicle"``  RPY angular rates in XYZ order
    ``"rpy/yxz"`` ``"camera"``   RPY angular rates in YXZ order
    ``"eul"``                     Euler angular rates in ZYZ order
    ``"exp"``                     exponential coordinate rates
    ============================  ========================================

    If ``full=True`` a block diagonal 6x6 matrix is returned which transforms analytic
    analytic rotational acceleration to angular acceleration.

    Reference:

       - ``symbolic/angvelxform.ipynb`` in this Toolbox
       - ``symbolic/angvelxform_dot.ipynb`` in this Toolbox

    :seealso: :func:`rotvelxform` :func:`eul2jac` :func:`rpy2r` :func:`exp2jac`
    """

    if sym.issymbol(𝚪):
        C = sym.cos
        S = sym.sin
    else:
        C = math.cos
        S = math.sin

    if representation in ("rpy/xyz", "arm"):
        # autogenerated by symbolic/angvelxform.ipynb
        alpha, beta, gamma = 𝚪
        alpha_dot, beta_dot, gamma_dot = 𝚪d

        Ainv_dot = np.array(
            [
                [
                    0,
                    -(
                        beta_dot * math.sin(beta) * S(gamma) / C(beta)
                        + gamma_dot * C(gamma)
                    )
                    / C(beta),
                    (beta_dot * S(beta) * C(gamma) / C(beta) - gamma_dot * S(gamma))
                    / C(beta),
                ],
                [0, -gamma_dot * S(gamma), gamma_dot * C(gamma)],
                [
                    0,
                    beta_dot * S(gamma) / C(beta) ** 2
                    + gamma_dot * C(gamma) * math.tan(beta),
                    -beta_dot * C(gamma) / C(beta) ** 2
                    + gamma_dot * S(gamma) * math.tan(beta),
                ],
            ]
        )

    elif representation in ("rpy/zyx", "vehicle"):
        # autogenerated by symbolic/angvelxform.ipynb
        alpha, beta, gamma = 𝚪
        alpha_dot, beta_dot, gamma_dot = 𝚪d

        Ainv_dot = np.array(
            [
                [
                    (beta_dot * S(beta) * C(gamma) / C(beta) - gamma_dot * S(gamma))
                    / C(beta),
                    (beta_dot * S(beta) * S(gamma) / C(beta) + gamma_dot * C(gamma))
                    / C(beta),
                    0,
                ],
                [-gamma_dot * C(gamma), -gamma_dot * S(gamma), 0],
                [
                    beta_dot * C(gamma) / C(beta) ** 2
                    - gamma_dot * S(gamma) * math.tan(beta),
                    beta_dot * S(gamma) / C(beta) ** 2
                    + gamma_dot * C(gamma) * math.tan(beta),
                    0,
                ],
            ]
        )

    elif representation in ("rpy/yxz", "camera"):
        # autogenerated by symbolic/angvelxform.ipynb
        alpha, beta, gamma = 𝚪
        alpha_dot, beta_dot, gamma_dot = 𝚪d

        Ainv_dot = np.array(
            [
                [
                    (beta_dot * S(beta) * S(gamma) / C(beta) + gamma_dot * C(gamma))
                    / C(beta),
                    0,
                    (beta_dot * S(beta) * C(gamma) / C(beta) - gamma_dot * S(gamma))
                    / C(beta),
                ],
                [-gamma_dot * S(gamma), 0, -gamma_dot * C(gamma)],
                [
                    beta_dot * S(gamma) / C(beta) ** 2 + gamma_dot * C(gamma) * T(beta),
                    0,
                    beta_dot * C(gamma) / C(beta) ** 2 - gamma_dot * S(gamma) * T(beta),
                ],
            ]
        )

    elif representation == "eul":
        # autogenerated by symbolic/angvelxform.ipynb
        phi, theta, psi = 𝚪
        phi_dot, theta_dot, psi_dot = 𝚪d

        Ainv_dot = np.array(
            [
                [
                    phi_dot * S(phi) / math.tan(theta)
                    + theta_dot * C(phi) / S(theta) ** 2,
                    -phi_dot * C(phi) / math.tan(theta)
                    + theta_dot * S(phi) / S(theta) ** 2,
                    0,
                ],
                [-phi_dot * C(phi), -phi_dot * S(phi), 0],
                [
                    -(phi_dot * S(phi) + theta_dot * C(phi) * C(theta) / S(theta))
                    / S(theta),
                    (phi_dot * C(phi) - theta_dot * S(phi) * C(theta) / S(theta))
                    / S(theta),
                    0,
                ],
            ]
        )

    elif representation == "exp":
        # autogenerated by symbolic/angvelxform_dot.ipynb
        v = 𝚪
        vd = 𝚪d
        sk = smb.skew(v)
        skd = smb.skew(vd)
        theta_dot = np.inner(𝚪, 𝚪d) / smb.norm(𝚪)
        theta = smb.norm(𝚪)
        Theta = (1.0 - theta / 2.0 * np.sin(theta) / (1.0 - np.cos(theta))) / theta**2

        # hand optimized version of code from notebook
        # TODO:
        #   results are close but different to numerical cross check
        #   something wrong in the derivation
        Theta_dot = (
            -theta * C(theta) - S(theta) + theta * S(theta) ** 2 / (1 - C(theta))
        ) * theta_dot / 2 / (1 - C(theta)) / theta**2 - (
            2 - theta * S(theta) / (1 - C(theta))
        ) * theta_dot / theta**3

        Ainv_dot = -0.5 * skd + 2.0 * sk @ skd * Theta + sk @ sk * Theta_dot
    else:
        raise ValueError("bad representation specified")

    if full:
        return sp.linalg.block_diag(np.eye(3, 3), Ainv_dot)
    else:
        return Ainv_dot


def tr2adjoint(T):
    r"""
    Adjoint matrix

    :param T: SO(3) or SE(3) matrix
    :type T: ndarray(3,3) or ndarray(4,4)
    :return: adjoint matrix
    :rtype: ndarray(6,6)

    Computes an adjoint matrix that maps spatial velocity between two frames defined by
    an SE(3) matrix.

    ``tr2jac(T)`` is an adjoint matrix (6x6) that maps spatial velocity or
    differential motion between frame {B} to frame {A} which are attached to the
    same moving body.  The pose of {B} relative to {A} is represented by the
    homogeneous transform T = :math:`{}^A {\bf T}_B`.

    .. runblock:: pycon

        >>> from spatialmath.smb import *
        >>> T = trotx(0.3, t=[4,5,6])
        >>> tr2adjoint(T)

    :Reference:
        - Robotics, Vision & Control: Second Edition, P. Corke, Springer 2016; p65.
        - `Lie groups for 2D and 3D Transformations <http://ethaneade.com/lie.pdf>_

    :SymPy: supported
    """

    Z = np.zeros((3, 3), dtype=T.dtype)
    if T.shape == (3, 3):
        # SO(3) adjoint
        R = T
        # fmt: off
        return np.block([
                    [R, Z],
                    [Z, R]
                ])
        # fmt: on
    elif T.shape == (4, 4):
        # SE(3) adjoint
        (R, t) = smb.tr2rt(T)
        # fmt: off
        return np.block([
                    [R, smb.skew(t) @ R], 
                    [Z, R]
                ])
        # fmt: on
    else:
        raise ValueError("bad argument")


def trprint(
    T,
    orient="rpy/zyx",
    label=None,
    file=sys.stdout,
    fmt="{:.3g}",
    degsym=True,
    unit="deg",
):
    """
     Compact display of SO(3) or SE(3) matrices

     :param T: SE(3) or SO(3) matrix
     :type T: ndarray(4,4) or ndarray(3,3)
     :param label: text label to put at start of line
     :type label: str
     :param orient: 3-angle convention to use
     :type orient: str
     :param file: file to write formatted string to. [default, stdout]
     :type file: file object
     :param fmt: conversion format for each number in the format used with ``format``
     :type fmt: str
     :param unit: angular units: 'rad' [default], or 'deg'
     :type unit: str
     :return: formatted string
     :rtype: str
     :raises ValueError: bad argument

     The matrix is formatted and written to ``file`` and the
     string is returned.  To suppress writing to a file, set ``file=None``.

    - ``trprint(R)`` prints the SO(3) rotation matrix to stdout in a compact
       single-line format:

         [LABEL:] ORIENTATION UNIT

     - ``trprint(T)`` prints the SE(3) homogoneous transform to stdout in a
       compact single-line format:

         [LABEL:] [t=X, Y, Z;] ORIENTATION UNIT

     - ``trprint(X, file=None)`` as above but returns the string rather than
       printing to a file

     Orientation is expressed in one of several formats:

     - 'rpy/zyx' roll-pitch-yaw angles in ZYX axis order [default]
     - 'rpy/yxz' roll-pitch-yaw angles in YXZ axis order
     - 'rpy/zyx' roll-pitch-yaw angles in ZYX axis order
     - 'eul' Euler angles in ZYZ axis order
     - 'angvec' angle and axis


     .. runblock:: pycon

         >>> from spatialmath.smb import transl, rpy2tr, trprint
         >>> T = transl(1,2,3) @ rpy2tr(10, 20, 30, 'deg')
         >>> trprint(T, file=None)
         >>> trprint(T, file=None, label='T', orient='angvec')
         >>> trprint(T, file=None, label='T', orient='angvec', fmt='{:8.4g}')

     .. notes::

         - If the 'rpy' option is selected, then the particular angle sequence can be
           specified with the options 'xyz' or 'yxz' which are passed through to ``tr2rpy``.
           'zyx' is the default.
         - Default formatting is for compact display of data
         - For tabular data set ``fmt`` to a fixed width format such as
           ``fmt='{:.3g}'``

     :seealso: :func:`~spatialmath.smb.transforms2d.trprint2` :func:`~tr2eul` :func:`~tr2rpy` :func:`~tr2angvec`
     :SymPy: not supported
    """

    s = ""

    if label is not None:
        s += "{:s}: ".format(label)

    # print the translational part if it exists
    if ishom(T):
        s += "t = {};".format(_vec2s(fmt, transl(T)))

    # print the angular part in various representations

    # define some aliases for rpy conventions for arms, vehicles and cameras
    aliases = {"arm": "rpy/xyz", "vehicle": "rpy/zyx", "camera": "rpy/yxz"}
    if orient in aliases:
        orient = aliases[orient]

    a = orient.split("/")
    if a[0] == "rpy":
        if len(a) == 2:
            seq = a[1]
        else:
            seq = None
        angles = tr2rpy(T, order=seq, unit=unit)
        if degsym and unit == "deg":
            fmt += "\u00b0"
        s += " {} = {}".format(orient, _vec2s(fmt, angles))

    elif a[0].startswith("eul"):
        angles = tr2eul(T, unit)
        if degsym and unit == "deg":
            fmt += "\u00b0"
        s += " eul = {}".format(_vec2s(fmt, angles))

    elif a[0] == "angvec":
        # as a vector and angle
        (theta, v) = tr2angvec(T, unit)
        if theta == 0:
            s += " R = nil"
        else:
            theta = fmt.format(theta)
            if degsym and unit == "deg":
                theta += "\u00b0"
            s += " angvec = ({} | {})".format(theta, _vec2s(fmt, v))
    else:
        raise ValueError("bad orientation format")

    if file:
        print(s, file=file)

    return s


def _vec2s(fmt, v):
    v = [x if np.abs(x) > 1e-6 else 0.0 for x in v]
    return ", ".join([fmt.format(x) for x in v])


def trplot(
    T,
    color="blue",
    frame=None,
    axislabel=True,
    axissubscript=True,
    textcolor=None,
    labels=("X", "Y", "Z"),
    length=1,
    style="arrow",
    originsize=20,
    origincolor=None,
    projection="ortho",
    block=False,
    anaglyph=None,
    wtl=0.2,
    width=None,
    ax=None,
    dims=None,
    d2=1.15,
    flo=(-0.05, -0.05, -0.05),
    **kwargs,
):
    """
    Plot a 3D coordinate frame

    :param T: SE(3) or SO(3) matrix
    :type T: ndarray(4,4) or ndarray(3,3) or an iterable returning same

    :param color: color of the lines defining the frame
    :type color: str or list(3) of str
    :param textcolor: color of text labels for the frame, default ``color``
    :type textcolor: str
    :param frame: label the frame, name is shown below the frame and as subscripts on the frame axis labels
    :type frame: str
    :param axislabel: display labels on axes, default True
    :type axislabel: bool
    :param axissubscript: display subscripts on axis labels, default True
    :type axissubscript: bool
    :param labels: labels for the axes, defaults to X, Y and Z
    :type labels: 3-tuple of strings
    :param length: length of coordinate frame axes, default 1
    :type length: float or array_like(3)
    :param style: axis style: 'arrow' [default], 'line', 'rviz' (Rviz style)
    :type style: str
    :param originsize: size of dot to draw at the origin, 0 for no dot (default 20)
    :type originsize: int
    :param origincolor: color of dot to draw at the origin, default is ``color``
    :type origincolor: str
    :param ax: the axes to plot into, defaults to current axes
    :type ax: Axes3D reference
    :param block: run the GUI main loop until all windows are closed, default True
    :type block: bool
    :param dims: dimension of plot volume as [xmin, xmax, ymin, ymax,zmin, zmax].
        If dims is [min, max] those limits are applied to the x-, y- and z-axes.
    :type dims: array_like(6) or array_like(2)
    :param anaglyph: 3D anaglyph display, left-right lens colors eg. ``'rc'``
    for red-cyan glasses.  To set the disparity (default 0.1) provide second
    argument in a tuple, eg. ``('rc', 0.2)``.  Bigger disparity exagerates the
    3D "pop out" effect.
    :type anaglyph: str or (str, float)
    :param wtl: width-to-length ratio for arrows, default 0.2
    :type wtl: float
    :param projection: 3D projection: ortho [default] or persp
    :type projection: str
    :param width: width of lines, default 1
    :type width: float
    :param flo: frame label offset, a vector for frame label text string relative
        to frame origin, default (-0.05, -0.05, -0.05)
    :type flo: array_like(3)
    :param d2: distance of frame axis label text from origin, default 1.15
    :type d2: float
    :return: axes containing the frame
    :rtype: Axes3DSubplot
    :raises ValueError: bad arguments

    Adds a 3D coordinate frame represented by the SO(3) or SE(3) matrix to the
    current axes. If ``T`` is iterable then multiple frames will be drawn.

    The appearance of the coordinate frame depends on many parameters:

    - coordinate axes depend on:
        - ``color`` of axes
        - ``width`` of line
        - ``length`` of line
        - ``style`` which is one of:
            - ``'arrow'`` [default], draw line with arrow head in ``color``
            - ``'line'``, draw line with no arrow head in ``color``
            - ``'rviz'``, draw line with no arrow head with color depending upon
              axis, red for X, green for Y, blue for Z
    - coordinate axis labels depend on:
        - ``axislabel`` if True [default] label the axis, default labels are X, Y, Z
        - ``labels`` 3-list of alternative axis labels
        - ``textcolor`` which defaults to ``color``
        - ``axissubscript`` if True [default] add the frame label ``frame`` as a subscript
          for each axis label
    - coordinate frame label depends on:
        - `frame` the label placed inside {} near the origin of the frame
    - a dot at the origin
        - ``originsize`` size of the dot, if zero no dot
        - ``origincolor`` color of the dot, defaults to ``color``

    Examples:

            trplot(T, frame='A')
            trplot(T, frame='A', color='green')
            trplot(T1, 'labels', 'UVW');

    .. note:: If ``axes`` is specified the plot is drawn there, otherwise:
        - it will draw in the current figure (as given by ``gca()``)
        - if no axes in the current figure, it will create a 3D axes
        - if no current figure, it will create one, and a 3D axes

    .. note:: The ``'rgb'`` style is a variant of the ``'line'`` style and
        is somewhat RViz like.  The axes are colored red, green, blue; are
        drawn thick (width=8) and have no arrows.

    .. note:: The ``anaglyph`` effect is induced by drawing two versions of the
        frame in different colors: one that corresponds to lens over the left
        eye and one to the lens over the right eye. The view for the right eye
        is from a view point shifted in the positive x-direction.

    .. note:: The origin is normally indicated with a marker of the same color
        as the frame.  The default size is 20. This can be disabled by setting
        its size to zero by ``originsize=0``.  For ``'rgb'`` style the default is 0
        but it can be set explicitly, and the color is as per the ``color``
        option.

    :SymPy: not supported

    :seealso: :func:`tranimate` :func:`plotvol3` :func:`axes_logic`
    """

    # TODO
    # animation
    # anaglyph

    if dims is None:
        ax = smb.axes_logic(ax, 3, projection)
    else:
        ax = smb.plotvol3(dims, ax=ax)

    try:
        if not ax.get_xlabel():
            ax.set_xlabel(labels[0])
        if not ax.get_ylabel():
            ax.set_ylabel(labels[1])
        if not ax.get_zlabel():
            ax.set_zlabel(labels[2])
    except AttributeError:
        pass  # if axes are an Animate object

    if anaglyph is not None:
        # enforce perspective projection
        ax.set_proj_type("persp")

        # collect all the arguments to use for left and right views
        args = {
            "ax": ax,
            "frame": frame,
            "length": length,
            "style": style,
            "wtl": wtl,
            "flo": flo,
            "d2": d2,
        }
        args = {**args, **kwargs}

        # unpack the anaglyph parameters
        if anaglyph is True:
            colors = "rc"
            shift = 0.1
        elif isinstance(anaglyph, tuple):
            colors = anaglyph[0]
            shift = anaglyph[1]
        else:
            colors = anaglyph
            shift = 0.1

        # the left eye sees the normal trplot
        trplot(T, color=colors[0], **args)

        # the right eye sees a from a viewpoint in shifted in the X direction
        if smb.isrot(T):
            T = smb.r2t(T)
        trplot(transl(shift, 0, 0) @ T, color=colors[1], **args)

        return

    if style == "rviz":
        if originsize is None:
            originsize = 0
        color = "rgb"
        if width is None:
            width = 8
        style = "line"

    if isinstance(color, str):
        if color == "rgb":
            color = ("red", "green", "blue")
        else:
            color = (color,) * 3

    # check input types
    if isrot(T, check=True):
        T = smb.r2t(T)
    elif ishom(T, check=True):
        pass
    else:
        # assume it is an iterable
        for Tk in T:
            trplot(
                Tk,
                ax=ax,
                block=block,
                dims=dims,
                color=color,
                frame=frame,
                textcolor=textcolor,
                labels=labels,
                length=length,
                style=style,
                projection=projection,
                originsize=originsize,
                origincolor=origincolor,
                wtl=wtl,
                width=width,
                d2=d2,
                flo=flo,
                anaglyph=anaglyph,
                axislabel=axislabel,
                **kwargs,
            )
        return

    if dims is not None:
        if len(dims) == 2:
            dims = dims * 3
        ax.set_xlim(dims[0:2])
        ax.set_ylim(dims[2:4])
        ax.set_zlim(dims[4:6])

    # create unit vectors in homogeneous form
    if not isinstance(length, Iterable):
        length = (length,) * 3

    o = T @ np.array([0, 0, 0, 1])
    x = T @ np.array([length[0], 0, 0, 1])
    y = T @ np.array([0, length[1], 0, 1])
    z = T @ np.array([0, 0, length[2], 1])

    # draw the axes

    if style == "arrow":
        ax.quiver(
            o[0],
            o[1],
            o[2],
            x[0] - o[0],
            x[1] - o[1],
            x[2] - o[2],
            arrow_length_ratio=wtl,
            linewidth=width,
            facecolor=color[0],
            edgecolor=color[1],
        )
        ax.quiver(
            o[0],
            o[1],
            o[2],
            y[0] - o[0],
            y[1] - o[1],
            y[2] - o[2],
            arrow_length_ratio=wtl,
            linewidth=width,
            facecolor=color[1],
            edgecolor=color[1],
        )
        ax.quiver(
            o[0],
            o[1],
            o[2],
            z[0] - o[0],
            z[1] - o[1],
            z[2] - o[2],
            arrow_length_ratio=wtl,
            linewidth=width,
            facecolor=color[2],
            edgecolor=color[2],
        )

        # plot some points
        #  invisible point at the end of each arrow to allow auto-scaling to work
        ax.scatter(
            xs=[o[0], x[0], y[0], z[0]],
            ys=[o[1], x[1], y[1], z[1]],
            zs=[o[2], x[2], y[2], z[2]],
            s=[0, 0, 0, 0],
        )
    elif style == "line":
        ax.plot(
            [o[0], x[0]], [o[1], x[1]], [o[2], x[2]], color=color[0], linewidth=width
        )
        ax.plot(
            [o[0], y[0]], [o[1], y[1]], [o[2], y[2]], color=color[1], linewidth=width
        )
        ax.plot(
            [o[0], z[0]], [o[1], z[1]], [o[2], z[2]], color=color[2], linewidth=width
        )

    if textcolor is None:
        textcolor = color[0]
    else:
        textcolor = "blue"
    if origincolor is None:
        origincolor = color[0]
    else:
        origincolor = "black"

    # label the frame
    if frame:
        if textcolor is None:
            textcolor = color[0]
        else:
            textcolor = "blue"
        if origincolor is None:
            origincolor = color[0]
        else:
            origincolor = "black"

        o1 = T @ np.array(np.r_[flo, 1])
        ax.text(
            o1[0],
            o1[1],
            o1[2],
            r"$\{" + frame + r"\}$",
            color=textcolor,
            verticalalignment="top",
            horizontalalignment="center",
        )

    if axislabel:
        # add the labels to each axis

        x = (x - o) * d2 + o
        y = (y - o) * d2 + o
        z = (z - o) * d2 + o

        if frame is None or not axissubscript:
            format = "${:s}$"
        else:
            format = "${:s}_{{{:s}}}$"

        ax.text(
            x[0],
            x[1],
            x[2],
            format.format(labels[0], frame),
            color=textcolor,
            horizontalalignment="center",
            verticalalignment="center",
        )
        ax.text(
            y[0],
            y[1],
            y[2],
            format.format(labels[1], frame),
            color=textcolor,
            horizontalalignment="center",
            verticalalignment="center",
        )
        ax.text(
            z[0],
            z[1],
            z[2],
            format.format(labels[2], frame),
            color=textcolor,
            horizontalalignment="center",
            verticalalignment="center",
        )

    if originsize > 0:
        ax.scatter(xs=[o[0]], ys=[o[1]], zs=[o[2]], color=origincolor, s=originsize)

    if block:
        # calling this at all, causes FuncAnimation to fail so when invoked from tranimate skip this bit
        import matplotlib.pyplot as plt

        # TODO move blocking into graphics
        plt.show(block=block)
    return ax


def tranimate(T, **kwargs):
    """
    Animate a 3D coordinate frame

    :param T: SE(3) or SO(3) matrix
    :type T: ndarray(4,4) or ndarray(3,3) or an iterable returning same
    :param nframes: number of steps in the animation [default 100]
    :type nframes: int
    :param repeat: animate in endless loop [default False]
    :type repeat: bool
    :param interval: number of milliseconds between frames [default 50]
    :type interval: int
    :param wait: wait until animation is complete, default False
    :type wait: bool
    :param movie: name of file to write MP4 movie into
    :type movie: str
    :param **kwargs: arguments passed to ``trplot``

    - ``tranimate(T)`` where ``T`` is an SO(3) or SE(3) matrix, animates a 3D
      coordinate frame moving from the world frame to the frame ``T`` in
      ``nsteps``.

    - ``tranimate(I)`` where ``I`` is an iterable or generator, animates a 3D
      coordinate frame representing the pose of each element in the sequence of
      SO(3) or SE(3) matrices.

    Examples:

            >>> tranimate(transl(1,2,3)@trotx(1), frame='A', arrow=False, dims=[0, 5])
            >>> tranimate(transl(1,2,3)@trotx(1), frame='A', arrow=False, dims=[0, 5], movie='spin.mp4')

    .. note:: For Jupyter this works with the ``notebook`` and ``TkAgg``
        backends.

    .. note:: The animation occurs in the background after ``tranimate`` has
        returned. If ``block=True`` this blocks after the animation has completed.

    .. note:: When saving animation to a file the animation does not appear
        on screen.  A ``StopIteration`` exception may occur, this seems to
        be a matplotlib bug #19599

    :SymPy: not supported

    :seealso: `trplot`, `plotvol3`
    """

    kwargs["block"] = kwargs.get("block", False)

    anim = smb.animate.Animate(**kwargs)
    try:
        del kwargs["dims"]
    except KeyError:
        pass

    anim.trplot(T, **kwargs)
    anim.run(**kwargs)

    # plt.show(block=block)


if __name__ == "__main__":  # pragma: no cover

    # import sympy
    # from spatialmath.base.symbolic import *

    # p, q, r = symbol('phi theta psi')
    # print(p)

    # print(angvelxform([p, q, r], representation='eul'))

    import pathlib

    exec(
        open(
            pathlib.Path(__file__).parent.parent.parent.absolute()
            / "tests"
            / "smb"
            / "test_transforms3d.py"
        ).read()
    )  # pylint: disable=exec-used

    exec(
        open(
            pathlib.Path(__file__).parent.parent.parent.absolute()
            / "tests"
            / "smb"
            / "test_transforms3d_plot.py"
        ).read()
    )  # pylint: disable=exec-used
