"""
Creates an enclosure
"""
from py2scad import *
from capillary_enclosure import Capillary_Enclosure

INCH2MM = 25.4

# Inside dimensions
x,y,z = 70.0, 45.0, 1.25*INCH2MM 
hole_list = []

params = {
        'inner_dimensions'         : (x,y,z), 
        'wall_thickness'           : 1.5, 
        'lid_radius'               : 3.0,  
        'top_x_overhang'           : 3.0,
        'top_y_overhang'           : 3.0,
        'bottom_x_overhang'        : 3.0,
        'bottom_y_overhang'        : 3.0, 
        'lid2front_tabs'           : (0.25,0.75),
        'lid2side_tabs'            : (0.25, 0.75),
        'side2side_tabs'           : (0.5,),
        'lid2front_tab_width'      : 7.0,
        'lid2side_tab_width'       : 7.0, 
        'side2side_tab_width'      : 7.0,
        'standoff_diameter'        : 0.25*INCH2MM,
        'standoff_offset'          : 0.05*INCH2MM,
        'standoff_hole_diameter'   : 0.116*INCH2MM, 
        'hole_list'                : hole_list,
        'sensor_mount_hole_diam'   : 0.11*INCH2MM,
        'sensor_mount_hole_space'  : 57.40, 
        'capillary_hole_diam'      : 0.98,  
        'capillary_hole_offset'    : (0.25,3.26+0.5),
        'cable_hole_width'         : 5.0, 
        'rubber_band_notch_width'  : 2.0, 
        'led_plate_xy'             : (x-3.0,y-17.0),
        'led_slot_xy'              : (3.02,1.5), 
        'led_num'                  : 10, 
        'sensor_length'            : 48.0,
        'led_standoff_length'      : (3.0/8.0)*INCH2MM,
        'diffuser_standoff_length' : (3.0/8.0)*INCH2MM,
        'diffuser_plate_xy'        : (x-3.0,y-17.0),
        }

enclosure = Capillary_Enclosure(params)
enclosure.make()

part_assembly = enclosure.get_assembly(
        show_top=True,
        show_bottom=True, 
        show_front=False,
        show_back=False,
        explode=(10,10,10)
        )

part_projection = enclosure.get_projection()

prog_assembly = SCAD_Prog()
prog_assembly.fn = 50
prog_assembly.add(part_assembly)
prog_assembly.write('enclosure_assembly.scad')

prog_projection = SCAD_Prog()
prog_projection.fn = 50
prog_projection.add(part_projection)
prog_projection.write('enclosure_projection.scad')
