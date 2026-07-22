install: requirements.txt
	pip install -r requirements.txt
run-agent:
	python src/agent.py
run-server:
	python src/vulnerable_server.py
run-payload:
	python examples/payload_demo.py
docker-build:
	docker build -t ai-hacking-simulator .
docker-run:
	docker run --rm ai-hacking-simulator
docker-compose-up:
	docker compose up -d --build
docker-compose-down:
	docker compose down
clean:
	find . -name "__pycache__" -delete