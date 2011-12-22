"""
Creates an enclosure
"""
from py2scad import *
from capillary_enclosure import Capillary_Enclosure

INCH2MM = 25.4

# Inside dimensions
x,y,z = 61.4, 45.0, 0.75*INCH2MM 
hole_list = []

params = {
        'inner_dimensions'                 : (x,y,z), 
        'wall_thickness'                   : 3.0, 
        'lid_radius'                       : 1.5,  
        'top_x_overhang'                   : 1.5,
        'top_y_overhang'                   : 1.5,
        'bottom_x_overhang'                : 8.0,
        'bottom_y_overhang'                : 3.0, 
        'lid2front_tabs'                   : (0.25,0.75),
        'lid2side_tabs'                    : (0.25, 0.75),
        'side2side_tabs'                   : (0.5,),
        'lid2front_tab_width'              : 7.0,
        'lid2side_tab_width'               : 7.0, 
        'side2side_tab_width'              : 7.0,
        'standoff_diameter'                : 0.1895*INCH2MM,
        'standoff_offset'                  : 0.05*INCH2MM,
        'standoff_hole_diameter'           : 0.089*INCH2MM, 
        'capillary_diam'                   : 1.0,
        'capillary_hole_size'              : (1.1,1.1,0.1),  
        'capillary_hole_offset'            : 0.25,
        'capillary_length'                 : 5*INCH2MM,
        'sensor_width'                     : 12.95,
        'sensor_length'                    : 61.33,
        'sensor_dimensions'                : (61.33,12.95,3.3),
        'sensor_hole_offset'               : 0.685,
        'sensor_mount_hole_space'          : 57.40, 
        'sensor_mount_hole_diam'           : 0.11*INCH2MM, 
        'led_pcb_dimensions'               : (61.0, 25.4, 1.7),
        'led_pcb_thru_hole_diam'           : 0.0890*INCH2MM,
        'led_pcb_tap_hole_diam'            : 0.0641*INCH2MM,
        'led_pcb_hole_offset'              : 0.15*INCH2MM,
        'led_cable_hole_size'              : (6.0,4.0),
        'led_cable_hole_pos'               : (0.0, 0.7*INCH2MM),
        'diffuser_dimensions'              : (61.0 ,25.4, 1.5),
        'diffuser_standoff_height'         : (7/32.0)*INCH2MM,
        'diffuser_standoff_diam'           : (3/16.0)*INCH2MM,
        'hole_list'                        : hole_list,
        'guide_plate_dimensions'           : (x-0.2, 0.5*INCH2MM, 0.0625*INCH2MM),
        'guide_thru_hole_diam'             : 0.0890*INCH2MM,
        'guide_tap_hole_diam'              : 0.0641*INCH2MM,
        'guide_hole_offset'                : 0.15*INCH2MM,
        }


enclosure = Capillary_Enclosure(params)
enclosure.make()

part_assembly = enclosure.get_assembly(
        show_top=False,
        show_bottom=False, 
        show_front=False,
        show_back=False,
        show_left=False,
        show_right=False,
        show_standoffs=True,
        show_capillary=True,
        show_sensor=True,
        show_diffuser=True,
        show_led_pcb=True,
        show_guide_plates=True,
        explode=(0,0,0),
        )


box_projection = enclosure.get_box_projection()
diffuser_projection = enclosure.get_diffuser_projection()
top_guide_projection = enclosure.get_guide_top_projection()
side_guide_projection = enclosure.get_guide_side_projection()

prog_assembly = SCAD_Prog()
prog_assembly.fn = 50
prog_assembly.add(part_assembly)
prog_assembly.write('enclosure_assembly.scad')

prog_box_projection = SCAD_Prog()
prog_box_projection.fn = 50
prog_box_projection.add(box_projection)
prog_box_projection.write('box_projection.scad')

prog_diffuser_projection = SCAD_Prog()
prog_diffuser_projection.fn = 50
prog_diffuser_projection.add(diffuser_projection)
prog_diffuser_projection.write('diffuser_projection.scad')

prog_top_guide_projection = SCAD_Prog()
prog_top_guide_projection.fn = 50
prog_top_guide_projection.add(top_guide_projection)
prog_top_guide_projection.write('top_guide_projection.scad')

prog_side_guide_projection = SCAD_Prog()
prog_side_guide_projection.fn = 50
prog_side_guide_projection.add(side_guide_projection)
prog_side_guide_projection.write('side_guide_projection.scad')

