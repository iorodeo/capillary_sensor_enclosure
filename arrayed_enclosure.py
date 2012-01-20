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
        self.make_bottom_mount_holes()

    def make_array_bottom(self):
        number_of_sensors = self.params['number_of_sensors']
        sensor_spacing = self.params['sensor_spacing']
        thickness = self.params['wall_thickness']
        lid_radius = self.params['lid_radius']
        overhang = self.params['array_bottom_overhang']
        bottom_x_overhang = self.params['bottom_x_overhang']
        bottom_y_overhang = self.params['bottom_y_overhang']

        # Create larger bottom plate for arrayed sensor
        plate_x = self.bottom_x
        plate_y = self.bottom_y + sensor_spacing*number_of_sensors + 2*overhang
        self.array_bottom_size = plate_x, plate_y
        self.array_bottom =  rounded_box(plate_x,plate_y,thickness,radius=lid_radius,round_z=False)

        # Get list of holes in single capillary sensor
        hole_list = self.params['hole_list'] + self.tab_hole_list + self.standoff_hole_list
        bottom_holes = [hole for hole in hole_list if hole['panel'] == 'bottom']

        # Create list of bottom holes for arrayed sensor
        array_bottom_holes = []
        array_y_values = self.get_array_y_values()
        for hole in bottom_holes:
            for pos_y in array_y_values:
                hole_new = dict(hole)
                hole_x, hole_y = hole['location']
                hole_new['location'] = hole_x, hole_y + pos_y
                hole_new['panel'] = 'array_bottom'
                array_bottom_holes.append(hole_new)

        self.add_holes(array_bottom_holes)

    def make_bottom_mount_holes(self):
        hole_diam = self.params['bottom_mount_hole_diam'] 
        hole_spacing = self.params['bottom_mount_hole_spacing'] 
        hole_inset = self.params['bottom_mount_hole_inset'] 
        bottom_x, bottom_y = self.array_bottom_size

        hole_list = []
        for i in (-1,1):
            for j in (-1,1):
                x_pos = i*0.5*hole_spacing
                y_pos = j*(0.5*bottom_y - hole_inset)
                hole = {
                        'panel'     : 'array_bottom',
                        'type'      : 'round',
                        'location'  : (x_pos,y_pos),
                        'size'      : hole_diam,
                        }
                hole_list.append(hole)
        self.add_holes(hole_list)

    def get_assembly(self,**kwargs):
        show_bottom = kwargs['show_bottom']
        kwargs['show_bottom'] = False
        top_parts = super(Arrayed_Enclosure,self).get_assembly(**kwargs)
        parts_list = []

        # Array top parts
        pos_values = self.get_array_y_values()
        for pos in pos_values:
            parts_list.append(Translate(top_parts,v=(0,pos,0)))

        x,y,z = self.params['inner_dimensions']
        thickness = self.params['wall_thickness']
        z_shift = -0.5*z - 0.5*thickness
        array_bottom = Translate(self.array_bottom,v=(0,0,z_shift))
        if show_bottom:
            parts_list.append(array_bottom)

        return parts_list

    def get_box_projection(self,show_ref_cube=True,spacing_factor=4,project=True):
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        top_x_overhang = self.params['top_x_overhang']
        top_y_overhang = self.params['top_y_overhang']
        bottom_x_overhang = self.params['bottom_x_overhang']
        bottom_y_overhang = self.params['bottom_y_overhang']
        spacing = spacing_factor*wall_thickness
        bottom = self.bottom

        # Translate front panel
        y_shift = -(0.5*self.bottom_y + 0.5*inner_z + wall_thickness + spacing)
        front = Translate(self.front, v=(0,y_shift,0))

        # Translate back panel
        y_shift = 0.5*self.bottom_y + 0.5*inner_z + wall_thickness + spacing
        back = Rotate(self.back,a=180,v=(1,0,0)) # Rotate part so that outside face is up in projection
        back = Translate(back, v=(0,y_shift,0))

        # Rotate and Translate left panel
        left = Rotate(self.left,a=90,v=(0,0,1))
        left = Rotate(left,a=180,v=(0,1,0)) # Rotate part so that outside face is up in projection
        x_shift = -(0.5*self.bottom_x + 0.5*inner_z + wall_thickness + spacing)
        left = Translate(left, v=(x_shift,0,0))

        # Rotate and translate right panel
        right = Rotate(self.right,a=90,v=(0,0,1))
        x_shift = 0.5*self.bottom_x + 0.5*inner_z + wall_thickness + spacing
        right = Translate(right,v=(x_shift,0,0))

        # Create reference cube
        ref_cube = Cube(size=(INCH2MM,INCH2MM,INCH2MM))
        y_shift = 0.5*self.bottom_y + 0.5*INCH2MM + inner_z + 2*wall_thickness + 2*spacing
        ref_cube = Translate(ref_cube,v=(0,y_shift,0))

        # Add capillary clamp
        thickness = self.params['wall_thickness']
        clamp_x, clamp_y, clamp_z = self.clamp_size
        x_shift = 0.5*self.top_x + 0.5*clamp_x + spacing_factor*thickness
        y_shift = 0.5*self.top_y + 0.5*clamp_y + spacing_factor*thickness
        clamp = Translate(self.capillary_clamp,v=(x_shift,y_shift,0))

        # Create part list
        part_list = [self.top, front, back, left, right, clamp]
        if show_ref_cube == True:
            part_list.append(ref_cube)

        # Project parts
        part_list_proj = []
        for part in part_list:
            if project:
                part_list_proj.append(Projection(part))
            else:
                part_list_proj.append(part)

        return part_list_proj

    def get_bottom_projection(self,show_ref_cube=True,spacing_factor=4):
        thickness = self.params['wall_thickness']
        ref_cube = Cube(size=(INCH2MM,INCH2MM,INCH2MM))
        x_shift = 0.5*self.bottom_x + 0.5*INCH2MM + spacing_factor*thickness
        ref_cube = Translate(ref_cube,v=(x_shift,0,0))

        bottom = Projection(self.array_bottom)
        parts_list = [bottom]
        if show_ref_cube:
            parts_list.append(Projection(ref_cube))

        return parts_list


    def get_array_y_values(self):
        number_of_sensors = self.params['number_of_sensors']
        sensor_spacing = self.params['sensor_spacing']
        array_length = sensor_spacing*number_of_sensors
        pos_values = numpy.linspace(-0.5*array_length, 0.5*array_length, number_of_sensors)
        return pos_values





