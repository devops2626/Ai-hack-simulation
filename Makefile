start: analyze
	python3 ai_hack_cli.py

analyze:
	python3 jarvis_analytics.py

jarvis:
	python3 jarvis_terminal.py

export:
	python3 export_to_obsidian.py
