from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .models import ScenarioQueryRequest, BusinessQueryRequest, UserQueryRequest, GraphRequest
from risk_query.pipeline.scenario_query_pipeline import ScenarioQueryPipeline
from risk_query.graph.repositories.graph_explorer_repo import GraphExplorerRepository
from risk_query.ui.app import index

app = FastAPI(title="Risk Semantic Query")
pipeline = ScenarioQueryPipeline.from_config()
graph_explorer = GraphExplorerRepository({"ontology": pipeline.graphs.ontology, "semantic": pipeline.graphs.semantic, "metadata": pipeline.graphs.metadata})

@app.post("/v1/scenario/query")
def scenario_query(request: ScenarioQueryRequest):
    return pipeline.execute_scenario(request)

@app.post("/v1/query/explain")
def explain_query(request: BusinessQueryRequest):
    return pipeline.explain_business_query(request)

def run():
    import uvicorn
    uvicorn.run("risk_query.api.routes:app", host="0.0.0.0", port=8080, reload=False)


@app.get("/")
def ui():
    return index()

@app.get("/ui")
def ui_alias():
    return index()

@app.post("/v1/query")
def user_query(request: UserQueryRequest):
    return pipeline.execute_user_query(request)

@app.post("/v1/graph/snapshot")
def graph_snapshot(request: GraphRequest):
    return graph_explorer.snapshot(request.layer, request.limit)
