# Chess Game

> how to play ?

Run the game
```cmd
pip install pygame
python3 main.py
```

> if you don't have python3 installed

* Download python3 [here](https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe)


* Add python3 to the PATH
```cmd
set PATH=%PATH%;C:\path\to\python3.exe
start cmd.exe && exit
```

* Install pip and run the game
``` cmd
python3 -m pip install
pip install pygame
python3 main.py
```

> custom game parameters

* show Grid (1 | 0)
* show Deltatime (1 | 0)
* show Fps (1 | 0)
* Window Size 200 <-> 1080 (0 if you don't want to change the size)
* round Value (1 | 0)
* Block Fps 30 <-> 1000 (0 if you don't want to block fps)
* white at the bottom (1 | 0)
* timer (second) 30s <-> 10min  (0 if you don't want a timer)
* only show game stats (1 | 0)
* hide last move (1 | 0)
* hide king chess (1 | 0)
* hide turn (1 | 0)

### Example
```cmd
python3 main.py 1 0 1 700 0 0 1 0 1 0 0
```

> info.log

|  key  |  action    |
|----|------|
|i|create info.log|
|esc|exit|

### Info.log file example
```python
Date 2021-07-24 20:26:38.439073

C:\APPS\run\ChessGame\assets\

Empty  0
King  1
Queen  2
Rook  3
Bishop  4
Knight  5
Pawn  6

3 5 4 1 2 4 5 3 
6 6 6 6 6 6 6 6 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
6 6 6 6 6 6 6 6 
3 5 4 1 2 4 5 3 

whiteAction True
showAsInt False
showGridEffect False
showDeltatime False
showFps False
showMoveTrue
startWhiteTop True
enableTimer -1 s
currentTimerTime 0 ms
currentMove [-1, -1]
lastcurrentMove [-1, -1]

```