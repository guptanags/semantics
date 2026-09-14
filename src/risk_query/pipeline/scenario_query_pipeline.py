from __future__ import annotations
from pathlib import Path
import uuid
import yaml

from risk_query.graph.federation import FederatedGraphs
from risk_query.graph.repositories.federation_registry import FederationRegistry
from risk_query.graph.repositories.ontology_repo import OntologyRepository
from risk_query.graph.repositories.semantic_repo import SemanticRepository
from risk_query.graph.repositories.metadata_repo import MetadataRepository
from risk_query.resolver.concept_resolver import ConceptResolver
from risk_query.resolver.entity_resolver import EntityResolver
from risk_query.resolver.metric_resolver import MetricResolver
from risk_query.planner.planner import QueryPlanner
from risk_query.sql.generator import SqlGenerator
from risk_query.sql.validator import SqlValidator
from risk_query.execution.security import QuerySecurityPolicy
from risk_query.execution.executor import QueryExecutor
from risk_query.llm.vertex_client import VertexAIClient
from risk_query.llm.intent_extractor import IntentExtractor
from risk_query.domain.result import QueryResult, Provenance

class ScenarioQueryPipeline:
    def __init__(
        self, graphs, intent_extractor, planner, sql_generator,
        sql_validator, executor, config
    ):
        self.graphs = graphs
        self.graph = graphs.ontology  # compatibility alias; ontology only
        self.intent_extractor = intent_extractor
        self.planner = planner
        self.sql_generator = sql_generator
        self.sql_validator = sql_validator
        self.executor = executor
        self.config = config
        self.federation_registry = FederationRegistry(config["graph"].get("federation_registry_path", "config/federation.yaml"))

    @classmethod
    def from_config(cls, config_path="config/application.yaml"):
        config = yaml.safe_load(Path(config_path).read_text())
        graphs = FederatedGraphs.from_config(config)

        ontology_repo = OntologyRepository(graphs.ontology)
        semantic_repo = SemanticRepository(graphs.semantic)
        metadata_repo = MetadataRepository(graphs.metadata)

        concept_resolver = ConceptResolver(ontology_repo)
        entity_resolver = EntityResolver(ontology_repo)
        metric_resolver = MetricResolver(semantic_repo)
        planner = QueryPlanner(concept_resolver, metric_resolver)

        llm_cfg = config["llm"]
        vertex = VertexAIClient(
            llm_cfg["project_id"],
            llm_cfg["location"],
            llm_cfg["model"],
        )
        intent_extractor = IntentExtractor(
            vertex,
            "src/risk_query/llm/prompts/intent_extraction.txt",
        )

        executor = QueryExecutor(
            dry_run=config["execution"]["dry_run"]
        )
        return cls(
            graphs, intent_extractor, planner, SqlGenerator(),
            SqlValidator(), executor, config
        )

    def execute_scenario(self, request):
        query_id = str(uuid.uuid4())
        intent = self.intent_extractor.extract(
            request.extraction_criteria,
            request.scenario_context,
        )

        # Scenario context should carry affected canonical concept IDs.
        # Preserve them in intent context so downstream resolvers do not
        # rediscover scenario semantics.
        intent.context.update(request.scenario_context)

        plan = self.planner.plan(intent)

        # Physical metadata resolution is intentionally required before SQL.
        if not plan.root_dataset_id:
            return QueryResult(
                status="DATA_UNAVAILABLE",
                warnings=[
                    "No logical/physical dataset binding has been resolved yet. "
                    "The semantic layer cannot manufacture the requested facts."
                ],
                provenance=Provenance(
                    query_id=query_id,
                    ontology_version="brso-v0.1",
                ),
            )

        sql = self.sql_generator.generate(plan)
        self.sql_validator.validate(sql)
        rows = self.executor.execute(sql)

        return QueryResult(
            status=plan.resolution_status,
            data=rows,
            row_count=len(rows),
            sql=sql,
            provenance=Provenance(
                query_id=query_id,
                ontology_version="brso-v0.1",
            ),
        )

    def execute_user_query(self, request):
        """Execute a natural-language user query through the same governed path.

        The UI uses this endpoint. Vertex AI is limited to intent extraction;
        graph resolution, planning, SQL generation and validation remain deterministic.
        """
        query_id = str(uuid.uuid4())
        intent = self.intent_extractor.extract([request.query], request.context)
        intent.context.update(request.context)
        plan = self.planner.plan(intent)

        if not plan.root_dataset_id:
            return QueryResult(
                status="DATA_UNAVAILABLE",
                warnings=[
                    "No logical/physical dataset binding has been resolved yet. "
                    "The semantic layer cannot manufacture the requested facts."
                ],
                provenance=Provenance(query_id=query_id, ontology_version="brso-v0.1"),
            ).model_dump()

        sql = self.sql_generator.generate(plan)
        self.sql_validator.validate(sql)
        rows = self.executor.execute(sql)
        return QueryResult(
            status=plan.resolution_status,
            data=rows if isinstance(rows, list) else [],
            row_count=len(rows) if isinstance(rows, list) else 0,
            sql=sql,
            provenance=Provenance(query_id=query_id, ontology_version="brso-v0.1"),
        ).model_dump()

    def explain_business_query(self, request):
        # Reverse path is deliberately deterministic after parsing SQL.
        # A production implementation should use sqlglot AST -> metadata ->
        # semantic -> ontology and construct the explanation from graph facts.
        return {
            "status": "NOT_SUPPORTED",
            "message": "Reverse SQL explanation adapter is scaffolded; "
                       "connect sqlglot + metadata graph bindings here."
        }
