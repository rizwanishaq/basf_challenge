import re
from bs4 import BeautifulSoup

def explodeXML(origfname):
    """Split an original file made of concatenated XML files into its constituent files:
    fname.xml becomes fname-1.xml ... fname-n.xml"""

    xml_documents = []

    with open(origfname, "r") as fin:
        xml_content = fin.read()

    # Split the concatenated XML content into separate documents
    separator = r"(?<=\?xml version=\"1\.0\" encoding=\"UTF-8\"\?>)"
    xml_documents = re.split(separator, xml_content)

    # Process each XML document
    for i, xml_document in enumerate(xml_documents):
        # Validate and process each individual XML document
        # print(f"XML Document {i+1}:")
        print('---------------------------------')
        soup = BeautifulSoup(xml_document, "xml")
        tags = soup.find_all("abstract")
        if len(tags)> 0:
            for tag in tags:
                child_tags = tag.find_all('p')
                for p_tag in child_tags:
                    print(p_tag.get_text())
                    # if p_tag.get_text().startswith("FIG. "):
                    #     pass
                    # else:
                    #     print(p_tag.get_text())
            

explodeXML("test_data/ipg230103.xml")