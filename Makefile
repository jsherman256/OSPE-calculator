run: build
	venv/bin/streamlit run app.py

venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

build: venv