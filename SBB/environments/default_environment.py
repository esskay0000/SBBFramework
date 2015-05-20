import abc

class DefaultPoint(object):
    """
    Encapsulates a value from the environment as a point.
    """

    def __init__(self, point_id, inputs):
        self.point_id = point_id
        self.inputs = inputs

class DefaultEnvironment(object):
    """
    Abstract class for environments. All environments must implement these 
    methods to be able to work with SBB.
    """
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        """
        Initialize the environment variables.
        """

    @abc.abstractmethod
    def reset_point_population(self):
         """
         Method that is called at the beginning of each run by SBB, to reset the 
         variables that will be used by the generations.
         """

    @abc.abstractmethod
    def setup_point_population(self):
         """
         Method that is called at the beginning of each generation by SBB, to set the 
         variables that will be used by the generation.
         """

    @abc.abstractmethod
    def point_population(self):
         """
         Returns a list of Points
         """

    @abc.abstractmethod
    def evaluate(self, team, is_training=False):
        """
        Evaluate the team using the environment inputs. May be executed in the training
        or the test mode.
        This method must set the attribute results_per_points of the team, if you intend to 
        use pareto.
        """

    @abc.abstractmethod
    def metrics(self):
        """
        Generate a string with the metrics for the environment. It is printed at the 
        start and at the end of the execution, and it is also saved in the output file.
        """