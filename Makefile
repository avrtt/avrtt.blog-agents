.PHONY: venv install run-research run-content run-dev run-smm clean

venv:
	python3 -m venv .venv
	@echo "Virtual environment created. Activate with: source .venv/bin/activate"

install:
	pip install -r requirements.txt

run-research:
	@if [ -z "$(TOPIC)" ]; then \
		echo "Usage: make run-research TOPIC=\"your research topic\""; \
		exit 1; \
	fi
	python -m agents.research_agent.main "$(TOPIC)"

run-content:
	@if [ -z "$(OUTLINE)" ]; then \
		echo "Usage: make run-content OUTLINE=\"path to outline file\""; \
		exit 1; \
	fi
	python -m agents.content_agent.main "$(OUTLINE)"

run-dev:
	python -m agents.dev_agent.main

run-smm:
	@if [ -z "$(POST)" ]; then \
		echo "Usage: make run-smm POST=\"path to markdown post\""; \
		exit 1; \
	fi
	python -m agents.smm_agent.main "$(POST)"

vector-search:
	@if [ -z "$(QUERY)" ]; then \
		echo "Usage: make vector-search QUERY=\"search query\""; \
		exit 1; \
	fi
	python -m agents.vector_search.cli search --query "$(QUERY)"

vector-stats:
	python -m agents.vector_search.cli stats

clean:
	rm -rf out/* logs/*
	@echo "Cleaned output and log directories"
