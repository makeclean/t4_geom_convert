'''Unit tests for the :mod:`~.Lattice module.'''
# pylint: disable=no-value-for-parameter

from math import cos, sin

import pytest
import numpy as np
from hypothesis import given, settings, note
from hypothesis.strategies import floats, integers, booleans, composite, one_of

from t4_geom_convert.Kernel.Transformation.TransformationError import (
    TransformationError)
from t4_geom_convert.Kernel.Transformation.Transformation import (
    normalize_matrix)


def make_euler(alpha, beta, gamma):
    '''Construct a rotation matrix from the XYX Euler angles.'''
    sin1, cos1 = sin(alpha), cos(alpha)
    sin2, cos2 = sin(beta), cos(beta)
    sin3, cos3 = sin(gamma), cos(gamma)
    mat = [cos2, -cos3*sin2, sin2*sin3,
           cos1*sin2, cos1*cos2*cos3 - sin1*sin3, - cos3*sin1 - cos1*cos2*sin3,
           sin1*sin2, cos1*sin3 + cos2*cos3*sin1, cos1*cos3 - cos2*sin1*sin3]
    return mat


@composite
def rotation(draw):
    '''Generate a random three-dimensional rotation matrix.'''
    component = floats(-1e5, 1e5, allow_nan=False, allow_infinity=False)
    alpha, beta, gamma = draw(component), draw(component), draw(component)
    return make_euler(alpha, beta, gamma)


def keep3(matrix, index, row):
    '''Return a new matrix with exactly 3 defined elements (the `index`-th row
    if `row` is True, else the `index`-th column).
    '''
    trunc = [None]*9
    if row:
        trunc[3*index:3*index+3] = matrix[3*index:3*index+3]
    else:
        trunc[index::3] = matrix[index::3]
    return trunc


def keep5(matrix, i_row, j_col):
    '''Return a new matrix with exactly 5 defined elements (the `i_row`-th row
    and the `j_col`-th column).'''
    matrix = matrix.copy()
    for i in range(3):
        if i == i_row:
            continue
        for j in range(3):
            if j == j_col:
                continue
            matrix[3*i + j] = None
    return matrix


def keep6(matrix, index, row):
    '''Return a new matrix with exactly 6 defined elements (all rows except the
    `index`-th one if `row` is True, else all columns except the `index`-th
    one).
    '''
    trunc = matrix.copy()
    if row:
        trunc[3*index:3*index+3] = [None]*3
    else:
        trunc[index::3] = [None]*3
    return trunc


@composite
def matrix3(draw):
    '''Generate a random matrix, truncate it to 3 elements and return it along
    with the non-truncated matrix.'''
    index = draw(integers(0, 2))
    row = draw(booleans())
    matrix = draw(rotation())
    return matrix, keep3(matrix, index, row)


@composite
def matrix5(draw):
    '''Generate a random matrix, truncate it to 5 elements and return it along
    with the non-truncated matrix.'''
    i_row, j_col = draw(integers(0, 2)), draw(integers(0, 2))
    matrix = draw(rotation())
    return matrix, keep5(matrix, i_row, j_col)


@composite
def matrix6(draw):
    '''Generate a random matrix, truncate it to 6 elements and return it along
    with the non-truncated matrix.'''
    index = draw(integers(0, 2))
    row = draw(booleans())
    matrix = draw(rotation())
    return matrix, keep6(matrix, index, row)


@composite
def matrix9(draw):
    '''Return two copies of a random matrix.'''
    matrix = draw(rotation())
    return matrix, matrix.copy()


@settings(max_examples=1000)
@given(mats=one_of(matrix3(), matrix5(), matrix6(), matrix9()))
def test_normalized(mats):
    '''Test that normalized matrices with 5, 6 or 9 elements are unitary and
    equal to the non-truncated version.'''
    full_mat, trunc_mat = mats
    norm_mat = normalize_matrix(trunc_mat)

    full_mat = np.array(full_mat).reshape(3, 3)
    norm_mat = np.array(norm_mat).reshape(3, 3)
    trunc_mat = np.array(trunc_mat).reshape(3, 3)
    note('norm_mat: {}'.format(norm_mat))
    note('trunc_mat: {}'.format(trunc_mat))

    prod = norm_mat.T.dot(norm_mat)
    assert np.allclose(prod, np.identity(3), atol=1e-5)
    prod = norm_mat.dot(norm_mat.T)
    assert np.allclose(prod, np.identity(3), atol=1e-5)

    mask = np.not_equal(trunc_mat, None)
    note('mask: {}'.format(mask))
    assert np.allclose(norm_mat[mask],
                       trunc_mat[mask].astype(norm_mat.dtype),
                       atol=1e-5)


@pytest.mark.parametrize('keep', (1, 2, 4, 7, 8))
def test_normalized_raises(keep):
    '''Check that trying to normalize a matrix with an unexpected number of
    missing elements results in an exception.'''
    mat = make_euler(100.0, 200.0, 300.0)
    mat[keep:] = [None]*(len(mat)-keep)
    with pytest.raises(TransformationError):
        normalize_matrix(mat)
