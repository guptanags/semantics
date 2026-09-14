from hashlib import sha256

class OntologyGraphIngester:
    def __init__(self, graph): self.graph=graph

    def ingest(self, documents):
        concepts=[d for d in documents if d['frontmatter'].get('kind')=='concept']
        rels=[]
        for d in concepts:
            fm=d['frontmatter']
            self.graph.execute('''
              MERGE (c:Concept {id:$id})
              SET c.name=$name,c.concept_type=$type,c.domain=$domain,
                  c.definition=$definition,c.status=$status,c.version=$version
            ''', {'id':fm['id'],'name':fm['title'],'type':fm.get('concept_type','BusinessConcept'),
                  'domain':fm.get('domain'),'definition':fm.get('description'),
                  'status':fm.get('status','ACTIVE'),'version':fm.get('version','brso-v0.1')})
            for r in fm.get('relationships',[]) or []:
                rels.append((fm['id'],r))

        ids={d['frontmatter']['id'] for d in concepts}
        missing=sorted({r['target'] for _,r in rels if r['target'] not in ids})
        if missing: raise ValueError(f'Ontology targets missing from bundle: {missing}')

        registry={}
        for _,r in rels:
            name=r['type']
            registry.setdefault(name, {'id':f'brso.rel.{name.lower()}','name':name,'status':'ACTIVE','version':'brso-v0.1'})
        for rt in registry.values():
            self.graph.execute('''
              MERGE (r:RelationshipType {id:$id})
              SET r.name=$name,r.status=$status,r.version=$version,
                  r.resolution_priority=100,r.transitive=false,r.symmetric=false,r.temporal=false
            ''', rt)

        for source,r in rels:
            name=r['type']
            registry.setdefault(name, {'id':f'brso.rel.{name.lower()}','name':name,'status':'ACTIVE','version':'brso-v0.1'})
            target=r['target']
            aid='brso.assertion.'+sha256(f'{source}|{name}|{target}'.encode()).hexdigest()[:24]
            self.graph.execute(f'''
              MATCH (s:Concept {{id:$source}})
              MATCH (t:Concept {{id:$target}})
              MERGE (s)-[e:{name} {{relationship_id:$aid}}]->(t)
              SET e.confidence=$confidence,e.approval_status=$approval
            ''', {'source':source,'target':target,'aid':aid,
                  'confidence':float(r.get('confidence',1.0)), 'approval':r.get('approval_status','approved')})
            self.graph.execute('''
              MERGE (a:RelationshipAssertion {id:$aid})
              SET a.relationship_type_id=$rtid,a.source_id=$source,a.target_id=$target,
                  a.confidence=$confidence,a.approval_status=$approval,a.ontology_version='brso-v0.1'
            ''', {'aid':aid,'rtid':registry[name]['id'],'source':source,'target':target,
                  'confidence':float(r.get('confidence',1.0)),'approval':r.get('approval_status','approved')})
            self.graph.execute('''
              MATCH (s:Concept {id:$source})
              MATCH (a:RelationshipAssertion {id:$aid})
              MATCH (t:Concept {id:$target})
              MATCH (rt:RelationshipType {id:$rtid})
              MERGE (s)-[:ASSERTS]->(a)
              MERGE (a)-[:TARGETS_ASSERTION]->(t)
              MERGE (a)-[:HAS_RELATIONSHIP_TYPE]->(rt)
            ''', {'source':source,'aid':aid,'target':target,'rtid':registry[name]['id']})

