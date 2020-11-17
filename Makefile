all: clean venv

venv: requirements.txt
    test -d venv || python -m venv venv
    source venv/bin/activate && pip install -r requirements.txt
    touch venv
    
clean:
    rm -rf venv