from hashlib import sha256

def rid(kind, source, target):
    return f"brso.graph.{kind}." + sha256(f"{source}|{target}".encode()).hexdigest()[:20]

class MetadataGraphIngester:
    def __init__(self, graph):
        self.graph = graph

    def ingest(self, documents):
        for d in documents:
            fm=d["frontmatter"]
            kind=fm.get("kind")
            if kind == "physical_data_asset": self._asset(fm)
            elif kind == "physical_column": self._column(fm)
            elif kind == "physical_join": self._join(fm)
            else: raise ValueError(f"Unsupported metadata OKF kind: {kind}")
        for d in documents:
            fm=d["frontmatter"]
            if fm.get("kind") == "physical_column": self._link_column(fm)

    def _asset(self,fm):
        self.graph.execute("""
          MERGE (a:PhysicalDataAsset {id:$id})
          SET a.name=$name,a.database_name=$db,a.schema_name=$schema,a.object_type=$object_type
        """, {"id":fm["id"],"name":fm.get("physical_name",fm["title"]),
              "db":fm.get("database_name"),"schema":fm.get("schema_name"),"object_type":fm.get("object_type","TABLE")})

    def _column(self,fm):
        self.graph.execute("""
          MERGE (c:PhysicalColumn {id:$id})
          SET c.asset_id=$asset,c.name=$name,c.data_type=$dtype,c.nullable=$nullable,c.is_key=$is_key
        """, {"id":fm["id"],"asset":fm["asset_id"],"name":fm["physical_name"],
              "dtype":fm["data_type"],"nullable":bool(fm.get("nullable",True)),"is_key":bool(fm.get("is_key",False))})

    def _link_column(self,fm):
        self.graph.execute("""
          MATCH (a:PhysicalDataAsset {id:$asset})
          MATCH (c:PhysicalColumn {id:$column_id})
          MERGE (a)-[:ASSET_HAS_COLUMN {relationship_id:$rid,confidence:1.0,approval_status:'approved'}]->(c)
        """, {"asset":fm["asset_id"],"column_id":fm["id"],"rid":rid("asset_column",fm["asset_id"],fm["id"])})

    def _join(self,fm):
        self.graph.execute("""
          MATCH (s:PhysicalDataAsset {id:$source})
          MATCH (t:PhysicalDataAsset {id:$target})
          MERGE (s)-[r:ASSET_JOINS_TO_ASSET {relationship_id:$rid}]->(t)
          SET r.source_column_id=$source_col,r.target_column_id=$target_col,
              r.cardinality=$cardinality,r.preferred=$preferred,r.certified=$certified,r.join_type=$join_type
        """, {"source":fm["source_asset_id"],"target":fm["target_asset_id"],
              "rid":fm["id"],"source_col":fm["source_column_id"],"target_col":fm["target_column_id"],
              "cardinality":fm["cardinality"],"preferred":bool(fm.get("preferred",False)),
              "certified":bool(fm.get("certified",False)),"join_type":fm.get("join_type","INNER")})
