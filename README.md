# Readme

## Getting Started

As pre-req we require the following software to be installed:
  
  - python 3.6 http://www.python36.com/install-python36-on-ubuntu/
    - pip (might be aliased as pip3 or pip3.6, installed as part of python 3)
  - virtualenv
    - run `pip install virtualenv`.
  
With the commands above, some systems might alias the commands as pip3 or pip3.6. Same with python.
  
  
 Once these are installed, clone this repo.
 ```bash
git clone git@bitbucket.org:omtio/pomegranate-cli.git && pomegranate-cli
```

Now we are in the folder and have the code. We need to create an environment to run the code in. This will allow us to isolate our code from the rest of the code on the system.

```bash 

virtualenv env -p `which python3` 

```

```bash

source env/bin/activate && pip install -r requirements.txt
```

*if python3 doesn't work, try python3.6 in the command above*

phew, all of that work to be able to run some python.  Before we can get studying, we ned to add a few words to study.

```
python app.py --add 一 --list numbers
python app.py --add 二 --list numbers
python app.py --add 三 --list numbers
python app.py --add 四 --list numbers
python app.py --add 五 --list numbers
```

At this point we now have some words associated with a list. Running the app ```python app.py``` will guide us through the study flow.