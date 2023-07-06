import os
import html
import datetime
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from glob import glob
from tqdm import tqdm




class ParseFile():
    def __init__(self, data_folder, logging=False):
        self.data_folder = data_folder
        self.logging = logging
        
   



    def parse_uspto_file(self, bs):
        """
        Parses a USPTO patent in a BeautifulSoup object.
        """

        application_type = bs.find('application-reference')['appl-type']

        if application_type != 'utility':
            return None

        abstracts = []
        for el in bs.find_all('abstract'):
            abstracts.append(el.text.strip('\n'))
        
        # FILTERING OUT NO ABSTRACT PATENTS HERE
        if len(abstracts) == 0:
            return None

        publication_title = bs.find('invention-title').text
        publication_num = bs['file'].split("-")[0]
        publication_date = bs.find('publication-reference').find('date').text
        


        # International Patent Classification (IPC) Docs:
        # https://www.wipo.int/classifications/ipc/en/
        sections = {}
        section_classes = {}
        section_class_subclasses = {}
        section_class_subclass_groups = {}
        for classes in bs.find_all('classifications-ipcr'):
            for el in classes.find_all('classification-ipcr'):

                section = el.find('section').text
                            
                classification  = section
                classification += el.find('class').text
                classification += el.find('subclass').text
                
                group = el.find('main-group').text + "/"
                group += el.find('subgroup').text

                sections[section] = True
                section_classes[section+el.find('class').text] = True
                section_class_subclasses[classification] = True
                section_class_subclass_groups[classification+" "+group] = True
                
        authors = []
        for parties in bs.find_all('parties'):
            for applicants in parties.find_all('applicants'):
                for el in applicants.find_all('addressbook'):
                    first_name = el.find('first-name').text
                    last_name = el.find('last-name').text
                    authors.append(first_name + " " + last_name)

        publication_date = datetime.strptime(publication_date, '%Y%m%d') 

        descriptions = []
        for el in bs.find_all('description'):
            descriptions.append(el.text.strip('\n'))
            
        claims = []
        for el in bs.find_all('claim'):
            claims.append(el.text.strip('\n'))

        uspto_patent = {
            "publication_title": publication_title,
            "publication_number": publication_num,
            "publication_date": '{:%B %d, %Y}'.format(publication_date),
            "application_type": application_type,
            "authors": authors, # list
            "sections": list(sections.keys()),
            "section_classes": list(section_classes.keys()),
            "section_class_subclasses": list(section_class_subclasses.keys()),
            "section_class_subclass_groups": list(section_class_subclass_groups.keys()),
            "abstract": abstracts, # list
            "descriptions": descriptions, # list
            "claims": claims # list
        }
        
            
        if self.logging:
            
            
            
            print("Filename:", self.filename)
            print("\n\n")
            print("\n--------------------------------------------------------\n")

            print("USPTO Invention Title:", publication_title)
            print("USPTO Publication Number:", publication_num)
            print("USPTO Publication Date:", publication_date)
            print("USPTO Application Type:", application_type)
                
            count = 1
            for classification in section_class_subclass_groups:
                print("USPTO Classification #"+str(count)+": " + classification)
                count += 1
            print("\n")
            
            count = 1
            for author in authors:
                print("Inventor #"+str(count)+": " + author)
                count += 1

            print("\n--------------------------------------------------------\n")

            print("Abstract:\n-----------------------------------------------")
            for abstract in abstracts:
                print(abstract)

            print("Description:\n-----------------------------------------------")
            for description in descriptions:
                print(description)

            print("Claims:\n-----------------------------------------------")
            for claim in claims:
                print(claim)

        return uspto_patent


    def gen_entry(self, filename,uspto_patent):

        uspto_db_entry = {
            "filename":filename,
            "publication_title": uspto_patent['publication_title'],
            "patent_number": uspto_patent['publication_number'],
            "publication_date": uspto_patent['publication_date'],
            "application_type": uspto_patent['application_type'],
            # "authors": ','.join(uspto_patent['authors']),
            "sections": ','.join(uspto_patent['sections']),
            "section_classes": ','.join(uspto_patent['section_classes']),
            "section_class_subclasses": ','.join(uspto_patent['section_class_subclasses']),
            "section_class_subclass_groups": ','.join(uspto_patent['section_class_subclass_groups']),
            "abstract": '\n'.join(uspto_patent['abstract']),
            "descriptions": '\n'.join(uspto_patent['descriptions']),
            "claims": '\n'.join(uspto_patent['claims'])
        }

        return uspto_db_entry

    
    def __call__(self):
        count = 1
        success_count = 0
        errors = []
        patentEntries=[]
        for filename in glob(os.path.join(self.data_folder, "*.xml")):
       
            xml_text = html.unescape(open(filename, 'r').read())
            for patent in tqdm(xml_text.split("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")):

                if patent is None or patent == "":
                    continue
        
                bs = BeautifulSoup(patent,features="html.parser")

                if bs.find('sequence-cwu') is not None:
                    continue # Skip DNA sequence documents

                application = bs.find('us-patent-grant')
                if application is None: # If no application, search for grant
                    application = bs.find('us-patent-application')
                title = "None"
        
                try:
                    title = application.find('invention-title').text
                except Exception as e:          
                    print("Error", count, e)

                uspto_patent=None
                try:
                    uspto_patent = self.parse_uspto_file(application)
                    if uspto_patent != None:
                        entry = self.gen_entry(filename,uspto_patent)
                        if len(entry['abstract']) > 0:
                            patentEntries.append(entry)
                            success_count += 1
                except Exception as e: 
                    exception_tuple = (count, title, e)
                    errors.append(exception_tuple)
                    print(exception_tuple)
                
                if uspto_patent != None:
                    if (success_count+len(errors)) % 50 == 0:
                        # print(success_count, filename, title)
                        pass
                count += 1


        print("\n\nErrors\n------------------------\n")
        for e in errors:
            print(e)
            
        print("Success Count:", success_count)
        print("Error Count:", len(errors))

        
        
        df = pd.DataFrame(patentEntries)        
        df = df.replace(',',' ')
        df.to_csv(f'{filename.replace(".xml",".csv")}',index=False)

        return filename.replace(".xml",".csv")



if __name__ == '__main__':
    data_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data"
    )
    
    parser = ParseFile(data_folder)
    parsed_csv_file = parser()
