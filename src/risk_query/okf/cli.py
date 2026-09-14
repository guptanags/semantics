import argparse
from risk_query.graph.schema import initialize_federated
from risk_query.okf.bundle_pipeline import OkfGraphIngestionPipeline


def main():
    p = argparse.ArgumentParser(
        description='Ingest ontology, semantic, and metadata OKF bundles into three disjoint Kùzu graphs.'
    )
    p.add_argument(
        '--db',
        required=True,
        help='Root directory for the three Kùzu databases; ontology/semantic/metadata are created below it.',
    )
    p.add_argument('--ontology', default='knowledge/ontology')
    p.add_argument('--semantic', default='knowledge/semantic')
    p.add_argument('--metadata', default='knowledge/metadata')
    args = p.parse_args()

    graphs = initialize_federated(args.db)
    result = OkfGraphIngestionPipeline(
        graphs['ontology'],
        graphs['semantic'],
        graphs['metadata'],
    ).ingest(args.ontology, args.semantic, args.metadata)
    print(result)


if __name__ == '__main__':
    main()
