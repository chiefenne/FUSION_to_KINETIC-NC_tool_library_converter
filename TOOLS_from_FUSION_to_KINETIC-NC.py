#! /bin/env python

"""
FUSION 360 to KINETIC-NC tool library converter
"""

__author__ = 'Andreas Ennemoser'
__license__ = 'MIT'
__date__ = '11-01-2020'
__version__ = '1.0'
__email__ = 'andreas.ennemoser@aon.at'

import sys
import json

if len(sys.argv) != 2:
    print('\nUsage: python {} filename.json\n'.format(sys.argv[0]))
    sys.exit(-1)

# read FUSION 360 tools library
with open(sys.argv[1], 'r') as fusion360_file:
    tool_data = fusion360_file.read()

# parse file
tools = json.loads(tool_data)

# put all on dictionary as tool are not sorted in FUSION 360 JSON
# works only if tools are in consecutive order (i.e. no gaps)
tools_dict = dict()
for index, tool in enumerate(tools['data']):

    tools_dict[tool['post-process']['number']] = \
        ['0.0',
         '1.0',
         tool['geometry']['DC'],
         '0.0',
         '50.0',
         '50.0',
         tool['start-values']['presets'][0]['n'],
         tool['start-values']['presets'][0]['n'],
         tool['start-values']['presets'][0]['v_f'],
         '',
         '',
         tool['description'],
         '0.0',
         '0.0']

# write KINETIC-NC file (ToolTable.txt)
with open('ToolTable.txt', 'w') as kinetics_file:
    # show values
    for index in range(len(tools_dict.keys())):

        para = tools_dict[index+1]

        kinetics_file.write('numT_{:02d}={:f}\n'.format(index, index+1))
        kinetics_file.write('numP_{:02d}={}\n'.format(index, para[0]))
        kinetics_file.write('type_{:02d}={}\n'.format(index, para[1]))
        kinetics_file.write('dia1_{:02d}={}\n'.format(index, para[2]))
        kinetics_file.write('dia2_{:02d}={}\n'.format(index, para[3]))
        kinetics_file.write('len1_{:02d}={}\n'.format(index, para[4]))
        kinetics_file.write('len2_{:02d}={}\n'.format(index, para[5]))
        kinetics_file.write('maxRpm_{:02d}={}\n'.format(index, para[6]))
        kinetics_file.write('defaultS_{:02d}={}\n'.format(index, para[7]))
        kinetics_file.write('defaultF_{:02d}={}\n'.format(index, para[8]))
        kinetics_file.write('maxLife_{:02d}={}\n'.format(index, para[9]))
        kinetics_file.write('useTime_{:02d}={}\n'.format(index, para[10]))
        kinetics_file.write('name_{:02d}={}\n'.format(index, para[11]))
        kinetics_file.write('overrideS_{:02d}={}\n'.format(index, para[12]))
        kinetics_file.write('overrideF_{:02d}={}\n'.format(index, para[13]))

    kinetics_file.write('numTools={}\n'.format(index + 1))
