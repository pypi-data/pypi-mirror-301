from .initializer_object import InitializerObject


class InitializerObjectInterface(InitializerObject):
    """
    Initializer used to initialize an Object from the interface.

    An initializer is created from a dictionary.
    The format is the following:

    - name: name of the initializer used as id
    - value_type: for Characteristic, the type of the value (as string)
    - subclass_initializer: name of sub initializer used to initialize sub BaseObject.
    \
                          For an object, the name of the subclass_initializer must be 'objectstate' \
                          These initializers must already exist in the game.
    """

    def __init__(self, game, initializer_dict: dict) -> None:
        """
        :param game: the game where the initializer is created
        :param initializer_dict: the dictionary used to create the initializer
        """
        super().__init__(game, initializer_dict)

        self.init_type = self.INIT_TYPE_INTERFACE
        """ initializer by interface """
