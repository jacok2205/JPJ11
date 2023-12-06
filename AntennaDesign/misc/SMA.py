"""
    Description:
    -----------
    This module is used for the declaration and construction of a SMA connector that will be practically used,
    specifically the SMA84NDA-0000 end launch SMA connector and only supports PCB thicknesses of 0.5 mm.

    The order of execution for constructing the SMA connector is as follows:
        -         First start with the shell-plate
        -         Subtract the plate with a cylinder that has an outer radius of the insulator and an inner
                  radius of the contact pin rod
        -         Add lower legs with shell-plate
        -         Add upper legs with shell-plate
        -         Insert contact pin
        -         Add contact pin rod with contact pin
        -         Insert insulator
        -         Add Ground cylinder with shell-plate
        -         Add waveguide port at the end of the SMA connector

    Global Variables:
    -----------------
    None.

    Imports:
    -------
    __init__:           The initialization module for the package.
    __config__:         Global variables to access from, according to what was configured from the user.

    Notes:
    -----
    The SMA connector can dynamically adjust itself to accommodate other PCB thicknesses where necessary. From the
    defaults, the SMA connector is again 0.57 mm (substrate 0.5 mm and 2 * 0.035 mm electrodeposited copper surfaces).
    For more documentation, see below for format standards.
"""

from AntennaDesign.cst_interface.__init__ import *
from AntennaDesign import __config__ as __config__


