import random
from collections import defaultdict

def player(prev_play, opponent_history=[]):
    if prev_play != "":
        opponent_history.append(prev_play)

    # Strategy counters for different opponents
    counter_strategy = {
        "R": "P",
        "P": "S",
        "S": "R"
    }

    # For quincy who repeats: R, R, P, P, S, S
    if len(opponent_history) >= 6:
        last_six = opponent_history[-6:]
        if last_six in [['R', 'R', 'P', 'P', 'S', 'S'], 
                        ['P', 'P', 'S', 'S', 'R', 'R'],
                        ['S', 'S', 'R', 'R', 'P', 'P']]:
            # Predict next move in quincy's sequence
            if last_six[-1] == 'R':
                return 'P'
            elif last_six[-1] == 'P':
                return 'S'
            else:
                return 'R'

    # For mrugesh who plays based on our last move (counter to our most frequent move)
    if len(opponent_history) >= 10:
        # Check if opponent is playing counter to our most frequent move
        # We'll need to track our own moves for this
        if not hasattr(player, 'my_history'):
            player.my_history = []
        
        if len(player.my_history) >= 2:
            last_my_move = player.my_history[-1]
            if opponent_history[-1] == counter_strategy[last_my_move]:
                # Predict they'll counter our last move again
                return counter_strategy[counter_strategy[last_my_move]]
    
    # For kris who always plays counter to our last move
    if len(opponent_history) >= 2:
        if len(player.my_history) >= 1:
            last_my_move = player.my_history[-1]
            if opponent_history[-1] == counter_strategy[last_my_move]:
                # Play the move that would counter their counter
                return last_my_move
    
    # For abbey who uses a Markov chain (looks at last 2 moves)
    if len(opponent_history) >= 3:
        # Build frequency table of next moves based on last two moves
        last_two = "".join(opponent_history[-2:])
        if not hasattr(player, 'markov_chain'):
            player.markov_chain = defaultdict(lambda: defaultdict(int))
        
        if len(opponent_history) >= 3:
            prev_two = "".join(opponent_history[-3:-1])
            player.markov_chain[prev_two][opponent_history[-1]] += 1
        
        potential_next = player.markov_chain[last_two]
        if potential_next:
            predicted_move = max(potential_next.keys(), key=lambda k: potential_next[k])
            return counter_strategy[predicted_move]
    
    # Default strategy (for first moves or when no pattern detected)
    if not opponent_history:
        player.my_history = []
        return random.choice(["R", "P", "S"])
    
    # Fallback: counter the opponent's most frequent move
    freq = {"R": 0, "P": 0, "S": 0}
    for move in opponent_history:
        freq[move] += 1
    most_frequent = max(freq, key=freq.get)
    my_move = counter_strategy[most_frequent]
    
    # Track our move for strategies that need it
    player.my_history.append(my_move)
    
    return my_move
