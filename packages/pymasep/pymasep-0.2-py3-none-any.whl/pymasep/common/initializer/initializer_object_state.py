from .initializer import Initializer


class InitializerObjectState(Initializer):
    """
   Initializer used to initialize an ObjectState.
   An initializer can be executed by the Engine (by default) or processed by the Interface.

   An initializer is created from a dictionary.
   The format is the following:

   - name: name of the initializer used as id
   - value_type: for Characteristic, the type of the value (as string)
   - subclass_initializer: name of sub initializer used to initialize sub BaseObject.
   \
                         For an object, the name of the subclass_initializer must be 'objectstate'.
                         \
                         These initializers must already exist in the game.
   """

    def apply(self, object_state):
        """
        Apply the initializer for an ObjectState. Apply the initializer of oll Characteristics

        :param object_state: The ObjectState to initialize
        """
        for charac_name, sub_init in self.subclass_initializer.items():
            charac = object_state.characteristics[charac_name]
            charac.value_type = sub_init.value_type
            sub_init.apply(charac)
            if sub_init.init_type == self.INIT_TYPE_INTERFACE:
                # initializer does nothing => it is an interface initializer => set state to init
                charac.state = 'init'
