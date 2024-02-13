# AI Flappy Bird Game
This is a recreation of the popular flappy bird game but with AI functionality included. This adds an AI to the bird that teaches itself how to play the game with every iteration of the game repeating. In every iteration, the game creates a population of birds with each having a unique score starting at 0. With every bird that passes a pipe, the score increases. Once all the birds lose, the game combines the birds with the highest scores together and repeats the process in the next iteration(Next game). This slowly causes the birds to get better as the game progresses.

INSTRUCTIONS:

1. Go over to my GitHub repository which contains all of the project files and cone the repository ('https://github.com/sharktankful/FlappyBird_AI')
 
 
2. in your terminal, install pipenv using the following command: ```pip install pipenv``` for windows or ```pip3 install pipenv``` for mac
 
3. CD to the root folder of the repository and navigate to the main.py file

4. Run the following command which will not only create the virtual enviorment but also install the dependencies from the pipfiles: ```pipenv shell```

5. Navigate to the main.py file and run the code to start the game!

6. If your want to exit the virtual enviornment made by pipenv, just run the command ```exit``` to exit. To start the enviornment again, run the command ```pipenv shell```
