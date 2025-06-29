#!/usr/bin/env python3
"""
run_shacl.py

A configurable script to load RDF graphs from a SPARQL endpoint,
run SHACL rules (including SPARQL-based rules) via pySHACL, and
serialize both the enriched graph and a detailed SHACL report.
"""

import argparse
import logging
from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from pyshacl import validate

def load_remote_graph(endpoint: str, graph_uri: str) -> Graph:
    """
    Load an RDF graph from a SPARQL endpoint context.
    Forces a full triple load to surface any connectivity errors immediately.
    """
    logging.info(f"Loading graph <{graph_uri}> from SPARQL endpoint {endpoint}")
    store = SPARQLStore(endpoint=endpoint, context=graph_uri)
    g = Graph(store=store, identifier=graph_uri)
    # Touch every triple so failures happen now, not later
    list(g.triples((None, None, None)))
    logging.info(f"Graph <{graph_uri}> loaded ({len(g)} triples)")
    return g

def main():
    # ------------------------------------------------------------------------
    # 1. Parse command-line arguments
    # ------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Run SHACL/SPARQL-based rules on OCQA-AC via pySHACL"
    )
    parser.add_argument(
        "--endpoint",
        default="http://localhost:7200/repositories/your-repo",
        help="SPARQL endpoint URL"
    )
    parser.add_argument(
        "--abox",
        default="http://example.org/graphs/abox",
        help="Graph URI for the A-Box (instance data)"
    )
    parser.add_argument(
        "--tbox",
        default="http://example.org/graphs/tbox",
        help="Graph URI for the T-Box (schema/ontology)"
    )
    parser.add_argument(
        "--shapes",
        default="http://example.org/graphs/shapes",
        help="Graph URI for the SHACL shapes"
    )
    parser.add_argument(
        "--inference",
        choices=['none', 'rdfs', 'owlrl'],
        default='none',
        help="Entailment/inference mode for pySHACL"
    )
    parser.add_argument(
        "--output",
        default="inferred_abox.ttl",
        help="File path to write the enriched A-Box (Turtle format)"
    )
    parser.add_argument(
        "--report",
        default="shacl_report.ttl",
        help="File path to write the SHACL validation report (Turtle format)"
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------------
    # 2. Configure logging
    # ------------------------------------------------------------------------
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s"
    )

    # ------------------------------------------------------------------------
    # 3. Load the remote graphs
    # ------------------------------------------------------------------------
    abox_graph = load_remote_graph(args.endpoint, args.abox)
    tbox_graph = load_remote_graph(args.endpoint, args.tbox)
    shapes_graph = load_remote_graph(args.endpoint, args.shapes)

    # ------------------------------------------------------------------------
    # 4. Merge T-Box into A-Box so SHACL rules see the full ontology
    # ------------------------------------------------------------------------
    enriched = Graph()
    enriched += abox_graph
    enriched += tbox_graph
    logging.info(f"Merged graph has {len(enriched)} triples before rules")

    # ------------------------------------------------------------------------
    # 5. Run pySHACL validation + rule execution
    #    - inference: controls OWL/RDFS entailment ('none', 'rdfs', 'owlrl')
    #    - advanced: enables SHACL-SPARQL rules
    #    - debug: prints extra debugging info
    #    - inplace: writes inferred triples into the 'enriched' graph
    # ------------------------------------------------------------------------
    conforms, report_graph, _ = validate(
        data_graph=enriched,
        shacl_graph=shapes_graph,
        inference=args.inference,
        advanced=True,
        inplace=True,
        debug=True
    )
    logging.info(f"SHACL conforms: {conforms}")
    logging.info(f"Graph now has {len(enriched)} triples after rule execution")

    # ------------------------------------------------------------------------
    # 6. Serialize the enriched graph and the SHACL report
    # ------------------------------------------------------------------------
    enriched.serialize(destination=args.output, format="turtle")
    logging.info(f"Inferred A-Box written to {args.output}")

    report_graph.serialize(destination=args.report, format="turtle")
    logging.info(f"SHACL report written to {args.report}")

if __name__ == "__main__":
    main()
