import re
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredFileLoader

file_path = "test_data/ipg230103.xml"

# Read the concatenated XML from the file
with open(file_path, "r") as file:
    concatenated_xml = file.read()

# Split the concatenated XML using the separator
separator = r"(?<=\?xml version=\"1\.0\" encoding=\"UTF-8\"\?>)"
individual_xml_documents = re.split(separator, concatenated_xml)

# Iterate over each individual XML document
for i, xml_document in enumerate(individual_xml_documents):
    # Add the missing XML declaration for each document
    
    # xml_document = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + xml_document
    

    soup = BeautifulSoup(xml_document, "xml")
    
    # descripition_tags = soup.find_all('description', id="description")
    
    # # print(soup.prettify())
    # # print(soup.find_all('p', id="description"))
    # # print(soup.find_all('p', id="description").findChildren())
    # if len(descripition_tags)> 0:
    #     for tags in descripition_tags:
    #         # print(tags.findChildren())
    #         print(soup.prettify())

    #         print("-----------------------------------------------------------------")



    # Perform XML data processing using BeautifulSoup
    # For example, you can access specific elements, extract data, or manipulate the XML structure
    # Here's an example that prints the XML structure

    # print(soup.prettify())
    # descripition_tags = soup.find_all('description')
    # if len(descripition_tags) > 0:
    #     # If desired, you can write the processed document back to the file
    filename = f"test_data/ipg230103/document_{i + 1}.xml"
    with open(filename, "w") as file:
        file.write(str(soup))

    #     print(f"Created {filename} successfully.")

    # soup = BeautifulSoup(xml_document, 'xml')
    # descripition_tags = soup.find_all('description')
    # if len(descripition_tags) > 0:
    #     print(xml_document)
    
    # for descrpition_tag in descripition_tags:
        
    #     child_tags = descrpition_tag.find_all(recursive=False)
    #     print(child_tags)
        