def get_sma_geometry(__x_shift__, __y_shift__, __z_shift__, __antenna_thickness__=0.57):
    """
    Description:
    ------------
    Generates the geometry for the SMA connector.

    Parameters:
    -----------
    __x_shift__:            float
                            Shifts all the parts of the SMA connector, along with the waveguide port, in the
                            x-direction.
    __y_shift__:            float
                            Shifts all the parts of the SMA connector, along with the waveguide port, in the
                            y-direction.
    __z_shift__:            float
                            Shifts all the parts of the SMA connector, along with the waveguide port, in the
                            z-direction.
    __antenna_thickness__:  float
                            A positive float value that defines the antenna thickness (substrate height +
                            conductor thicknesses). Default is 0.57 mm (0.5 mm substrate height + 2 * 0.035 mm
                            electrodeposited copper surfaces).

    Return:
    -------
    Returns the geometry, in priority order, of the SMA connector.

    Notes:
    ------
    The following are the properties/geometry components for the SMA connector.

    shell_plate:        list
                        The vertical rectangular portion of the SMA connector. This list is a brick shape as specified
                        from CST Microwave Studio Suite.
    lower_leg_1:        list
                        The first conductive leg of the SMA connector and is one of the lower legs of the SMA connector.
                        This list is a brick shape as specified from CST Microwave Studio Suite.
    lower_leg_2:        list
                        The second conductive leg of the SMA connector and is one of the other lower legs of the SMA
                        connector. This list is a brick shape as specified from CST Microwave Studio Suite.
    upper_leg_1:        list
                        The third conductive leg of the SMA connector and is one of the upper legs of the SMA connector.
                        This list is a brick shape as specified from CST Microwave Studio Suite.
    upper_leg_2:        list
                        The fourth conductive leg of the SMA connector and is one of the other upper leg of the SMA
                        connector. This list is a brick shape as specified from CST Microwave Studio Suite.
    contact_pin:        list
                        A centered pin that extends horizontally and is used to make contact to the transmission line/
                        feedline of the antenna. This list is a brick shape as specified from CST Microwave Studio
                        Suite.
    contact_pin_rod:    list
                        A positive conductive cylinder that is part of the contact_pin, but is added to the
                        contact_pin and does not occupy the portion where the contact_pin connects to the antenna's
                        feedline. This list is a cylinder shape as specified from CST Microwave Studio Suite.
    cylinder_void:      list
                        A cylinder to remove a cylinder volume from the shell_plate. This list is a cylinder shape as
                        specified from CST Microwave Studio Suite.
    insulator:          list
                        A cylinder that acts as the insulator of the SMA connector. This list is a cylinder shape as
                        specified from CST Microwave Studio Suite.
    ground:             list
                        A cylinder that covers the insulator and acts as the ground of the SMA connector. This list is
                        a cylinder shape as specified from CST Microwave Studio Suite.
    waveguide_port:     list
                        The features needed to construct a waveguide port as specified in the CST Microwave Studio
                        Suite software, see:
                        https://space.mit.edu/RADIO/CST_online/mergedProjects/3D/special_overview/special_overview_waveguideover.htm
    SMA_Connector:      list
                        Contains all the shapes needed to build the SMA connector, including the waveguide port. The
                        list is in priority order, where the first element has the highest priority and the last
                        element has the lowest priority with respect to building sequence.
    """

    # Brick
    # Format:
    # [Shape_Type, Solid_Name, Material_Name, Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, "'Add', 'Subtract', or 'None'", Add or
    # subtract operation for the provided list]
    # For more documentation, query the CST Microwave Studio Suite manual
    shell_plate = [
        'Brick',
        'Shell Plate',
        __config__.__material__[0],
        __x_shift__ - 6.35 / 2,
        __x_shift__ + 6.35 / 2,
        __y_shift__,
        __y_shift__ - 1.6,
        __z_shift__ - 2.55 + abs(0.57 - __antenna_thickness__),
        __z_shift__ + 6.35 - 2.55 + abs(0.57 - __antenna_thickness__),
        'None',
        []
    ]
    lower_leg_1 = [
        'Brick',
        'Lower Leg 1',
        __config__.__material__[0],
        __x_shift__ + 6.35 / 2,
        __x_shift__ + 6.35 / 2 - 1,
        __y_shift__,
        __y_shift__ + 4.7,
        __z_shift__ - 2.55 + abs(0.57 - __antenna_thickness__),
        __z_shift__,
        'Add',
        [shell_plate[1], 'Lower Leg 1']
    ]
    lower_leg_2 = [
        'Brick',
        'Lower Leg 2',
        __config__.__material__[0],
        __x_shift__ - 6.35 / 2,
        __x_shift__ - 6.35 / 2 + 1,
        __y_shift__,
        __y_shift__ + 4.7,
        __z_shift__ - 2.55 + abs(0.57 - __antenna_thickness__),
        __z_shift__,
        'Add',
        [shell_plate[1], 'Lower Leg 2']
    ]
    upper_leg_1 = [
        'Brick',
        'Upper Leg 1',
        __config__.__material__[0],
        __x_shift__ + 6.35 / 2,
        __x_shift__ + 6.35 / 2 - 1,
        __y_shift__,
        __y_shift__ + 4.7,
        __z_shift__ + 2.55 + 0.57 - 2.55 + abs(0.57 - __antenna_thickness__),
        __z_shift__ + 2.55 + 0.57 + 0.67 - 2.55 + abs(0.57 - __antenna_thickness__),
        'Add',
        [shell_plate[1], 'Upper Leg 1']
    ]
    upper_leg_2 = [
        'Brick',
        'Upper Leg 2',
        __config__.__material__[0],
        __x_shift__ - 6.35 / 2,
        __x_shift__ - 6.35 / 2 + 1,
        __y_shift__,
        __y_shift__ + 4.7,
        __z_shift__ + 2.55 + 0.57 - 2.55 + abs(0.57 - __antenna_thickness__),
        __z_shift__ + 2.55 + 0.57 + 0.67 - 2.55 + abs(0.57 - __antenna_thickness__),
        'Add',
        [shell_plate[1], 'Upper Leg 2']
    ]
    contact_pin = [
        'Brick',
        'Contact Pin',
        __config__.__material__[0],
        __x_shift__ - 0.5 / 2,
        __x_shift__ + 0.5 / 2,
        __y_shift__ + 2.5,
        __y_shift__ - 9.5,
        __z_shift__ + 2.55 + 0.57 - 2.55 + abs(0.57 - __antenna_thickness__),
        __z_shift__ + 2.55 + 0.57 + 0.25 - 2.55 + abs(0.57 - __antenna_thickness__),
        'None',
        []
    ]

    # Cylinder
    # Format:
    # [Shape_Type, Solid_Name, Material_Name, Normal, Outer_Radius, Inner_Radius,
    # Xcenter, Zcenter, Yrange, Num_of_Segments, "'Add', 'Subtract', or 'None'", Add or subtract
    # operation for the provided list]
    # For more documentation, query the CST Microwave Studio Suite
    contact_pin_rod = [
        'Cylinder',
        'Contact Pin Rod',
        __config__.__material__[0],
        __config__.__normal__,
        0.78,
        0.0,
        __x_shift__,
        __z_shift__ + 2.55 + 0.5 + 0.25 / 2 - 2.55 + abs(0.57 - __antenna_thickness__),
        [__y_shift__, __y_shift__ - 9.5],
        1000,
        'Add',
        [contact_pin[1], 'Contact Pin Rod']
    ]
    cylinder_void = [
        'Cylinder',
        'cylinder_sub',
        'Vacuum',
        __config__.__normal__,
        1.60,
        0.0,
        __x_shift__,
        __z_shift__ + 2.55 + 0.5 + 0.25 / 2 - 2.55 + abs(0.57 - __antenna_thickness__),
        [__y_shift__, __y_shift__ - 1.6],
        1000,
        'Subtract',
        [shell_plate[1], 'cylinder_sub']
    ]
    insulator = [
        'Cylinder',
        'Insulator',
        __config__.__material__[1],
        __config__.__normal__,
        1.60,
        0.78,
        __x_shift__,
        __z_shift__ + 2.55 + 0.5 + 0.25 / 2 - 2.55 + abs(0.57 - __antenna_thickness__),
        [__y_shift__, __y_shift__ - 9.5],
        1000,
        'None',
        []
    ]
    ground = [
        'Cylinder',
        'Ground',
        __config__.__material__[0],
        __config__.__normal__,
        2.65,
        1.6,
        __x_shift__,
        __z_shift__ + 2.55 + 0.5 + 0.25 / 2 - 2.55 + abs(0.57 - __antenna_thickness__),
        [__y_shift__ - 1.6, __y_shift__ - 9.5],
        1000,
        'Add',
        [shell_plate[1], 'Ground']
    ]

    # Waveguide Port
    # Format:
    # [Shape_Type, Port_Number, Normal_To, Orientation_of_Propagation, Coordinates, Xrange,
    # Yrange, Zrange, AddXrange, AddYrange, AddZrange]
    # For more documentation, query the CST Microwave Studio Suite
    waveguide_port = [
        'Waveguide',
        __config__.__port_number__,
        __config__.__normal__,
        __config__.__orientation__,
        __config__.__coordinates__,
        [__x_shift__ - 2.65, __x_shift__ + 2.65],
        [__y_shift__ - 9.5, __y_shift__ - 9.5],
        [__z_shift__ + 2.55 + 0.5 + 0.25 / 2 - 2.65 - 2.55 + abs(0.57 - __antenna_thickness__),
         __z_shift__ + 2.55 + 0.5 + 0.25 / 2 + 2.65 - 2.55 + abs(0.57 - __antenna_thickness__)],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0]
    ]

    # Group the above lists in priority order, i.e. the first element is the highest priority and the last element
    # is the lowest priority with respect to building sequence
    SMA_Connector = [shell_plate, lower_leg_1, lower_leg_2, upper_leg_1, upper_leg_2, cylinder_void, contact_pin,
                     contact_pin_rod, insulator, ground, waveguide_port]

    return SMA_Connector


