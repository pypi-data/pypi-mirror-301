from pymasep.utils import native_xml_types


class Initializer:
    """
    Initializer used to initialize the value of BaseObject.
    An initializer can be executed by the Engine (by default) or processed by the Interface.

    An initializer is created from a dictionary.
    The format is the following:

    - name: name of the initializer used as id
    - value_type: for Characteristic, the type of the value (as string)
    - subclass_initializer: name of sub initializer used to initialize sub BaseObject.\
                              These initializers must already exist in the game
    """

    INIT_TYPE_ENGINE = 'Engine'
    """ Initializer by the Engine """

    INIT_TYPE_INTERFACE = 'Interface'
    """ Initializer by the Interface """

    def __init__(self, game, initializer_dict: dict) -> None:
        """
        :param game: the game where the initializer is created
        :param initializer_dict: the dictionary used to create the initializer
        """
        self.game = game

        self.name = initializer_dict['name']
        """ name of the initializer used as id """

        self.value_type = native_xml_types[initializer_dict.get('value_type')]
        """ type of the value (as string) for Characteristic"""

        self.subclass_initializer = {}
        """ name of sub initializers used to initialize sub BaseObject """

        if 'subclass_initializer' in initializer_dict:
            for sub_element, init_str in initializer_dict['subclass_initializer'].items():
                if sub_element != 'containers':
                    self.subclass_initializer[sub_element] = game.initializers[init_str]
                else:
                    self.subclass_initializer[sub_element] = []
                    for c in init_str:
                        self.subclass_initializer[sub_element].append((c[0], game.initializers[c[1]]))

        self.init_type = self.INIT_TYPE_ENGINE
        """ initializer by engine by default """

    def apply(self, base_object) -> None:
        """
        Apply the initializer.

        :param base_object: The BaseObject to initialize
        """
        pass
