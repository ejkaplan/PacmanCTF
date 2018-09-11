# PacmanCTF
PacmanCTF for APCS-P 2017-18

AI Contest for APCS-P 2018, reimplementation of http://ai.berkeley.edu/contest.html, with different maze generation and slightly modified rules. Students write a bot which inherits from ctf_director, which determines which direction each bot will move when their turn comes around.

## The game
The red player is trying to steal dots from the blue player's territory and vice versa. If a bot stands on a dot in enemy territory, they eat the dot. They do not score points until they successfully return to friendly territory, at which point they score (n * (n+1))/2 points, where n is the number of dots eaten. If an enemy agent touches your bot while it is in enemy territory, your bot is caught and sent back to its spawn point back in your territory. The dots they had eaten are returned to their original position, and no points are scored.

## The maze generation algorithm
Maze generation is based on [this algorithm](https://www.contralogic.com/2d-pac-man-style-maze-generation/ "2D Pac-Man style maze generation"), with checks to ensure that the mazes are sufficiently large. The algorithm is also modified to make the mazes rotationally symmetrical. After the maze is generated, it is divided into red and blue territory by starting two flood fills from symmetrical points on the maze and running them simultaneously until all spaces are divided up.

![](https://github.com/ejkaplan/PacmanCTF/blob/master/pac_ctf.gif)
