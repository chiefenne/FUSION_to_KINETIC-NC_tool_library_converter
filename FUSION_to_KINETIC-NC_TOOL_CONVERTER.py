"""
FUSION 360 to KINETIC-NC tool library converter.
"""

__author__ = "Andreas Ennemoser"
__license__ = "MIT"
__date__ = "09-01-2024"
__version__ = "1.1"
__email__ = "andreas.ennemoser@aon.at"

import sys
import json


if len(sys.argv) != 2:
    sys.exit(f"\nUsage: python {sys.argv[0]} filename.json\n")

# read FUSION tools library file
with open(sys.argv[1], 'r') as fusion_tools_file:
    fusion_tools_json = fusion_tools_file.read()

# parse file
fusion_tools = json.loads(fusion_tools_json)

# put tools in a dictionary as tools are not sorted in FUSION JSON
# works only if tools are in consecutive order (i.e., no gaps)
tools_dict = {
    tool['post-process']['number']: [
        '1.0',                                    # tool position (automatic tool changer)
        tool['type'],                             # tool type
        tool['geometry']['DC'],                   # tool diameter
        '0.0',                                    # tool diameter 2
        '50.0',
        '50.0',
        tool['start-values']['presets'][0]['n'],
        tool['start-values']['presets'][0]['n'],
        '1000.0',
        '0.0',
        '0.0',
        tool['description'],
        '0.0',
        '0.0'
    ]
    for tool in fusion_tools['data']
}

maxRpm = 24000.0

# tool types Fusion to Kinetic-NC
tool_types = {
    'flat end mill': '1.0', # fräser
    'face mill': '1.0', # planfräser
    'ball end mill': '7.0', # kugelfräser
    'bull nose end mill': '6.0', # torusfräser
    'chamfer mill': '4.0', # gravur und fasenfräser
    'counter sink': '8.0', # senker
    'thread mill': '0.0', # gewindewirbler
    'drill': '2.0', # bohrer
    'radius mill': '3.0' # radiusfräser
}

with open('ToolTable.txt', 'w') as kinetics_tools:
    for i in range(len(tools_dict)):
        para = tools_dict[i+1]
        if para[1] not in tool_types:
            # meassage if tool type is not in the dictionary
            print(f"Tool type {para[1]} not in dictionary")
            para[1] = 'flat end mill'
        kinetics_tools.write(f'numT_{i:02d}={i+1:.1f}\n')                      # tool number
        kinetics_tools.write(f'numP_{i:02d}={para[0]}\n')                      # tool position (automatic tool changer)
        kinetics_tools.write(f'type_{i:02d}={tool_types[para[1]]}\n')                      # tool type
        kinetics_tools.write(f'dia1_{i:02d}={float(para[2]):f}\n')             # tool diameter
        kinetics_tools.write(f'dia2_{i:02d}={float(para[3]):f}\n')             # shaft diameter
        kinetics_tools.write(f'len1_{i:02d}={para[4]}\n')                      # tool length 1
        kinetics_tools.write(f'len2_{i:02d}={para[5]}\n')                      # tool length 2
        kinetics_tools.write(f'maxRpm_{i:02d}={maxRpm:f}\n')                   # maximum RPM
        kinetics_tools.write(f'defaultS_{i:02d}={float(para[7]):f}\n')         # default spindle speed fot the tool
        kinetics_tools.write(f'defaultF_{i:02d}={para[8]}\n')                  # default feed rate for the tool
        kinetics_tools.write(f'maxLife_{i:02d}={para[9]}\n')                   # maximum tool life
        kinetics_tools.write(f'useTime_{i:02d}={para[10]}\n')                  # tool usage time
        kinetics_tools.write(f'name_{i:02d}={para[11]}\n')                     # tool name
        kinetics_tools.write(f'overrideS_{i:02d}={float(para[12]):f}\n')       # override spindle speed
        kinetics_tools.write(f'overrideF_{i:02d}={float(para[13]):f}\n')       # override feed rate

    kinetics_tools.write(f'numTools={i+1}\n')
