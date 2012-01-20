from py2scad import *
from arrayed_enclosure import Arrayed_Enclosure
from make_enclosure import params

params['number_of_sensors'] = 5
params['sensor_spacing'] = INCH2MM*2.0
params['array_bottom_overhang'] = 1.0*INCH2MM
params['bottom_mount_hole_diam'] = 0.2010*INCH2MM 
params['bottom_mount_hole_spacing'] = INCH2MM 
params['bottom_mount_hole_inset'] = 0.5*INCH2MM

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    enclosure = Arrayed_Enclosure(params)
    enclosure.make()

    part_assembly = enclosure.get_assembly(
            show_top=False,
            show_bottom=True, 
            show_front=False,
            show_back=False,
            show_left=False,
            show_right=False,
            show_standoffs=False,
            show_capillary=False,
            show_sensor=False,
            show_diffuser=False,
            show_diffuser_standoffs=False,
            show_led_pcb=False,
            show_guide_plates=False,
            show_guide_top=False,
            show_clamp=False,
            explode=(0,0,0),
            )
    prog_assembly = SCAD_Prog()
    prog_assembly.fn = 50
    prog_assembly.add(part_assembly)
    prog_assembly.write('arrayed_assembly.scad')

    box_projection = enclosure.get_box_projection()
    bottom_projection = enclosure.get_bottom_projection()
    diffuser_projection = enclosure.get_diffuser_projection()
    top_guide_projection = enclosure.get_guide_top_projection()
    side_guide_projection = enclosure.get_guide_side_projection()

    prog_box_projection = SCAD_Prog()
    prog_box_projection.fn = 50
    prog_box_projection.add(box_projection)
    prog_box_projection.write('arrayed_box_projection.scad')

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

    prog_bottom_projection = SCAD_Prog()
    prog_bottom_projection.fn = 50
    prog_bottom_projection.add(bottom_projection)
    prog_bottom_projection.write('arrayed_bottom_projection.scad')
