#!/usr/bin/env python
# Copyright (C) 2015 by Ken Guyton.  All Rights Reserved.

"""Test the enigma rotor shifter module."""

import enigma
import unittest


class TestRotorshifter(unittest.TestCase):
  def setUp(self):
    self.rotor_map = enigma.RotorMap(enigma.ENIGMA_I_1930)
    self.rotor_map2 = enigma.RotorMap(enigma.ENIGMA_II_1930)
    self.rotor_shifter2 = enigma.RotorShifter(self.rotor_map2)
    self.rotor_shifter = enigma.RotorShifter(self.rotor_map,
                                             self.rotor_shifter2)

  def test_create(self):
    self.assertNotEqual(self.rotor_shifter, None)
    self.assertEqual(self.rotor_shifter.shift, 0)
    self.assertEqual(self.rotor_shifter.next_shifter, self.rotor_shifter2)
    self.assertEqual(self.rotor_shifter.turnover, 25)
    self.assertFalse(self.rotor_shifter.double_step)

  def test_init_with_shift_turnover(self):
    self.rotor_shifter = enigma.RotorShifter(rotor_map=self.rotor_map,
                                             next_shifter=self.rotor_shifter2,
                                             shift_letter='C',
                                             turnover_letter='M')

    self.assertEqual(self.rotor_shifter.rotor_map, self.rotor_map)
    self.assertEqual(self.rotor_shifter.next_shifter, self.rotor_shifter2)
    self.assertEqual(self.rotor_shifter.shift, 2)
    self.assertEqual(self.rotor_shifter.turnover, 12)

  def test_flow(self):
    self.assertEqual(self.rotor_shifter.flow('A'), 'E')
    self.assertEqual(self.rotor_shifter.flow('K'), 'N')

  def test_reverse_flow(self):
    self.assertEqual(self.rotor_shifter.reverse_flow('E'), 'A')
    self.assertEqual(self.rotor_shifter.reverse_flow('N'), 'K')

  def test_get_shift(self):
    self.assertEqual(self.rotor_shifter.get_shift(), 'A')

  def test_set_shift(self):
    self.rotor_shifter.set_shift('B')
    self.assertEqual(self.rotor_shifter.get_shift(), 'B')
    self.assertEqual(self.rotor_shifter.shift, 1)

  def test_step(self):
    self.rotor_shifter.step()
    self.assertEqual(self.rotor_shifter.get_shift(), 'B')
    self.rotor_shifter.step()
    self.assertEqual(self.rotor_shifter.get_shift(), 'C')

  def test_step_crossing_z(self):
    self.rotor_shifter.set_shift('Z')
    self.rotor_shifter.step()
    self.assertEqual(self.rotor_shifter.get_shift(), 'A')

  def test_step_next_rotor(self):
    self.rotor_shifter.set_shift('Z')
    self.rotor_shifter.step()
    self.assertEqual(self.rotor_shifter2.get_shift(), 'B')

  def test_step_next_rotor_none(self):
    self.rotor_shifter2.set_shift('Z')
    self.rotor_shifter2.step()
    self.assertEqual(self.rotor_shifter2.get_shift(), 'A')

  def test_set_turnover(self):
    self.rotor_shifter.set_turnover('D')
    self.assertEqual(self.rotor_shifter.turnover, 3)

  def test_flow_after_step(self):
    self.assertEqual(self.rotor_shifter.flow('A'), 'E')
    self.rotor_shifter.step()
    self.assertEqual(self.rotor_shifter.flow('A'), 'J')
    self.rotor_shifter.step()
    self.assertEqual(self.rotor_shifter.flow('A'), 'K')
    self.assertEqual(self.rotor_shifter.flow('B'), 'D')

  def test_reverse_flow_after_step(self):
    self.assertEqual(self.rotor_shifter.reverse_flow('E'), 'A')
    self.rotor_shifter.step()
    self.assertEqual(self.rotor_shifter.reverse_flow('J'), 'A')
    self.rotor_shifter.step()
    self.assertEqual(self.rotor_shifter.reverse_flow('K'), 'A')
    self.assertEqual(self.rotor_shifter.reverse_flow('D'), 'B')

  def _shift_positions(self, rs1, rs2, rs3):
    """Return the shift positions of the three rotors I-II-III as a str."""

    num_to_letter = rs1.rotor_map.num_to_letter
    return ''.join([num_to_letter(rs.shift) for rs in rs1, rs2, rs3])

  def test_double_step_sequence(self):
    rotor_map1 = enigma.RotorMap(enigma.ENIGMA_I_1930)
    rotor_map2 = enigma.RotorMap(enigma.ENIGMA_II_1930)
    rotor_map3 = enigma.RotorMap(enigma.ENIGMA_III_1930)

    rs1 = enigma.RotorShifter(rotor_map1, turnover_letter='Q',
                                         shift_letter='A')
    rs2 = enigma.RotorShifter(rotor_map2, next_shifter=rs1,
                                         turnover_letter='E', shift_letter='D')
    rs3 = enigma.RotorShifter(rotor_map3, next_shifter=rs2,
                                         turnover_letter='V', shift_letter='U')

    rs2.double_step = True

    self.assertEqual(self._shift_positions(rs1, rs2, rs3), 'ADU')
    rs3.step()
    self.assertEqual(self._shift_positions(rs1, rs2, rs3), 'ADV')
    rs3.step()
    self.assertEqual(self._shift_positions(rs1, rs2, rs3), 'AEW')

    # Now the middle rotor double-steps.
    rs3.step()
    self.assertEqual(self._shift_positions(rs1, rs2, rs3), 'BFX')
    rs3.step()
    self.assertEqual(self._shift_positions(rs1, rs2, rs3), 'BFY')


if __name__ == '__main__':
  unittest.main()
