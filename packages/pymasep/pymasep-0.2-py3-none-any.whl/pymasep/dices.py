"""
Module to launch many dices, any types, with modifiers.
"""

from typing import Tuple, List
from random import randint, seed
import re


def roll_dice(dice: str, random_seed: int = None) -> Tuple[int, List[int]]:
    """
    Roll one or many dices of one type and return the total and all the values

    :param dice: String format xDy with 0<x<inf and 0<y<inf.
    :param random_seed: Random seed for testing only (or cheating but, hum, what's the point ? it's just a game.).
    :return: (`result`, `details`).\
     `result` is the result of the dice and `details` is list of all details for all launches.

    :Example::

        >>> roll_dice('2D6')
        (4, [1, 3])

    """
    seed(random_seed)
    values = []
    d_index = dice.find('D')
    if d_index != -1:
        nb_d = 0
        type_d = 0
        if dice[:d_index].isdigit():
            nb_d = int(dice[:d_index])
        if dice[d_index + 1:].isdigit():
            type_d = int(dice[d_index + 1:])
        if nb_d != 0 and type_d != 0:
            for i in range(nb_d):
                values.append(randint(1, type_d))
    total = sum(values)
    return total, values


def roll_dices(dices: str, random_seed: int = None) -> Tuple[int, List[int]]:
    """
    Roll many dices and sum/substract all terms. No parenthesis is allowed.

    :param dices: Expression with format ``((\d+)?D(\d+)|([\+\-]\d+))+?`` (not totally sure of the regexp, see tests)
    :param random_seed: seed used in tests. Should not be used in a real scenario except for reproductible scenarios
    :return: (`result`, `details`). `Result` is the sum of all dices and modifiers and `details` is list of all \
            details, including modifiers

    :Example::

        >>> roll_dices('2D6+1D4+3')
        (13, [5, 4, 1, 3])

    """
    total = 0
    values = []
    dices_list = re.split('[+-]', dices)
    signs = [element for element in dices if element in ['+', '-']]
    if dices[0] != '-':
        signs.insert(0, '+')
    for idx, one_dice in enumerate(dices_list):
        if one_dice.isdigit():
            sub_total = int(one_dice)
            sub_values = [int(one_dice)]
        else:
            sub_total, sub_values = roll_dice(one_dice, random_seed)
        if signs[idx] == '+':
            total += sub_total
            values.extend(sub_values)
        else:
            total -= sub_total
            values.extend([sv * -1 for sv in sub_values])
    return total, values


def min_max_dice(dice: str):
    """
    get the min and max values of dice

    :param dice: string format xDy with 0<x<inf and 0<y<inf.

    :return: min and max values of dice
    """
    d_index = dice.find('D')
    min = 0
    max = 0
    if d_index != -1:
        nb_d = 0
        type_d = 0
        if dice[:d_index].isdigit():
            nb_d = int(dice[:d_index])
        if dice[d_index + 1:].isdigit():
            type_d = int(dice[d_index + 1:])
        min = nb_d
        max = nb_d * type_d
    return min, max


def min_max_dices(dices: str):
    """
   get the min and max of dices expression.

   :param dices: expression with format ``((\d+)?D(\d+)|([\+\-]\d+))+?`` (not totally sure of the regexp, see tests)\
    No parenthesis is allowed.
   :return: (`min`, `max`).

   :Example::

       >>> min_max_dices('2D6+1D4+3')
       (6, 19)

   """
    min = 0
    max = 0
    dices_list = re.split('[+-]', dices)
    signs = [element for element in dices if element in ['+', '-']]
    if dices[0] != '-':
        signs.insert(0, '+')
    for idx, one_dice in enumerate(dices_list):
        if one_dice.isdigit():
            sub_min = int(one_dice)
            sub_max = int(one_dice)
        else:
            sub_min, sub_max = min_max_dice(one_dice)
        if signs[idx] == '+':
            min += sub_min
            max += sub_max
        else:
            min -= sub_max
            max -= sub_min
    return min, max