import subprocess
import os.path
from py2scad import *
from arrayed_enclosure import Arrayed_Enclosure
from make_enclosure import params

create_dxf = False 

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

    # Display size of bottom plate.
    print [x/INCH2MM for x in enclosure.array_bottom_size]

    part_assembly = enclosure.get_assembly(
            show_top=True,
            show_bottom=True, 
            show_front=True,
            show_back=True,
            show_left=True,
            show_right=True,
            show_standoffs=True,
            show_capillary=True,
            show_sensor=True,
            show_diffuser=True,
            show_diffuser_standoffs=True,
            show_led_pcb=True,
            show_guide_plates=True,
            show_guide_top=True,
            show_clamp=True,
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

    # Create scad files
    filename = 'arrayed_box_projection.scad'
    scad_projection_files = []
    prog_box_projection = SCAD_Prog()
    prog_box_projection.fn = 50
    prog_box_projection.add(box_projection)
    prog_box_projection.write(filename)
    scad_projection_files.append(filename)

    filename = 'diffuser_projection.scad'
    prog_diffuser_projection = SCAD_Prog()
    prog_diffuser_projection.fn = 50
    prog_diffuser_projection.add(diffuser_projection)
    prog_diffuser_projection.write(filename)
    scad_projection_files.append(filename)
    
    filename = 'top_guide_projection.scad'
    prog_top_guide_projection = SCAD_Prog()
    prog_top_guide_projection.fn = 50
    prog_top_guide_projection.add(top_guide_projection)
    prog_top_guide_projection.write(filename)
    scad_projection_files.append(filename)
    
    filename = 'side_guide_projection.scad'
    prog_side_guide_projection = SCAD_Prog()
    prog_side_guide_projection.fn = 50
    prog_side_guide_projection.add(side_guide_projection)
    prog_side_guide_projection.write(filename)
    scad_projection_files.append(filename)

    filename = 'arrayed_bottom_projection.scad'
    prog_bottom_projection = SCAD_Prog()
    prog_bottom_projection.fn = 50
    prog_bottom_projection.add(bottom_projection)
    prog_bottom_projection.write(filename)
    scad_projection_files.append(filename)

    # Create dxf files
    if create_dxf:
        for scad_name in scad_projection_files:
            base_name, ext = os.path.splitext(scad_name)
            dxf_name = '{0}.dxf'.format(base_name)
            print '{0} -> {1}'.format(scad_name, dxf_name)
            subprocess.call(['openscad', '-x', dxf_name, scad_name])


