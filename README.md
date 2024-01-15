# School Planning

Work in progress...

### Built With

* 🖊️ Markdown
* 🐙 Github
* 💻 VsCode

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Git
```sh
sudo apt-get install git
```

### Installation

Clone the repo
```sh
git clone git@github.com:lolothi/schoolPlanning.git
```

## Usage
- to calculate the cost of the month with school activities 
- to check the price with the school bill
- to keep in memory the special activities, with day off or personnel strike


# Installation local use
On your computer:

Install the python environment:
```sh
python3 -m venv venv

#Activation
source venv/bin/activate
# With Fish : source venv/bin/activate.fish
#(Windows)
venv\Scripts\activate.bat

# install Flask:
pip install Flask

# if you need : install your library saved in requirements.txt
pip install -r ./requirements.txt

```

# Run the server
On your computer:

```sh
flask --app app run --port [numero de port]
```