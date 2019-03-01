python -m venv VENV
VENV\Scripts\activate
python -m pip install --upgrade pip
pip install lxml
pip install seaborn
pip freeze > requirements.txt
VENV\Scripts\deactivate
