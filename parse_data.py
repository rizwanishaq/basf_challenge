import os
from Parser.parsing import ParseFile



# Parsing the .xml files
data_folder = os.path.join(os.path.dirname(__file__),"data")
parser = ParseFile(data_folder)
parsed_csv_file = parser()