from __future__ import annotations

NODE_TABLES = {
    "ontology": [("Concept","ontology"),("RelationshipType","ontology"),("RelationshipAssertion","ontology"),("SemanticRole","ontology"),("Synonym","ontology"),("ExternalMapping","ontology"),("OntologyVersion","ontology")],
    "semantic": [("SemanticDataElement","semantic"),("LogicalDataset","semantic")],
    "metadata": [("PhysicalDataAsset","metadata"),("PhysicalColumn","metadata")],
}
REL_TABLES = {
    "ontology": ["IS_A","PART_OF","HAS_MEMBER","PART_OF_GEOGRAPHY","CONTAINS_GEOGRAPHY","HAS_CLASSIFICATION","HAS_PRIMARY_INDUSTRY","OPERATES_IN","DOMICILED_IN","HAS_FACILITY","HAS_EXPOSURE","AGAINST","MEASURED_BY","DENOMINATED_IN","AS_OF","ASSERTS","TARGETS_ASSERTION","HAS_RELATIONSHIP_TYPE","HAS_ROLE","HAS_SYNONYM","HAS_EXTERNAL_MAPPING","HAS_VERSION"],
    "semantic": ["ELEMENT_PART_OF_DATASET"],
    "metadata": ["ASSET_HAS_COLUMN","ASSET_JOINS_TO_ASSET"],
}

def _rows(result):
    if hasattr(result,"get_all"): return result.get_all()
    if hasattr(result,"get_as_pl"):
        try: return result.get_as_pl().to_dicts()
        except Exception: pass
    return list(result) if result is not None else []

def _scalar(value):
    return value if isinstance(value,(str,int,float,bool)) or value is None else str(value)

class GraphExplorerRepository:
    def __init__(self, graphs): self.graphs=graphs

    def snapshot(self, layer="all", limit=250):
        allowed={"all","ontology","semantic","metadata"}
        if layer not in allowed: raise ValueError(f"Unsupported graph layer: {layer}")
        layers=[layer] if layer!="all" else ["ontology","semantic","metadata"]
        nodes=[]; edges=[]
        for current in layers:
            graph=self.graphs[current]
            node_ids=set()
            for table, table_layer in NODE_TABLES[current]:
                try:
                    for row in _rows(graph.execute(f"MATCH (n:{table}) RETURN n LIMIT {limit}")):
                        value=row[0] if isinstance(row,(list,tuple)) else row.get("n",row)
                        if isinstance(value,dict): ident=value.get("id"); name=value.get("name") or ident; props={k:_scalar(v) for k,v in value.items()}
                        else: ident=getattr(value,"id",None); name=getattr(value,"name",None) or ident; props={}
                        if ident is None: continue
                        ident=str(ident)
                        if ident in node_ids: continue
                        node_ids.add(ident); nodes.append({"id":ident,"label":str(name or ident),"type":table,"layer":table_layer,"properties":props})
                except Exception: continue
            for rel in REL_TABLES[current]:
                try:
                    for row in _rows(graph.execute(f"MATCH (s)-[r:{rel}]->(t) RETURN s.id, t.id LIMIT {limit}")):
                        source,target=(row.get("s.id"),row.get("t.id")) if isinstance(row,dict) else (row[0],row[1])
                        source,target=str(source),str(target)
                        if source in node_ids and target in node_ids: edges.append({"id":f"{rel}:{source}:{target}","source":source,"target":target,"label":rel,"layer":current})
                except Exception: continue
        return {"nodes":nodes[:limit],"edges":edges[:limit],"layer":layer,"disjoint":True,"graphs":layers}
