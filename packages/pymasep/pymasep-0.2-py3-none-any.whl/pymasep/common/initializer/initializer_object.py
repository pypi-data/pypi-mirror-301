from .initializer import Initializer


class InitializerObject(Initializer):
    """
    Initializer used to initialize an Object.
    An initializer can be executed by the Engine (by default) or processed by the Interface.

    An initializer is created from a dictionary.
    The format is the following:

    - name: name of the initializer used as id
    - value_type: for Characteristic, the type of the value (as string)
    - subclass_initializer: name of sub initializer used to initialize sub BaseObject.\
                          For an object, the name of the subclass_initializer must be 'objectstate'.\
                          These initializers must already exist in the game
    """

    def apply(self, one_object):
        """
        Apply the initializer for an Object. Apply the initializer of the ObjectState

        :param one_object: The Object to initialize
        """
        init_object_state = self.subclass_initializer['objectstate']
        init_object_state.apply(one_object.object_state)
        if 'containers' in self.subclass_initializer:
            for c in self.subclass_initializer['containers']:
                container = one_object.containers[c[0]]
                initializer = c[1]
                initializer.apply(container)
                if initializer.init_type == self.INIT_TYPE_INTERFACE:
                    container.state = 'init'
                    container.initializer = initializer

