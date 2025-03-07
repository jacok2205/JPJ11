# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 22:24:41 2022

@author: Unknown
@contributor: jacok2205
"""

from AntennaDesign.pycst.config import debug as debug


def efield_monitor(mws, eFieldName, frequency):
    '''
    Parameters
    ----------
    mws : TYPE
        DESCRIPTION.
    eFieldName : TYPE
        DESCRIPTION.
    frequency : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occured, else 0 is returned.
    '''

    try:
        monitor = mws.Monitor

        monitor.Reset()
        monitor.Name(eFieldName)
        monitor.Dimension('Volume')
        monitor.Domain('Frequency')
        monitor.FieldType('Efield')
        monitor.Frequency(str(frequency))
        monitor.UseSubvolume('False')
        monitor.SetSubvolume('-53.310273111111', '53.310273111111', '-53.310273111111', '53.310273111111',
                             '-33.310273111111', '71.310273111111')
        monitor.Create()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def hfield_monitor(mws, hFieldName, frequency):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    hFieldName : TYPE
        DESCRIPTION
    frequency : TYPE
        DESCRIPTION

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        monitor = mws.Monitor

        monitor.Reset()
        monitor.Name(hFieldName)
        monitor.Dimension('Volume')
        monitor.Domain('Frequency')
        monitor.FieldType('Hfield')
        monitor.Frequency(str(frequency))
        monitor.UseSubvolume('False')
        monitor.SetSubvolume('-209.896229', '229.896229', '-179.896229', '179.896229', '-149.896229', '187.896229')
        monitor.Create()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def farfield_monitor(mws, farfieldName, frequency, domain):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    farfieldName : TYPE
        DESCRIPTION
    frequency : TYPE
        DESCRIPTION
    domain : str
        Frequency, Time

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        monitor = mws.Monitor

        monitor.Reset()
        monitor.Name(farfieldName)
        monitor.Domain(domain)
        monitor.FieldType('Farfield')
        monitor.Frequency(str(frequency))
        monitor.UseSubvolume('False')
        monitor.ExportFarfieldSource('False')
        monitor.SetSubvolume('-53.310273111111', '53.310273111111', '-53.310273111111', '53.310273111111',
                             '-33.310273111111', '71.310273111111')
        monitor.Create()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def frequency_range(mws, frange1, frange2):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    frange1 : TYPE
        DESCRIPTION
    frange2 : TYPE
        DESCRIPTION

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """
    try:
        Solver = mws.Solver
        Solver.FrequencyRange(str(frange1), str(frange2))

        mesh = mws.Mesh
        mesh_settings = mws.MeshSettings
        mesh_settings.SetMeshType('Hex')
        mesh_settings.Set('Version', '1%')
        mesh.MeshType('PBA')

    except Exception as __error__:
        if debug:
            print(__error__)


def waveguide_port(mws, portNumber, normal, xrange, yrange, zrange, xrangeAdd=(0, 0), yrangeAdd=(0, 0),
                   zrangeAdd=(0, 0), coordinates='Free', orientation='Positive'):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    portNumber : TYPE
        DESCRIPTION.
    normal: TYPE
        DESCRIPTION.
    xrange : TYPE
        DESCRIPTION.
    yrange : TYPE
        DESCRIPTION.
    zrange : TYPE
        DESCRIPTION.
    xrangeAdd : TYPE
        DESCRIPTION.
    yrangeAdd : TYPE
        DESCRIPTION.
    zrangeAdd : TYPE
        DESCRIPTION.
    coordinates : TYPE
        DESCRIPTION.
    orientation : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        port = mws.Port

        port.Reset()
        port.PortNumber(str(portNumber))
        port.Label('')
        port.NumberOfModes('1')
        port.Normal(normal)
        port.AdjustPolarization('False')
        port.PolarizationAngle('0.0')
        port.ReferencePlaneDistance('0')
        port.TextSize('50')
        port.Coordinates(coordinates)
        port.Orientation(orientation)
        port.PortOnBound('False')
        port.ClipPickedPortToBound('False')
        port.Xrange(str(xrange[0]), str(xrange[1]))
        port.Yrange(str(yrange[0]), str(yrange[1]))
        port.Zrange(str(zrange[0]), str(zrange[1]))
        port.XrangeAdd(str(xrangeAdd[0]), str(xrangeAdd[1]))
        port.YrangeAdd(str(yrangeAdd[0]), str(yrangeAdd[1]))
        port.ZrangeAdd(str(zrangeAdd[0]), str(zrangeAdd[1]))
        port.SingleEnded('False')
        port.Create()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def delete_waveguide_port(mws, port_number):
    try:
        mws.Port.Delete(port_number)
    except Exception as __error__:
        if debug:
            print(__error__)

    return -1

    
