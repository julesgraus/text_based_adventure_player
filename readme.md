# Text based adventure player
In this repository i am building my first python project.
A text based adventure player. It opens in the terminal, and allows you to play games
that are presented via text dialogs in which the user is offered a little store, and can
type commands to interact with the worlds created with this project.

> Notice:
At this time, its isn't possible yet to play a game, I just created some code with can scaffold a very simple game. 
But you cannot play it yet. When it's possible to create and play games with this tool i will state that in this
readme file.

## Setting up the project
1. Open it in an ide. For example Pycharm.
2. Make sure you have at least python 3.12.5 installed on your machine
3. Run ```pip install -r requirements.txt```
4. Let pycharm setup your venv or run ```python -m venv venv```. I used python version Python 3.12.5.
5. Activate that environment if needed by running ```source ./venv/bin/activate```

## Running the app
In Pycharm you should see Run configurations that run the app in regular and creator mode.
You can use those to run the app. Or you can run in manually like this:

Regular mode:
```./venv/bin/python ./src/main.py```

Creator mode mode:
```./venv/bin/python ./src/main.py```

### Creator mode
In creator mode you do get an extra option which allows you to create a new game.
After creating it, you must manually modify and add files into a zipped folder (tba file)
to create your game. Just have a look inside the created game and start messing around
with it to create your game. If I do get to a point I do see it as good enough I will 
provide more info in that.

## Building a binary
You can build a binary that will have python and the app inside of it, that can run
on each computer. More info on the tool that does this for you, 
can be found [here](https://pyinstaller.org/en/stable/).

1. Run ```./venv/bin/pyinstaller ./src/main.py --noconfirm --onefile --console```
2. It creates a binary in the dist folder that you can run by double clicking it.
