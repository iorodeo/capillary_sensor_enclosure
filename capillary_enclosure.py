import scipy
from py2scad import *


class Capillary_Enclosure(Basic_Enclosure):

    def __init__(self,params):
        self.params = params
        self.add_sensor_mount_holes()
        self.add_sensor_cable_hole()
        self.add_capillary_holes()
        self.add_capillary_clamp_holes()
        self.add_led_cable_hole()
        super(Capillary_Enclosure,self).__init__(self.params)

    def make(self):
        super(Capillary_Enclosure,self).make()
        #self.make_rubber_band_notch()
        self.make_backlight_standoffs()
        self.make_led_plate()
        self.make_diffuser_plate()
        self.make_sensor()
        self.make_clamp_standoffs()
        self.make_clamp_plates()
        self.make_led_standoffs()
        self.make_diffuser_standoffs()
        self.make_capillary()

    def get_assembly(self,**kwargs):
        """
        Get enclosure assembly
        """
        try:
            show_led_plate = kwargs['show_led_plate']
        except KeyError:
            show_led_plate = True
        try:
            show_diffuser_plate = kwargs['show_diffuser_plate']
        except KeyError:
            show_diffuser_plate = True
        try:
            show_sensor = kwargs['show_sensor']
        except KeyError:
            show_sensor = True
        try:
            show_clamp_standoffs = kwargs['show_clamp_standoffs']
        except KeyError:
            show_clamp_standoffs = True
        try:
            show_clamp_plates = kwargs['show_clamp_plates']
        except KeyError:
            show_clamp_plates = True
        try:
            show_led_standoffs = kwargs['show_led_standoffs']
        except KeyError:
            show_led_standoffs = True
        try:
            show_diffuser_standoffs = kwargs['show_diffuser_standoffs']
        except KeyError:
            show_diffuser_standoffs = True
        try:
            show_capillary = kwargs['show_capillary']
        except KeyError:
            show_capillary = True
        try:
            explode = kwargs['explode']
        except KeyError:
            explode = (0,0,0)
        explode_x, explode_y, explode_z = explode


        parts_list = super(Capillary_Enclosure,self).get_assembly(**kwargs)

        # Add led plate
        x,y,z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        led_standoff_length = self.params['led_standoff_length']
        led_plate = self.led_plate
        z_shift = 0.5*z - led_standoff_length - 0.5*wall_thickness 
        z_shift += explode_z
        led_plate = Translate(led_plate,v=(0,0,z_shift))
        if show_led_plate:
            parts_list.append(led_plate)

        # Add diffuser plate
        diffuser_standoff_length = self.params['diffuser_standoff_length']
        diffuser_plate = self.diffuser_plate
        z_shift = 0.5*z - 1.5*wall_thickness -  led_standoff_length - diffuser_standoff_length
        z_shift += explode_z
        diffuser_plate = Translate(diffuser_plate, v=(0,0,z_shift))
        if show_diffuser_plate:
            parts_list.append(diffuser_plate)

        # Add sensor
        sensor_x, sensor_y, sensor_z = self.params['sensor_dimensions']
        sensor = self.sensor
        z_shift = -0.5*z+0.5*sensor_z - explode_z
        sensor = Translate(sensor,v=(0,0,z_shift))
        if show_sensor:
            parts_list.append(sensor)

        # Add clamp standoffs
        clamp_standoff_length = self.params['capillary_clamp_standoff_length']
        z_shift = -0.5*z+0.5*clamp_standoff_length - explode_z
        for standoff in self.clamp_standoff_list:
            standoff = Translate(standoff,v=(0,0,z_shift))
            if show_clamp_standoffs:
                parts_list.append(standoff)

        # Add clamp plates
        plate_x, plate_y, plate_z = self.params['capillary_clamp_plate_dimensions']
        hole_space = self.params['sensor_mount_hole_space']
        for clamp_plate, sgn in zip(self.clamp_plate_list,(-1,1)):
            x_shift = 0.5*sgn*hole_space
            y_shift = 0
            z_shift = -0.5*z + 0.5*plate_z + clamp_standoff_length - explode_z
            clamp_plate = Translate(clamp_plate,v=(x_shift,y_shift,z_shift))
            if show_clamp_plates:
                parts_list.append(clamp_plate)

        # Add led standoffs
        led_standoff_length = self.params['led_standoff_length']
        z_shift = 0.5*z - 0.5*led_standoff_length
        z_shift += explode_z
        for standoff in self.led_standoff_list:
            standoff = Translate(standoff,v=(0,0,z_shift))
            if show_led_standoffs:
                parts_list.append(standoff)

        # Add diffuser standoffs
        diffuser_standoff_length = self.params['diffuser_standoff_length']
        z_shift = 0.5*z - led_standoff_length - wall_thickness - 0.5*diffuser_standoff_length
        z_shift += explode_z
        for standoff in self.diffuser_standoff_list:
            standoff = Translate(standoff,v=(0,0,z_shift))
            if show_diffuser_standoffs:
                parts_list.append(standoff)

        # Add capillary
        cap_offset_x, cap_offset_y = self.params['capillary_hole_offset']
        cap_hole_diam = self.params['capillary_hole_diam']
        y_shift = cap_offset_x
        z_shift = -0.5*z + 0.5*cap_hole_diam + cap_offset_y - explode_z
        capillary = self.capillary
        capillary = Translate(self.capillary,v=(0,y_shift,z_shift))
        if show_capillary:
            parts_list.append(capillary)
        
        return parts_list

    def get_opaque_projection(self,show_ref_cube=True, spacing_factor=4):
        """
        Get 2D projected layout of parts for laser cutting.
        """
        parts_list = super(Capillary_Enclosure,self).get_projection(show_ref_cube,spacing_factor)

        x,y,z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        spacing = spacing_factor*wall_thickness
        
        # Add led plate - two in case of mistakes
        led_plate_x, led_plate_y = self.params['led_plate_xy']
        led_plate = self.led_plate
        x_shift = 0.5*self.bottom_x + 0.5*led_plate_x + spacing
        y_shift = 0.5*self.bottom_y + 0.5*led_plate_y + spacing
        led_plate0 = Translate(led_plate,v=(x_shift,y_shift,0))
        led_plate1 = Translate(led_plate,v=(-x_shift,y_shift,0))
        led_plate0 = Projection(led_plate0)
        led_plate1 = Projection(led_plate1)
        parts_list.append(led_plate0)
        parts_list.append(led_plate1)

        # Add clamping plates
        clamp_x, clamp_y, clamp_z = self.params['capillary_clamp_plate_dimensions']
        for i in range(0,2):
            for clamp_plate, sgn in zip(self.clamp_plate_list,(-1,1)):
                x_shift = sgn*(0.5*self.bottom_x + 0.5*clamp_x + spacing)
                y_shift = -0.5*self.bottom_y -0.5*clamp_y - spacing - i*(spacing + clamp_y)
                clamp_plate = Translate(clamp_plate,v=(x_shift,y_shift,0))
                clamp_plate = Projection(clamp_plate)
                parts_list.append(clamp_plate)

        return parts_list

    def get_diffuser_projection(self,ref_cube=True,spacing_factor=4):
        """
        Get 2D projection for diffuser - projection is separate because different 
        materials will be used.
        """
        parts_list = []
        wall_thickness = self.params['wall_thickness']
        spacing = spacing_factor*wall_thickness

        # Add diffuer plate projection
        diffuser_plate = self.diffuser_plate
        diffuser_plate = Projection(diffuser_plate)
        parts_list.append(diffuser_plate)

        # Add reference cube
        diffuser_x, diffuser_y = self.params['diffuser_plate_xy']
        cube = Cube(size=(INCH2MM, INCH2MM, INCH2MM))
        x_shift = 0.0
        y_shift = 0.5*diffuser_y + 0.5*INCH2MM + spacing
        cube = Translate(cube,v=(x_shift,y_shift,0))
        cube = Projection(cube)
        if ref_cube:
            parts_list.append(cube)

        return parts_list 

    def add_capillary_holes(self):
        """
        Add holes for capillary positioning
        """
        hole_list = [] 
        hole_diam = self.params['capillary_hole_diam']
        hole_offset_x, hole_offset_y = self.params['capillary_hole_offset']
        x,y,z = self.params['inner_dimensions']
        panel_list= ('left', 'right')
        for panel in panel_list:
            x_pos = hole_offset_x
            y_pos = -0.5*z + 0.5*hole_diam + hole_offset_y
            hole = {
                    'panel'    : panel,
                    'type'     : 'round',
                    'location' : (x_pos, y_pos),
                    'size'     : hole_diam,
                    }
            hole_list.append(hole)
        self.params['hole_list'].extend(hole_list)

    def add_sensor_mount_holes(self):
        """
        Add mount holes for sensor
        """
        hole_list = [] 
        hole_diam = self.params['sensor_mount_hole_diam']
        hole_space = self.params['sensor_mount_hole_space']
        for i in (-1,1):
            x_pos, y_pos = i*0.5*hole_space, 0.0
            hole = {
                    'panel'    : 'bottom', 
                    'type'     : 'round', 
                    'location' : (x_pos, y_pos),
                    'size'     : hole_diam,
                    }
            hole_list.append(hole)
        self.params['hole_list'].extend(hole_list)

    def add_capillary_clamp_holes(self):
        """
        Add holes for clamping capillary in place
        """
        hole_list = []
        hole_diam = self.params['capillary_clamp_hole_diam']
        sensor_hole_space = self.params['sensor_mount_hole_space']
        clamp_hole_space = self.params['capillary_clamp_hole_space']
        self.capillary_clamp_holes_xy = []
        for i in (-1,1):
            for j in (-1,1):
                x_pos = 0.5*i*sensor_hole_space
                y_pos = 0.5*j*clamp_hole_space
                self.capillary_clamp_holes_xy.append((x_pos,y_pos))
                hole = {
                        'panel'    : 'bottom',
                        'type'     : 'round',
                        'location' : (x_pos,y_pos),
                        'size'     : hole_diam,
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

    def add_led_cable_hole(self):
        hole_list = []
        hole_width = self.params['led_cable_hole_width']
        x,y,z = self.params['inner_dimensions']

        x_pos = 0
        y_pos = 0.5*z - 0.5*hole_width 
        hole = {
                'panel'    : 'front',
                'type'     : 'round',
                'location' : (x_pos,y_pos),
                'size'     : hole_width,
                }
        hole_list.append(hole)

        x_pos = 0
        y_pos = 0.5*z
        hole = {
                'panel'    : 'front', 
                'type'     : 'square', 
                'location' : (x_pos, y_pos), 
                'size'     : (hole_width, hole_width),
                }
        hole_list.append(hole)
        self.params['hole_list'].extend(hole_list)

    def make_rubber_band_notch(self):
        hole_list = []
        hole_width = self.params['rubber_band_notch_width']
        sensor_space = self.params['sensor_mount_hole_space']
        x,y,z = self.params['inner_dimensions']

        # Create holes for bottom panel
        for i in (-1,1):
            for j in (-1,1):

                # Round portion of hole
                x_pos = i*0.5*sensor_space
                y_pos = j*(0.5*self.bottom_y - 0.5*hole_width)
                hole = {
                        'panel'    : 'bottom',
                        'type'     : 'round', 
                        'location' : (x_pos, y_pos),
                        'size'     : hole_width,
                        }
                hole_list.append(hole)

                # Rectangular portion of hole
                y_pos = j*0.5*self.bottom_y
                hole = {
                        'panel'    : 'bottom',
                        'type'     : 'square', 
                        'location' : (x_pos, y_pos), 
                        'size'     : (hole_width, hole_width),
                        }
                hole_list.append(hole)

        #Create holes for front and back panels
        panel_list = ('front' , 'back')
        for panel in panel_list:
            for i in (-1,1): 
                # Round portion of hole
                x_pos = i*0.5*sensor_space
                y_pos = -(0.5*z - 0.5*hole_width)
                hole = {
                        'panel'    : panel,
                        'type'     : 'round',
                        'location' : (x_pos, y_pos),
                        'size'     : hole_width,
                        }
                hole_list.append(hole)

                # Square portion of hole
                y_pos = -0.5*z
                hole = {
                        'panel'    : panel,
                        'type'     : 'square', 
                        'location' : (x_pos, y_pos),
                        'size'     : (hole_width, hole_width),
                        }
                hole_list.append(hole)

        self.add_holes(hole_list)


    def make_backlight_standoffs(self):
        hole_list = []
        hole_diam = self.params['standoff_hole_diameter']
        x_pos_list = [x for x,y in self.standoff_xy_pos]

        
        self.backlight_standoff_xy = []
        for x_pos in x_pos_list:
            y_pos = 0
            self.backlight_standoff_xy.append((x_pos,y_pos))
            hole = {
                    'panel'    : 'top',
                    'type'     : 'round',
                    'location' : (x_pos, y_pos),
                    'size'     : hole_diam,
                    }
            hole_list.append(hole)

        self.add_holes(hole_list)

    def make_led_plate(self):
        wall_thickness = self.params['wall_thickness']
        plate_x, plate_y = self.params['led_plate_xy']
        hole_diam = self.params['standoff_hole_diameter']
        sensor_length = self.params['sensor_length']
        led_num = self.params['led_num']
        led_slot_x, led_slot_y = self.params['led_slot_xy']

        self.led_plate = Cube(size=(plate_x,plate_y,wall_thickness))

        # Add standoff holes
        hole_list = []
        for x_pos, y_pos in self.backlight_standoff_xy:
            hole = {
                    'panel'    : 'led_plate',
                    'type'     : 'round',
                    'location' : (x_pos, y_pos),
                    'size'     : hole_diam,
                    }
            hole_list.append(hole)

        # Add led holes
        x_pos_array = scipy.linspace(-0.5*sensor_length + 1.0, 0.5*sensor_length -1.0, led_num)
        for x_pos in x_pos_array:
            y_pos = 0.0
            hole = {
                    'panel'    : 'led_plate',
                    'type'     : 'rounded_square',
                    'location' : (x_pos, y_pos),
                    'size'     : (led_slot_x, led_slot_y, 0.5*led_slot_y),
                    }
            hole_list.append(hole)
        
        self.add_holes(hole_list)

    def make_diffuser_plate(self):
        wall_thickness = self.params['wall_thickness']
        plate_x, plate_y = self.params['diffuser_plate_xy']
        hole_diam = self.params['standoff_hole_diameter']

        self.diffuser_plate = Cube(size=(plate_x,plate_y,wall_thickness))

        # Add standoff holes
        hole_list = []
        for x_pos, y_pos in self.backlight_standoff_xy:
            hole = {
                    'panel'    : 'diffuser_plate',
                    'type'     : 'round',
                    'location' : (x_pos, y_pos),
                    'size'     : hole_diam,
                    }
            hole_list.append(hole)
        self.add_holes(hole_list)

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

    def make_clamp_standoffs(self):
        hole_space = self.params['sensor_mount_hole_space']
        standoff_diam = self.params['capillary_clamp_standoff_diam']
        standoff_length = self.params['capillary_clamp_standoff_length']
        standoff_hole_diam = self.params['capillary_clamp_hole_diam']

        r = 0.5*standoff_diam
        standoff_template = Cylinder(h=standoff_length, r1=r, r2=r)
        r = 0.5*standoff_hole_diam
        cut_cyl = Cylinder(h=2*standoff_length, r1=r, r2=r)
        standoff_template = Difference([standoff_template,cut_cyl])
        
        self.clamp_standoff_list = []
        for x_pos, y_pos in self.capillary_clamp_holes_xy:
            standoff = Translate(standoff_template, v=(x_pos, y_pos,0))
            self.clamp_standoff_list.append(standoff)

    def make_clamp_plates(self):
        plate_x, plate_y, plate_z = self.params['capillary_clamp_plate_dimensions']
        clamp_hole_space = self.params['capillary_clamp_hole_space']
        hole_diam = self.params['capillary_clamp_hole_diam']

        # Create hole list
        hole_list = []
        for i in (-1,1):
            x_pos = 0.0
            y_pos = i*0.5*clamp_hole_space 
            hole = (x_pos, y_pos, hole_diam)
            hole_list.append(hole)

        # Create clamp plates
        self.clamp_plate_list = []
        for i in (0,2):
            clamp_plate = plate_w_holes(plate_x, plate_y, plate_z,hole_list)
            self.clamp_plate_list.append(clamp_plate)

    def make_led_standoffs(self):
        standoff_diam = self.params['led_standoff_diam']
        standoff_length = self.params['led_standoff_length']

        r = 0.5*standoff_diam
        standoff_template = Cylinder(h=standoff_length,r1=r,r2=r)

        self.led_standoff_list = []
        for x_pos, y_pos in self.backlight_standoff_xy:
            standoff = Translate(standoff_template,v=(x_pos, y_pos, 0))
            self.led_standoff_list.append(standoff)


    def make_diffuser_standoffs(self):
        standoff_diam = self.params['diffuser_standoff_diam']
        standoff_length = self.params['diffuser_standoff_length']
        r = 0.5*standoff_diam
        standoff_template = Cylinder(h=standoff_length,r1=r,r2=r)
        self.diffuser_standoff_list = []
        for x_pos, y_pos in self.backlight_standoff_xy:
            standoff = Translate(standoff_template,v=(x_pos,y_pos,0))
            self.diffuser_standoff_list.append(standoff)

    def make_capillary(self):
        diameter = self.params['capillary_hole_diam']
        length = self.params['capillary_length']
        r = 0.5*diameter
        capillary = Cylinder(h=length,r1=r,r2=r)
        capillary = Rotate(capillary, a=90, v=(0,1,0))
        self.capillary = capillary