def plane_wave_excitation(mws, normal, eVector, polarization, referenceFrequency, phaseDifference, circularDirection,
                          axialRatio):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    normal : TYPE
        DESCRIPTION.
    eVector : TYPE
        DESCRIPTION.
    polarization : TYPE
        DESCRIPTION.
    referenceFrequency : TYPE
        DESCRIPTION.
    phaseDifference : TYPE
        DESCRIPTION.
    circularDirection : TYPE
        DESCRIPTION.
    axialRatio : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        planeWave = mws.PlaneWave

        planeWave.Reset()
        planeWave.Normal(str(normal(0)), str(normal(1)), str(normal(2)))
        planeWave.EVector(str(eVector(0)), str(eVector(1)), str(eVector(2)))
        planeWave.Polarization(polarization)
        planeWave.ReferenceFrequency(str(referenceFrequency))
        planeWave.PhaseDifference(str(phaseDifference))
        planeWave.CircularDirection(circularDirection)
        planeWave.AxialRatio(str(axialRatio))
        planeWave.SetUserDecouplingPlane('False')
        planeWave.Store()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1

    
def discrete_port(mws, portNumber, setP1, setP2):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    portNumber : TYPE
        DESCRIPTION.
    setP1 : TYPE
        DESCRIPTION.
    setP2 : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        discrete_port = mws.DiscretePort

        discrete_port.Reset()
        discrete_port.PortNumber(str(portNumber))
        discrete_port.Type('SParameter')
        discrete_port.Label('')
        discrete_port.Impedance('50')
        discrete_port.VoltagePortImpedance('0.0')
        discrete_port.Voltage('1.0')
        discrete_port.Current('1.0')
        discrete_port.SetP1('False', setP1[0], setP1[1], setP1[2])
        discrete_port.SetP2('False', setP2[0], setP2[1], setP2[2])
        discrete_port.InvertDirection('False')
        discrete_port.LocalCoordinates('False')
        discrete_port.Monitor('True')
        discrete_port.Radius('0.0')
        discrete_port.Wire('')
        discrete_port.Position('end1')
        discrete_port.Create()
        format(discrete_port)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1

    
def discrete_face_port(mws, portNumber, setP1, setP2):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    portNumber : TYPE
        DESCRIPTION.
    setP1 : TYPE
        DESCRIPTION.
    setP2 : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        discrete_face_port = mws.DiscreteFacePort

        discrete_face_port.Reset()
        discrete_face_port.PortNumber(portNumber)
        discrete_face_port.Type('SParameter')
        discrete_face_port.Label('')
        discrete_face_port.Impedance('50')
        discrete_face_port.VoltagePortImpedance('0.0')
        discrete_face_port.VoltageAmplitude('1.0')
        discrete_face_port.setP1('True', setP1[0], setP1[1], setP1[2])
        discrete_face_port.setP2('True', setP2[0], setP2[1], setP2[2])
        discrete_face_port.InvertDirection('False')
        discrete_face_port.LocalCoordinates('False')
        discrete_face_port.Monitor('True')
        discrete_face_port.CenterEdge('True')
        discrete_face_port.UseProjection('False')
        discrete_face_port.ReverseProjection('False')
        discrete_face_port.Create()
        format(discrete_face_port)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1

    
