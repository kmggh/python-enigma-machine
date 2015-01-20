# Copyright (C) 2015 by Ken Guyton.  All Rights Reserved.

"""An emulator for the enigma machine.

The sequence of data flow is:

in --> pb-r3-r2-r1-refl-r1-r2-r3-pb --> out
          --------      --------
          forward       reverse

pb is the PlugBoard.
r1, r2, r3 are the rotors, specifically the RotorShifters.
refl is the Reflector.          
"""

import string

ENIGMA_I_1930 = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
ENIGMA_II_1930 = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
ENIGMA_III_1930 = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'

REFLECTOR_A = 'EJMZALYXVBWFCRQUONTSPIKHGD'
REFLECTOR_B = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
REFLECTOR_C = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'


class RotorMap(object):
  """An object representing a rotor which maps inputs to outputs.

  There are 26 inputs and 26 outputs.  The inputs are the natural indices
  of a list of 26 items, 0--25.  The outputs are the values in the list.

  The ints 0--25 represent the alphabet A--Z.

  Even though the maps are based on ints, the input and output are 
  upper case letters in most cases, so they are converted incoming and
  outgoing.
  """

  def __init__(self, alpha_seq):
    """Initialize the rotor with an output sequence letters.

    The output sequence is what you have if the input sequence is A--Z.

    Args:
      alpha_seq: str. A str of the 26 capital letters in a scrambled
        order.
    """

    self.map = self.letter_seq_to_num(alpha_seq)
    self.rev_map = self.reverse_map(self.map)

  def letter_to_num(self, letter):
    """Convert a single letter to a number."""

    return ord(letter) - 65

  def num_to_letter(self, num):
    """Convert a single letter to a number."""

    return chr(num + 65)

  def letter_seq_to_num(self, letter_seq):
    """Convert a sequence of letters into numbers."""

    return [self.letter_to_num(l) for l in letter_seq]

  def num_seq_to_letter(self, num_seq):
    """Convert a sequence of int to str capital letters."""

    return ''.join([self.num_to_letter(n) for n in num_seq])

  def map_flow(self, a_map, input_letter):
    """Follow the current flow with a particular map.

    Args:
      a_map: list of int.  A mapping of sequence positions of letters to
        other sequence positions.
      input_letter: str of single char A--Z.
    Returns:
      An output letter as a str.
    """

    input_num = self.letter_to_num(input_letter)
    output_num = a_map[input_num]
    return self.num_to_letter(output_num)

  def flow(self, input_letter):
    """Follow the current flow through the mapping of a single rotor.

    Args:
      a_map: list of int.  A mapping of sequence positions of letters to
        other sequence positions.
      input_letter: str of single char A--Z.
    Returns:
      An output letter as a str.
    """

    return self.map_flow(self.map, input_letter)

  def reverse_flow(self, input_letter):
    """Follow the reverse current flow through a single rotor.

    Args:
      a_map: list of int.  A mapping of sequence positions of letters to
        other sequence positions.
      input_letter: str of single char A--Z.
    Returns:
      An output letter as a str.
    """

    return self.map_flow(self.rev_map, input_letter)

  def reverse_map(self, input_map):
    """Build a reverse map given an input map.

    Each value in the input_map becomes an index in the reverse, with
    the original index as it's value.  It performs the exact reverse
    mapping of the original.

    Args:
      input_map: list of int.
    Returns:
      Another list of int which is the reverse map.
    """

    reverse = [None] * 26
    for index in range(len(input_map)):
      reverse[input_map[index]] = index

    return reverse


class RotorShifter(object):
  """The shifter handles shifting and clicking of the rotor."""

  def __init__(self, rotor_map, next_shifter=None, shift_letter='A',
               turnover_letter='Z'):
    """Initialize with a RotorMap.

    The turnover is the position in this rotor where the next rotor
    will be stepped.

    Args:
      rotor_map: RotorMap.
      next_shifter: RotorShifter.  The shifter for the next rotor in the
        machine (that will be stepped by this rotor's notch).
      shift: int.  An initial shift position.
    """

    self.rotor_map = rotor_map
    self.next_shifter = next_shifter
    self.shift = rotor_map.letter_to_num(shift_letter)
    self.turnover = rotor_map.letter_to_num(turnover_letter)

  def increment_letter_by_shift(self, letter):
    """Step a letter by the shift amount and wrap around Z."""

    num = self.rotor_map.letter_to_num(letter)
    num = (num + self.shift) % 26
    return self.rotor_map.num_to_letter(num)

  def decrement_letter_by_shift(self, letter):
    """Unstep a letter by the shift amount and wrap around Z."""

    num = self.rotor_map.letter_to_num(letter)
    num = (num - self.shift) % 26
    return self.rotor_map.num_to_letter(num)

  def flow(self, input_letter):
    """Follow the current flow through the mapping of a single rotor.

    Args:
      a_map: list of int.  A mapping of sequence positions of letters to
        other sequence positions.
      input_letter: str of single char A--Z.
    Returns:
      An output letter as a str.
    """

    shifted_letter = self.increment_letter_by_shift(input_letter)
    output_letter = self.rotor_map.flow(shifted_letter)
    shifted_output = self.decrement_letter_by_shift(output_letter)
    return shifted_output

  def reverse_flow(self, input_letter):
    """Follow the reverse current flow through a single rotor.

    Args:
      a_map: list of int.  A mapping of sequence positions of letters to
        other sequence positions.
      input_letter: str of single char A--Z.
    Returns:
      An output letter as a str.
    """

    shifted_letter = self.increment_letter_by_shift(input_letter)
    output_letter = self.rotor_map.reverse_flow(shifted_letter)
    return self.decrement_letter_by_shift(output_letter)

  def get_shift(self):
    """Return the current shift value as a letter."""

    return self.rotor_map.num_to_letter(self.shift)

  def set_shift(self, letter):
    """Set the shift to a particular value.

    Args:
      letter: str. A single letter A--Z.
    """

    self.shift = self.rotor_map.letter_to_num(letter)

  def step(self):
    """Increment the shift by one.  At Z it rotates to A."""

    if self.next_shifter and self.shift == self.turnover:
      self.next_shifter.step()

    self.shift = (self.shift + 1) % 26

  def set_turnover(self, letter):
    """Set the turnover, where the step causes the next rotor to step.

    Args:
      letter: str. A single letter from 'A' to 'Z'.
    """

    self.turnover = self.rotor_map.letter_to_num(letter)


