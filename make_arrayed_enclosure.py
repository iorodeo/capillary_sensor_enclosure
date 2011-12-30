from py2scad import *
from arrayed_enclosure import Arrayed_Enclosure
from make_enclosure import params

params['number_of_sensors'] = 4
params['sensor_spacing'] = INCH2MM*2.0
params['array_bottom_overhang'] = 1.0*INCH2MM

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    enclosure = Arrayed_Enclosure(params)
    enclosure.make()

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
            show_led_pcb=True,
            show_guide_plates=True,
            explode=(0,0,0),
            )
    prog_assembly = SCAD_Prog()
    prog_assembly.fn = 50
    prog_assembly.add(part_assembly)
    prog_assembly.write('arrayed_assembly.scad')




