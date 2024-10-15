from typing import List, Tuple

from .initializer_charac_interface import InitializerCharacInterface


class InitializerCharacInterfaceShared(InitializerCharacInterface):
    """
    Initializer to choose Characteristic with VALUE_MODE_CHOICE shared among multiple interface.
    """

    def filter_choice(self, charac_name: str, state) -> List[Tuple[str, str]]:
        """
        Filter choices when an interface chose a value, all others must remove this choice.

        :param charac_name: Characteristic name used to filter other characteristics
        :param state: state where the characteristic is stored
        :return: the new list of choices filtered removing the value of
        """
        result = self.param.copy()
        for o in state.objects.values():
            if charac_name in o.object_state.characteristics:
                value = o.object_state.characteristics[charac_name].value
                elements_to_remove = [element for element in result if element[1] == value]
                if elements_to_remove:
                    result.remove(elements_to_remove[0])
        return result
