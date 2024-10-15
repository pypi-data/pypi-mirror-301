from typing import Optional, List
from .initializer import Initializer


class InitializerContainer(Initializer):
    """
    Initializer used to initialize a Container
    An initializer can be executed by the Engine (by default) or processed by the Interface.

    An initializer is created from a dictionary. The format is the following:

    - name: name of the initializer used as id
    - type: type of initialization. ALL: all the objects in obj_init will be created. BUY: the player must choose the objects to buy
    - obj_init : dictionary containing the name of the objects that could be created/bought as the keys. Values are dictionaries with three keys: "cost", the cost of the object, 'template': the template to create the object and 'initializer' used to initialize the object.
    """

    def __init__(self, game, initializer_dict: dict) -> None:
        """
        :param game: the game where the initializer is created
        :param initializer_dict: the dictionary used to create the initializer
        """
        super().__init__(game, initializer_dict)

        self.type = initializer_dict['type']
        """ type of the initializer """

        self.obj_init = initializer_dict.get('obj_init', None)
        """ object creation and initialization """

    def apply(self, base_object) -> None:
        """
        Apply the initializer.

        :param base_object: The Container to initialize with all objects in the initializer
        """
        self.apply_with_params(base_object, self.obj_init.keys())

    def apply_with_params(self, base_object, list_obj_to_create: Optional[List[str]]) -> None:
        """
        Create objects in the container and set the container state as 'run'

        :param base_object: The Container to initialize with list_obj_to_create objects
        :param list_obj_to_create: the objects to create in the container. This list contains all names of the objects.\
        These names must be in the obj_init dictionary keys. May be None or empty
        """
        env = base_object.environment
        if list_obj_to_create:
            for o in list_obj_to_create:
                params_for_obj = self.obj_init[o]
                tmplt = env.game.templates[params_for_obj['template']]
                obj = env.create_object(name=o, template=tmplt)
                initializer = env.game.initializers[params_for_obj['initializer']]
                initializer.apply(obj)
                base_object.add(obj)
        base_object.set_run()
