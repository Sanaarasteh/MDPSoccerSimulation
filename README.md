### Disclaimer:
To implement MCTS we followed the instruction provided in this site: https://ai-boson.github.io/mcts/

## <span style="color: green">Monte Carlo Tree Search </span>
To run this project run MCTS.py file.

This code implements the Monte Carlo Tree Search (MCTS) algorithm. MCTS is a heuristic search algorithm often used in artificial intelligence for decision making in large state spaces. In particular, it is used in games that have many possible moves and the state space cannot be completely explored in a reasonable amount of time.

The code also includes a State class (in state.py file) and a pyRDDLGym environment (RDDLEnv class) that provide an interface for the MCTS algorithm to interact with the game.
More precisely, the State class converts the RDDL simulation output to a suitable format which can be manipulated by the MCTS class and algorithm.

### <span style="color: green">Usage </span>

The MonteCarloTreeSearchNode class provides the main functionality of the MCTS algorithm and implements a node in the tree. The State class is used to represent the state of the game, and the RDDLEnv class is used to interact with the game environment coded in RDDL. The InstanceInfo class is used to parse information about the game instance.

To use this code, you must provide the path to the domain and instance files in the domain_path and instance_path variables. You can then create an instance of the RDDLEnv class and an initial state using the State class.

After initializing the root node of the MCTS tree with the initial state, you can call the best_action method of the root node to get the best action to take in the current state of the game.

### <span style="color: green">Dependencies </span>

This code uses the following external packages:

    numpy
    tqdm

Additionally, the pyRDDLGym package and the state and utils modules provided in this repository are required to run this code.

## <span style="color: green">Problem Description </span>
In this project, we strive to model a soccer game from the moment a team possesses the ball until they lose the ball (either by scoring a goal, or by losing the ball to the opponent). Here, the players of the opponent team are not modelled, but rather their effects are implicitly present via different ball-lost-probabilities.

The soccer pitch is discretized into a grid for which the coordinates of the boundaries are known.Each player can move in x and y direction inside the grid and if they possess the ball they can also pass the ball to another player or they can shoot the ball. Of course, since the opponent is modelled via action failure probabilities, the outcome of such actions are probabilistic.

The team is not rewarded anything until a player scores a goal. Here, we only care about a goal being scored, and not the specific player who scores it. In other words, we focus on the winning of a team rather than the individual success of a player.

## <span style="color: green">A General Note On the Codes and Results</span>

In the presented code, we have completely modelled the movement of players, passing and shooting actions, and we have incorporated the probabilities of losing the ball while movement, losing the ball while passing, or having an unsuccessful shot, depending on the region of the player.

To define the different regions of the pitch, which play key roles in our modelling, we find the line equations of the boundaries of each region and check whether the player's positions falls into the polygon of the region (interm-fluens *is_in_defense*, *is_in_mid_field*, *is_in_upper_wing*, *is_in_lower_wing*, and *is_in_offense*, implement the functions to check the position of a player). 

## <span style="color: green">State Representation </span>
The state of the soccer game is represented using a set of states and intermidate fluents. State fluents include boolean values such as whether a player has the possession of the ball or whether the team has scored a goal. They also include integer values to store the location of the players. Intermidate fluents are boolean values that represent intermediate states of the game, such as whether a player has passed the ball or whether they are in the opponent's defense area.

### <span style="color: green">Non Fluents: </span>
The non fluents are defined to specify some constants that remain unchanged during the simulation. Here we have defined the following non fluents

* **PASS_INTERCEPT_PROB1**: specifies the probability of a pass being intercepted when originating from the defense area.
* **PASS_INTERCEPT_PROB2**: specifies the probability of a pass being intercepted when originating from the mid-field area.
* **PASS_INTERCEPT_PROB3**: specifies the probability of a pass being intercepted when originating from the upper wing area.
* **PASS_INTERCEPT_PROB4**: specifies the probability of a pass being intercepted when originating from the lower win area.
* **PASS_INTERCEPT_PROB5**: specifies the probability of a pass being intercepted when originating from the offense area.

