run: build
	venv/bin/streamlit run "CO2 Limit - Basic.py"

venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

build: venv