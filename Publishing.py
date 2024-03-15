from pylode import OntDoc, MakeDocco, APP_DIR
#from pathlib import Path
from os.path import join, dirname, abspath

# initialise
#od = OntDoc(ontology="C:/Users/verwalter/Documents/GitHub/OntologyForConstructionQualityAssurance/08_Puclication/OCQA03.ttl")
#od = OntDoc(Path(__file__).parent / "OBPA.ttl")
#Version 3.0.4
#input_rdf = Path(__file__).parent / "OBPA.ttl"
#output_html = Path(__file__).parent / "OBPA.html"
#print(input_rdf)

#od = OntDoc(ontology=input_rdf)
#html = od.make_html(include_css=True, destination=output_html)

#Version 2.8.5
#input_rdf = Path(__file__).parent / "OBPA.ttl"
#output_html = Path(__file__).parent / "OBPA.html"
#print(input_rdf)
#print(output_html)
TESTS_DIR = dirname(abspath(__file__))
print(TESTS_DIR)
print(join(TESTS_DIR, "230707_OCQA_03.ttl"))
#od=OntDoc(default_language="en",source_info=input_rdf, g=input_rdf)
h = MakeDocco(input_data_file=join(TESTS_DIR, "230707_OCQA_03.ttl"))
# generate the HTML doc
h.document(destination=join(TESTS_DIR, "newindex.html"))


#html = OntDoc(source_info=input_rdf, include_css=True, outputformat="html", default_language="en",get_curies_online=False,use_curies_stored=True, g=any, destination)
#html = OntDoc(input_rdf).make_html(destination="OCQA_03some-resulting-html-file.html")
# produce HTML
#html = od.make_html()

# or save HTML to a file
#od.make_html(destination="OCQA_03some-resulting-html-file.html")
#html = OntDoc(ontology=input_rdf)
#html._make_restriction_html