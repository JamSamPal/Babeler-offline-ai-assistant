# Description

An offline ai assistant which can learn from documentation and then answer questions on what it has been taught, enabling you to use natural language to query papers, articles etc... Alternatively, you can be the one to teach it by conversing with it.

- Supports a mic/speaker setup so you can converse naturally
  
- Personality customization
  
- Persists learned facts and configuration to disk

## How to run

pip install -e .

python -m spacy download en_core_web_sm

sudo apt install espeak

python run.py (--text)      (no mic or speaker mode)


