The folder "Original_Chess" has the base code for the user to be able to play with another user or to play with the basic chess engine.

The chess engine or AIEngine is based on the minimax alpha-beta pruning algorithm to make decisions and make moves.


The main.py is the main module to be run.

The modules "alpha_zero_chess_model", "chess_ai_training", "IDK" and "Main_Training_Loop" are coded on a trial basis for the neural architecture and are not to be included right now....

I am currently facing a lot of minor issues in making AIEngine_1 play against AIEngine_2 and also the engine stops playing after attaining check and not checkmate

Edit:
The folder "Self-Play" has the base code for the AIEngine_1 to be able to play with AIEngine_2. Except for the minor issue that it asks the user to help it come out of the "Check" state and then the players switch places.......

Edit 2:
1. Fixed the swapping places issue
2. Now able to represent the board in arrays and amtrices
3. Added a randomized function for opening

Edit 3:
1. Gonna Pick up the board GUI from the below link: "https://github.com/AlejoG10/python-chess-ai-yt/blob/master/src/dragger.py"
2. Will Update the Repositary after playing Valorant and F1

Edit 4:
1. Built a separate GUI folder on pygame for chess
2. Will integrate AIEngine in the GUI folder after some time
3. 'Original Chess' and 'Self Play' are for IDLE or on the output terminal whereas 'GUI' creates a separate popup

Edit 5:
1. Stockfish Linux Version for evaluation (Collab) or windows for local

Edit 6:
1. Basic RL model structure built
2. Future work will be refining the parameters and cleaning the code for better functionality
