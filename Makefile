.PHONY: validate flagship-check

validate:
	python scripts/validate_repository.py
	python scripts/schema_check.py
	python scripts/verify_al_contract.py
	python scripts/doc_tests.py

flagship-check:
	python scripts/validate_repository.py
