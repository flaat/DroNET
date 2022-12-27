from src.drawing import stddraw
from src.entities.environment.environment import Environment
from collections import defaultdict
from src.simulation.configurator import Configurator


# printer the environment
class PathPlanningDrawer:

    def __init__(self, env: Environment, borders=False, padding=25):
        """ init the path plannind drawer """
        self.width = env.width
        self.height = env.height
        self.borders = borders
        self.config = Configurator().configuration
        stddraw.setXscale(0 - padding, self.width + padding)
        stddraw.setYscale(0 - padding, self.height + padding)
        if self.borders:
            self.__borders_plot()

        # self.__grid_plot()
        self.keep_indictor = defaultdict(list)  # list of couples (time stamp, drone)

    def save(self, filename):
        """
        saves the current plot in the specified file
        @param filename: file in which to dump data
        """
        stddraw.save(filename)

    def __borders_plot(self):
        """
        draws the borders in the simulation window representing the borders of the environment
        @return:
        """
        stddraw.setPenColor(c=stddraw.RED)
        stddraw.setPenRadius(0.0025)
        stddraw.line(0, 0, 0, self.width)
        stddraw.line(0, 0, self.height, 0)
        stddraw.line(0, self.width, self.height, self.width)
        stddraw.line(self.height, 0, self.height, self.width)
        self.__reset_pen()

    # TODO: i feel like this method is useless: if you need a specific color and a specific radius this will be used,
    #  but sometimes you need another color with the same thickness and the setPenColor and setPenRadius methods will
    #  be called manually. What's the point?
    @staticmethod
    def __reset_pen():
        """
        Reset the pen into the default values
        @return:
        """
        stddraw.setPenColor(c=stddraw.BLACK)
        stddraw.setPenRadius(0.0055)

    def draw_drone(self, drone):
        """
        Draw the drone object on the pygame canvas
        @param drone:
        @return:
        """
        coords = drone.coordinates

        # change color when find a packet
        if drone.buffer_length > 0:
            stddraw.setPenColor(c=stddraw.GREEN)

        else:
            stddraw.setPenColor(c=stddraw.BLACK)

        stddraw.setPenRadius(0.0055)
        stddraw.point(coords[0], coords[1])

        self.__draw_drone_info(drone)
        self.__draw_communication_range(drone)

        # TODO: why draw the sensing range for all drones if it is always zero?
        self.__draw_sensing_range(drone)
        self.__reset_pen()

        if self.config.show_dir_vec:
            self.__draw_next_target(drone.coordinates, drone.next_target())

    def update(self, rate=1, save=False, show=True, filename=None):
        """
        Update the canvas
        @param rate:
        @param save:
        @param show:
        @param filename:
        @return:
        """
        if self.borders:
            self.__borders_plot()

        if show:
            stddraw.show(rate)

        if save:
            assert (filename is not None)
            self.save(filename)

        stddraw.clear()

    def draw_event(self, event):
        """
        draws the event @event by briefly changing the color of a dot in the middle of the drone representation.
        @param event: An event object.
        @return:
        """
        coords = event.coordinates
        stddraw.setPenRadius(0.0055)
        stddraw.setPenColor(c=stddraw.RED)
        stddraw.point(coords[0], coords[1])
        stddraw.setPenColor()
        self.__reset_pen()

    def draw_depot(self, depot):
        """
        This function draw the depot on the PyGame Canvas
        @param depot: A depot Object
        @return: None
        """
        coords = depot.coordinates

        # Set pen style and radius
        pen_radius = 0.01
        stddraw.setPenRadius(pen_radius)
        stddraw.setPenColor(c=stddraw.DARK_RED)

        # Set depot draw size
        size_depot = 50

        # Draw the depot polygon
        stddraw.filledPolygon([coords[0] - (size_depot / 2),
                               coords[0],
                               coords[0] + (size_depot / 2)],
                              [coords[1],
                               coords[1] + size_depot,
                               coords[1]])

        self.__draw_communication_range(depot)
        self.__reset_pen()

        # draw the buffer size
        stddraw.setPenRadius(0.0125)
        stddraw.setPenColor(c=stddraw.BLACK)
        stddraw.text(depot.coordinates[0], depot.coordinates[1] + 100, "pk: " + str(len(depot.all_packets)))

    @staticmethod
    def __draw_sensing_range(body):
        """
        Draws sensing range of an object, either a drone or a depot. It gets drawn as a Red circle around the entity
        @param body:
        @return:
        """

        # Set pen radius and color
        stddraw.setPenRadius(0.0015)
        stddraw.setPenColor(c=stddraw.RED)

        # Draws circle
        stddraw.circle(body.coordinates[0], body.coordinates[1],
                       body.sensing_range)

        # Resets color
        stddraw.setPenColor(c=stddraw.BLACK)

    @staticmethod
    def __draw_communication_range(object):
        """
        Draw a circle representing the object communication range
        @param object:
        @return:
        """

        # Set pen radius and color
        stddraw.setPenRadius(0.0015)
        stddraw.setPenColor(c=stddraw.BLUE)

        # Draw circle
        stddraw.circle(object.coordinates[0],
                       object.coordinates[1],
                       object.communication_range)

        # Resets color
        stddraw.setPenColor(c=stddraw.BLACK)

    # TODO: just a small thing on consistency: in all other methods we pass an object and then extract the data,
    #  now we directly pass the data. Which should we adopt?
    def __draw_next_target(self, drone_coo, target):
        """
        Draws a point representing the next target for the drone and a straight line that highlights the path to such point.
        @param drone_coo: coordinates of the drone
        @param target: the next target generated.
        @return:
        """
        stddraw.setPenRadius(0.0055)
        stddraw.setPenColor(c=stddraw.BLUE)
        stddraw.point(target[0], target[1])
        stddraw.setPenColor()
        self.__reset_pen()

        stddraw.setPenColor(c=stddraw.BLUE)
        stddraw.setPenRadius(0.0025)
        stddraw.line(drone_coo[0], drone_coo[1], target[0], target[1])
        self.__reset_pen()

    @staticmethod
    def __draw_drone_info(drone):
        """
        Draw all the infos about the current drone
        @param drone: The drone object
        @return:
        """
        stddraw.setPenRadius(0.0125)
        stddraw.setPenColor(c=stddraw.BLACK)

        # buffer
        stddraw.text(x=drone.coordinates[0],
                     y=drone.coordinates[1] + drone.communication_range / 3.0,
                     s=f"buffer: {str(drone.buffer_length)}")
        # speed
        stddraw.text(x=drone.coordinates[0],
                     y=drone.coordinates[1] + drone.communication_range / 3.0 - 30,
                     s=f"speed: {str(drone.speed)} m\\s")
        # index
        stddraw.text(x=drone.coordinates[0],
                     y=drone.coordinates[1] + (drone.communication_range / 2.0),
                     s="ID: " + str(drone.identifier))

        if drone.buffer_length > 0:

            stddraw.text(x=drone.coordinates[0],
                         y=drone.coordinates[1] - (drone.communication_range / 2.0),
                         s="retr: " + str(drone.routing_algorithm.current_n_transmission))

        # If the buffer is empty, do not show the retransmission counters since they are not updated
        else:

            stddraw.text(x=drone.coordinates[0],
                         y=drone.coordinates[1] - (drone.communication_range / 2.0),
                         s="retr: -- \\ --")

    def draw_simulation_info(self, cur_step, max_steps):
        """
        Draw the current simulation info
        @param cur_step: current timestep (integer)
        @param max_steps: maximum timestep (integer)
        @return: None
        """

        TEXT_LEFT = 60
        TEXT_TOP = 20

        stddraw.text(x=TEXT_LEFT + 20,
                     y=self.height - TEXT_TOP,
                     s=str(cur_step) + "/" + str(max_steps))

        self.__reset_pen()
