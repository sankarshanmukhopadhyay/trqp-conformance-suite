.PHONY: validate flagship-check assurance-check evidence v3-candidate-check

validate:
	python scripts/validate_repository.py
	python scripts/schema_check.py
	python scripts/verify_al_contract.py
	python scripts/validate_project_status.py
	python scripts/doc_tests.py
	python scripts/validate_v3_candidate.py
	python -m unittest tests.test_v3_candidate

v3-candidate-check:
	python scripts/validate_v3_candidate.py
	python -m unittest tests.test_v3_candidate

assurance-check: validate
	python scripts/generate_assurance_artifacts.py

evidence: assurance-check

flagship-check:
	python scripts/validate_repository.py
