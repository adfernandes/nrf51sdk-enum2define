#!/usr/bin/env python
#
# https://devzone.nordicsemi.com/question/7830/please-fix-the-enum-in-ble_gattsh/
#
# Note that on the Cortex-M0, SVC call operands must be in the range of 0-255, and hence
# fit in an 'unsigned char'. This also follows the Keil ARMCC 5 convention for enums.
#
# for i in `fgrep -lR '--include=*.h' _SVCS ..`; do
#   ./enum2define.py "$i"
# done

import fileinput, re

def enum( **enums ):
    return type( 'Enum', (), enums )

Expecting = enum( DECLARATION=0, OPENING_BRACE=1, FIRST_LINE=2, ADDITIONAL_LINE=3 )
state = Expecting.DECLARATION

def print_define( string, comment ):
    if not comment:
        comment = ''
    statement = '#define {:40s} ({:s} + {:3d})    {:s}'.format( string, enum_base, enum_count, comment )
    statement = statement.rstrip()
    print( statement )

for line in fileinput.input( inplace=True ):
    line = line.rstrip()

    if state == Expecting.DECLARATION:
        match = re.search( '^\s*enum\s+(\w+_SVCS)\s*$', line )
        if not match:
            print( line )
            continue
        print( 'typedef unsigned char {:s}; // enum'.format( match.group(1) ) )
        state = Expecting.OPENING_BRACE
        continue

    if state == Expecting.OPENING_BRACE:
        if not re.search( '^\s*{\s*$', line ):
            raise Exception('Expected a lone opening brace.')
        state = Expecting.FIRST_LINE
        continue

    if state == Expecting.FIRST_LINE:
        match = re.search( '^\s*(\w+)\s*=\s*(\w+_BASE)\s*,?\s*(.*)?\s*$', line )
        if not match:
            raise Exception('First \'enum\' line did not have the expected form.')
        enum_base = match.group(2)
        enum_count = 0
        print_define( match.group(1), match.group(3) )
        state = Expecting.ADDITIONAL_LINE
        continue

    if state == Expecting.ADDITIONAL_LINE:
        if re.search( '^\s*}\s*;\s*$', line ):
            state = Expecting.DECLARATION
            continue
        match = re.search( '^\s*(\w+)\s*(=\s*(\w+)\s*)?,?\s*(.*)?\s*$', line )
        if not match:
            raise Exception('Additional \'enum\' line did not have the expected form.')
        enum_count = enum_count + 1
        if match.group(3):
            enum_base = match.group(3)
            enum_count = 0
        print_define( match.group(1), match.group(4) )
        continue
