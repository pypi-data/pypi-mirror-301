from .initializer import Initializer


class InitializerFixed(Initializer):
    """
    Initialize Characteristic with fixed value

    An initializer is created from a dictionary.
    The format is the following:

    - name: name of the initializer used as id
    - value_type: for Characteristic, the type of the value (as string)
    - subclass_initializer: name of sub initializer used to initialize sub BaseObject.
    \
                          These initializers must already exist in the game
    - value: fixed value used to initialize the characteristic
    """

    def __init__(self, game, initializer_dict: dict) -> None:
        """
        :param game: the game where the initializer is created
        :param initializer_dict: the dictionary used to create the initializer
        """
        super().__init__(game, initializer_dict)

        self.fixed_value = initializer_dict['value']
        """ value used to initialize the characteristic """

    def apply(self, base_object) -> None:
        """
        Apply the initializer.

        :param base_object: The characteristic to initialize
        """
        base_object.value = self.fixed_value
