"""
    Owl image commands
"""


class AbstractImageCommand:
    """Abstract image command"""
    def execute(self):
        pass


class ResampleImageCommand(AbstractImageCommand):
    """Resample image command"""
    def __init__(self, operator, *args):
        """Constructor

        :param operator: image operator
        :type operator: AbstractImageOperator
        """
        self.__operator = operator
        self.__args = args

    def execute(self):
        """Execute command"""
        self.__operator.resample(*self.__args)


class ConvertImageCommand(AbstractImageCommand):
    """Convert image command"""
    def __init__(self, operator, *args):
        """Constructor

        :param operator: image operator
        :type operator: AbstractImageOperator
        """
        self.__operator = operator
        self.__args = args

    def execute(self):
        """Execute command"""
        self.__operator.convert(*self.__args)


class SaturateImageCommand(AbstractImageCommand):
    """Saturate image command"""
    def __init__(self, operator, *args):
        """Constructor

        :param operator: image operator
        :type operator: AbstractImageOperator
        """
        self.__operator = operator
        self.__args = args

    def execute(self):
        """Execute command"""
        self.__operator.saturate(*self.__args)


class BlurImageCommand(AbstractImageCommand):
    """Blur image command"""
    def __init__(self, operator, *args):
        """Constructor

        :param operator: image operator
        :type operator: AbstractImageOperator
        """
        self.__operator = operator
        self.__args = args

    def execute(self):
        """Execute command"""
        self.__operator.blur(*self.__args)


class BrightImageCommand(AbstractImageCommand):
    """Saturate image command"""
    def __init__(self, operator, *args):
        """Constructor

        :param operator: image operator
        :type operator: AbstractImageOperator
        """
        self.__operator = operator
        self.__args = args

    def execute(self):
        """Execute command"""
        self.__operator.bright(*self.__args)
        
        
class WatermarkImageCommand(AbstractImageCommand):
    """Apply watermark to the image command"""
    def __init__(self, operator, *args):
        """Constructor

        :param operator: image operator
        :type operator: AbstractImageOperator
        """
        self.__operator = operator
        self.__args = args

    def execute(self):
        """Execute command"""
        self.__operator.watermark(*self.__args)