class Reflector(RotorMap):
  """The reflector at the end of the rotor sequence."""

  def __init__(self, alpha_seq):
    """Initialize the rotor with an output sequence letters.

    The output sequence is what you have if the input sequence is A--Z.

    Args:
      alpha_seq: str. A str of the 26 capital letters in a scrambled
        order.
    """

    RotorMap.__init__(self, alpha_seq)


class PlugBoard(RotorMap):
  """The reflector at the end of the rotor sequence."""

  def __init__(self, config):
    """Initialize the plugboard with a config tuple.

    The output sequence is what you have if the input sequence is A--Z.
    Typically, no more than 10 pairs were used and any letter must appear
    only *once* in the entire config, i.e., a letter can't be reused in
    another pair.

    Args:
      config: A tuple of tuple pairs of str letters.  The letters are all
        capitals, 'A'--'Z'.  Example:  (('A', 'E'), ('M', 'Y')).
    """

    normal_map = string.ascii_uppercase
    swapped_map = self.swap_seq_of_pairs(normal_map, config)
    RotorMap.__init__(self, swapped_map)

  def swap_pair(self, input_map, pair):
    """Swap the two letters in the pair in the map.

    Args:
      The input_map is a str of letters 'A'--'Z' in some order.  The pair
      is a tuple pair of two letters.  In the returned str, those two
      letters are swapped.  Note, the letters will be in their original
      alphabet order position.
    Returns:
      A str of uppercase letters.
    """

    num_map = self.letter_seq_to_num(input_map)

    first = self.letter_to_num(pair[0])
    second = self.letter_to_num(pair[1])

    num_map[first] = second
    num_map[second] = first

    return self.num_seq_to_letter(num_map)

  def swap_seq_of_pairs(self, input_map, seq_of_pairs):
    """Swap pairs of letters in an input map.

    Args:
      input_map: str.  Letters 'A'--'Z' in some order.
      seq_of_pairs: A tuple of tuple pairs of str letters.  The letters are
        all capitals, 'A'--'Z'.  Example:  (('A', 'E'), ('M', 'Y')).
    Returns:
      A str of the 26 capital letters in the resulting order.
    """

    current_map = input_map
    for pair in seq_of_pairs:
      current_map = self.swap_pair(current_map, pair)

    return current_map


class Machine(object):
  """The enigma machine with all of the parts assembled."""

  def __init__(self, rotor1, rotor2, rotor3, reflector, plugboard):
    """Collect the parts.

    Args:
      rotor1, rotor2, rotor3: RotorShifter objects.
      reflector: Reflector object.
      plugboard: PlugBoard object.
    """

    self.rotor1 = rotor1
    self.rotor2 = rotor2
    self.rotor3 = rotor3
    self.reflector = reflector
    self.plugboard = plugboard

  def step_and_flow(self, input_letter):
    """Follow the current flow through the mapping of a single rotor.

    Note that we step the rotor set first, the flow the letter.

    Rotor3 is the fast stepping.  Rotor2 is stepped when Rotor3 hits its
    turnover point.  Similarly Rotor1 is stepped when Rotor2 is stepped.

    Args:
      a_map: list of int.  A mapping of sequence positions of letters to
        other sequence positions.
      input_letter: str of single char A--Z.
    Returns:
      An output letter as a str.
    """

    self.rotor3.step()
    after_pb = self.plugboard.flow(input_letter)
    phase1 = self.rotor1.flow(self.rotor2.flow(self.rotor3.flow(after_pb)))
    refl = self.reflector.flow(phase1)
    phase2 = self.rotor3.reverse_flow(self.rotor2.reverse_flow(
        self.rotor1.reverse_flow(refl)))
    final = self.plugboard.reverse_flow(phase2)

    return final

  def stream(self, input_stream):
    """Process a stream of data from a generator as a generator.

    Args:
      stream: generator that yields a str.  The generator yields a single
        str letter 'A'--'Z' at a time.
    Yields:
      The corresponding, encrypted letter.
    """

    for input_letter in input_stream:
      yield self.step_and_flow(input_letter)
