"""
This module provides access to math operations.

[NOTE]
Classes, methods and attributes that accept vectors also accept other numeric sequences,
such as tuples, lists.

Submodules:

mathutils.geometry.rst
mathutils.bvhtree.rst
mathutils.kdtree.rst
mathutils.interpolate.rst
mathutils.noise.rst

:maxdepth: 1

The mathutils module provides the following classes:

* Color,
* Euler,
* Matrix,
* Quaternion,
* Vector,

```../examples/mathutils.py```

"""

import typing
import collections.abc
import typing_extensions
from . import bvhtree as bvhtree
from . import geometry as geometry
from . import interpolate as interpolate
from . import kdtree as kdtree
from . import noise as noise

class Color:
    """This object gives access to Colors in Blender."""

    b: float
    """ Blue color channel.

    :type: float
    """

    g: float
    """ Green color channel.

    :type: float
    """

    h: float
    """ HSV Hue component in [0, 1].

    :type: float
    """

    hsv: Vector | collections.abc.Sequence[float]
    """ HSV Values in [0, 1].

    :type: Vector | collections.abc.Sequence[float]
    """

    is_frozen: bool
    """ True when this object has been frozen (read-only).

    :type: bool
    """

    is_wrapped: bool
    """ True when this object wraps external data (read-only).

    :type: bool
    """

    owner: typing.Any
    """ The item this is wrapping or None  (read-only)."""

    r: float
    """ Red color channel.

    :type: float
    """

    s: float
    """ HSV Saturation component in [0, 1].

    :type: float
    """

    v: float
    """ HSV Value component in [0, 1].

    :type: float
    """

    def copy(self) -> typing_extensions.Self:
        """Returns a copy of this color.

        :return: A copy of the color.
        :rtype: typing_extensions.Self
        """

    def freeze(self) -> typing_extensions.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing_extensions.Self
        """

    def __init__(self, rgb=(0.0, 0.0, 0.0)):
        """

        :param rgb:
        """

    def __get__(self, instance, owner) -> typing_extensions.Self:
        """

        :param instance:
        :param owner:
        :return:
        :rtype: typing_extensions.Self
        """

    def __set__(
        self, instance, value: collections.abc.Sequence[float] | typing_extensions.Self
    ):
        """

        :param instance:
        :param value:
        :type value: collections.abc.Sequence[float] | typing_extensions.Self
        """

    def __add__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __sub__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __mul__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    def __truediv__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    def __radd__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __rsub__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __rmul__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    def __rtruediv__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    def __iadd__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __isub__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __imul__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    def __itruediv__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    @typing.overload
    def __getitem__(self, key: int) -> float:
        """

        :param key:
        :type key: int
        :return:
        :rtype: float
        """

    @typing.overload
    def __getitem__(self, key: slice) -> tuple[float, ...]:
        """

        :param key:
        :type key: slice
        :return:
        :rtype: tuple[float, ...]
        """

    @typing.overload
    def __setitem__(self, key: int, value: float):
        """

        :param key:
        :type key: int
        :param value:
        :type value: float
        """

    @typing.overload
    def __setitem__(self, key: slice, value: collections.abc.Iterable[float]):
        """

        :param key:
        :type key: slice
        :param value:
        :type value: collections.abc.Iterable[float]
        """

class Euler:
    """This object gives access to Eulers in Blender.`Euler angles <https://en.wikipedia.org/wiki/Euler_angles>`__ on Wikipedia."""

    is_frozen: bool
    """ True when this object has been frozen (read-only).

    :type: bool
    """

    is_wrapped: bool
    """ True when this object wraps external data (read-only).

    :type: bool
    """

    order: typing.Any
    """ Euler rotation order."""

    owner: typing.Any
    """ The item this is wrapping or None  (read-only)."""

    x: float
    """ Euler axis angle in radians.

    :type: float
    """

    y: float
    """ Euler axis angle in radians.

    :type: float
    """

    z: float
    """ Euler axis angle in radians.

    :type: float
    """

    def copy(self) -> typing_extensions.Self:
        """Returns a copy of this euler.

        :return: A copy of the euler.
        :rtype: typing_extensions.Self
        """

    def freeze(self) -> typing_extensions.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing_extensions.Self
        """

    def make_compatible(self, other):
        """Make this euler compatible with another,
        so interpolating between them works as intended.

                :param other:
        """

    def rotate(
        self,
        other: Matrix
        | Quaternion
        | collections.abc.Sequence[collections.abc.Sequence[float]]
        | collections.abc.Sequence[float]
        | typing_extensions.Self,
    ):
        """Rotates the euler by another mathutils value.

        :param other: rotation component of mathutils value
        :type other: Matrix | Quaternion | collections.abc.Sequence[collections.abc.Sequence[float]] | collections.abc.Sequence[float] | typing_extensions.Self
        """

    def rotate_axis(self, axis: str, angle: float):
        """Rotates the euler a certain amount and returning a unique euler rotation
        (no 720 degree pitches).

                :param axis: single character in ['X, 'Y', 'Z'].
                :type axis: str
                :param angle: angle in radians.
                :type angle: float
        """

    def to_matrix(self) -> Matrix:
        """Return a matrix representation of the euler.

        :return: A 3x3 rotation matrix representation of the euler.
        :rtype: Matrix
        """

    def to_quaternion(self) -> Quaternion:
        """Return a quaternion representation of the euler.

        :return: Quaternion representation of the euler.
        :rtype: Quaternion
        """

    def zero(self):
        """Set all values to zero."""

    def __init__(self, angles=(0.0, 0.0, 0.0), order="XYZ"):
        """

        :param angles:
        :param order:
        """

    def __get__(self, instance, owner) -> typing_extensions.Self:
        """

        :param instance:
        :param owner:
        :return:
        :rtype: typing_extensions.Self
        """

    def __set__(
        self, instance, value: collections.abc.Sequence[float] | typing_extensions.Self
    ):
        """

        :param instance:
        :param value:
        :type value: collections.abc.Sequence[float] | typing_extensions.Self
        """

    @typing.overload
    def __getitem__(self, key: int) -> float:
        """

        :param key:
        :type key: int
        :return:
        :rtype: float
        """

    @typing.overload
    def __getitem__(self, key: slice) -> tuple[float, ...]:
        """

        :param key:
        :type key: slice
        :return:
        :rtype: tuple[float, ...]
        """

    @typing.overload
    def __setitem__(self, key: int, value: float):
        """

        :param key:
        :type key: int
        :param value:
        :type value: float
        """

    @typing.overload
    def __setitem__(self, key: slice, value: collections.abc.Iterable[float]):
        """

        :param key:
        :type key: slice
        :param value:
        :type value: collections.abc.Iterable[float]
        """

