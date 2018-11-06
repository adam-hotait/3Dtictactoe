# 3Dtictactoe
Academic project - Last year MSc studies @ [CentraleSupélec](http://www.centralesupelec.fr/en)

_Gasser Philip, Hotait Adam, Lagattu Mickael_


## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

This projects needs `Python3`, as well as the `numpy` and `pygame` packages.
If `Python3` is installed on your machine, you can automatically install the requirements using pip:

```
pip install -r requirements.txt
```

## Play

To run the game, just launch `TicTacToe.py`:

```
python TicTacToe.py
```

## Built With

* [Python3](https://www.python.org/) - The programming language used
* [NumPy](http://www.numpy.org/) - Used for back-end board management
* [pygame](https://www.pygame.org/) - Used for the game's GUI

## Version control

We use [GitHub](https://github.com/adam-hotait/3Dtictactoe) for version control. 

## Troubleshooting

#### Impossible to connect
The LAN game mode does not work on the `eduroam` network and might not work with some firewalls.

If not other network is available, we suggest to connect through a mobile phone access point. 

#### MacOS Mojave
There is an upstream SDL issue on MacOS Mojave (see [bug report](https://github.com/pygame/pygame/issues/555)).
The game doesn't work on the Python version that [Homebrew](https://brew.sh/) installs.

**To play the game on OS Mojave, a workaround is to use the [miniconda](https://conda.io/miniconda.html) version of Python, and [pygame from CogSci](https://anaconda.org/cogsci/pygame).**