def time_domain_solver(mws, steadyStateLimit):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    steadyStateLimit : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mesh = mws.Mesh
        mesh.SetCreator('High Frequency')

        solver = mws.Solver
        # solver.Method('Hexahedral')
        # solver.CalculationType('TD-S')
        # solver.StimulationPort('All')
        # solver.StimulationMode('All')
        solver.SteadyStateLimit(f'{steadyStateLimit}')
        # solver.MeshAdaption('False')
        # solver.NormingImpedance('50')
        # solver.CalculateModesOnly('False')
        # solver.SParaSymmetry('False')
        # solver.StoreTDResultsInCache('False')
        # solver.FullDeembedding('False')
        # solver.SuperimposePLWExcitation('False')
        # solver.UseSensitivityAnalysis('False')
        solver.MaximumNumberOfThreads('12')
        solver.Start

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def open_boundary(mws, minfrequency, xmin, xmax, ymin, ymax, zmin, zmax):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    minfrequency : TYPE
        DESCRIPTION.
    xmin : TYPE
        DESCRIPTION.
    xmax : TYPE
        DESCRIPTION.
    ymin : TYPE
        DESCRIPTION.
    ymax : TYPE
        DESCRIPTION.
    zmin : TYPE
        DESCRIPTION.
    zmax : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        boundary = mws.Boundary
        plot = mws.Plot

        boundary.Xmin(xmin)
        boundary.Xmax(xmax)
        boundary.Ymin(ymin)
        boundary.Ymax(ymax)
        boundary.Zmin(zmin)
        boundary.Zmax(zmax)
        boundary.Xsymmetry('none')
        boundary.Ysymmetry('none')
        boundary.Zsymmetry('none')
        boundary.XminThermal('isothermal')
        boundary.XmaxThermal('isothermal')
        boundary.YminThermal('isothermal')
        boundary.YmaxThermal('isothermal')
        boundary.ZminThermal('isothermal')
        boundary.ZmaxThermal('isothermal')
        boundary.XsymmetryThermal('none')
        boundary.YsymmetryThermal('none')
        boundary.ZsymmetryThermal('none')
        boundary.ApplyInAllDirections('False')
        boundary.ApplyInAllDirectionsThermal('False')
        boundary.XminTemperature('')
        boundary.XminTemperatureType('None')
        boundary.XmaxTemperature('')
        boundary.XmaxTemperatureType('None')
        boundary.YminTemperature('')
        boundary.YminTemperatureType('None')
        boundary.YmaxTemperature('')
        boundary.YmaxTemperatureType('None')
        boundary.ZminTemperature('')
        boundary.ZminTemperatureType('None')
        boundary.ZmaxTemperature('')
        boundary.ZmaxTemperatureType('None')

        if xmin == 'unit cell':
            boundary.XPeriodicShift('0.0')
            boundary.YPeriodicShift('0.0')
            boundary.ZPeriodicShift('0.0')
            boundary.PeriodicUseConstantAngles('False')
            boundary.SetPeriodicBoundaryAngles('0.0', '0.0')
            boundary.SetPeriodicBoundaryAnglesDirection('outward')
            boundary.UnitCellFitToBoundingBox('True')
            boundary.UnitCellDs1('0.0')
            boundary.UnitCellDs2('0.0')
            boundary.UnitCellAngle('90.0')

        if xmin == 'expanded open':
            boundary.ReflectionLevel('0.0001')
            boundary.MinimumDistanceType('Fraction')
            boundary.MinimumDistancePerWavelengthNewMeshEngine('4')
            boundary.MinimumDistanceReferenceFrequencyType('CenterNMonitors')
            boundary.FrequencyForMinimumDistance(str(minfrequency))
            boundary.SetAbsoluteDistance('0.0')
            plot.DrawBox('True')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1
