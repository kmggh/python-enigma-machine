#!/usr/bin/env python
# Copyright (C) 2015 by Ken Guyton.  All Rights Reserved.

"""Test the enigma library module."""

import enigma
import string
import unittest

PLUGBOARD_CONFIG = (('A', 'E'), ('M', 'Y'))


class TestRotorMap(unittest.TestCase):
  def setUp(self):
    self.rotor_map = enigma.RotorMap(enigma.ENIGMA_I_1930)

  def test_create(self):
    self.assertNotEqual(self.rotor_map, None)

  def test_letter_to_num(self):
    self.assertEqual(self.rotor_map.letter_to_num('A'), 0)
    self.assertEqual(self.rotor_map.letter_to_num('B'), 1)
    self.assertEqual(self.rotor_map.letter_to_num('M'), 12)
    self.assertEqual(self.rotor_map.letter_to_num('N'), 13)
    self.assertEqual(self.rotor_map.letter_to_num('Z'), 25)

  def test_num_to_letter(self):
    self.assertEqual(self.rotor_map.num_to_letter(0), 'A')
    self.assertEqual(self.rotor_map.num_to_letter(1), 'B')
    self.assertEqual(self.rotor_map.num_to_letter(12), 'M')
    self.assertEqual(self.rotor_map.num_to_letter(13), 'N')
    self.assertEqual(self.rotor_map.num_to_letter(25), 'Z')

  def test_letter_seq_to_num(self):
    self.assertEqual(self.rotor_map.letter_seq_to_num('ABMNZ'),
                     [0, 1, 12, 13, 25])

  def test_flow(self):
    self.assertEqual(self.rotor_map.flow('A'), 'E')
    self.assertEqual(self.rotor_map.flow('K'), 'N')

  def test_reverse_flow(self):
    self.assertEqual(self.rotor_map.reverse_flow('E'), 'A')
    self.assertEqual(self.rotor_map.reverse_flow('N'), 'K')

  def test_reverse_map(self):
    input_map = [22, 25, 23, 24]
    rev_map = self.rotor_map.reverse_map(input_map)
    self.assertEqual(rev_map[22], 0)
    self.assertEqual(rev_map[25], 1)
    self.assertEqual(rev_map[23], 2)
    self.assertEqual(rev_map[24], 3)


class TestReflector(unittest.TestCase):
  def setUp(self):
    self.reflector = enigma.Reflector(enigma.REFLECTOR_A)

  def test_create(self):
    self.assertNotEqual(self.reflector, None)
    # This is just a property of a reflector.
    self.assertEqual(self.reflector.map, self.reflector.rev_map)

  def test_flow(self):
    self.assertEqual(self.reflector.flow('A'), 'E')
    self.assertEqual(self.reflector.flow('B'), 'J')
    self.assertEqual(self.reflector.flow('E'), 'A')
    self.assertEqual(self.reflector.flow('J'), 'B')


class TestPlugboard(unittest.TestCase):
  def setUp(self):
    self.plugboard = enigma.PlugBoard(PLUGBOARD_CONFIG)

  def test_create(self):
    self.assertNotEqual(self.plugboard, None)

  def test_flow(self):
    self.assertEqual(self.plugboard.flow('A'), 'E')
    self.assertEqual(self.plugboard.flow('E'), 'A')
    self.assertEqual(self.plugboard.flow('M'), 'Y')
    self.assertEqual(self.plugboard.flow('Y'), 'M')

  def test_swap_pair(self):
    input_map = string.ascii_uppercase
    self.assertEqual(self.plugboard.swap_pair(input_map, ('A', 'E')),
                     'EBCDAFGHIJKLMNOPQRSTUVWXYZ')

  def test_swap_pair_two(self):
    self.assertEqual(self.plugboard.swap_pair('EBCDAFGHIJKLMNOPQRSTUVWXYZ',
                                              ('M', 'Y')),
                     'EBCDAFGHIJKLYNOPQRSTUVWXMZ')

  def test_swap_seq_of_pairs(self):
    input_map = string.ascii_uppercase
    pairs = (('A', 'E'), ('M', 'Y'))
    self.assertEqual(self.plugboard.swap_seq_of_pairs(input_map, pairs),
                     'EBCDAFGHIJKLYNOPQRSTUVWXMZ')


if __name__ == '__main__':
  unittest.main()
