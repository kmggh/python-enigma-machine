#!/usr/bin/env python
# Copyright (C) 2015 by Ken Guyton.  All Rights Reserved.

"""Test a whole enigma machine.

The sequence is:

-> pb -> III -> II -> I -> Reflector -> revI -> revII -> revIII -> pb -> 

"""

import enigma
import unittest

PLUGBOARD_CONFIG = (('A', 'E'), ('M', 'Y'))


class TestRotorshifter(unittest.TestCase):
  def setUp(self):
    self.rotor_map1 = enigma.RotorMap(enigma.ENIGMA_I_1930)
    self.rotor_map2 = enigma.RotorMap(enigma.ENIGMA_II_1930)
    self.rotor_map3 = enigma.RotorMap(enigma.ENIGMA_III_1930)

    self.rotor_shifter1 = enigma.RotorShifter(self.rotor_map1,
                                              turnover_letter='Q')
    self.rotor_shifter2 = enigma.RotorShifter(
        self.rotor_map2, next_shifter=self.rotor_shifter1, turnover_letter='E')
    self.rotor_shifter3 = enigma.RotorShifter(
        self.rotor_map3, next_shifter=self.rotor_shifter2, turnover_letter='V')

    self.reflector = enigma.Reflector(enigma.REFLECTOR_A)
    self.plugboard = enigma.PlugBoard(PLUGBOARD_CONFIG)

    self.machine = enigma.Machine(rotor1=self.rotor_shifter1,
                                  rotor2=self.rotor_shifter2,
                                  rotor3=self.rotor_shifter3,
                                  reflector=self.reflector,
                                  plugboard=self.plugboard)

  def test_create(self):
    self.assertNotEqual(self.machine, None)

  def test_step_and_flow(self):
    self.assertEqual(self.machine.step_and_flow('A'), 'B')

  def test_stream(self):
    self.assertEqual(''.join(list(self.machine.stream('HELLO'))), 'KSUBR')

  def test_example(self):
    self.machine.reflector = enigma.Reflector(enigma.REFLECTOR_B)
    self.machine.plugboard = enigma.PlugBoard(
        (('P', 'O'), ('M', 'L'), ('I', 'U'), ('K', 'J'), ('N', 'H'),
         ('Y', 'T'), ('G', 'B'), ('V', 'F'), ('R', 'E'), ('D', 'C'),))
    self.assertEqual(''.join(list(self.machine.stream('HELLO'))), 'TDJPK')


if __name__ == '__main__':
  unittest.main()
