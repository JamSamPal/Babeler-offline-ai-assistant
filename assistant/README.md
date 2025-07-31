# Assistant

## json
Holds the contents of the assistant's "brain" including its personality and what it knows, the latter can be queried and updated by the user

## python
Enables the running of the assistant: the tts and stt functionalities as well as its ability to interpret inputs as queries/updates of its personality and knowledge.

command_parser.py contains the available commands the user can access, including those to update the assistant's knowledgebase which holds all its facts and its personality like its name and tone of voice.

## voice models

wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

or

curl -O https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

then extract
