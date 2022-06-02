"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    # 遍历paragraphs，开始找符合要求的p
    satisfy_index = -1  # 当前符合要求的paragrph的序号
    for paragraph in paragraphs:
        # 符合要求，进行计数
        if select(paragraph):
            satisfy_index += 1
        # 找到了
        if satisfy_index == k:
            return paragraph
    # 遍历完依旧没找到
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'

    # BEGIN PROBLEM 2
    def select(paragraph):
        """returns whether a paragraph contains one of the words in TOPIC."""
        # 把paragraph转化成一个list，处理好upper case & punctuation
        to_be_tested_paragraph = paragraph_to_list(paragraph)
        # 比对topic和to_be_tested_paragraph两个list
        for word in topic:
            if word in to_be_tested_paragraph:
                return True
        return False

    def paragraph_to_list(paragraph):
        """returns a list of lower words in paragraph without punctuation"""
        # 去除标点
        paragraph = ''.join([c for c in paragraph if c.isalnum() or c.isspace()])
        # 变成小写
        paragraph = paragraph.lower()
        # 分割成单词
        return paragraph.split()

    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    # 特殊情况，typed为空，不需要计算了
    if len(typed_words) == 0:
        return 0.0

    matched_words_count = 0
    iteration_count = min(len(typed_words), len(reference_words))  # 需比对的单词数
    for index in range(iteration_count):
        # 单词完全相同
        if typed_words[index] == reference_words[index]:
            matched_words_count += 1

    accuracy_rate = matched_words_count / len(typed_words) * 100
    return accuracy_rate
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    length_of_characters = len(typed)
    average_typed_word = length_of_characters / 5
    words_per_minute = average_typed_word * 60 / elapsed
    return words_per_minute
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    # 遍历valid_words，和user_word进行比对
    minimum_difference = len(user_word)
    minimum_diff_word = user_word
    for valid_word in valid_words:
        # 完全一样，直接返回
        if user_word == valid_word:
            return user_word
        # 有不同，不断找最小差别的那个
        temp_difference = diff_function(user_word, valid_word, limit)
        if minimum_difference > temp_difference:
            minimum_difference = temp_difference
            minimum_diff_word = valid_word

    # 检查最小差别是否超过能容忍极限
    if minimum_difference > limit:
        return user_word
    else:
        return minimum_diff_word
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    if limit < 0:  # 已超过limit，没有统计后续diff的必要了
        return 0
    elif not start:  # 任意一个list为[]，返回剩余list长度为diff
        return len(goal)
    elif not goal:
        return len(start)
    else:  # 逐个比较char的diff，记录
        if start[0] != goal[0]:
            return 1 + shifty_shifts(start[1:], goal[1:], limit - 1)
        else:
            return shifty_shifts(start[1:], goal[1:], limit)


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    if limit < 0:        # 已超过limit，没有统计后续diff的必要了
        return 0
    elif not start:               # 任意一个list为[]，返回剩余list长度为diff
        return len(goal)
    elif not goal:
        return len(start)
    else:
        if start[0] != goal[0]:
            add_diff = 1 + pawssible_patches(start, goal[1:], limit - 1)
            remove_diff = 1 + pawssible_patches(start[1:], goal, limit - 1)
            substitute_diff = 1 + pawssible_patches(start[1:], goal[1:], limit - 1)
            return min(add_diff, remove_diff, substitute_diff)
        else:
            return pawssible_patches(start[1:], goal[1:], limit)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    # calculate progress
    progress = calculate_progress(typed, prompt)
    # send progress to the server
    progress_msg = {'id': user_id, 'progress': progress}
    send(progress_msg)
    return progress
    # END PROBLEM 8


def calculate_progress(typed, prompt):
    """return a ratio of the words in the prompt that you have typed correctly,
     up to the first incorrect word, divided by the number of prompt words."""
    correct_count = 0
    total = len(prompt)

    # 计算正确配对单词数量
    for word in typed:
        if word != prompt[correct_count]:
            break
        correct_count += 1

    return correct_count / total


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    times = []
    for player_timestamp in times_per_player:
        one_player_time = []
        for i in range(1, len(player_timestamp)):
            # 第i-1时刻到第i时刻用的时间，即第i-1个word所花费时间
            ith_time_cost = player_timestamp[i] - player_timestamp[i - 1]
            one_player_time.append(ith_time_cost)
        # one_player_time是否需要清空？
        times.append(one_player_time)
    return game(words, times)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))  # contains an *index* for each word
    # BEGIN PROBLEM 10
    # 创建list，准备记录fastest word到对应player位置
    players_fastest_words = create_list(player_indices)

    # 从第1个word开始逐次比较时间
    for word_index in word_indices:
        # 当前word花费时间最少的player
        player_index = find_fastest_player(game, word_index, player_indices)
        # 记录word到对应player处
        word = word_at(game, word_index)  # 当前word
        players_fastest_words[player_index].append(word)
    return players_fastest_words
    # END PROBLEM 10


def create_list(player_indices):
    """ Return a list of lists waiting to store which words each player typed fastest"""
    players_fastest_words = [None] * len(player_indices)
    for player_index in player_indices:
        players_fastest_words[player_index] = []
    return players_fastest_words


def find_fastest_player(game, word_index, player_indices):
    """Return which player typed this word(word_index) fastest."""
    # 取第一个玩家时间为初始值
    minimum_time = time(game, 0, word_index)
    fastest_player_index = 0

    for temp_player_index in player_indices:
        temp_time = time(game, temp_player_index, word_index)
        if temp_time < minimum_time:
            minimum_time = temp_time
            fastest_player_index = temp_player_index
    return fastest_player_index


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])


enable_multiplayer = False  # Change to True when you're ready to race.


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
