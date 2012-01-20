import scipy
from py2scad import *


class Capillary_Enclosure(Basic_Enclosure):

    def __init__(self,params):
        self.params = params
        self.add_sensor_cutout()
        self.add_capillary_holes()
        self.add_guide_tap_holes()
        self.add_led_tap_holes()
        self.add_led_cable_hole()
        super(Capillary_Enclosure,self).__init__(self.params)

    def make(self):
        super(Capillary_Enclosure,self).make()
        self.make_sensor()
        self.make_capillary()
        self.make_guide_plates()
        self.make_led_pcb()
        self.make_diffuser()
        self.make_led_standoffs()
        self.make_capillary_clamp_thru_holes()
        self.make_capillary_clamp()

    def get_assembly(self,**kwargs):
        """
        Get enclosure assembly
        """
        try:
            show_sensor = kwargs['show_sensor']
        except KeyError:
            show_sensor = True
        try:
            show_capillary = kwargs['show_capillary']
        except KeyError:
            show_capillary = True
        try:
            show_guide_plates = kwargs['show_guide_plates']
        except KeyError:
            show_guide_plates = True
        try:
            show_guide_top = kwargs['show_guide_top']
        except KeyError:
            show_guide_top = True
        try:
            show_led_pcb = kwargs['show_led_pcb']
        except KeyError:
            show_led_pcb = True
        try:
            show_diffuser = kwargs['show_diffuser']
        except KeyError:
            show_diffuser = True
        try:
            show_diffuser_standoffs = kwargs['show_diffuser_standoffs']
        except KeyError:
            show_diffuser_standoffs = True
        try:
            explode = kwargs['explode']
        except KeyError:
            explode = (0,0,0)
        try:
            show_clamp = kwargs['show_clamp']
        except KeyError:
            show_clamp = True

        explode_x, explode_y, explode_z = explode

        parts_list = super(Capillary_Enclosure,self).get_assembly(**kwargs)
        x,y,z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']

        # Add sensor
        sensor_x, sensor_y, sensor_z = self.params['sensor_dimensions']
        sensor = self.sensor
        z_shift = -0.5*z-0.5*sensor_z - explode_z
        sensor = Translate(sensor,v=(0,0,z_shift))
        sensor = Color(sensor,rgba=(0.5,0.5,0.5))
        if show_sensor:
            parts_list.append(sensor)

        # Add capillary
        cap_offset_x = self.params['capillary_hole_offset']
        cap_hole_diam = self.params['capillary_diam']
        y_shift = cap_offset_x
        z_shift = -0.5*z + 0.5*cap_hole_diam  - explode_z
        capillary = self.capillary
        capillary = Translate(self.capillary,v=(0,y_shift,z_shift))
        if show_capillary:
            parts_list.append(capillary)
        
        # Add guide plate
        guide_x, guide_y, guide_z = self.params['guide_plate_dimensions']
        y_shift = 0.5*guide_y + 0.5*self.params['capillary_diam'] + cap_offset_x
        z_shift = -0.5*z + 0.5*guide_z
        guide_plate_pos = Translate(self.guide_plate_pos,v=[0,y_shift,z_shift])
        y_shift = -0.5*guide_y - 0.5*self.params['capillary_diam'] + cap_offset_x
        guide_plate_neg = Translate(self.guide_plate_neg,v=[0,y_shift,z_shift])
        y_shift = cap_offset_x
        z_shift = -0.5*z + 1.5*guide_z 
        guide_plate_top = Translate(self.guide_plate_top,v=[0,y_shift,z_shift])
        if show_guide_plates:
           parts_list.extend([guide_plate_pos,guide_plate_neg])
        if show_guide_top:
           parts_list.extend([guide_plate_top])


        # Add led pcb
        pcb_x, pcb_y, pcb_z = self.params['led_pcb_dimensions']
        z_shift = 0.5*z - 0.5*pcb_z
        led_pcb = Translate(self.led_pcb,v=(0,0,z_shift))
        if show_led_pcb:
            parts_list.append(led_pcb)

        # Add diffuser
        diff_x, diff_y, diff_z = self.params['diffuser_dimensions']
        diffuser_standoff_height = self.params['diffuser_standoff_height']
        z_shift = 0.5*z - pcb_z - 0.5*diff_z -  diffuser_standoff_height
        diffuser = Translate(self.diffuser,v=(0,0,z_shift))
        if show_diffuser:
            parts_list.append(diffuser)

        # Add diffuser standoffs
        led_hole_tuples = self.get_led_holes()
        z_shift = 0.5*z - pcb_z- 0.5*self.params['diffuser_standoff_height']
        for x_shift,y_shift, dummy in led_hole_tuples:
            if x_shift < 0:
                standoff = self.diffuser_standoff_neg
            else:
                standoff = self.diffuser_standoff_pos
            standoff = Translate(standoff,v=(x_shift,y_shift,z_shift))
            if show_diffuser_standoffs:
                parts_list.append(standoff)

        # Add capillary clamp
        bottom_x_overhang = self.params['bottom_x_overhang']
        clamp_x, clamp_y, clamp_z = self.clamp_size
        x_shift = 0.5*self.bottom_x - 0.5*bottom_x_overhang
        z_shift = -0.5*z + 0.5*wall_thickness + cap_hole_diam
        capillary_clamp = Translate(self.capillary_clamp,v=(x_shift,0,z_shift))
        if show_clamp:
            parts_list.append(capillary_clamp)

        return parts_list


    def get_box_projection(self,show_ref_cube=True, spacing_factor=4):
        """
        Get 2D projected layout of parts for laser cutting.
        """
        parts_list = super(Capillary_Enclosure,self).get_projection(show_ref_cube,spacing_factor)

        # Add capillary clamp
        thickness = self.params['wall_thickness']
        clamp_x, clamp_y, clamp_z = self.clamp_size
        x_shift = 0.5*self.bottom_x + 0.5*clamp_x + spacing_factor*thickness
        y_shift = 0.5*self.bottom_y + 0.5*clamp_y + spacing_factor*thickness
        clamp = Translate(self.capillary_clamp,v=(x_shift,y_shift,0))
        parts_list.append(Projection(clamp))
        return parts_list


    def get_guide_side_projection(self,show_ref_cube=True,spacing_factor=2):
        """
        Get 2D projected layout of the two side guide plates for laser cutting.
        """
        parts_list = []
        guide_x, guide_y, guide_z = self.params['guide_plate_dimensions']
        thickness = self.params['wall_thickness']

        # Add the side guide plates
        y_shift = 0.5*guide_y + 0.5*spacing_factor*thickness
        guide_plate_pos = Translate(self.guide_plate_pos,v=(0,y_shift,0))
        guide_plate_pos = Projection(guide_plate_pos)
        parts_list.append(guide_plate_pos)

        guide_plate_neg = Translate(self.guide_plate_neg,v=(0,-y_shift,0))
        guide_plate_neg = Projection(guide_plate_neg)
        parts_list.append(guide_plate_neg)

        # Add reference cube
        ref_cube = Cube(size=(INCH2MM, INCH2MM, INCH2MM))   
        x_shift = 0.5*guide_x + 0.5*INCH2MM + spacing_factor*thickness
        ref_cube = Translate(ref_cube,v=(x_shift,0,0))
        ref_cube = Projection(ref_cube)
        if show_ref_cube:
            parts_list.append(ref_cube)

        return parts_list


    def get_guide_top_projection(self,show_ref_cube=True,spacing_factor=2):
        """
        Get 2D projected layout of the top guide plate for laser cutting.
        """
        parts_list = []
        top_x, top_y, top_z = self.get_guide_plate_top_dim()
        thickness = self.params['wall_thickness']

        # Add top guide plate
        guide_plate_top = Projection(self.guide_plate_top)
        parts_list.append(guide_plate_top)

        # Add reference cube
        ref_cube = Cube(size=(INCH2MM, INCH2MM, INCH2MM))   
        x_shift = 0.5*top_x + 0.5*INCH2MM + spacing_factor*thickness
        ref_cube = Translate(ref_cube,v=(x_shift,0,0))
        ref_cube = Projection(ref_cube)
        if show_ref_cube:
            parts_list.append(ref_cube)

        return parts_list
        

    def get_diffuser_projection(self,show_ref_cube=True,spacing_factor=2):
        """
        Get 2D projected layout of the diffuser for laser cutting.
        """
        parts_list = []
        diff_x, diff_y, diff_z = self.params['diffuser_dimensions']
        thickness = self.params['wall_thickness']
        
        # Add diffuser
        diffuser = Projection(self.diffuser)
        parts_list.append(diffuser)

        # Add reference cube
        ref_cube = Cube(size=(INCH2MM, INCH2MM, INCH2MM))   
        x_shift = 0.5*diff_x + 0.5*INCH2MM + spacing_factor*thickness
        ref_cube = Translate(ref_cube,v=(x_shift,0,0))
        ref_cube = Projection(ref_cube)
        if show_ref_cube:
            parts_list.append(ref_cube)
        return parts_list


    def add_capillary_holes(self):
        """
        Add holes for capillary positioning
        """
        hole_x, hole_y, hole_r = self.params['capillary_hole_size']
        hole_y = 2*hole_y
        hole_offset_x =  self.params['capillary_hole_offset']
        x,y,z = self.params['inner_dimensions']
        panel_list= ('left', 'right')
        hole_list = [] 
        for panel in panel_list:
            pos_x = hole_offset_x
            pos_y = -0.5*z 
            hole = {
                    'panel'    : panel,
                    'type'     : 'rounded_square',
                    'location' : (pos_x, pos_y),
                    'size'     : (hole_x, hole_y, hole_r),
                    }
            hole_list.append(hole)
        self.params['hole_list'].extend(hole_list)

    def add_sensor_cutout(self):
        """
        Add cutout for sensor
        """
        hole_list = [] 
        sensor_width = self.params['sensor_width']
        sensor_length = self.params['sensor_length']
        hole_offset = self.params['sensor_hole_offset']
        x_pos = 0;
        y_pos = -hole_offset;
        hole = {
                    'panel'    : 'bottom', 
                    'type'     : 'square', 
                    'location' : (x_pos, y_pos),
                    'size'     : (sensor_length, sensor_width),
                    }
        hole_list.append(hole)
        self.params['hole_list'].extend(hole_list)

    def add_sensor_cable_hole(self):
        """
        Add cable hole for sensor.
        """
        hole_list = [] 
        hole_width = self.params['sensor_cable_hole_width']
        x,y,z = self.params['inner_dimensions']

        x_pos = 0
        y_pos = -0.5*z + 0.5*hole_width 
        hole = {
                'panel'     : 'front',
                'type'      : 'round',
                'location'  : (x_pos, y_pos),
                'size'      : hole_width,
                }
        hole_list.append(hole)

        x_pos = 0
        y_pos = -0.5*z
        hole = {
                'panel'    : 'front', 
                'type'     : 'square', 
                'location' : (x_pos, y_pos), 
                'size'     : (hole_width, hole_width),
                }
        hole_list.append(hole)

        self.params['hole_list'].extend(hole_list)

    def make_sensor(self):
        sensor_x, sensor_y, sensor_z = self.params['sensor_dimensions']
        hole_offset = self.params['sensor_hole_offset']
        hole_diam = self.params['sensor_mount_hole_diam']
        hole_space = self.params['sensor_mount_hole_space']

        # Create hole list 
        hole_list = []
        for i in (-1,1):
            x_pos = i*0.5*hole_space
            y_pos = hole_offset
            hole = (x_pos, y_pos,hole_diam)
            hole_list.append(hole)

        # Create sensor
        sensor = plate_w_holes(sensor_x, sensor_y, sensor_z, hole_list)
        self.sensor = Translate(sensor,v=(0,-hole_offset,0))

    def make_capillary(self):
        diameter = self.params['capillary_diam']
        length = self.params['capillary_length']
        r = 0.5*diameter
        capillary = Cylinder(h=length,r1=r,r2=r)
        capillary = Rotate(capillary, a=90, v=(0,1,0))
        self.capillary = capillary

    def make_guide_plates(self):
        guide_x, guide_y, guide_z = self.params['guide_plate_dimensions']
        hole_diam = self.params['guide_thru_hole_diam']
        hole_offset = self.params['guide_hole_offset']

        # Create pos and neg guide plates
        hole_list_pos = []
        hole_list_neg = []
        for i in (-1,1):
            x_pos = i*(0.5*guide_x - hole_offset) 
            y_pos = 0.5*guide_y - hole_offset 
            hole_pos = (x_pos, y_pos, hole_diam)
            hole_neg = (x_pos, -y_pos, hole_diam)
            hole_list_pos.append(hole_pos)
            hole_list_neg.append(hole_neg)
        self.guide_plate_pos = plate_w_holes(guide_x, guide_y, guide_z, holes=hole_list_pos)
        self.guide_plate_neg = plate_w_holes(guide_x, guide_y, guide_z, holes=hole_list_neg)

        # Create top guide plate
        top_x, top_y, top_z = self.get_guide_plate_top_dim()
        hole_list_top = self.get_guide_plate_holes(hole_type='through')
        self.guide_plate_top = plate_w_holes(top_x,top_y,top_z,holes=hole_list_top)

    def add_guide_tap_holes(self):
        hole_tuples = self.get_guide_plate_holes(hole_type='tap')
        hole_list = []
        for x,y,diam in hole_tuples:
            hole = {
                    'panel'    : 'bottom',
                    'type'     : 'round',
                    'location' : (x,y),
                    'size'     : diam,
                    }
            hole_list.append(hole)
        self.params['hole_list'].extend(hole_list)

    def get_guide_plate_holes(self,hole_type='through'):
        guide_x, guide_y, guide_z = self.params['guide_plate_dimensions']
        hole_offset = self.params['guide_hole_offset']
        if hole_type == 'through':
            hole_diam = self.params['guide_thru_hole_diam']
        else:
            hole_diam = self.params['guide_tap_hole_diam']
        hole_list = []
        top_x, top_y, top_z = self.get_guide_plate_top_dim()
        for i in (-1,1):
            for j in (-1,1):
                x_pos = i*(0.5*top_x - hole_offset)
                y_pos = j*(0.5*top_y - hole_offset)
                hole = (x_pos, y_pos, hole_diam)
                hole_list.append(hole)
        return hole_list

    def get_guide_plate_top_dim(self):
        guide_x, guide_y, guide_z = self.params['guide_plate_dimensions']
        top_x = guide_x
        top_y = 2*guide_y + self.params['capillary_diam']
        top_z = guide_z
        return top_x, top_y, top_z

    def make_led_pcb(self):
        led_x, led_y, led_z = self.params['led_pcb_dimensions']
        hole_list = self.get_led_holes(hole_type='through')
        #print hole_list
        self.led_pcb = plate_w_holes(led_x, led_y, led_z, holes=hole_list)

    def make_diffuser(self):
        diff_x, diff_y, diff_z = self.params['diffuser_dimensions']
        hole_list = self.get_led_holes(hole_type='through')
        self.diffuser = plate_w_holes(diff_x, diff_y, diff_z, holes=hole_list)

    def add_led_tap_holes(self):
        hole_tuples = self.get_led_holes(hole_type='tap')
        hole_list = []
        for x,y,diam in hole_tuples:
            hole = {
                    'panel'    : 'top',
                    'type'     : 'round',
                    'location' : (x,y),
                    'size'     : diam,
                    }
            hole_list.append(hole)
        self.params['hole_list'].extend(hole_list)

    def get_led_holes(self, hole_type='through'):
        led_x, led_y, led_z = self.params['led_pcb_dimensions']
        hole_offset = self.params['led_pcb_hole_offset']
        if hole_type == 'through':
            diam = self.params['led_pcb_thru_hole_diam']
        else:
            diam = self.params['led_pcb_tap_hole_diam']
        hole_list = []
        for i in (-1,1):
            x_pos = i*(0.5*led_x - hole_offset)
            y_pos = 0.5*led_y - hole_offset
            hole = (x_pos, y_pos, diam)
            hole_list.append(hole)
        return hole_list

    def make_led_standoffs(self):
        height = self.params['diffuser_standoff_height']
        diam = self.params['diffuser_standoff_diam']
        radius = 0.5*diam
        self.diffuser_standoff_pos = Cylinder(h=height,r1=radius,r2=radius)
        self.diffuser_standoff_neg = Cylinder(h=height,r1=radius,r2=radius)

    def add_led_cable_hole(self):
        hole_size_x, hole_size_y = self.params['led_cable_hole_size']
        hole_pos_x, hole_pos_y = self.params['led_cable_hole_pos']
        #print hole_pos_x, hole_pos_y
        hole = {
                'panel'     : 'bottom',
                'type'      : 'square',
                'location'  : (hole_pos_x, hole_pos_y),
                'size'      : (hole_size_x, hole_size_y),
                }
        self.params['hole_list'].append(hole)

    def make_capillary_clamp_thru_holes(self):
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        bottom_x_overhang = self.params['bottom_x_overhang']
        hole_diam = self.params['capillary_clamp_thru_hole_diam']
        hole_offset = self.params['capillary_clamp_hole_offset']

        hole_list = []
        for i in (-1,1):
            x_pos = i*(0.5*self.bottom_x - 0.5*bottom_x_overhang)
            y_pos = hole_offset 
            hole = {
                    'panel'    : 'bottom',
                    'type'     : 'round',
                    'location' : (x_pos, y_pos),
                    'size'     : hole_diam,
                    }
            hole_list.append(hole)

        self.params['hole_list'].extend(hole_list)
        self.add_holes(hole_list)

    def make_capillary_clamp(self):
        bottom_x_overhang = self.params['bottom_x_overhang']
        wall_thickness = self.params['wall_thickness']
        clamp_length = self.params['capillary_clamp_length']
        clamp_tolerance = self.params['capillary_clamp_tolerance']
        clamp_radius = self.params['capillary_clamp_radius']
        hole_offset = self.params['capillary_clamp_hole_offset']
        hole_diam = self.params['capillary_clamp_tap_hole_diam']

        clamp_x = bottom_x_overhang - 2*clamp_tolerance
        clamp_y = clamp_length
        clamp_z = wall_thickness 
        self.clamp_size = clamp_x, clamp_y, clamp_z

        hole_list = [(0,hole_offset,hole_diam)]

        clamp = plate_w_holes(clamp_x,clamp_y,clamp_z,hole_list,radius=clamp_radius)
        self.capillary_clamp = clamp






