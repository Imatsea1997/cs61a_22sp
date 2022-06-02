"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    sum_of_the_outcomes = 0 #存储总点数
    is_sow_sad = False  #是否存在某次点数为1，即sow sad
    while num_rolls > 0:
        #投骰子
        temp_points = dice()
        num_rolls -= 1
        #记录，求和
        #当前点数为1，标记
        if temp_points == 1:
            is_sow_sad = True
        #不为1，累加到总点数
        else:
            sum_of_the_outcomes += temp_points
    return 1 if is_sow_sad else sum_of_the_outcomes
    # END PROBLEM 1


def digit_fn(digit):
    """Return the corresponding function for the given DIGIT.

    value:  The value which this function starts at.
    """
    # Error if DIGIT is not one of: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    assert isinstance(digit, int) and 0 <= digit < 10
    # List of pre-defined functions
    f0 = lambda value: value + 1
    f1 = lambda value: value ** 2
    f2 = lambda value: value * 3
    f3 = lambda value: value // 4
    f4 = lambda value: value - 5
    f5 = lambda value: value % 6
    f6 = lambda value: int((value % 7) * 8)
    f7 = lambda value: int(value * 8.8)
    f8 = lambda value: int(value / 99 * 15) + 10
    f9 = lambda value: value
    # Mapping from digit to function
    if digit == 0:
        return f0
    elif digit == 1:
        return f1
    elif digit == 2:
        return f2
    elif digit == 3:
        return f3
    elif digit == 4:
        return f4
    elif digit == 5:
        return f5
    elif digit == 6:
        return f6
    elif digit == 7:
        return f7
    elif digit == 8:
        return f8
    elif digit == 9:
        return f9


def hefty_hogs(player_score, opponent_score):
    """Return the points scored by player due to Hefty Hogs.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.
    """
    # BEGIN PROBLEM 2
    #hefty_dogs-1: opponent_score为0
    if opponent_score == 0:
        return 1
    # hefty_dogs-2: opponent_score不为0
    result = player_score
    while opponent_score != 0:
        #找到当前位数字 eg:32的话为2
        temp_digit = opponent_score % 10
        #找到当前function eg:f2
        temp_function = digit_fn(temp_digit)
        #计算当前结果
        result = temp_function(result)
        #迭代下一轮
        opponent_score //= 10
    return result % 30
    # END PROBLEM 2


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a turn rolling NUM_ROLLS dice,
    which may be 0 in the case of a player using Hefty Hogs.
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    player_score:    The total score of the current player.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    goal:            The goal score of the game.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert max(player_score, opponent_score) < goal, 'The game should be over.'
    # BEGIN PROBLEM 3
    #check if hefty_hogs
    if num_rolls == 0:
        return hefty_hogs(player_score, opponent_score)
    return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def hog_pile(player_score, opponent_score):
    """Return the points scored by player due to Hog Pile.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.
    """
    # BEGIN PROBLEM 4
    #check if hog_pile
    player_ones_digit = player_score % 10
    opponent_ones_digit = opponent_score % 10
    if player_ones_digit != opponent_ones_digit:
        return 0
    else:
        return player_ones_digit
    # END PROBLEM 4


