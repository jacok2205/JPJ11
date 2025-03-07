# -*- coding: utf-8 -*-
"""
@author: Unknown
@contributor: jacok2205

Post processing functions for CST 2021

TODO:
    Include more result types from the 1D tree.
    Include 2D/3D and Farfield result trees.
"""

import math
from AntennaDesign.pycst.config import debug as debug


def result_parameters(mws, *, parent_path=r'1D Results\S-Parameters', run_id=0, result_id=0):
    """
    Provides access to S-parameters from the 1D results tree.

    Parameters
    ----------
    mws : TYPE
        DESCRIPTION.
    * : TYPE
        DESCRIPTION.
    parent_path : TYPE, optional
        DESCRIPTION. The default is r'1D Results\S-Parameters'.
    run_id : TYPE, optional
        DESCRIPTION. The default is 0.
    result_id : TYPE, optional
        DESCRIPTION. The default is 0.

    Returns
    -------
    TYPE
        DESCRIPTION.
    """

    try:
        result_tree = mws.Resulttree

        result_path_list = list()
        if result_tree.DoesTreeItemExist(parent_path):
            child = result_tree.GetFirstChildName(parent_path)

            while len(child) > 0:
                result_path_list.append(child)
                child = result_tree.GetNextItemName(child)

            run_ids = result_tree.GetResultIDsFromTreeItem(result_path_list[result_id])
            run_id_name = list(run_ids)[run_id]
            object_res = result_tree.GetResultFromTreeItem(result_path_list[result_id], run_id_name)
            result_type = object_res.GetResultObjectType

            frequencies_list = list(object_res.GetArray('x'))

            if result_type == '1DC':
                y_real = list(object_res.GetArray('yre'))
                y_imag = list(object_res.GetArray('yim'))

                y_list = []
                for i, yval in enumerate(y_real):
                    y_list.append(20 * math.log10(abs(complex(y_real[i], y_imag[i]))))
            else:
                y_list = list(object_res.GetArray('y'))

            x_label = object_res.GetXLabel
            y_label = object_res.GetYLabel
            y_real = []
            y_imag = []
            plot_title = object_res.GetTitle

            if result_type == '1DC':
                return frequencies_list, [y_real, y_imag], y_list, [x_label, y_label, plot_title]
            else:
                return frequencies_list, y_list, [x_label, y_label, plot_title]
        else:
            raise(Exception('Result tree item not found'))

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def export_touchstone(mws, exportpath):
    """
    Provides access to S-parameters from the 1D results tree.

    Parameters
    ----------
    mws : TYPE
        DESCRIPTION.
    exportpath : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if an error occurred, else 0 is returned.
    """

    try:
        touchstone = mws.TOUCHSTONE
        touchstone.Reset()
        touchstone.FileName(exportpath)
        touchstone.Impedance('50')
        touchstone.FrequencyRange('full')
        touchstone.Renormalize('True')
        touchstone.UseARResults('False')
        touchstone.SetNSamples('1001')
        touchstone.Write()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1
