This package migrates Java based Lambda source code to SpringBoot application using OpenAI GenAI API calls. Below architecture will allow migration of around 40 Lambdas
to SpringBoot one by one by preserving the dependencies and replacing AWS services with respective SpringBoot inherent libraries. 

lambda-to-spring-migrator/
│
├── README.md
├── pyproject.toml
├── requirements.txt
│
├── input/
│   ├── lambdas/
│   │   ├── lambda-order-service/
│   │   │   ├── pom.xml
│   │   │   └── src/main/java/...
│   │   ├── lambda-payment-service/
│   │   └── ...
│   └── shared-libs/
│
├── analysis/
│   ├── __init__.py
│   ├── java_parser.py
│   ├── dependency_graph.py
│   ├── aws_usage_scanner.py
│   └── lambda_classifier.py
│
├── orchestration/
│   ├── __init__.py
│   ├── graph.py
│   ├── state.py
│   ├── nodes/
│   │   ├── analyze_lambda.py
│   │   ├── generate_blueprint.py
│   │   ├── migrate_class.py
│   │   ├── reconcile_files.py
│   │   ├── compile_and_test.py
│   │   └── fix_errors.py
│   └── routing.py
│
├── prompts/
│   ├── analysis/
│   │   ├── classify_lambda.txt
│   │   ├── identify_aws_services.txt
│   │   └── extract_entrypoints.txt
│   ├── spring/
│   │   ├── generate_project_structure.txt
│   ├── migration/
│   │   ├── migrate_java_class.txt
│   └── validation/
│       ├── self_review.txt
│       └── compile_error_fix.txt
│
├── execution/
│   ├── __init__.py
│   ├── runner.py
│   ├── batch_runner.py
│   ├── maven_executor.py
│   └── diff_writer.py
│
├── output/
│   ├── spring-apps/
│   │   ├── order-service/
│   │   │   ├── pom.xml
│   │   │   └── src/main/java/...
│   │   └── payment-service/
│   └── reports/
│       ├── migration-summary.json
│       └── compile-errors.json
│
├── tests/
│   ├── test_java_parser.py
│   ├── test_dependency_graph.py
│   └── test_langgraph_flow.py
│
└── ci/
    ├── github-actions.yaml
    └── preflight-checks.sh
