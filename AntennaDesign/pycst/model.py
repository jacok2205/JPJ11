# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 20:40:37 2022

@author: Will
@contributor: jacok2205

Provides modelling functionality 
"""
from AntennaDesign.pycst.config import debug as debug


# Modelling options
##############################################################################
def add(mws, component1, solid1, component2, solid2):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    component1 : TYPE
        DESCRIPTION
    component2 : TYPE
        DESCRIPTION

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mws.Solid.Add(f'{component1}:{solid1}', f'{component2}:{solid2}')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def subtract(mws, component1, solid1, component2, solid2):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    component1 : TYPE
        DESCRIPTION
    component2 : TYPE
        DESCRIPTION

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mws.Solid.Subtract(f'{component1}:{solid1}', f'{component2}:{solid2}')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def insert(mws, component1, solid1, component2, solid2):
    try:
        mws.Solid.Insert(f'{component1}:{solid1}', f'{component2}:{solid2}')
    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def align_wcs_with_face(mws):
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
        wcs = mws.WCS
        wcs.AlignWCSWithSelected('Face')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def align_wcs_with_point(mws):
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
        wcs = mws.WCS
        wcs.AlignWCSWithSelected('Point')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def clear_picks(mws):
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
        pick = mws.Pick
        pick.ClearAllPicks()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def pick_edge(mws, componentName, position):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    componentName : TYPE
        DESCRIPTION.
    position : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        pick = mws.Pick
        pick.PickEdgeFromId((f'component1:{componentName}'), str(position), str(position))

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def pick_face(mws, name, _id):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    name : TYPE
        DESCRIPTION
    _id : TYPE
        DESCRIPTION

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        pick = mws.Pick
        pick.PickFaceFromId((f'component1:{name}'), str(_id))

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def pick_face_from_point(mws, component, name, xPoint, yPoint, zPoint):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    component : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.
    xPoint : TYPE
        DESCRIPTION.
    yPoint : TYPE
        DESCRIPTION.
    zPoint : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        pick = mws.Pick
        pick.PickFaceFromPoint((f'component1:{name}'), str(xPoint), str(yPoint), str(zPoint))

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def pick_mid_point(mws, name, _id):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    name : TYPE
        DESCRIPTION.
    _id : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        pick = mws.Pick
        pick.PickMidpointFromId((f'component1:{name}'), str(_id))

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


# Shapes
##############################################################################
def brick(mws, name, component, material, xrange, yrange, zrange):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    name : TYPE
        DESCRIPTION.
    component : TYPE
        DESCRIPTION.
    material : TYPE
        DESCRIPTION.
    xrange : TYPE
        DESCRIPTION.
    yrange : TYPE
        DESCRIPTION.
    zrange : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        brick = mws.Brick
        brick.Reset()
        brick.Name(name)
        brick.Component(component)
        brick.Material(material)
        brick.xrange(str(xrange[0]), str(xrange[1]))
        brick.yrange(str(yrange[0]), str(yrange[1]))
        brick.zrange(str(zrange[0]), str(zrange[1]))
        brick.Create

        format(brick)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def cylinder(mws, name, component, material, orientation, outerRadius, innerRadius, Xcenter=None, Ycenter=None,
             Zcenter=None, Xrange=None, Yrange=None, Zrange=None, segments=0):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    name : TYPE
        DESCRIPTION.
    component : TYPE
        DESCRIPTION
    material : TYPE
        DESCRIPTION.
    orientation : TYPE
        DESCRIPTION.
    outerRadius : TYPE
        DESCRIPTION.
    innerRadius : TYPE
        DESCRIPTION.
    Xcenter : TYPE
        DESCRIPTION.
    Ycenter : TYPE
        DESCRIPTION.
    Zcenter : TYPE
        DESCRIPTION.
    Xrange : TYPE
        DESCRIPTION.
    Yrange : TYPE
        DESCRIPTION.
    Zrange : TYPE
        DESCRIPTION.
    segments : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        cylinder = mws.Cylinder
        cylinder.Reset()
        cylinder.Name(name)
        cylinder.Component(component)
        cylinder.Material(material)
        cylinder.Axis(orientation)
        cylinder.Outerradius(outerRadius)
        cylinder.Innerradius(innerRadius)

        if orientation == 'Z':
            cylinder.Xcenter(str(Xcenter))
            cylinder.Ycenter(str(Ycenter))
            cylinder.Zrange(str(Zrange[0]), str(Zrange[1]))
        elif orientation == 'X':
            cylinder.Ycenter(str(Ycenter))
            cylinder.Zcenter(str(Zcenter))
            cylinder.Xrange(str(Xrange[0]), str(Xrange[1]))
        elif orientation == 'Y':
            cylinder.Xcenter(str(Xcenter))
            cylinder.Zcenter(str(Zcenter))
            cylinder.Yrange(str(Yrange[0]), str(Yrange[1]))

        cylinder.Segments(segments)

        cylinder.Create()
        format(cylinder)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def sphere(mws, name, component, material, axis, centreRadius, topRadius, bottomRadius, centre):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    name : TYPE
        DESCRIPTION.
    component : TYPE
        DESCRIPTION.
    material : TYPE
        DESCRIPTION.
    axis : TYPE
        DESCRIPTION.
    centreRadius : TYPE
        DESCRIPTION.
    topRadius : TYPE
        DESCRIPTION.
    bottomRadius : TYPE
        DESCRIPTION.
    centre : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        sphere = mws.Sphere
        sphere.Reset()
        sphere.Name(name)
        sphere.Component(component)
        sphere.Material(material)
        sphere.Axis(axis)
        sphere.CenterRadius(str(centreRadius))
        sphere.TopRadius(str(topRadius))
        sphere.BottomRadius(str(bottomRadius))
        sphere.Centre(str(centre(0)), str(centre(1)), str(centre(2)))
        sphere.Segments('0')
        sphere.Create()
        format(sphere)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


# Delete shape(s) and component(s)
##############################################################################
def delete_solid(mws, component, solid):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    component : TYPE
        DESCRIPTION.
    solid : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mws.Solid.Delete(f'{component}:{solid}')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def delete_component(mws, component):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    component : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mws.Component.Delete(f'{component}')

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1
