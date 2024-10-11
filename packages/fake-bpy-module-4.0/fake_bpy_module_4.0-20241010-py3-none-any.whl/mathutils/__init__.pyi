"""
This module provides access to math operations.

[NOTE]
Classes, methods and attributes that accept vectors also accept other numeric sequences,
such as tuples, lists.

The mathutils module provides the following classes:

* Color,
* Euler,
* Matrix,
* Quaternion,
* Vector,

mathutils.geometry.rst
mathutils.bvhtree.rst
mathutils.kdtree.rst
mathutils.interpolate.rst
mathutils.noise.rst

:maxdepth: 1
:caption: Submodules

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
    """This object gives access to Colors in Blender.Most colors returned by Blender APIs are in scene linear color space, as defined by    the OpenColorIO configuration. The notable exception is user interface theming colors,    which are in sRGB color space."""

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

    is_valid: bool
    """ True when the owner of this data is valid.

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

    def from_aces_to_scene_linear(self) -> typing_extensions.Self:
        """Convert from ACES2065-1 linear to scene linear color space.

        :return: A color in scene linear color space.
        :rtype: typing_extensions.Self
        """

    def from_rec709_linear_to_scene_linear(self) -> typing_extensions.Self:
        """Convert from Rec.709 linear color space to scene linear color space.

        :return: A color in scene linear color space.
        :rtype: typing_extensions.Self
        """

    def from_scene_linear_to_aces(self) -> typing_extensions.Self:
        """Convert from scene linear to ACES2065-1 linear color space.

        :return: A color in ACES2065-1 linear color space.
        :rtype: typing_extensions.Self
        """

    def from_scene_linear_to_rec709_linear(self) -> typing_extensions.Self:
        """Convert from scene linear to Rec.709 linear color space.

        :return: A color in Rec.709 linear color space.
        :rtype: typing_extensions.Self
        """

    def from_scene_linear_to_srgb(self) -> typing_extensions.Self:
        """Convert from scene linear to sRGB color space.

        :return: A color in sRGB color space.
        :rtype: typing_extensions.Self
        """

    def from_scene_linear_to_xyz_d65(self) -> typing_extensions.Self:
        """Convert from scene linear to CIE XYZ (Illuminant D65) color space.

        :return: A color in XYZ color space.
        :rtype: typing_extensions.Self
        """

    def from_srgb_to_scene_linear(self) -> typing_extensions.Self:
        """Convert from sRGB to scene linear color space.

        :return: A color in scene linear color space.
        :rtype: typing_extensions.Self
        """

    def from_xyz_d65_to_scene_linear(self) -> typing_extensions.Self:
        """Convert from CIE XYZ (Illuminant D65) to scene linear color space.

        :return: A color in scene linear color space.
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

    is_valid: bool
    """ True when the owner of this data is valid.

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

    is_identity: bool
    """ True if this is an identity matrix (read-only).

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

    is_valid: bool
    """ True when the owner of this data is valid.

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
    def LocRotScale(
        cls,
        location: Vector | collections.abc.Sequence[float] | None,
        rotation: Euler | Quaternion | collections.abc.Sequence[float] | None,
        scale: Vector | collections.abc.Sequence[float] | None,
    ) -> typing_extensions.Self:
        """Create a matrix combining translation, rotation and scale,
        acting as the inverse of the decompose() method.Any of the inputs may be replaced with None if not needed.

                :param location: The translation component.
                :type location: Vector | collections.abc.Sequence[float] | None
                :param rotation: The rotation component.
                :type rotation: Euler | Quaternion | collections.abc.Sequence[float] | None
                :param scale: The scale component.
                :type scale: Vector | collections.abc.Sequence[float] | None
                :return: Combined transformation matrix.
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
        """Set the matrix to its adjugate.`Adjugate matrix <https://en.wikipedia.org/wiki/Adjugate_matrix>`__ on Wikipedia."""

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
        """Return the determinant of a matrix.`Determinant <https://en.wikipedia.org/wiki/Determinant>`__ on Wikipedia.

        :return: Return the determinant of a matrix.
        :rtype: float
        """

    def freeze(self) -> typing_extensions.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing_extensions.Self
        """

    def identity(self):
        """Set the matrix to the identity matrix.`Identity matrix <https://en.wikipedia.org/wiki/Identity_matrix>`__ on Wikipedia."""

    def invert(
        self,
        fallback: collections.abc.Sequence[collections.abc.Sequence[float]]
        | typing_extensions.Self
        | None = None,
    ):
        """Set the matrix to its inverse.`Inverse matrix <https://en.wikipedia.org/wiki/Inverse_matrix>`__ on Wikipedia.

                :param fallback: Set the matrix to this value when the inverse cannot be calculated
        (instead of raising a `ValueError` exception).
                :type fallback: collections.abc.Sequence[collections.abc.Sequence[float]] | typing_extensions.Self | None
        """

    def invert_safe(self):
        """Set the matrix to its inverse, will never error.
        If degenerated (e.g. zero scale on an axis), add some epsilon to its diagonal, to get an invertible one.
        If tweaked matrix is still degenerated, set to the identity matrix instead.`Inverse Matrix <https://en.wikipedia.org/wiki/Inverse_matrix>`__ on Wikipedia.

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

    def to_2x2(self) -> typing_extensions.Self:
        """Return a 2x2 copy of this matrix.

        :return: a new matrix.
        :rtype: typing_extensions.Self
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
        """Set the matrix to its transpose.`Transpose <https://en.wikipedia.org/wiki/Transpose>`__ on Wikipedia."""

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

    is_valid: bool
    """ True when the owner of this data is valid.

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

    def make_compatible(self, other):
        """Make this quaternion compatible with another,
        so interpolating between them works as intended.

                :param other:
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
        """Return the exponential map representation of the quaternion.This representation consist of the rotation axis multiplied by the rotation angle.
        Such a representation is useful for interpolation between multiple orientations.To convert back to a quaternion, pass it to the `Quaternion` constructor.

                :return: exponential map.
        """

    def to_matrix(self) -> Matrix:
        """Return a matrix representation of the quaternion.

        :return: A 3x3 rotation matrix representation of the quaternion.
        :rtype: Matrix
        """

    def to_swing_twist(self, axis) -> tuple[Quaternion, float]:
        """Split the rotation into a swing quaternion with the specified
        axis fixed at zero, and the remaining twist rotation angle.

                :param axis: twist axis as a string in ['X', 'Y', 'Z']
                :return: swing, twist angle.
                :rtype: tuple[Quaternion, float]
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

    is_valid: bool
    """ True when the owner of this data is valid.

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
    """ Undocumented, consider contributing."""

    www: typing.Any
    """ Undocumented, consider contributing."""

    wwww: typing.Any
    """ Undocumented, consider contributing."""

    wwwx: typing.Any
    """ Undocumented, consider contributing."""

    wwwy: typing.Any
    """ Undocumented, consider contributing."""

    wwwz: typing.Any
    """ Undocumented, consider contributing."""

    wwx: typing.Any
    """ Undocumented, consider contributing."""

    wwxw: typing.Any
    """ Undocumented, consider contributing."""

    wwxx: typing.Any
    """ Undocumented, consider contributing."""

    wwxy: typing.Any
    """ Undocumented, consider contributing."""

    wwxz: typing.Any
    """ Undocumented, consider contributing."""

    wwy: typing.Any
    """ Undocumented, consider contributing."""

    wwyw: typing.Any
    """ Undocumented, consider contributing."""

    wwyx: typing.Any
    """ Undocumented, consider contributing."""

    wwyy: typing.Any
    """ Undocumented, consider contributing."""

    wwyz: typing.Any
    """ Undocumented, consider contributing."""

    wwz: typing.Any
    """ Undocumented, consider contributing."""

    wwzw: typing.Any
    """ Undocumented, consider contributing."""

    wwzx: typing.Any
    """ Undocumented, consider contributing."""

    wwzy: typing.Any
    """ Undocumented, consider contributing."""

    wwzz: typing.Any
    """ Undocumented, consider contributing."""

    wx: typing.Any
    """ Undocumented, consider contributing."""

    wxw: typing.Any
    """ Undocumented, consider contributing."""

    wxww: typing.Any
    """ Undocumented, consider contributing."""

    wxwx: typing.Any
    """ Undocumented, consider contributing."""

    wxwy: typing.Any
    """ Undocumented, consider contributing."""

    wxwz: typing.Any
    """ Undocumented, consider contributing."""

    wxx: typing.Any
    """ Undocumented, consider contributing."""

    wxxw: typing.Any
    """ Undocumented, consider contributing."""

    wxxx: typing.Any
    """ Undocumented, consider contributing."""

    wxxy: typing.Any
    """ Undocumented, consider contributing."""

    wxxz: typing.Any
    """ Undocumented, consider contributing."""

    wxy: typing.Any
    """ Undocumented, consider contributing."""

    wxyw: typing.Any
    """ Undocumented, consider contributing."""

    wxyx: typing.Any
    """ Undocumented, consider contributing."""

    wxyy: typing.Any
    """ Undocumented, consider contributing."""

    wxyz: typing.Any
    """ Undocumented, consider contributing."""

    wxz: typing.Any
    """ Undocumented, consider contributing."""

    wxzw: typing.Any
    """ Undocumented, consider contributing."""

    wxzx: typing.Any
    """ Undocumented, consider contributing."""

    wxzy: typing.Any
    """ Undocumented, consider contributing."""

    wxzz: typing.Any
    """ Undocumented, consider contributing."""

    wy: typing.Any
    """ Undocumented, consider contributing."""

    wyw: typing.Any
    """ Undocumented, consider contributing."""

    wyww: typing.Any
    """ Undocumented, consider contributing."""

    wywx: typing.Any
    """ Undocumented, consider contributing."""

    wywy: typing.Any
    """ Undocumented, consider contributing."""

    wywz: typing.Any
    """ Undocumented, consider contributing."""

    wyx: typing.Any
    """ Undocumented, consider contributing."""

    wyxw: typing.Any
    """ Undocumented, consider contributing."""

    wyxx: typing.Any
    """ Undocumented, consider contributing."""

    wyxy: typing.Any
    """ Undocumented, consider contributing."""

    wyxz: typing.Any
    """ Undocumented, consider contributing."""

    wyy: typing.Any
    """ Undocumented, consider contributing."""

    wyyw: typing.Any
    """ Undocumented, consider contributing."""

    wyyx: typing.Any
    """ Undocumented, consider contributing."""

    wyyy: typing.Any
    """ Undocumented, consider contributing."""

    wyyz: typing.Any
    """ Undocumented, consider contributing."""

    wyz: typing.Any
    """ Undocumented, consider contributing."""

    wyzw: typing.Any
    """ Undocumented, consider contributing."""

    wyzx: typing.Any
    """ Undocumented, consider contributing."""

    wyzy: typing.Any
    """ Undocumented, consider contributing."""

    wyzz: typing.Any
    """ Undocumented, consider contributing."""

    wz: typing.Any
    """ Undocumented, consider contributing."""

    wzw: typing.Any
    """ Undocumented, consider contributing."""

    wzww: typing.Any
    """ Undocumented, consider contributing."""

    wzwx: typing.Any
    """ Undocumented, consider contributing."""

    wzwy: typing.Any
    """ Undocumented, consider contributing."""

    wzwz: typing.Any
    """ Undocumented, consider contributing."""

    wzx: typing.Any
    """ Undocumented, consider contributing."""

    wzxw: typing.Any
    """ Undocumented, consider contributing."""

    wzxx: typing.Any
    """ Undocumented, consider contributing."""

    wzxy: typing.Any
    """ Undocumented, consider contributing."""

    wzxz: typing.Any
    """ Undocumented, consider contributing."""

    wzy: typing.Any
    """ Undocumented, consider contributing."""

    wzyw: typing.Any
    """ Undocumented, consider contributing."""

    wzyx: typing.Any
    """ Undocumented, consider contributing."""

    wzyy: typing.Any
    """ Undocumented, consider contributing."""

    wzyz: typing.Any
    """ Undocumented, consider contributing."""

    wzz: typing.Any
    """ Undocumented, consider contributing."""

    wzzw: typing.Any
    """ Undocumented, consider contributing."""

    wzzx: typing.Any
    """ Undocumented, consider contributing."""

    wzzy: typing.Any
    """ Undocumented, consider contributing."""

    wzzz: typing.Any
    """ Undocumented, consider contributing."""

    x: float
    """ Vector X axis.

    :type: float
    """

    xw: typing.Any
    """ Undocumented, consider contributing."""

    xww: typing.Any
    """ Undocumented, consider contributing."""

    xwww: typing.Any
    """ Undocumented, consider contributing."""

    xwwx: typing.Any
    """ Undocumented, consider contributing."""

    xwwy: typing.Any
    """ Undocumented, consider contributing."""

    xwwz: typing.Any
    """ Undocumented, consider contributing."""

    xwx: typing.Any
    """ Undocumented, consider contributing."""

    xwxw: typing.Any
    """ Undocumented, consider contributing."""

    xwxx: typing.Any
    """ Undocumented, consider contributing."""

    xwxy: typing.Any
    """ Undocumented, consider contributing."""

    xwxz: typing.Any
    """ Undocumented, consider contributing."""

    xwy: typing.Any
    """ Undocumented, consider contributing."""

    xwyw: typing.Any
    """ Undocumented, consider contributing."""

    xwyx: typing.Any
    """ Undocumented, consider contributing."""

    xwyy: typing.Any
    """ Undocumented, consider contributing."""

    xwyz: typing.Any
    """ Undocumented, consider contributing."""

    xwz: typing.Any
    """ Undocumented, consider contributing."""

    xwzw: typing.Any
    """ Undocumented, consider contributing."""

    xwzx: typing.Any
    """ Undocumented, consider contributing."""

    xwzy: typing.Any
    """ Undocumented, consider contributing."""

    xwzz: typing.Any
    """ Undocumented, consider contributing."""

    xx: typing.Any
    """ Undocumented, consider contributing."""

    xxw: typing.Any
    """ Undocumented, consider contributing."""

    xxww: typing.Any
    """ Undocumented, consider contributing."""

    xxwx: typing.Any
    """ Undocumented, consider contributing."""

    xxwy: typing.Any
    """ Undocumented, consider contributing."""

    xxwz: typing.Any
    """ Undocumented, consider contributing."""

    xxx: typing.Any
    """ Undocumented, consider contributing."""

    xxxw: typing.Any
    """ Undocumented, consider contributing."""

    xxxx: typing.Any
    """ Undocumented, consider contributing."""

    xxxy: typing.Any
    """ Undocumented, consider contributing."""

    xxxz: typing.Any
    """ Undocumented, consider contributing."""

    xxy: typing.Any
    """ Undocumented, consider contributing."""

    xxyw: typing.Any
    """ Undocumented, consider contributing."""

    xxyx: typing.Any
    """ Undocumented, consider contributing."""

    xxyy: typing.Any
    """ Undocumented, consider contributing."""

    xxyz: typing.Any
    """ Undocumented, consider contributing."""

    xxz: typing.Any
    """ Undocumented, consider contributing."""

    xxzw: typing.Any
    """ Undocumented, consider contributing."""

    xxzx: typing.Any
    """ Undocumented, consider contributing."""

    xxzy: typing.Any
    """ Undocumented, consider contributing."""

    xxzz: typing.Any
    """ Undocumented, consider contributing."""

    xy: typing.Any
    """ Undocumented, consider contributing."""

    xyw: typing.Any
    """ Undocumented, consider contributing."""

    xyww: typing.Any
    """ Undocumented, consider contributing."""

    xywx: typing.Any
    """ Undocumented, consider contributing."""

    xywy: typing.Any
    """ Undocumented, consider contributing."""

    xywz: typing.Any
    """ Undocumented, consider contributing."""

    xyx: typing.Any
    """ Undocumented, consider contributing."""

    xyxw: typing.Any
    """ Undocumented, consider contributing."""

    xyxx: typing.Any
    """ Undocumented, consider contributing."""

    xyxy: typing.Any
    """ Undocumented, consider contributing."""

    xyxz: typing.Any
    """ Undocumented, consider contributing."""

    xyy: typing.Any
    """ Undocumented, consider contributing."""

    xyyw: typing.Any
    """ Undocumented, consider contributing."""

    xyyx: typing.Any
    """ Undocumented, consider contributing."""

    xyyy: typing.Any
    """ Undocumented, consider contributing."""

    xyyz: typing.Any
    """ Undocumented, consider contributing."""

    xyz: typing.Any
    """ Undocumented, consider contributing."""

    xyzw: typing.Any
    """ Undocumented, consider contributing."""

    xyzx: typing.Any
    """ Undocumented, consider contributing."""

    xyzy: typing.Any
    """ Undocumented, consider contributing."""

    xyzz: typing.Any
    """ Undocumented, consider contributing."""

    xz: typing.Any
    """ Undocumented, consider contributing."""

    xzw: typing.Any
    """ Undocumented, consider contributing."""

    xzww: typing.Any
    """ Undocumented, consider contributing."""

    xzwx: typing.Any
    """ Undocumented, consider contributing."""

    xzwy: typing.Any
    """ Undocumented, consider contributing."""

    xzwz: typing.Any
    """ Undocumented, consider contributing."""

    xzx: typing.Any
    """ Undocumented, consider contributing."""

    xzxw: typing.Any
    """ Undocumented, consider contributing."""

    xzxx: typing.Any
    """ Undocumented, consider contributing."""

    xzxy: typing.Any
    """ Undocumented, consider contributing."""

    xzxz: typing.Any
    """ Undocumented, consider contributing."""

    xzy: typing.Any
    """ Undocumented, consider contributing."""

    xzyw: typing.Any
    """ Undocumented, consider contributing."""

    xzyx: typing.Any
    """ Undocumented, consider contributing."""

    xzyy: typing.Any
    """ Undocumented, consider contributing."""

    xzyz: typing.Any
    """ Undocumented, consider contributing."""

    xzz: typing.Any
    """ Undocumented, consider contributing."""

    xzzw: typing.Any
    """ Undocumented, consider contributing."""

    xzzx: typing.Any
    """ Undocumented, consider contributing."""

    xzzy: typing.Any
    """ Undocumented, consider contributing."""

    xzzz: typing.Any
    """ Undocumented, consider contributing."""

    y: float
    """ Vector Y axis.

    :type: float
    """

    yw: typing.Any
    """ Undocumented, consider contributing."""

    yww: typing.Any
    """ Undocumented, consider contributing."""

    ywww: typing.Any
    """ Undocumented, consider contributing."""

    ywwx: typing.Any
    """ Undocumented, consider contributing."""

    ywwy: typing.Any
    """ Undocumented, consider contributing."""

    ywwz: typing.Any
    """ Undocumented, consider contributing."""

    ywx: typing.Any
    """ Undocumented, consider contributing."""

    ywxw: typing.Any
    """ Undocumented, consider contributing."""

    ywxx: typing.Any
    """ Undocumented, consider contributing."""

    ywxy: typing.Any
    """ Undocumented, consider contributing."""

    ywxz: typing.Any
    """ Undocumented, consider contributing."""

    ywy: typing.Any
    """ Undocumented, consider contributing."""

    ywyw: typing.Any
    """ Undocumented, consider contributing."""

    ywyx: typing.Any
    """ Undocumented, consider contributing."""

    ywyy: typing.Any
    """ Undocumented, consider contributing."""

    ywyz: typing.Any
    """ Undocumented, consider contributing."""

    ywz: typing.Any
    """ Undocumented, consider contributing."""

    ywzw: typing.Any
    """ Undocumented, consider contributing."""

    ywzx: typing.Any
    """ Undocumented, consider contributing."""

    ywzy: typing.Any
    """ Undocumented, consider contributing."""

    ywzz: typing.Any
    """ Undocumented, consider contributing."""

    yx: typing.Any
    """ Undocumented, consider contributing."""

    yxw: typing.Any
    """ Undocumented, consider contributing."""

    yxww: typing.Any
    """ Undocumented, consider contributing."""

    yxwx: typing.Any
    """ Undocumented, consider contributing."""

    yxwy: typing.Any
    """ Undocumented, consider contributing."""

    yxwz: typing.Any
    """ Undocumented, consider contributing."""

    yxx: typing.Any
    """ Undocumented, consider contributing."""

    yxxw: typing.Any
    """ Undocumented, consider contributing."""

    yxxx: typing.Any
    """ Undocumented, consider contributing."""

    yxxy: typing.Any
    """ Undocumented, consider contributing."""

    yxxz: typing.Any
    """ Undocumented, consider contributing."""

    yxy: typing.Any
    """ Undocumented, consider contributing."""

    yxyw: typing.Any
    """ Undocumented, consider contributing."""

    yxyx: typing.Any
    """ Undocumented, consider contributing."""

    yxyy: typing.Any
    """ Undocumented, consider contributing."""

    yxyz: typing.Any
    """ Undocumented, consider contributing."""

    yxz: typing.Any
    """ Undocumented, consider contributing."""

    yxzw: typing.Any
    """ Undocumented, consider contributing."""

    yxzx: typing.Any
    """ Undocumented, consider contributing."""

    yxzy: typing.Any
    """ Undocumented, consider contributing."""

    yxzz: typing.Any
    """ Undocumented, consider contributing."""

    yy: typing.Any
    """ Undocumented, consider contributing."""

    yyw: typing.Any
    """ Undocumented, consider contributing."""

    yyww: typing.Any
    """ Undocumented, consider contributing."""

    yywx: typing.Any
    """ Undocumented, consider contributing."""

    yywy: typing.Any
    """ Undocumented, consider contributing."""

    yywz: typing.Any
    """ Undocumented, consider contributing."""

    yyx: typing.Any
    """ Undocumented, consider contributing."""

    yyxw: typing.Any
    """ Undocumented, consider contributing."""

    yyxx: typing.Any
    """ Undocumented, consider contributing."""

    yyxy: typing.Any
    """ Undocumented, consider contributing."""

    yyxz: typing.Any
    """ Undocumented, consider contributing."""

    yyy: typing.Any
    """ Undocumented, consider contributing."""

    yyyw: typing.Any
    """ Undocumented, consider contributing."""

    yyyx: typing.Any
    """ Undocumented, consider contributing."""

    yyyy: typing.Any
    """ Undocumented, consider contributing."""

    yyyz: typing.Any
    """ Undocumented, consider contributing."""

    yyz: typing.Any
    """ Undocumented, consider contributing."""

    yyzw: typing.Any
    """ Undocumented, consider contributing."""

    yyzx: typing.Any
    """ Undocumented, consider contributing."""

    yyzy: typing.Any
    """ Undocumented, consider contributing."""

    yyzz: typing.Any
    """ Undocumented, consider contributing."""

    yz: typing.Any
    """ Undocumented, consider contributing."""

    yzw: typing.Any
    """ Undocumented, consider contributing."""

    yzww: typing.Any
    """ Undocumented, consider contributing."""

    yzwx: typing.Any
    """ Undocumented, consider contributing."""

    yzwy: typing.Any
    """ Undocumented, consider contributing."""

    yzwz: typing.Any
    """ Undocumented, consider contributing."""

    yzx: typing.Any
    """ Undocumented, consider contributing."""

    yzxw: typing.Any
    """ Undocumented, consider contributing."""

    yzxx: typing.Any
    """ Undocumented, consider contributing."""

    yzxy: typing.Any
    """ Undocumented, consider contributing."""

    yzxz: typing.Any
    """ Undocumented, consider contributing."""

    yzy: typing.Any
    """ Undocumented, consider contributing."""

    yzyw: typing.Any
    """ Undocumented, consider contributing."""

    yzyx: typing.Any
    """ Undocumented, consider contributing."""

    yzyy: typing.Any
    """ Undocumented, consider contributing."""

    yzyz: typing.Any
    """ Undocumented, consider contributing."""

    yzz: typing.Any
    """ Undocumented, consider contributing."""

    yzzw: typing.Any
    """ Undocumented, consider contributing."""

    yzzx: typing.Any
    """ Undocumented, consider contributing."""

    yzzy: typing.Any
    """ Undocumented, consider contributing."""

    yzzz: typing.Any
    """ Undocumented, consider contributing."""

    z: float
    """ Vector Z axis (3D Vectors only).

    :type: float
    """

    zw: typing.Any
    """ Undocumented, consider contributing."""

    zww: typing.Any
    """ Undocumented, consider contributing."""

    zwww: typing.Any
    """ Undocumented, consider contributing."""

    zwwx: typing.Any
    """ Undocumented, consider contributing."""

    zwwy: typing.Any
    """ Undocumented, consider contributing."""

    zwwz: typing.Any
    """ Undocumented, consider contributing."""

    zwx: typing.Any
    """ Undocumented, consider contributing."""

    zwxw: typing.Any
    """ Undocumented, consider contributing."""

    zwxx: typing.Any
    """ Undocumented, consider contributing."""

    zwxy: typing.Any
    """ Undocumented, consider contributing."""

    zwxz: typing.Any
    """ Undocumented, consider contributing."""

    zwy: typing.Any
    """ Undocumented, consider contributing."""

    zwyw: typing.Any
    """ Undocumented, consider contributing."""

    zwyx: typing.Any
    """ Undocumented, consider contributing."""

    zwyy: typing.Any
    """ Undocumented, consider contributing."""

    zwyz: typing.Any
    """ Undocumented, consider contributing."""

    zwz: typing.Any
    """ Undocumented, consider contributing."""

    zwzw: typing.Any
    """ Undocumented, consider contributing."""

    zwzx: typing.Any
    """ Undocumented, consider contributing."""

    zwzy: typing.Any
    """ Undocumented, consider contributing."""

    zwzz: typing.Any
    """ Undocumented, consider contributing."""

    zx: typing.Any
    """ Undocumented, consider contributing."""

    zxw: typing.Any
    """ Undocumented, consider contributing."""

    zxww: typing.Any
    """ Undocumented, consider contributing."""

    zxwx: typing.Any
    """ Undocumented, consider contributing."""

    zxwy: typing.Any
    """ Undocumented, consider contributing."""

    zxwz: typing.Any
    """ Undocumented, consider contributing."""

    zxx: typing.Any
    """ Undocumented, consider contributing."""

    zxxw: typing.Any
    """ Undocumented, consider contributing."""

    zxxx: typing.Any
    """ Undocumented, consider contributing."""

    zxxy: typing.Any
    """ Undocumented, consider contributing."""

    zxxz: typing.Any
    """ Undocumented, consider contributing."""

    zxy: typing.Any
    """ Undocumented, consider contributing."""

    zxyw: typing.Any
    """ Undocumented, consider contributing."""

    zxyx: typing.Any
    """ Undocumented, consider contributing."""

    zxyy: typing.Any
    """ Undocumented, consider contributing."""

    zxyz: typing.Any
    """ Undocumented, consider contributing."""

    zxz: typing.Any
    """ Undocumented, consider contributing."""

    zxzw: typing.Any
    """ Undocumented, consider contributing."""

    zxzx: typing.Any
    """ Undocumented, consider contributing."""

    zxzy: typing.Any
    """ Undocumented, consider contributing."""

    zxzz: typing.Any
    """ Undocumented, consider contributing."""

    zy: typing.Any
    """ Undocumented, consider contributing."""

    zyw: typing.Any
    """ Undocumented, consider contributing."""

    zyww: typing.Any
    """ Undocumented, consider contributing."""

    zywx: typing.Any
    """ Undocumented, consider contributing."""

    zywy: typing.Any
    """ Undocumented, consider contributing."""

    zywz: typing.Any
    """ Undocumented, consider contributing."""

    zyx: typing.Any
    """ Undocumented, consider contributing."""

    zyxw: typing.Any
    """ Undocumented, consider contributing."""

    zyxx: typing.Any
    """ Undocumented, consider contributing."""

    zyxy: typing.Any
    """ Undocumented, consider contributing."""

    zyxz: typing.Any
    """ Undocumented, consider contributing."""

    zyy: typing.Any
    """ Undocumented, consider contributing."""

    zyyw: typing.Any
    """ Undocumented, consider contributing."""

    zyyx: typing.Any
    """ Undocumented, consider contributing."""

    zyyy: typing.Any
    """ Undocumented, consider contributing."""

    zyyz: typing.Any
    """ Undocumented, consider contributing."""

    zyz: typing.Any
    """ Undocumented, consider contributing."""

    zyzw: typing.Any
    """ Undocumented, consider contributing."""

    zyzx: typing.Any
    """ Undocumented, consider contributing."""

    zyzy: typing.Any
    """ Undocumented, consider contributing."""

    zyzz: typing.Any
    """ Undocumented, consider contributing."""

    zz: typing.Any
    """ Undocumented, consider contributing."""

    zzw: typing.Any
    """ Undocumented, consider contributing."""

    zzww: typing.Any
    """ Undocumented, consider contributing."""

    zzwx: typing.Any
    """ Undocumented, consider contributing."""

    zzwy: typing.Any
    """ Undocumented, consider contributing."""

    zzwz: typing.Any
    """ Undocumented, consider contributing."""

    zzx: typing.Any
    """ Undocumented, consider contributing."""

    zzxw: typing.Any
    """ Undocumented, consider contributing."""

    zzxx: typing.Any
    """ Undocumented, consider contributing."""

    zzxy: typing.Any
    """ Undocumented, consider contributing."""

    zzxz: typing.Any
    """ Undocumented, consider contributing."""

    zzy: typing.Any
    """ Undocumented, consider contributing."""

    zzyw: typing.Any
    """ Undocumented, consider contributing."""

    zzyx: typing.Any
    """ Undocumented, consider contributing."""

    zzyy: typing.Any
    """ Undocumented, consider contributing."""

    zzyz: typing.Any
    """ Undocumented, consider contributing."""

    zzz: typing.Any
    """ Undocumented, consider contributing."""

    zzzw: typing.Any
    """ Undocumented, consider contributing."""

    zzzx: typing.Any
    """ Undocumented, consider contributing."""

    zzzy: typing.Any
    """ Undocumented, consider contributing."""

    zzzz: typing.Any
    """ Undocumented, consider contributing."""

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
    def Range(cls, start: int, stop: int, step: int = 1):
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
    ) -> float:
        """Return the dot product of this vector and another.

        :param other: The other vector to perform the dot product with.
        :type other: collections.abc.Sequence[float] | typing_extensions.Self
        :return: The dot product.
        :rtype: float
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
