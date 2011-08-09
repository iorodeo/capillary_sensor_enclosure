import scipy
from py2scad import *


class Capillary_Enclosure(Basic_Enclosure):

    def __init__(self,params):
        self.params = params
        self.add_sensor_mount_holes()
        self.add_capillary_holes()
        self.add_cable_hole()
        super(Capillary_Enclosure,self).__init__(self.params)

    def make(self):
        super(Capillary_Enclosure,self).make()
        self.make_rubber_band_notch()
        self.make_backlight_standoffs()
        self.make_led_plate()
        self.make_diffuser_plate()

    def get_assembly(self,**kwargs):
        parts_list = super(Capillary_Enclosure,self).get_assembly(**kwargs)

        # Add led plate
        x,y,z = self.params['inner_dimensions']
        led_standoff_length = self.params['led_standoff_length']
        led_plate = self.led_plate
        z_shift = 0.5*z - led_standoff_length 
        led_plate = Translate(led_plate,v=(0,0,z_shift))
        parts_list.append(led_plate)

        # Add diffuser plate
        diffuser_standoff_length = self.params['diffuser_standoff_length']
        diffuser_plate = self.diffuser_plate
        z_shift = 0.5*z - led_standoff_length - diffuser_standoff_length
        diffuser_plate = Translate(diffuser_plate, v=(0,0,z_shift))
        parts_list.append(diffuser_plate)

        return parts_list

    def get_projection(self,**kwargs):
        parts_list = super(Capillary_Enclosure,self).get_projection(**kwargs)

        wall_thickness = self.params['wall_thickness']
        spacing = kwargs['spacing_factor']*wall_thickness
        
        # Add led plate
        led_plate = self.led_plate
        led_plate = Projection(led_plate)
        parts_list.append(led_plate)

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
            x_pos, y_pos = hole_offset_x,-0.5*z + 0.5*hole_diam + hole_offset_y
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

    def add_cable_hole(self):
        hole_list = [] 
        hole_width = self.params['cable_hole_width']
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



