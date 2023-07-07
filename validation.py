import json
parsed_json_file = 'data/ipg230103.json'

with open(parsed_json_file) as json_file:
    data = json.load(json_file)



for d in data:
    print(f"Publication Title: {d['publication_title']}, Application_type: {d['application_type']}, Section: {d['sections']}, Section_class: {d['section_classes']}, Section_subclass: {d['section_class_subclasses']}, Section_subclass_group: {d['section_class_subclass_groups']}")
        
            
            
            