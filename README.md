# **Playing Breakthru with MiniMax, Alpha-Beta pruning**

## **Introduction:**

This repository contains an implementation of the Breakthru 
([See the rules of Breakthru on Wikipedia](https://en.wikipedia.org/wiki/Breakthru_(board_game) "Breathru Wikipedia")) 
board game with visualizations done
in Pygame. The repository also contains an implementation of the MiniMax searching algorithm, with Alpha-Beta 
enhancements which is able to play the Breakthru game. Initially, this was an assignment for a university course but a
year later, I rewrote the entire code in Object-Oriented Programming as an exercise to practice my knew knowledge of 
Python. 

## **Learning goals:**

Initially, the learning goals of this project was to be able to apply the MiniMax algorithm, with Alpha-Beta pruning to 
the Breakthru game. I initially did this when I was first starting out in my Master's program and with basic python 
knowledge, which resulted in what we call 'Spaghetti code.' 

A year later, my python skills had improved dramatically, and so I decided to rewrite the whole assignment. The goal 
here was to apply Object-Oriented programming to this assignment and try to make it a bit more efficient. In addition,
I wanted the code to be more understandable. With that being said, I did not implement some of the extra optimization 
techniques such as Hash tables and iterative deepening.

## **Code structure:**

- breakthru.py contains the original code. 
- The remaining files are the rewritten codes.
- main.py is the main file to run the game and to choose players etc.
- game.py contains the Game class which is used to start the game and run player turns.
- board.py contains the Board class which is used to compute possible moves and also evaluate the board.
- minimax_AI.py contains the MiniMax_AI class which is used to find the moves that the AI will play by utilizing the 
MiniMax search algorithm.
- Random_AI.py contains a basic AI which simply plays random moves with a bias towards possible elimination moves.


## **Current Progress and future work:**

- The re-writing of the code went well but this was almost half a year ago since the writing of this README.md.
- Therefore, there is potential to further improve the method.
- Some examples of improvements are:
  - Uses args.parser to reduce the recalling of variables over and over again.
  - Implement hash tables and iterative deepening again.
  - Keep all the info in the board. Don't use silver arrays and gold arrays.
  - Implement Monte-Carlo tree search.
- Although there is room for improvement, further work will probably be done on an entirely new game due to the vast
complexity of the Breakthru board game.