def construct_SMA_connector(__mws__, __x_shift__=0, __y_shift__=0, __z_shift__=0, __antenna_thickness__=0.57):
    """
    Description:
    ------------
    Constructs the SMA connector along with its waveguide port. Note that the specific SMA connector used is
    the SMA84NDA-0000, which only supports a PCB thickness of 0.5 mm. The function can, however, also accommodate
    other PCB thicknesses, through manipulation of the lower legs, where necessary.

    Parameters:
    -----------
    __mws__:                Active3D Object
                            The Active3D object that was created from the win32com object (cst.Active3D()).
    __x_shift__:            float
                            Shifts all the parts of the SMA connector, along with the waveguide port, in the
                            x-direction. Default is 0.
    __y_shift__:            float
                            Shifts all the parts of the SMA connector, along with the waveguide port, in the
                            y-direction. Default is 0.
    __z_shift__:            float
                            Shifts all the parts of the SMA connector, along with the waveguide port, in the
                            z-direction. Default is 0.
    __antenna_thickness__:  float
                            A positive float value that defines the antenna thickness (substrate height(s) +
                            conductor thicknesses). Default is 0.57 mm (0.5 mm substrate height + 2 * 0.035 mm
                            electrodeposited copper surfaces).

    Return:
    ------
    None.

    Notes:
    -----
    None.
    """

    # Load material first
    for __i__ in __config__.__material__:
        pycst.load_material(mws=__mws__, name=__i__)

    # Retrieve the geometry parts of the SMA connector
    SMA_Connector = get_sma_geometry(__x_shift__=__x_shift__, __y_shift__=__y_shift__, __z_shift__=__z_shift__,
                                     __antenna_thickness__=__antenna_thickness__)

    for __i__ in SMA_Connector:

        # If a brick
        if __i__[0] == 'Brick':
            pycst.brick(mws=__mws__, name=__i__[1], component=__config__.__component__, material=__i__[2],
                        xrange=[__i__[3], __i__[4]],
                        yrange=[__i__[5], __i__[6]],
                        zrange=[__i__[7], __i__[8]])

            # Perform an 'Add' operation
            if __i__[9] == 'Add':
                pycst.add(mws=__mws__,
                          component1=__config__.__component__,
                          solid1=__i__[10][0],
                          component2=__config__.__component__,
                          solid2=__i__[10][1])

            # Perform a 'Subtract' operation
            elif __i__[9] == 'Subtract':
                pycst.subtract(mws=__mws__,
                               component1=__config__.__component__,
                               solid1=__i__[10][0],
                               component2=__i__[3],
                               solid2=__i__[10][1])

            # No operation was specified
            else:
                continue

        # If a cylinder
        elif __i__[0] == 'Cylinder':
            pycst.cylinder(mws=__mws__, name=__i__[1], component=__config__.__component__, material=__i__[2],
                           orientation=__i__[3],
                           outerRadius=__i__[4],
                           innerRadius=__i__[5],
                           Xcenter=__i__[6],
                           Zcenter=__i__[7],
                           Yrange=__i__[8],
                           segments=__i__[9])

            # Perform an 'Add' operation
            if __i__[10] == 'Add':
                pycst.add(mws=__mws__,
                          component1=__config__.__component__,
                          solid1=__i__[11][0],
                          component2=__config__.__component__,
                          solid2=__i__[11][1])

            # Perform a 'Subtract' operation
            elif __i__[10] == 'Subtract':
                pycst.subtract(mws=__mws__,
                               component1=__config__.__component__,
                               solid1=__i__[11][0],
                               component2=__config__.__component__,
                               solid2=__i__[11][1])

            # No operation was specified
            else:
                continue

        # If waveguide port
        elif __i__[0] == 'Waveguide':
            pycst.waveguide_port(mws=__mws__, portNumber=__i__[1], normal=__i__[2], orientation=__i__[3],
                                 coordinates=__i__[4], xrange=__i__[5], yrange=__i__[6], zrange=__i__[7],
                                 xrangeAdd=__i__[8], yrangeAdd=__i__[9], zrangeAdd=__i__[10])

        else:
            continue


def delete_SMA_connector(__mws__):
    """
    Description:
    ------------
    Deletes the connector, if present, as well as the waveguide port associated with the connector.

    Parameters:
    -----------
    mws :   Active3D Object
            The Active3D object that was created from the win32com object (cst.Active3D()).

    Return:
    ------
    None.

    Notes:
    -----
    None.
    """

    pycst.delete_component(mws=__mws__, component=__config__.__component__)
    pycst.delete_waveguide_port(mws=__mws__, port_number=__config__.__port_number__)
