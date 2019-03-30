## Python Aliens

Everyone has to start somewhere when learning Python. I started here, using the book
["Python Crash Course"](https://www.amazon.com/Python-Crash-Course-Hands-Project-Based/dp/1593276036).

This repository contains a basic "Alien Invasion" game created using [pygame](https://www.pygame.org/news).
In this game, the player controls a ship at the bottom of the screen. The ship can be moved left and
right (arrow keys) and can fire bullets (space bar). The alien fleet gets faster every level. If
any alien ship hits the player's ship, it is destroyed. **Can you save the human race???**

## Installation

A Python project, Aliens depends on Python 3. It also uses pygame. We use Python 3.7.0 and pygame 1.9.4.
Other versions may or may not be compatible.

On Linux you should use `pip3` and your package manager to install dependencies. On OS X, you should
use `pip3` and `homebrew`. You should never use Windows. Ever.... Seriously.

### Linux Install:

```
$ sudo apt-get install python3-dev mercurial python-pygame libsdl-image1.2-dev libsdl2-dev libsdl-ttf2.0-dev
$ sudo python get-pip.py
```

### OSX Install:

```
sudo python get-pip.py
brew install hg sdl sdl_image sdl_ttf
$ python3 -m pip install -U pygame --user
```