def next_player(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> next_player(0)
    1
    >>> next_player(1)
    0
    """
    return 1 - who


def silence(score0, score1, leader=None):
    """Announce nothing (see Phase 2)."""
    return leader, None


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call every turn.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    leader = None  # To be used in problem 7
    # BEGIN PROBLEM 5
    while score0 < goal and score1 < goal:
        # 当前是player0的回合
        if who == 0:
            score0 = one_turn_play(strategy0, score0, score1, dice, goal)
        # 当前是player1的回合
        else:
            score1 = one_turn_play(strategy1, score1, score0, dice, goal)
        who = next_player(who)

    # END PROBLEM 5
    # (note that the indentation for the problem 7 prompt (***YOUR CODE HERE***) might be misleading)
    # BEGIN PROBLEM 7
        # say
        leader, message = say(score0, score1, leader)
        if message is not None and message != "":
            print(message)
    # END PROBLEM 7
    return score0, score1

def one_turn_play(strategy, player=0, opponent=0, dice=six_sided, goal=GOAL_SCORE):
    """模拟一轮的投骰子过程，返回当前玩家本轮结束后得分
    """
    # 当前turn的基本得分
    player += take_turn(strategy(player, opponent), player, opponent, dice, goal)
    # 检查是否有hog pile额外加分
    player += hog_pile(player, opponent)
    return player

#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1, player=None):
    """A commentary function that announces the score for each player."""
    message = f"Player 0 now has {score0} and now Player 1 has {score1}"
    return player, message


def announce_lead_changes(score0, score1, last_leader=None):
    """A commentary function that announces when the leader has changed.

    >>> leader, message = announce_lead_changes(5, 0)
    >>> print(message)
    Player 0 takes the lead by 5
    >>> leader, message = announce_lead_changes(5, 12, leader)
    >>> print(message)
    Player 1 takes the lead by 7
    >>> leader, message = announce_lead_changes(8, 12, leader)
    >>> print(leader, message)
    1 None
    >>> leader, message = announce_lead_changes(8, 13, leader)
    >>> leader, message = announce_lead_changes(15, 13, leader)
    >>> print(message)
    Player 0 takes the lead by 2
    """
    # BEGIN PROBLEM 6
    # 分数相同，不存在change。leader和分差都不存在
    if score0 == score1:
        return None, None
    # 记录当前lead
    current_leader = 0 if score0 > score1 else 1
    # 不存在leader change
    if current_leader == last_leader:
        return current_leader, None
    # 存在leader change
    else:
        return current_leader, f"Player {current_leader} takes the lead by {abs(score0 - score1)}"
    # END PROBLEM 6

def both(f, g):
    """A commentary function that says what f says, then what g says.

    >>> say_both = both(say_scores, announce_lead_changes)
    >>> player, message = say_both(10, 0)
    >>> print(message)
    Player 0 now has 10 and now Player 1 has 0
    Player 0 takes the lead by 10
    >>> player, message = say_both(10, 8, player)
    >>> print(message)
    Player 0 now has 10 and now Player 1 has 8
    >>> player, message = say_both(10, 17, player)
    >>> print(message)
    Player 0 now has 10 and now Player 1 has 17
    Player 1 takes the lead by 7
    """
    def say(score0, score1, player=None):
        f_player, f_message = f(score0, score1, player)
        g_player, g_message = g(score0, score1, player)
        if f_message and g_message:
            return g_player, f_message + "\n" + g_message
        else:
            return g_player, f_message or g_message
    return say


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(original_function, total_samples=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TOTAL_SAMPLES times.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 1000)
    >>> averaged_dice(1, dice)
    3.0
    """
    # BEGIN PROBLEM 8
    # 执行orginal_function多次，并计算平均值的函数
    def average_f(*args):
        sum = 0
        k = 0
        while k < total_samples:
            sum += original_function(*args)
            k += 1
        return sum / total_samples
    return average_f
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, total_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of TOTAL_SAMPLES times.
    Assume that the dice always return pos itive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    max_average = 0  #记录最大平均值
    num_of_rolls = 0 #最大平均值对应的骰子数
    test_num = 1 # 逐步测试骰子数为多少合适
    averaged_dice = make_averaged(roll_dice, total_samples)
    while test_num <= 10:
        # 测试骰子数为test_num时的平均点数
        temp_average = averaged_dice(test_num, dice)
        if temp_average > max_average:
            num_of_rolls = test_num
            max_average = temp_average
        test_num += 1
    return num_of_rolls
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)
    print('always_roll(6) win rate:', average_win_rate(always_roll(6)))

    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))
    print('hefty_hogs_strategy win rate:', average_win_rate(hefty_hogs_strategy))
    print('hog_pile_strategy win rate:', average_win_rate(hog_pile_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


def hefty_hogs_strategy(score, opponent_score, threshold=8, num_rolls=6):
    """This strategy returns 0 dice if that gives at least THRESHOLD points, and
    returns NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    temp_score = hefty_hogs(score, opponent_score)
    return 0 if temp_score >= threshold else num_rolls
    # END PROBLEM 10


def hog_pile_strategy(score, opponent_score, threshold=8, num_rolls=6):
    """This strategy returns 0 dice when this would result in Hog Pile taking
    effect. It also returns 0 dice if it gives at least THRESHOLD points.
    Otherwise, it returns NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    # 检查hefty_hogs得分是否超过threshold
    if hefty_hogs_strategy(score, opponent_score, threshold, num_rolls) == 0:
        return 0
    # 检查是否产生hog pile 并且hog pile收益大于0
    temp_score = score + hefty_hogs(score, opponent_score)
    if (temp_score % 10) == (opponent_score % 10) and temp_score % 10 != 0:
        return 0
    return num_rolls
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """继承hog_pile的判断条件返回0；其余情况调用max_scoring_num_rolls判断返回多少
    """
    # BEGIN PROBLEM 12
    # 基础策略，threshold定多少合适？
    temp_num_rolls = hog_pile_strategy(score, opponent_score)
    if temp_num_rolls == 0:
        return temp_num_rolls
    return max_scoring_num_rolls()
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