* **LOSE_POSSESSION_PROB1**: specifies the probability of losing the ball while moving in the defense area
* **LOSE_POSSESSION_PROB2**: specifies the probability of losing the ball while moving in the mid-field area
* **LOSE_POSSESSION_PROB3**: specifies the probability of losing the ball while moving in the upper wing area
* **LOSE_POSSESSION_PROB4**: specifies the probability of losing the ball while moving in the lower wing area
* **LOSE_POSSESSION_PROB5**: specifies the probability of losing the ball while moving in the offense area

* **SHOOT_SUCCESS_PROB1**: specifies the probability of a shoot to be score a goal if originated from the defense area.
* **SHOOT_SUCCESS_PROB2**: specifies the probability of a shoot to be score a goal if originated from the mid-field area.
* **SHOOT_SUCCESS_PROB3**: specifies the probability of a shoot to be score a goal if originated from the upper wing area.
* **SHOOT_SUCCESS_PROB4**: specifies the probability of a shoot to be score a goal if originated from the lower wing area.
* **SHOOT_SUCCESS_PROB5**: specifies the probability of a shoot to be score a goal if originated from the offense area.

* **LEFT_BOUNDARY_X**: specifies the x coordinate of the left boundary of the pitch.
* **RIGHT_BOUNDARY_X**: specifies the x coordinate of the right boundary of the pitch.
* **LOWER_BOUNDARY_Y**: specifies the y coordinate of the upper boundary of the pitch.
* **UPPER_BOUNDARY_Y**: specifies the y coordinate of the lower boundary of the pitch.
* **DEFENSE_AREA_X**: specifies the x coordinate of the defense line.
* **DEFENSE_AREA_Y**: specifies the upper y coordinate of the defense line.
* **OFFENSE_AREA_X**: specifies the x coordinate of the offense line.
* **OFFENSE_AREA_Y**: specifies the upper y coordinate of the offense line.

![Alt text](locations.png)

### <span style="color: green">State Fluents: </span>
Here are the state fluents used in the model and their descriptions.
* **player_pos_x(player)**: the x-coordinate of the player's position on the field as an integer
* **player_pos_y(player)**: the y-coordinate of the player's position on the field as an integer
* **has_ball(player)**: a boolean value indicating whether the player has possession of the ball
* **has_scored**: a boolean value indicating whether a player has scored a goal
* **lost_possession**: a boolean value indicating whether a player has lost possession of the ball

For the has_ball state we have also introduced a constraint (in the state-action-constraints section) such that at each state at most one player has the ball.


### <span style="color: green">Interm Fluents: </span>

* **valid_move_up(player)**: a boolean value indicating whether the player can move up
* **valid_move_down(player)**: a boolean value indicating whether the player can move down
* **valid_move_left(player)**: a boolean value indicating whether the player can move left
* **valid_move_right(player)**: a boolean value indicating whether the player can move right
* **is_in_defense(player)**: a boolean value indicating whether the player is in their own defense area
* **is_in_offense(player)**: a boolean value indicating whether the player is in the opponent's defense area
* **is_in_upper_wing(player)**: a boolean value indicating whether the player is in the upper wing of the field
* **is_in_lower_wing(player)**: a boolean value indicating whether the player is in the lower wing of the field
* **is_in_mid_field(player)**: a boolean value indicating whether the player is in the middle of the field
* **passed_the_ball(player)**: a boolean value indicating whether the player has passed the ball to another player
* **shot_the_ball(player)**: a boolean value indicating whether the player has shot the ball towards the opponent's net
* **scored(player)**: a boolean value indicating whether the player has scored a goal

## <span style="color: green">Action Representation: </span>

The actions that can be performed by the players in the soccer domain are as follows:

* **move_up(player)**: increments the y coordinate of the player
* **move_down(player)**: decrements the y coordinate of the player
* **move_left(player)**: decrements the x coordinate of the player
* **move_right(player)**: increments the x coordinate of the player
* **pass(player1, player2)**: pass the ball from player1 to player2
* **shoot(player)**: shoot the ball towards the opponent's net

## <span style="color: green">Goal Defenition: </span>
The goal of the agent is to maximize its reward, which is a function of the goals scored, possession of the ball, and the time taken to score. The agent needs to learn to pass the ball effectively, move around the field, and shoot accurately to score goals while also defending its own goal

