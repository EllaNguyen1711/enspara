import unittest

import numpy as np

from numpy.testing import assert_array_equal, assert_array_almost_equal

from ..tpt import committors, reactive_fluxes, mfpts


class Test_Fluxes(unittest.TestCase):

    def test_committors(self):
        Tij1 = np.array(
            [
                [0.5, 0.4, 0.1],
                [0.25, 0.5, 0.25],
                [0.1, 0.5, 0.4]])

        true_committors = np.array([0, 0.5, 1.])

        for_committors = committors(Tij1, 0, 2)
        assert_array_equal(for_committors, true_committors)

        for_committors = committors(Tij1, [0], [2])
        assert_array_equal(for_committors, true_committors)

        Tij2 = np.array(
            [
                [0.5, 0.4, 0.1, 0.],
                [0.25, 0.5, 0.2, 0.05],
                [0.1, 0.15, 0.5, 0.25],
                [0., 0.1, 0.4, 0.5]])

        true_committors = np.array([0, 0.34091, 0.60227, 1.])

        for_committors = np.around(committors(Tij2, 0, 3), 5)
        assert_array_equal(for_committors, true_committors)

        for_committors = committors(Tij2, [0,2], [3])
        assert_array_equal(for_committors, np.array([0, 0.1, 0, 1.0]))

    def test_fluxes(self):
        Tij = np.array(
            [
                [0.5, 0.5, 0],
                [0.5, 0, 0.5],
                [0, 0.5, 0.5]])
        pops = np.zeros(3) + (1/3.)

        # true fluxes
        true_fluxes = np.zeros((3,3))
        true_fluxes[0,1] = 1/12.
        true_fluxes[1,2] = 1/12.
        true_fluxes = np.around(true_fluxes, 5)

        # test fluxes
        calc_fluxes = np.around(reactive_fluxes(
            Tij, 0, 2, populations=pops), 5)
        assert_array_equal(calc_fluxes, true_fluxes)

        # test fluxes without pops
        calc_fluxes = np.around(reactive_fluxes(Tij, 0, 2), 5)
        assert_array_equal(calc_fluxes, true_fluxes)

    def test_mfpts(self):
        tcounts = np.array([[2, 1, 1], [2, 1, 2], [3, 2, 1]])
        T_test = tcounts/tcounts.sum(axis=1)[:,None]

        # test all to all
        all_mfpts = mfpts(T_test)
        assert_array_almost_equal(
            all_mfpts, np.array(
                [
                    [0., 3.71428571, 3.5],
                    [2.3125, 0., 3.],
                    [2.125, 3.42857143, 0.]]), 5)

        # test all to sinks
        sink_mfpts = mfpts(T_test, sinks=[0])
        assert_array_almost_equal(
            sink_mfpts,
            np.array([0., 2.3125, 2.125]), 5)

        #lagtime 1
        sink_mfpts_lagtime1 = mfpts(T_test, sinks=[0,1])
        assert_array_almost_equal(
            sink_mfpts_lagtime1,
            np.array([0., 0., 1.2]), 5)

        # check lagtime
        sink_mfpts_lagtime5 = mfpts(T_test, sinks=[0,1], lagtime=5.0)
        assert_array_almost_equal(
            sink_mfpts_lagtime1*5.0,
            sink_mfpts_lagtime5, 5)

        assert_array_almost_equal(
            mfpts(T_test)*5.0,
            mfpts(T_test,lagtime=5), 5)
