import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############




def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # print('DEBUG:call eval, expr is: ', expr)
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:       # special forms
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:                                                                   # call expressions
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        """ map一下expr的所有元素 """
        procedure = scheme_eval(first, env)         # first，可能会有special form的情况
        arguments = rest.map(lambda expr: scheme_eval(expr, env))   # 这段代码很牛逼！！
        return scheme_apply(procedure, arguments, env)
        # END PROBLEM 3


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""

    # print('DEBUG:call apply, procedure is {0}, args is {1}'.format(procedure, args))

    validate_procedure(procedure)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        args_list = []
        while args is not nil:      # args(pair存储) 转化为 args_list(list存储)
            args_list.append(args.first)
            args = args.rest
        if procedure.expect_env:
            args_list.append(env)

        try:
            return procedure.py_func(*args_list)    # procedure对应的python函数，传入对应参数(用*[]
        except TypeError:                           # 如果不写typeError，任何error都会进入这个分支
            raise SchemeError('incorrect number of arguments')
        # END PROBLEM 2
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        """ 创建child_env，args的value 赋给 formals"""
        child_env = procedure.env.make_child_frame(procedure.formals, args)       # 是哪个env里make_child?很重要这句话
        """ 在child_env中逐句执行body，返回最后一句结果 """
        return eval_all(procedure.body, child_env)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        child_env = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, child_env)
        
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    #print('DEBUG:eval all, expr is: ', expressions)

    # BEGIN PROBLEM 6
    while expressions != nil:
        last_value = scheme_eval(expressions.first, env)
        if expressions.rest == nil:                         # 到最后一条了
            return last_value
        expressions = expressions.rest

    return None
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        # END PROBLEM EC
    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
scheme_eval = optimize_tail_calls(scheme_eval)
