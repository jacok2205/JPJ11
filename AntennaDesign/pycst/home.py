# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 22:24:41 2022

@author: Yates
@contributor: jacok2205

A win32com COMObject with the following Fields and Methods (win32com.client.dynamic.Dispatch(CSTStudio.Application):
    Fields:
        Object has no fields to print
    Methods:
        Active3D
        ActiveDS
        CloseProject
        FileNew
        GetFileMainVersion
        GetFilePatchVersion
        NewCS
        NewDS
        NewDesign
        NewEMS
        NewMPS
        NewMWS
        NewPCBS
        NewPS
        NewProject
        NewSystemsimulator
        OpenDesign
        OpenFile
        ProtectProject
        Quit
        ReleaseUniqueID
        SetQuietMode
"""
from AntennaDesign.pycst.config import debug as debug


def SetQuietMode(cst):
    try:
        cst.SetQuietMode(1)
        return 0

    except Exception as __error__:
        if debug:
            print(__error__)
    return -1


def ClearQuietMode(cst):
    try:
        cst.SetQuietMode(0)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def quit_cst(cst):
    """
    Parameters
    ----------
    cst : COMObject
        The win32com object that is controlling CST Studio Suite.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        cst.Quit()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def new_project(cst, projectType):
    """
    Parameters
    ----------
    cst : COMObject
        The win32com object that is controlling CST Studio Suite.
    projectType: str
        Project types are the following:
        NewCS, NewDS, NewDesign, NewEMS, NewMPS, NewMWS, NewPCBS, NewPS

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        exec(f'cst.{projectType}()')
        mws = cst.Active3D()

        return mws

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1, -1


def open_project(cst, path):
    """
    Parameters
    ----------
    cst : Active3D Object
        The Active3D object that was created from the win32com object, "cst.Active3D()".
    path : str
        The path of the project to open. Note that the full path is required.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """
    try:
        cst.OpenFile(path)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def get_active_3d(cst):
    try:
        return cst.Active3D()

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


# Not working (yet)
def save_project(mws):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mws.Save()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


# Not working (yet)
def save_as_project(mws, filename):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    filename : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mws.SaveAs(f'{filename}.cst')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def save_zip(mws, keepAll, keep1D, keepFarfield, deleteProjFolder):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    keepAll : TYPE
        DESCRIPTION.
    keep1D: TYPE
        DESCRIPTION
    keepFarfield: TYPE
        DESCRIPTION
    deleteProjFolder: TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mws.StoreinArchive(keepAll, keep1D, keepFarfield, deleteProjFolder)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def backup(mws, filename):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    filename : str
        The file name that will be used to back-up from. Note that the path is needed prior to the filename

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mws.Backup(f'{filename}.cst')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def close_project(cst, path):
    """
    Parameters
    ----------
    cst : COMObject
        The win32com object that is controlling CST Studio Suite.
    path : str
        The path to the project that you want to close. Note that the full path is required.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        cst.CloseProject(path)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def set_units(mws, dimension='mm', frequency='GHz', temperature='Kelvin', time='ns',
                  voltage='V', current='A', resistance='Ohm', conductance='Siemens', capacitance='PikoF',
                  inductance='NanoH'):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    dimension:
    frequency:
    temperature:
    time:
    voltage:
    current:
    resistance:
    conductance:
    capacitance:
    inductance:

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        Units = mws.Units
        Units.Geometry(dimension)
        Units.Frequency(frequency)
        Units.TemperatureUnit(temperature)
        Units.Time(time)
        Units.Voltage(voltage)
        Units.Current(current)
        Units.Resistance(resistance)
        Units.Conductance(conductance)
        Units.Capacitance(capacitance)
        Units.Inductance(inductance)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1
    

def activate_local_wcs(mws, setNormal, setOrigin, setUVector, activate):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    setNormal: TYPE
        DESCRIPTION.
    setOrigin: TYPE
        DESCRIPTION.
    setUVector: TYPE
        DESCRIPTION.
    activate: bool
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        wcs = mws.WCS

        if activate:
            wcs.activateWCS('local')
            wcs.setNormal(str(setNormal(0)), str(setNormal(1)), str(setNormal(2)))
            wcs.setOrigin(str(setOrigin(0)), str(setOrigin(1)), str(setOrigin(2)))
            wcs.setUVector(str(setUVector(0)), str(setUVector(1)), str(setUVector(2)))
        else:
            wcs.ActivateWCS('Global')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def mesh_initiator(mws):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        FDSolver = mws.FDSolver
        mesh = mws.Mesh
        Mesh_Settings = mws.MeshSettings
        meshAdaption3D = mws.MeshAdaption3D
        PostProcess1D = mws.PostProcess1D

        FDSolver.ExtrudeOpenBC('True')

        mesh.MergeThinPECLayerFixpoints('True')
        mesh.RatioLimit('20')
        mesh.AutomeshRefineAtPecLines('True', '6')
        mesh.FPBAAvoidNonRegUnite('True')
        mesh.ConsiderSpaceForLowerMeshLimit('False')
        mesh.MinimumStepNumber('5')
        mesh.AnisotropicCurvatureRefinement('True')
        mesh.AnisotropicCurvatureRefinementFSM('True')
    
        # Default mesh settings
    
        Mesh_Settings.SetMeshType('Hex')
        Mesh_Settings.Set('RatioLimitGeometry', '20')
        Mesh_Settings.Set('EdgeRefinementOn', '1')
        Mesh_Settings.Set('EdgeRefinementRatio', '6')
        Mesh_Settings.SetMeshType('HexTLM')
        Mesh_Settings.Set('RatioLimitGeometry', '20')
        Mesh_Settings.SetMeshType('Tet')
        Mesh_Settings.Set('VolMeshGradation', '1.5')
        Mesh_Settings.Set('SrfMeshGradation', '1.5')
        Mesh_Settings.SetMeshType('Hex')
        Mesh_Settings.Set('Version', '1%')

        meshAdaption3D.SetAdaptionStrategy('Energy')
        mesh.MeshType('PBA')
        PostProcess1D.ActivateOperation('vswr', 'true')
        PostProcess1D.ActivateOperation('yz-matrices', 'true')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def units(mws, geometry, frequency, time, temperatureUnit, voltage, current, resistance, conductance, capacitance, inductance):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    geometry: TYPE
        DESCRIPTION.
    frequency: TYPE
        DESCRIPTION.
    time: TYPE
        DESCRIPTION.
    temperatureUnit: TYPE
        DESCRIPTION.
    voltage: TYPE
        DESCRIPTION.
    current: TYPE
        DESCRIPTION.
    resistance: TYPE
        DESCRIPTION.
    conductance: TYPE
        DESCRIPTION.
    capacitance: TYPE
        DESCRIPTION.
    inductance: TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        Units = mws.Units

        Units.Geometry(geometry)
        Units.Frequency(frequency)
        Units.TemperatureUnit(temperatureUnit)
        Units.Time(time)
        Units.Voltage(voltage)
        Units.Current(current)
        Units.Resistance(resistance)
        Units.Conductance(conductance)
        Units.Capacitance(capacitance)
        Units.Inductance(inductance)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def background_material(mws, xmin, xmax, ymin, ymax, zmin, zmax):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    xmin: TYPE
        DESCRIPTION.
    xmax: TYPE
        DESCRIPTION.
    ymin: TYPE
        DESCRIPTION.
    ymax: TYPE
        DESCRIPTION.
    zmin: TYPE
        DESCRIPTION.
    zmax: TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        background = mws.Background
        material = mws.Material

        background.ResetBackground()
        background.Type('Normal')
        background.Epsilon('1.0')
        background.Mu('1.0')
        background.XminSpace(str(xmin))
        background.XmaxSpace(str(xmax))
        background.YminSpace(str(ymin))
        background.YmaxSpace(str(ymax))
        background.ZminSpace(str(zmin))
        background.ZmaxSpace(str(zmax))

        material.Reset()
        material.FrqType('all')
        material.Type('Normal')
        material.MaterialUnit('Frequency', 'Hz')
        material.MaterialUnit('Geometry', 'm')
        material.MaterialUnit('Time', 's')
        material.MaterialUnit('Temperature', 'Kelvin')
        material.Epsilon('1.0')
        material.Mue('1.0')
        material.Sigma('0.0')
        material.TanD('0.0')
        material.TanDFreq('0.0')
        material.TanDGiven('False')
        material.TanDModel('ConstSigma')
        material.EnableUserConstTanDModelOrderEps('False')
        material.ConstTanDModelOrderEps('1')
        material.SetElParametricConductivity('False')
        material.ReferenceCoordSystem('Global')
        material.CoordSystemType('Cartesian')
        material.SigmaM('0')
        material.TanDM('0.0')
        material.TanDMFreq('0.0')
        material.TanDMGiven('False')
        material.TanDMModel('ConstSigma')
        material.EnableUserConstTanDModelOrderMue('False')
        material.ConstTanDModelOrderMue('1')
        material.SetMagParametricConductivity('False')
        material.DispModelEps('None')
        material.DispModelMue('None')
        material.DispersiveFittingSchemeEps('Nth Order')
        material.MaximalOrderNthModelFitEps('10')
        material.ErrorLimitNthModelFitEps('0.1')
        material.UseOnlyDataInSimFreqRangeNthModelEps('False')
        material.DispersiveFittingSchemeMue('Nth Order')
        material.MaximalOrderNthModelFitMue('10')
        material.ErrorLimitNthModelFitMue('0.1')
        material.UseOnlyDataInSimFreqRangeNthModelMue('False')
        material.UseGeneralDispersionEps('False')
        material.UseGeneralDispersionMue('False')
        material.NLAnisotropy('False')
        material.NLAStackingFactor('1')
        material.NLADirectionX('1')
        material.NLADirectionY('0')
        material.NLADirectionZ('0')
        material.Rho('0.0')
        material.ThermalType('Normal')
        material.ThermalConductivity('0.0')
        material.HeatCapacity('0.0')
        material.MetabolicRate('0')
        material.BloodFlow('0')
        material.VoxelConvection('0')
        material.MechanicsType('Unused')
        material.Colour('0.6', '0.6', '0.6')
        material.Wireframe('False')
        material.Reflection('False')
        material.Allowoutline('True')
        material.Transparentoutline('False')
        material.Transparency('0')
        material.ChangeBackgroundMaterial()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def mesh_settings(mws, cellsPerWavelength, minCell):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    cellsPerWavelength: TYPE
        DESCRIPTION.
    minCell: TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mesh = mws.Mesh
        Mesh_Settings = mws.MeshSettings
        discretiser = mws.Discretizer

        mesh.MeshType('PBA')
        mesh.SetCreator('High Frequency')  # warning

        Mesh_Settings.SetMeshType('Hex')
        Mesh_Settings.Set('Version', '1%')
        Mesh_Settings.Set.StepsPerWaveNear(str(cellsPerWavelength))
        Mesh_Settings.Set.StepsPerWaveFar(str(cellsPerWavelength))
        Mesh_Settings.Set.WavelengthRefinementSameAsNear('1')
        Mesh_Settings.Set.StepsPerBoxNear(str(cellsPerWavelength))
        Mesh_Settings.Set.StepsPerBoxFar(str(cellsPerWavelength))
        Mesh_Settings.Set.MaxStepNear(str(cellsPerWavelength))
        Mesh_Settings.Set.MaxStepFar(str(cellsPerWavelength))
        Mesh_Settings.Set.ModelBoxDescrNear('maxedge')
        Mesh_Settings.Set.ModelBoxDescrFar('maxedge')
        Mesh_Settings.Set.UseMaxStepAbsolute('0')
        Mesh_Settings.Set.GeometryRefinementSameAsNear('1')
        Mesh_Settings.Set.UseRatioLimitGeometry('1')
        Mesh_Settings.Set.RatioLimitGeometry(str(minCell))
        Mesh_Settings.Set.MinStepGeometryX('0')
        Mesh_Settings.Set.MinStepGeometryY('0')
        Mesh_Settings.Set.MinStepGeometryZ('0')
        Mesh_Settings.Set.UseSameMinStepGeometryXYZ('1')
        Mesh_Settings.SetMeshType('Hex')
        Mesh_Settings.Set.FaceRefinementOn('0')
        Mesh_Settings.Set.FaceRefinementPolicy('2')
        Mesh_Settings.Set.FaceRefinementRatio('2')
        Mesh_Settings.Set.FaceRefinementStep('0')
        Mesh_Settings.Set.FaceRefinementNSteps('2')
        Mesh_Settings.Set.EllipseRefinementOn('0')
        Mesh_Settings.Set.EllipseRefinementPolicy('2')
        Mesh_Settings.Set.EllipseRefinementRatio('2')
        Mesh_Settings.Set.EllipseRefinementStep('0')
        Mesh_Settings.Set.EllipseRefinementNSteps('2')
        Mesh_Settings.Set.FaceRefinementBufferLines('3')
        Mesh_Settings.Set.EdgeRefinementOn('1')
        Mesh_Settings.Set.EdgeRefinementPolicy('1')
        Mesh_Settings.Set.EdgeRefinementRatio('2')
        Mesh_Settings.Set.EdgeRefinementStep('0')
        Mesh_Settings.Set.EdgeRefinementBufferLines('3')
        Mesh_Settings.Set.RefineEdgeMaterialGlobal('0')
        Mesh_Settings.Set.RefineAxialEdgeGlobal('0')
        Mesh_Settings.Set.BufferLinesNear('3')
        Mesh_Settings.Set.UseDielectrics('1')
        Mesh_Settings.Set.EquilibrateOn('0')
        Mesh_Settings.Set.Equilibrate('1.5')
        Mesh_Settings.Set.IgnoreThinPanelMaterial('0')
        Mesh_Settings.SetMeshType('Hex')
        Mesh_Settings.Set.SnapToAxialEdges('1')
        Mesh_Settings.Set.SnapToPlanes('1')
        Mesh_Settings.Set.SnapToSpheres('1')
        Mesh_Settings.Set.SnapToEllipses('1')
        Mesh_Settings.Set.SnapToCylinders('1')
        Mesh_Settings.Set.SnapToCylinderCenters('1')
        Mesh_Settings.Set.SnapToEllipseCenters('1')

        discretiser.MeshType('PBA')
        discretiser.PBAType('Fast PBA')
        discretiser.AutomaticPBAType('True')
        discretiser.FPBAAccuracyEnhancement('enable')
        discretiser.ConnectivityCheck('False')
        discretiser.ConvertGeometryDataAfterMeshing('True')
        discretiser.UsePecEdgeModel('True')
        discretiser.GapDetection('False')
        discretiser.FPBAGapTolerance('1e-3')
        discretiser.SetMaxParallelMesherThreads('Hex', '12')
        discretiser.SetParallelMesherMode('Hex', 'Maximum')
        discretiser.PointAccEnhancement('0')
        discretiser.UseSplitComponents('True')
        discretiser.EnableSubgridding('False')
        discretiser.PBAFillLimit('99')
        discretiser.AlwaysExcludePec('False')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1
