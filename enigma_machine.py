#!/usr/bin/env python
# Copyright (C) 2015 by Ken Guyton.  All Rights Reserved.

"""A simple Enigma machine emulateor for testing.

This one emulates with Enigma I.
"""

from __future__ import print_function

import enigma
import string
import sys

PLUGBOARD_CONFIG = (('A', 'E'), ('M', 'Y'))


def create_machine():
  """Get the rotors, reflector and plugboard set up."""

  rotor_map1 = enigma.RotorMap(enigma.ENIGMA_I_1930)
  rotor_map2 = enigma.RotorMap(enigma.ENIGMA_II_1930)
  rotor_map3 = enigma.RotorMap(enigma.ENIGMA_III_1930)

  rotor_shifter1 = enigma.RotorShifter(rotor_map1, turnover_letter='Q')
  rotor_shifter2 = enigma.RotorShifter(
      rotor_map2, next_shifter=rotor_shifter1, turnover_letter='E')
  rotor_shifter3 = enigma.RotorShifter(
      rotor_map3, next_shifter=rotor_shifter2, turnover_letter='V')

  reflector = enigma.Reflector(enigma.REFLECTOR_A)
  plugboard = enigma.PlugBoard(PLUGBOARD_CONFIG)

  machine = enigma.Machine(rotor1=rotor_shifter1,
                           rotor2=rotor_shifter2,
                           rotor3=rotor_shifter3,
                           reflector=reflector,
                           plugboard=plugboard)

  return machine


def clean_input(line):
  """Clean up a line of input so it only contains 'A'--'Z'."""

  line = line.strip()
  output = []
  for char in line:
    char = char.upper()
    if char in string.ascii_uppercase:
      output.append(char)

  return ''.join(output)


def main():
  machine = create_machine()

  line = sys.stdin.readline()
  while line:
    cleaned_line = clean_input(line)
    print(cleaned_line)
    print(''.join(list(machine.stream(cleaned_line))))
    line = sys.stdin.readline()


if __name__ == '__main__':
  main()