class Matrix:
    """This object gives access to Matrices in Blender, supporting square and rectangular
    matrices from 2x2 up to 4x4.
    """

    col: typing.Any
    """ Access the matrix by columns, 3x3 and 4x4 only, (read-only)."""

    is_frozen: bool
    """ True when this object has been frozen (read-only).

    :type: bool
    """

    is_negative: bool
    """ True if this matrix results in a negative scale, 3x3 and 4x4 only, (read-only).

    :type: bool
    """

    is_orthogonal: bool
    """ True if this matrix is orthogonal, 3x3 and 4x4 only, (read-only).

    :type: bool
    """

    is_orthogonal_axis_vectors: bool
    """ True if this matrix has got orthogonal axis vectors, 3x3 and 4x4 only, (read-only).

    :type: bool
    """

    is_wrapped: bool
    """ True when this object wraps external data (read-only).

    :type: bool
    """

    median_scale: float
    """ The average scale applied to each axis (read-only).

    :type: float
    """

    owner: typing.Any
    """ The item this is wrapping or None  (read-only)."""

    row: typing.Any
    """ Access the matrix by rows (default), (read-only)."""

    translation: Vector
    """ The translation component of the matrix.

    :type: Vector
    """

    @classmethod
    def Diagonal(
        cls, vector: Vector | collections.abc.Sequence[float]
    ) -> typing_extensions.Self:
        """Create a diagonal (scaling) matrix using the values from the vector.

        :param vector: The vector of values for the diagonal.
        :type vector: Vector | collections.abc.Sequence[float]
        :return: A diagonal matrix.
        :rtype: typing_extensions.Self
        """

    @classmethod
    def Identity(cls, size: int) -> typing_extensions.Self:
        """Create an identity matrix.

        :param size: The size of the identity matrix to construct [2, 4].
        :type size: int
        :return: A new identity matrix.
        :rtype: typing_extensions.Self
        """

    @classmethod
    def OrthoProjection(
        cls, axis: Vector | collections.abc.Sequence[float] | str, size: int
    ) -> typing_extensions.Self:
        """Create a matrix to represent an orthographic projection.

                :param axis: Can be any of the following: ['X', 'Y', 'XY', 'XZ', 'YZ'],
        where a single axis is for a 2D matrix.
        Or a vector for an arbitrary axis
                :type axis: Vector | collections.abc.Sequence[float] | str
                :param size: The size of the projection matrix to construct [2, 4].
                :type size: int
                :return: A new projection matrix.
                :rtype: typing_extensions.Self
        """

    @classmethod
    def Rotation(
        cls,
        angle: float,
        size: int,
        axis: Vector | collections.abc.Sequence[float] | str | None = "",
    ) -> typing_extensions.Self:
        """Create a matrix representing a rotation.

                :param angle: The angle of rotation desired, in radians.
                :type angle: float
                :param size: The size of the rotation matrix to construct [2, 4].
                :type size: int
                :param axis: a string in ['X', 'Y', 'Z'] or a 3D Vector Object
        (optional when size is 2).
                :type axis: Vector | collections.abc.Sequence[float] | str | None
                :return: A new rotation matrix.
                :rtype: typing_extensions.Self
        """

    @classmethod
    def Scale(
        cls,
        factor: float,
        size: int,
        axis: Vector | collections.abc.Sequence[float] | None = [],
    ) -> typing_extensions.Self:
        """Create a matrix representing a scaling.

        :param factor: The factor of scaling to apply.
        :type factor: float
        :param size: The size of the scale matrix to construct [2, 4].
        :type size: int
        :param axis: Direction to influence scale. (optional).
        :type axis: Vector | collections.abc.Sequence[float] | None
        :return: A new scale matrix.
        :rtype: typing_extensions.Self
        """

    @classmethod
    def Shear(cls, plane: str, size: int, factor: float) -> typing_extensions.Self:
        """Create a matrix to represent an shear transformation.

                :param plane: Can be any of the following: ['X', 'Y', 'XY', 'XZ', 'YZ'],
        where a single axis is for a 2D matrix only.
                :type plane: str
                :param size: The size of the shear matrix to construct [2, 4].
                :type size: int
                :param factor: The factor of shear to apply. For a 3 or 4 size matrix
        pass a pair of floats corresponding with the plane axis.
                :type factor: float
                :return: A new shear matrix.
                :rtype: typing_extensions.Self
        """

    @classmethod
    def Translation(
        cls, vector: Vector | collections.abc.Sequence[float]
    ) -> typing_extensions.Self:
        """Create a matrix representing a translation.

        :param vector: The translation vector.
        :type vector: Vector | collections.abc.Sequence[float]
        :return: An identity matrix with a translation.
        :rtype: typing_extensions.Self
        """

    def adjugate(self):
        """Set the matrix to its adjugate.`Adjugate matrix <https://en.wikipedia.org/wiki/Adjugate_matrix>` on Wikipedia."""

    def adjugated(self) -> typing_extensions.Self:
        """Return an adjugated copy of the matrix.

        :return: the adjugated matrix.
        :rtype: typing_extensions.Self
        """

    def copy(self) -> typing_extensions.Self:
        """Returns a copy of this matrix.

        :return: an instance of itself
        :rtype: typing_extensions.Self
        """

    def decompose(self) -> tuple[Vector, Quaternion, Vector]:
        """Return the translation, rotation, and scale components of this matrix.

        :return: tuple of translation, rotation, and scale
        :rtype: tuple[Vector, Quaternion, Vector]
        """

    def determinant(self) -> float:
        """Return the determinant of a matrix.`Determinant <https://en.wikipedia.org/wiki/Determinant>` on Wikipedia.

        :return: Return the determinant of a matrix.
        :rtype: float
        """

    def freeze(self) -> typing_extensions.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing_extensions.Self
        """

    def identity(self):
        """Set the matrix to the identity matrix.`Identity matrix <https://en.wikipedia.org/wiki/Identity_matrix>` on Wikipedia."""

    def invert(
        self,
        fallback: collections.abc.Sequence[collections.abc.Sequence[float]]
        | typing_extensions.Self
        | None = None,
    ):
        """Set the matrix to its inverse.`Inverse matrix <https://en.wikipedia.org/wiki/Inverse_matrix>` on Wikipedia.

                :param fallback: Set the matrix to this value when the inverse cannot be calculated
        (instead of raising a `ValueError` exception).
                :type fallback: collections.abc.Sequence[collections.abc.Sequence[float]] | typing_extensions.Self | None
        """

    def invert_safe(self):
        """Set the matrix to its inverse, will never error.
        If degenerated (e.g. zero scale on an axis), add some epsilon to its diagonal, to get an invertible one.
        If tweaked matrix is still degenerated, set to the identity matrix instead.`Inverse Matrix <https://en.wikipedia.org/wiki/Inverse_matrix>` on Wikipedia.

        """

    def inverted(self, fallback: typing.Any | None = None) -> typing_extensions.Self:
        """Return an inverted copy of the matrix.

                :param fallback: return this when the inverse can't be calculated
        (instead of raising a `ValueError`).
                :type fallback: typing.Any | None
                :return: the inverted matrix or fallback when given.
                :rtype: typing_extensions.Self
        """

    def inverted_safe(self) -> typing_extensions.Self:
        """Return an inverted copy of the matrix, will never error.
        If degenerated (e.g. zero scale on an axis), add some epsilon to its diagonal, to get an invertible one.
        If tweaked matrix is still degenerated, return the identity matrix instead.

                :return: the inverted matrix.
                :rtype: typing_extensions.Self
        """

    def lerp(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]]
        | typing_extensions.Self,
        factor: float,
    ) -> typing_extensions.Self:
        """Returns the interpolation of two matrices. Uses polar decomposition, see   "Matrix Animation and Polar Decomposition", Shoemake and Duff, 1992.

        :param other: value to interpolate with.
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing_extensions.Self
        :param factor: The interpolation value in [0.0, 1.0].
        :type factor: float
        :return: The interpolated matrix.
        :rtype: typing_extensions.Self
        """

    def normalize(self):
        """Normalize each of the matrix columns."""

    def normalized(self) -> typing_extensions.Self:
        """Return a column normalized matrix

        :return: a column normalized matrix
        :rtype: typing_extensions.Self
        """

    def resize_4x4(self):
        """Resize the matrix to 4x4."""

    def rotate(
        self,
        other: Euler
        | Quaternion
        | collections.abc.Sequence[collections.abc.Sequence[float]]
        | collections.abc.Sequence[float]
        | typing_extensions.Self,
    ):
        """Rotates the matrix by another mathutils value.

        :param other: rotation component of mathutils value
        :type other: Euler | Quaternion | collections.abc.Sequence[collections.abc.Sequence[float]] | collections.abc.Sequence[float] | typing_extensions.Self
        """

    def to_3x3(self) -> typing_extensions.Self:
        """Return a 3x3 copy of this matrix.

        :return: a new matrix.
        :rtype: typing_extensions.Self
        """

    def to_4x4(self) -> typing_extensions.Self:
        """Return a 4x4 copy of this matrix.

        :return: a new matrix.
        :rtype: typing_extensions.Self
        """

    def to_euler(
        self,
        order: str | None = "",
        euler_compat: Euler | collections.abc.Sequence[float] | None = [],
    ) -> Euler:
        """Return an Euler representation of the rotation matrix
        (3x3 or 4x4 matrix only).

                :param order: Optional rotation order argument in
        ['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'].
                :type order: str | None
                :param euler_compat: Optional euler argument the new euler will be made
        compatible with (no axis flipping between them).
        Useful for converting a series of matrices to animation curves.
                :type euler_compat: Euler | collections.abc.Sequence[float] | None
                :return: Euler representation of the matrix.
                :rtype: Euler
        """

    def to_quaternion(self) -> Quaternion:
        """Return a quaternion representation of the rotation matrix.

        :return: Quaternion representation of the rotation matrix.
        :rtype: Quaternion
        """

    def to_scale(self) -> Vector:
        """Return the scale part of a 3x3 or 4x4 matrix.

        :return: Return the scale of a matrix.
        :rtype: Vector
        """

    def to_translation(self) -> Vector:
        """Return the translation part of a 4 row matrix.

        :return: Return the translation of a matrix.
        :rtype: Vector
        """

    def transpose(self):
        """Set the matrix to its transpose.`Transpose <https://en.wikipedia.org/wiki/Transpose>` on Wikipedia."""

    def transposed(self) -> typing_extensions.Self:
        """Return a new, transposed matrix.

        :return: a transposed matrix
        :rtype: typing_extensions.Self
        """

    def zero(self) -> typing_extensions.Self:
        """Set all the matrix values to zero.

        :return:
        :rtype: typing_extensions.Self
        """

    def __init__(
        self,
        rows=(
            (1.0, 0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0, 0.0),
            (0.0, 0.0, 0.0, 1.0),
        ),
    ):
        """

        :param rows:
        """

    def __get__(self, instance, owner) -> typing_extensions.Self:
        """

        :param instance:
        :param owner:
        :return:
        :rtype: typing_extensions.Self
        """

    def __set__(
        self,
        instance,
        value: collections.abc.Sequence[collections.abc.Sequence[float]]
        | typing_extensions.Self,
    ):
        """

        :param instance:
        :param value:
        :type value: collections.abc.Sequence[collections.abc.Sequence[float]] | typing_extensions.Self
        """

    @typing.overload
    def __getitem__(self, key: int) -> Vector:
        """

        :param key:
        :type key: int
        :return:
        :rtype: Vector
        """

    @typing.overload
    def __getitem__(self, key: slice) -> tuple[Vector, ...]:
        """

        :param key:
        :type key: slice
        :return:
        :rtype: tuple[Vector, ...]
        """

    @typing.overload
    def __setitem__(self, key: int, value: Vector | collections.abc.Iterable[float]):
        """

        :param key:
        :type key: int
        :param value:
        :type value: Vector | collections.abc.Iterable[float]
        """

    @typing.overload
    def __setitem__(
        self,
        key: slice,
        value: collections.abc.Iterable[Vector | collections.abc.Iterable[float]],
    ):
        """

        :param key:
        :type key: slice
        :param value:
        :type value: collections.abc.Iterable[Vector | collections.abc.Iterable[float]]
        """

    def __len__(self) -> int:
        """

        :return:
        :rtype: int
        """

    def __add__(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]]
        | typing_extensions.Self,
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __sub__(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]]
        | typing_extensions.Self,
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __mul__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    @typing.overload
    def __matmul__(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]]
        | typing_extensions.Self,
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    @typing.overload
    def __matmul__(self, other: Vector | collections.abc.Sequence[float]) -> Vector:
        """

        :param other:
        :type other: Vector | collections.abc.Sequence[float]
        :return:
        :rtype: Vector
        """

    def __radd__(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]]
        | typing_extensions.Self,
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __rsub__(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]]
        | typing_extensions.Self,
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __rmul__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    def __imul__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

class Quaternion:
    """This object gives access to Quaternions in Blender.The constructor takes arguments in various forms:"""

    angle: float
    """ Angle of the quaternion.

    :type: float
    """

    axis: Vector
    """ Quaternion axis as a vector.

    :type: Vector
    """

    is_frozen: bool
    """ True when this object has been frozen (read-only).

    :type: bool
    """

    is_wrapped: bool
    """ True when this object wraps external data (read-only).

    :type: bool
    """

    magnitude: float
    """ Size of the quaternion (read-only).

    :type: float
    """

    owner: typing.Any
    """ The item this is wrapping or None  (read-only)."""

    w: float
    """ Quaternion axis value.

    :type: float
    """

    x: float
    """ Quaternion axis value.

    :type: float
    """

    y: float
    """ Quaternion axis value.

    :type: float
    """

    z: float
    """ Quaternion axis value.

    :type: float
    """

    def conjugate(self):
        """Set the quaternion to its conjugate (negate x, y, z)."""

    def conjugated(self) -> typing_extensions.Self:
        """Return a new conjugated quaternion.

        :return: a new quaternion.
        :rtype: typing_extensions.Self
        """

    def copy(self) -> typing_extensions.Self:
        """Returns a copy of this quaternion.

        :return: A copy of the quaternion.
        :rtype: typing_extensions.Self
        """

    def cross(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """Return the cross product of this quaternion and another.

        :param other: The other quaternion to perform the cross product with.
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return: The cross product.
        :rtype: typing_extensions.Self
        """

    def dot(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> float:
        """Return the dot product of this quaternion and another.

        :param other: The other quaternion to perform the dot product with.
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return: The dot product.
        :rtype: float
        """

    def freeze(self) -> typing_extensions.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing_extensions.Self
        """

    def identity(self) -> typing_extensions.Self:
        """Set the quaternion to an identity quaternion.

        :return:
        :rtype: typing_extensions.Self
        """

    def invert(self):
        """Set the quaternion to its inverse."""

    def inverted(self) -> typing_extensions.Self:
        """Return a new, inverted quaternion.

        :return: the inverted value.
        :rtype: typing_extensions.Self
        """

    def negate(self) -> typing_extensions.Self:
        """Set the quaternion to its negative.

        :return:
        :rtype: typing_extensions.Self
        """

    def normalize(self):
        """Normalize the quaternion."""

    def normalized(self) -> typing_extensions.Self:
        """Return a new normalized quaternion.

        :return: a normalized copy.
        :rtype: typing_extensions.Self
        """

    def rotate(
        self,
        other: Euler
        | Matrix
        | collections.abc.Sequence[collections.abc.Sequence[float]]
        | collections.abc.Sequence[float]
        | typing_extensions.Self,
    ):
        """Rotates the quaternion by another mathutils value.

        :param other: rotation component of mathutils value
        :type other: Euler | Matrix | collections.abc.Sequence[collections.abc.Sequence[float]] | collections.abc.Sequence[float] | typing_extensions.Self
        """

    def rotation_difference(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """Returns a quaternion representing the rotational difference.

        :param other: second quaternion.
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return: the rotational difference between the two quat rotations.
        :rtype: typing_extensions.Self
        """

    def slerp(
        self,
        other: collections.abc.Sequence[float] | typing_extensions.Self,
        factor: float,
    ) -> typing_extensions.Self:
        """Returns the interpolation of two quaternions.

        :param other: value to interpolate with.
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :param factor: The interpolation value in [0.0, 1.0].
        :type factor: float
        :return: The interpolated rotation.
        :rtype: typing_extensions.Self
        """

    def to_axis_angle(self) -> tuple[Vector, float]:
        """Return the axis, angle representation of the quaternion.

        :return: axis, angle.
        :rtype: tuple[Vector, float]
        """

    def to_euler(
        self,
        order: str | None = "",
        euler_compat: Euler | collections.abc.Sequence[float] | None = [],
    ) -> Euler:
        """Return Euler representation of the quaternion.

                :param order: Optional rotation order argument in
        ['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'].
                :type order: str | None
                :param euler_compat: Optional euler argument the new euler will be made
        compatible with (no axis flipping between them).
        Useful for converting a series of matrices to animation curves.
                :type euler_compat: Euler | collections.abc.Sequence[float] | None
                :return: Euler representation of the quaternion.
                :rtype: Euler
        """

    def to_exponential_map(self):
        """Return the exponential map representation of the quaternion.This representation consist of the rotation axis multiplied by the rotation angle.   Such a representation is useful for interpolation between multiple orientations.To convert back to a quaternion, pass it to the `Quaternion` constructor.

        :return: exponential map.
        """

    def to_matrix(self) -> Matrix:
        """Return a matrix representation of the quaternion.

        :return: A 3x3 rotation matrix representation of the quaternion.
        :rtype: Matrix
        """

    def __init__(self, seq=(1.0, 0.0, 0.0, 0.0)):
        """

        :param seq:
        """

    def __get__(self, instance, owner) -> typing_extensions.Self:
        """

        :param instance:
        :param owner:
        :return:
        :rtype: typing_extensions.Self
        """

    def __set__(
        self, instance, value: collections.abc.Sequence[float] | typing_extensions.Self
    ):
        """

        :param instance:
        :param value:
        :type value: collections.abc.Sequence[float] | typing_extensions.Self
        """

    def __len__(self) -> int:
        """

        :return:
        :rtype: int
        """

    @typing.overload
    def __getitem__(self, key: int) -> float:
        """

        :param key:
        :type key: int
        :return:
        :rtype: float
        """

    @typing.overload
    def __getitem__(self, key: slice) -> tuple[float, ...]:
        """

        :param key:
        :type key: slice
        :return:
        :rtype: tuple[float, ...]
        """

    @typing.overload
    def __setitem__(self, key: int, value: float):
        """

        :param key:
        :type key: int
        :param value:
        :type value: float
        """

    @typing.overload
    def __setitem__(self, key: slice, value: collections.abc.Iterable[float]):
        """

        :param key:
        :type key: slice
        :param value:
        :type value: collections.abc.Iterable[float]
        """

    def __add__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __sub__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __mul__(
        self, other: collections.abc.Sequence[float] | float | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | float | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    @typing.overload
    def __matmul__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    @typing.overload
    def __matmul__(self, other: Vector | collections.abc.Sequence[float]) -> Vector:
        """

        :param other:
        :type other: Vector | collections.abc.Sequence[float]
        :return:
        :rtype: Vector
        """

    def __radd__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __rsub__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __rmul__(
        self, other: collections.abc.Sequence[float] | float | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | float | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __imul__(
        self, other: collections.abc.Sequence[float] | float | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | float | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

class Vector:
    """This object gives access to Vectors in Blender."""

    is_frozen: bool
    """ True when this object has been frozen (read-only).

    :type: bool
    """

    is_wrapped: bool
    """ True when this object wraps external data (read-only).

    :type: bool
    """

    length: float
    """ Vector Length.

    :type: float
    """

    length_squared: float
    """ Vector length squared (v.dot(v)).

    :type: float
    """

    magnitude: float
    """ Vector Length.

    :type: float
    """

    owner: typing.Any
    """ The item this is wrapping or None  (read-only)."""

    w: float
    """ Vector W axis (4D Vectors only).

    :type: float
    """

    ww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    www: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wwzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wxzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wywx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wywy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wywz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wyzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    wzzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    x: float
    """ Vector X axis.

    :type: float
    """

    xw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xwzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xxzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xywx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xywy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xywz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xyzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    xzzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    y: float
    """ Vector Y axis.

    :type: float
    """

    yw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    ywzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yxzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yywx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yywy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yywz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yyzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    yzzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    z: float
    """ Vector Z axis (3D Vectors only).

    :type: float
    """

    zw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zwzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zxzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zywx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zywy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zywz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zyzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzww: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzwx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzwy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzwz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzxw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzxx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzxy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzxz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzyw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzyx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzyy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzyz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzzw: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzzx: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzzy: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    zzzz: typing.Any
    """ Undocumented contribute <https://developer.blender.org/T51061>"""

    @classmethod
    def Fill(cls, size: int, fill: float = 0.0):
        """Create a vector of length size with all values set to fill.

        :param size: The length of the vector to be created.
        :type size: int
        :param fill: The value used to fill the vector.
        :type fill: float
        """

    @classmethod
    def Linspace(cls, start: int, stop: int, size: int):
        """Create a vector of the specified size which is filled with linearly spaced values between start and stop values.

        :param start: The start of the range used to fill the vector.
        :type start: int
        :param stop: The end of the range used to fill the vector.
        :type stop: int
        :param size: The size of the vector to be created.
        :type size: int
        """

    @classmethod
    def Range(cls, start: int = 0, stop: int = -1, step: int = 1):
        """Create a filled with a range of values.

        :param start: The start of the range used to fill the vector.
        :type start: int
        :param stop: The end of the range used to fill the vector.
        :type stop: int
        :param step: The step between successive values in the vector.
        :type step: int
        """

    @classmethod
    def Repeat(cls, vector, size: int):
        """Create a vector by repeating the values in vector until the required size is reached.

        :param vector:
        :param size: The size of the vector to be created.
        :type size: int
        """

    def angle(
        self,
        other: collections.abc.Sequence[float] | typing_extensions.Self,
        fallback: typing.Any | None = None,
    ) -> float:
        """Return the angle between two vectors.

                :param other: another vector to compare the angle with
                :type other: collections.abc.Sequence[float] | typing_extensions.Self
                :param fallback: return this when the angle can't be calculated (zero length vector),
        (instead of raising a `ValueError`).
                :type fallback: typing.Any | None
                :return: angle in radians or fallback when given
                :rtype: float
        """

    def angle_signed(
        self,
        other: collections.abc.Sequence[float] | typing_extensions.Self,
        fallback: typing.Any,
    ) -> float:
        """Return the signed angle between two 2D vectors (clockwise is positive).

                :param other: another vector to compare the angle with
                :type other: collections.abc.Sequence[float] | typing_extensions.Self
                :param fallback: return this when the angle can't be calculated (zero length vector),
        (instead of raising a `ValueError`).
                :type fallback: typing.Any
                :return: angle in radians or fallback when given
                :rtype: float
        """

    def copy(self) -> typing_extensions.Self:
        """Returns a copy of this vector.

        :return: A copy of the vector.
        :rtype: typing_extensions.Self
        """

    def cross(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """Return the cross product of this vector and another.

        :param other: The other vector to perform the cross product with.
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return: The cross product.
        :rtype: typing_extensions.Self
        """

    def dot(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """Return the dot product of this vector and another.

        :param other: The other vector to perform the dot product with.
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return: The dot product.
        :rtype: typing_extensions.Self
        """

    def freeze(self) -> typing_extensions.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing_extensions.Self
        """

    def lerp(
        self,
        other: collections.abc.Sequence[float] | typing_extensions.Self,
        factor: float,
    ) -> typing_extensions.Self:
        """Returns the interpolation of two vectors.

        :param other: value to interpolate with.
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :param factor: The interpolation value in [0.0, 1.0].
        :type factor: float
        :return: The interpolated vector.
        :rtype: typing_extensions.Self
        """

    def negate(self):
        """Set all values to their negative."""

    def normalize(self):
        """Normalize the vector, making the length of the vector always 1.0."""

    def normalized(self) -> typing_extensions.Self:
        """Return a new, normalized vector.

        :return: a normalized copy of the vector
        :rtype: typing_extensions.Self
        """

    def orthogonal(self) -> typing_extensions.Self:
        """Return a perpendicular vector.

        :return: a new vector 90 degrees from this vector.
        :rtype: typing_extensions.Self
        """

    def project(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """Return the projection of this vector onto the other.

        :param other: second vector.
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return: the parallel projection vector
        :rtype: typing_extensions.Self
        """

    def reflect(
        self, mirror: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """Return the reflection vector from the mirror argument.

        :param mirror: This vector could be a normal from the reflecting surface.
        :type mirror: collections.abc.Sequence[float] | typing_extensions.Self
        :return: The reflected vector matching the size of this vector.
        :rtype: typing_extensions.Self
        """

    def resize(self, size=3):
        """Resize the vector to have size number of elements.

        :param size:
        """

    def resize_2d(self):
        """Resize the vector to 2D  (x, y)."""

    def resize_3d(self):
        """Resize the vector to 3D  (x, y, z)."""

    def resize_4d(self):
        """Resize the vector to 4D (x, y, z, w)."""

    def resized(self, size=3) -> typing_extensions.Self:
        """Return a resized copy of the vector with size number of elements.

        :param size:
        :return: a new vector
        :rtype: typing_extensions.Self
        """

    def rotate(
        self,
        other: Euler
        | Matrix
        | Quaternion
        | collections.abc.Sequence[collections.abc.Sequence[float]]
        | collections.abc.Sequence[float],
    ):
        """Rotate the vector by a rotation value.

        :param other: rotation component of mathutils value
        :type other: Euler | Matrix | Quaternion | collections.abc.Sequence[collections.abc.Sequence[float]] | collections.abc.Sequence[float]
        """

    def rotation_difference(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> Quaternion:
        """Returns a quaternion representing the rotational difference between this
        vector and another.

                :param other: second vector.
                :type other: collections.abc.Sequence[float] | typing_extensions.Self
                :return: the rotational difference between the two vectors.
                :rtype: Quaternion
        """

    def slerp(
        self,
        other: collections.abc.Sequence[float] | typing_extensions.Self,
        factor: float,
        fallback: typing.Any | None = None,
    ) -> typing_extensions.Self:
        """Returns the interpolation of two non-zero vectors (spherical coordinates).

                :param other: value to interpolate with.
                :type other: collections.abc.Sequence[float] | typing_extensions.Self
                :param factor: The interpolation value typically in [0.0, 1.0].
                :type factor: float
                :param fallback: return this when the vector can't be calculated (zero length vector or direct opposites),
        (instead of raising a `ValueError`).
                :type fallback: typing.Any | None
                :return: The interpolated vector.
                :rtype: typing_extensions.Self
        """

    def to_2d(self) -> typing_extensions.Self:
        """Return a 2d copy of the vector.

        :return: a new vector
        :rtype: typing_extensions.Self
        """

    def to_3d(self) -> typing_extensions.Self:
        """Return a 3d copy of the vector.

        :return: a new vector
        :rtype: typing_extensions.Self
        """

    def to_4d(self) -> typing_extensions.Self:
        """Return a 4d copy of the vector.

        :return: a new vector
        :rtype: typing_extensions.Self
        """

    def to_track_quat(self, track: str, up: str) -> Quaternion:
        """Return a quaternion rotation from the vector and the track and up axis.

        :param track: Track axis in ['X', 'Y', 'Z', '-X', '-Y', '-Z'].
        :type track: str
        :param up: Up axis in ['X', 'Y', 'Z'].
        :type up: str
        :return: rotation from the vector and the track and up axis.
        :rtype: Quaternion
        """

    def to_tuple(self, precision: int = -1) -> tuple:
        """Return this vector as a tuple with.

        :param precision: The number to round the value to in [-1, 21].
        :type precision: int
        :return: the values of the vector rounded by precision
        :rtype: tuple
        """

    def zero(self):
        """Set all values to zero."""

    def __init__(self, seq=(0.0, 0.0, 0.0)):
        """

        :param seq:
        """

    def __get__(self, instance, owner) -> typing_extensions.Self:
        """

        :param instance:
        :param owner:
        :return:
        :rtype: typing_extensions.Self
        """

    def __set__(
        self, instance, value: collections.abc.Sequence[float] | typing_extensions.Self
    ):
        """

        :param instance:
        :param value:
        :type value: collections.abc.Sequence[float] | typing_extensions.Self
        """

    def __len__(self) -> int:
        """

        :return:
        :rtype: int
        """

    @typing.overload
    def __getitem__(self, key: int) -> float:
        """

        :param key:
        :type key: int
        :return:
        :rtype: float
        """

    @typing.overload
    def __getitem__(self, key: slice) -> tuple[float, ...]:
        """

        :param key:
        :type key: slice
        :return:
        :rtype: tuple[float, ...]
        """

    @typing.overload
    def __setitem__(self, key: int, value: float):
        """

        :param key:
        :type key: int
        :param value:
        :type value: float
        """

    @typing.overload
    def __setitem__(self, key: slice, value: collections.abc.Iterable[float]):
        """

        :param key:
        :type key: slice
        :param value:
        :type value: collections.abc.Iterable[float]
        """

    def __neg__(self) -> typing_extensions.Self:
        """

        :return:
        :rtype: typing_extensions.Self
        """

    def __add__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __sub__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    @typing.overload
    def __mul__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    @typing.overload
    def __mul__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __truediv__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    @typing.overload
    def __matmul__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> float:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: float
        """

    @typing.overload
    def __matmul__(
        self, other: Matrix | collections.abc.Sequence[collections.abc.Sequence[float]]
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: Matrix | collections.abc.Sequence[collections.abc.Sequence[float]]
        :return:
        :rtype: typing_extensions.Self
        """

    def __radd__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __rsub__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __rmul__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    def __rtruediv__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    def __iadd__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __isub__(
        self, other: collections.abc.Sequence[float] | typing_extensions.Self
    ) -> typing_extensions.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return:
        :rtype: typing_extensions.Self
        """

    def __imul__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """

    def __itruediv__(self, other: float) -> typing_extensions.Self:
        """

        :param other:
        :type other: float
        :return:
        :rtype: typing_extensions.Self
        """
