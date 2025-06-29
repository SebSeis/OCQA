from rdflib import Graph
from pyshacl import validate

shape_graph_file = \
    'C:/Users/Seiss_Consultant/OneDrive - Technische Universität Ilmenau/Neuer Ordner/10_Veroeffentlichungen/2024_EG-ICE/SHACL_Rule.ttl'
#C:\Users\verwalter\Documents\GitHub\OntologyForConstructionQualityAssurance\06_Example\InspectionCost
shacl_ttl_file = \
    'C:/Users/Seiss_Consultant/OneDrive - Technische Universität Ilmenau/Neuer Ordner/10_Veroeffentlichungen/2024_EG-ICE/EvauationCase2Version3.ttl'
    #'C:/Users/verwalter/OneDrive - Technische Universität Ilmenau/03_Promotion/03_Veröffentlichungen/ECPPM_Judith/02_Rules/rulefiles.ttl'
    #C:\Users\Seiss_Consultant\OneDrive - Technische Universität Ilmenau\Neuer Ordner\10_Veroeffentlichungen\2024_EG-ICE

shape_graph = Graph().parse(source=shape_graph_file, format="turtle")
data_graph = Graph().parse(source=shacl_ttl_file, format="turtle")
data_graph_orig = Graph()
for t in data_graph:
    data_graph_orig.add(t)  

conforms, result_graph, result_text = validate(data_graph, shacl_graph=shape_graph, advanced=True, inference='none', debug=True, js=True)
#assert not conforms
added_triples = data_graph - data_graph_orig
print('Added triples: ', len(added_triples))
print(added_triples.serialize(format="turtle"))

knows_query = """

prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
prefix xsd:   <http://www.w3.org/2001/XMLSchema#> 
prefix rdfs:               <http://www.w3.org/2000/01/rdf-schema#>
prefix owl:   <http://www.w3.org/2002/07/owl#> 
prefix ocqa:                <https://w3id.org/ocqa#>
prefix ocqa-screed:                <https://w3id.org/ocqa-screed-inspections#>
prefix ocqa-risk:                <http://www.semanticweb.org/sebas/ontologies/2023/7/untitled-ontology-21#>


	SELECT  ?PotentialNonConfirmity IF(?AppraisalCost > (?AverageNCC * ?Likelihood * ?PotentialNCC AS ?MonetaryRiskValue),"INSPECTION IS NOT RECOMMMENDED","INSPECTION RECOMMMENDED") AS ?DecisionSupport
 
	WHERE {ocqa-screed:42015 ocqa-risk:detects ?PotentialNonConfirmity;
                                ocqa-ac:hasAppraisalCost ?AppraisalCost.
	             ?PotentialNonConfirmity  ocqa-risk:hasAverageNCC ?AverageNCC;
                              ocqa-risk:hasLikelihood ?Likelihood;
                            ocqa-risk:hasPotentialNCC ?PotentialNCC
                              
                }
                #?PotentialNonConfirmity [Get all assigned costs as ?SpecificNonConfirmityCost].}
                #SELECT DISTINCT ?individual
#WHERE {
#  ?individual rdf:type owl:NamedIndividual.
#}


"""
#print(data_graph.serialize(format="turtle"))

#qres = data_graph.query(knows_query)
#print (qres)
#for row in qres:
    #print(f"{row.this}")
	#print(row)  