import numpy
from py2scad import *
from capillary_enclosure import Capillary_Enclosure


class Arrayed_Enclosure(Capillary_Enclosure):

    def __init__(self,params):
        self.params = params
        super(Arrayed_Enclosure,self).__init__(self.params)

    def make(self):
        super(Arrayed_Enclosure,self).make()
        self.make_array_bottom()

    def make_array_bottom(self):
        number_of_sensors = self.params['number_of_sensors']
        sensor_spacing = self.params['sensor_spacing']
        thickness = self.params['wall_thickness']
        lid_radius = self.params['lid_radius']
        overhang = self.params['array_bottom_overhang']
        bottom_x_overhang = self.params['bottom_x_overhang']
        bottom_y_overhang = self.params['bottom_y_overhang']

        # Get list of current bottom parts - shifted into position
        shifted_bottoms = []
        pos_values = self.get_array_positions()
        for pos in pos_values:
            shifted_bottoms.append(Translate(self.bottom,v=(0,pos,0)))

        # Get intersection plate
        plate_x = self.bottom_x
        plate_y = self.bottom_y + sensor_spacing*number_of_sensors + 2*overhang
        plate =  rounded_box(plate_x,plate_y,thickness,radius=lid_radius,round_z=False)

        # Remove holes in plate for arrayed bottoms 
        cut_block_list = []
        for pos in pos_values:
            cut_block = rounded_box(
                    self.bottom_x-bottom_x_overhang,
                    self.bottom_y-bottom_y_overhang,
                    2*thickness,
                    lid_radius,
                    round_z=False
                    )
            cut_block = Translate(cut_block,v=(0,pos,0))
            cut_block_list.append(cut_block)
        diff_list = [plate] + cut_block_list
        plate = Difference(diff_list)

        # Add in arrayed bottoms
        union_list = [plate] + shifted_bottoms
        self.array_bottom = Union(union_list) 



    def get_assembly(self,**kwargs):
        show_bottom = kwargs['show_bottom']
        kwargs['show_bottom'] = False
        top_parts = super(Arrayed_Enclosure,self).get_assembly(**kwargs)
        parts_list = []

        # Array top parts
        pos_values = self.get_array_positions()
        for pos in pos_values:
            parts_list.append(Translate(top_parts,v=(0,pos,0)))

        x,y,z = self.params['inner_dimensions']
        thickness = self.params['wall_thickness']
        z_shift = -0.5*z - 0.5*thickness
        array_bottom = Translate(self.array_bottom,v=(0,0,z_shift))
        if show_bottom:
            parts_list.append(array_bottom)

        return parts_list


    def get_array_positions(self):
        number_of_sensors = self.params['number_of_sensors']
        sensor_spacing = self.params['sensor_spacing']
        array_length = sensor_spacing*number_of_sensors
        pos_values = numpy.linspace(-0.5*array_length, 0.5*array_length, number_of_sensors)
        return pos_values





