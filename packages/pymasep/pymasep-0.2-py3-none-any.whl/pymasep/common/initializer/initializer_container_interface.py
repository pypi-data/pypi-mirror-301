from .initializer_container import InitializerContainer


class InitializerContainerInterface(InitializerContainer):
    """
    Initializer used to initialize a Container by the interface
    An initializer can be executed by the Engine (by default) or processed by the Interface.

    An initializer is created from a dictionary. The format is the following:

    - name: name of the initializer used as id
    - type: type of initialization. ALL: all the objects in obj_init will be created. BUY: the player must choose the objects to buy
    - obj_init : dictionary containing the name of the objects that could be created/bought as the keys.
                Values are dictionaries with 3 keys: "cost", the cost of the object, 'template': the template to create the object
                and 'initializer' used to initialize the object.
    """

    def __init__(self, game, initializer_dict: dict) -> None:
        """
        :param game: the game where the initializer is created
        :param initializer_dict: the dictionary used to create the initializer
        """
        super().__init__(game, initializer_dict)

        self.init_type = self.INIT_TYPE_INTERFACE
        """ initializer by interface """

    def apply(self, base_object) -> None:
        """
        Apply the initializer. Do nothing since it is an interface initializer.

        :param base_object: The BaseObject to initialize
        """
        pass
