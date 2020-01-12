# FUSION 360 to KINETIC-NC tool library converter

Python script to automate the transfer of all tools which were generated in FUSION 360 to the KINETIC-NC software.

# Usage

 - Export all tools from FUSION 360 to a JSON file
 - Run the script on that file
   - E.g.: python TOOLS_from_FUSION_to_KINETIC-NC.py my_tool_library.json
 - A file named **ToolTable.txt** will be generated
 - Copy this file to:
   - **C:\ProgramData\KinetiC-NC**
 - Then start KINETIC-NC and the tool library will be the same as exported from FUSION 360
 
