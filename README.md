# schoolPlanning

# Installation local use
On your computer:

Install the python environment:
```sh
python3 -m venv venv

#Activation
source venv/bin/activate
#(Windows)
venv\Scripts\activate.bat

# install Flask:
pip install Flask

# if you need : install your library saved in requirements.txt
pip install -r ./requirements.txt
# With Fish : source venv/bin/activate.fish
```

# lancer le server
On your computer:

```sh
flask --app app run --port [numero de port]
```