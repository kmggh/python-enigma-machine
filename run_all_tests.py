#!/usr/bin/env python
# Sat 2015-01-17 11:09:04 -0500
# Copyright (c) 2012, 2013, 2015 by Ken Guyton. All Rights Reserved.

"""Run all tests."""

import os

TESTS = ('enigma', 'shifter')


def run_test(test_name):
  """Run a particular test."""

  print 'Running test_%s...' % test_name
  os.system('./test_%s.py' % test_name)
  print


def main():
  """Run all tests."""

  for test_name in TESTS:
    run_test(test_name)


if __name__ == '__main__':
  main()
