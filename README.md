# Recipe Finding Chatbot
## Acknowledgment
This chatbot is based off of the pizza ordering chatbot found at https://github.com/Dingdong-LIU/Lab1_Chatbot_Rasa/tree/main/chatbot/02-forms-pizza-ordering-chatbot

## Install Anaconda
Install Anaconda via https://conda.io/projects/conda/en/latest/user-guide/install/index.html#

### Create a virtualenv via Conda
```bash
conda create -n rasa_env python=3.9
```
This will create a Conda virtual environment with <code>Python3.9</code>. Then you need to install <code>rasa</code> via <code>pip3</code>.

### Activate virtual environment
```bash
conda activate rasa_env
```
### Install rasa 3
```bash
pip3 install rasa
```

### Install edamam
```bash
python -m pip install py-edamam
```

### Uninstall uvloop
```bash
python -m pip uninstall uvloop
```
Note: this library leads to exceptions with forms

### Running the chatbot
First, clone the repository.
Then, open two terminal windows and activate rasa_env in both
In one window, run the action server:
```bash
rasa run actions
```

In another window, run the chatbot:
```bash
rasa run shell
```

## Links


*   [Rasa Forms Documentation](https://rasa.com/docs/rasa/forms)
*   [Rasa Project on GitHub](https://github.com/RasaHQ/conversationl-ai-course-3.x/tree/main/video-09-1-basic-forms)
