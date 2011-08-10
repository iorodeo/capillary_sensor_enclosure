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
        'inner_dimensions'                 : (x,y,z), 
        'wall_thickness'                   : 1.5, 
        'lid_radius'                       : 3.0,  
        'top_x_overhang'                   : 3.0,
        'top_y_overhang'                   : 3.0,
        'bottom_x_overhang'                : 3.0,
        'bottom_y_overhang'                : 3.0, 
        'lid2front_tabs'                   : (0.25,0.75),
        'lid2side_tabs'                    : (0.25, 0.75),
        'side2side_tabs'                   : (0.5,),
        'lid2front_tab_width'              : 7.0,
        'lid2side_tab_width'               : 7.0, 
        'side2side_tab_width'              : 7.0,
        'standoff_diameter'                : 0.25*INCH2MM,
        'standoff_offset'                  : 0.05*INCH2MM,
        'standoff_hole_diameter'           : 0.116*INCH2MM, 
        'capillary_hole_diam'              : 0.85,  
        'capillary_hole_offset'            : (0.25,3.32),
        'capillary_length'                 : 125.0,
        'rubber_band_notch_width'          : 2.0, 
        'led_plate_xy'                     : (x-3.0,y-17.0),
        'led_slot_xy'                      : (3.02,1.5), 
        'led_standoff_diam'                : 0.25*INCH2MM,
        'led_standoff_length'              : (1.0/4.0)*INCH2MM,
        'led_num'                          : 10, 
        'led_cable_hole_width'             : 3.0,
        'sensor_length'                    : 48.0,
        'diffuser_standoff_length'         : (1.0/4.0)*INCH2MM,
        'diffuser_standoff_diam'           : 0.25*INCH2MM,
        'diffuser_plate_xy'                : (x-3.0,y-17.0),
        'sensor_dimensions'                : (61.33,12.95,3.3),
        'sensor_hole_offset'               : 0.685,
        'sensor_cable_hole_width'          : 5.0, 
        'sensor_mount_hole_diam'           : 0.11*INCH2MM,
        'sensor_mount_hole_space'          : 57.40, 
        'capillary_clamp_hole_space'       : 22.0,
        'capillary_clamp_hole_diam'        : 0.11*INCH2MM,
        'capillary_clamp_standoff_diam'    : 0.25*INCH2MM, 
        'capillary_clamp_standoff_length'  : (5.0/32.0)*INCH2MM,
        'capillary_clamp_plate_dimensions' : (6.35,28.35,1.5),
        'hole_list'                        : hole_list,
        }


enclosure = Capillary_Enclosure(params)
enclosure.make()

part_assembly = enclosure.get_assembly(
        show_top=True,
        show_bottom=True, 
        show_front=True,
        show_back=True,
        show_left=True,
        show_right=True,
        show_led_plate=True,
        show_diffuser_plate=True,
        show_standoffs=True,
        show_led_standoffs=True,
        show_diffuser_standoffs=True,
        show_capillary=False,
        show_sensor=True,
        show_clamp_plates=True,
        show_clamp_standoffs=True,
        explode=(8,8,8),
        )


opaque_part_projection = enclosure.get_opaque_projection()
diffuser_projection = enclosure.get_diffuser_projection()

prog_assembly = SCAD_Prog()
prog_assembly.fn = 50
prog_assembly.add(part_assembly)
prog_assembly.write('enclosure_assembly.scad')

prog_opaque_projection = SCAD_Prog()
prog_opaque_projection.fn = 50
prog_opaque_projection.add(opaque_part_projection)
prog_opaque_projection.write('enclosure_opaque_projection.scad')

prog_diffuser_projection = SCAD_Prog()
prog_diffuser_projection.fn = 50
prog_diffuser_projection.add(diffuser_projection)
prog_diffuser_projection.write('enclosure_diffuser_projection.scad')
