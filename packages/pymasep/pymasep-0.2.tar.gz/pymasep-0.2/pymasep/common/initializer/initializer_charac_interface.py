from .initializer import Initializer


class InitializerCharacInterface(Initializer):
    """
    Initializer used to initialize a Characteristic from the interface.

    An initializer is created from a dictionary. The format is the following:

    - name: name of the initializer used as id
    - value_type: for Characteristic, the type of the value (as string)
    - subclass_initializer: name of sub initializer used to initialize sub BaseObject. \
                          These initializers must already exist in the game
    - value_mode: mode of the interface initialization : VALUE_MODE_*
    - param: for VALUE_MODE_DICE, string representing the dices and VALUE_MODE_CHOICE, list of tuples (description, value)
    """

    VALUE_MODE_VALUE = 'value'
    """ Value is chosen in the interface"""

    VALUE_MODE_DICE = 'dice'
    """ value is chosen by a dice interface"""

    VALUE_MODE_CHOICE = 'choice'
    """ value is chosen in the interface among some choices"""

    def __init__(self, game, initializer_dict: dict) -> None:
        """
        :param game: the game where the initializer is created
        :param initializer_dict: the dictionary used to create the initializer
        """
        super().__init__(game, initializer_dict)

        self.value_mode = initializer_dict.get('value_mode')
        """ Way of choosing the initializer value. see VALUE_MODE_*  """

        self.param = initializer_dict.get('param', None)
        """ parameter depending of initializer type """

        self.init_type = self.INIT_TYPE_INTERFACE
        """ initializer by interface """
