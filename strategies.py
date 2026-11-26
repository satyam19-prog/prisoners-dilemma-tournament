import random

def always_cooperate(my_history, opp_history):
    return 'C'


def always_defect(my_history, opp_history):
    return 'D'


def tit_for_tat(my_history, opp_history):
    if len(opp_history) == 0:
        return 'C'
    return opp_history[-1]


def grim_trigger(my_history, opp_history):
    if 'D' in opp_history:
        return 'D'
    return 'C'


def generous_tit_for_tat(my_history, opp_history):
    """
    Like Tit-for-Tat, but forgives an opponent's defection 15% of the time.
    Helps break accidental retaliation loops in noisy environments.
    """
    if len(opp_history) == 0:
        return 'C'
    if opp_history[-1] == 'D':
        if random.random() < 0.15:
            return 'C'
        else:
            return 'D'
    return 'C'


def pavlov(my_history, opp_history):
    """
    Win-Stay, Lose-Shift.
    Repeats its last move if the last round gave a good payoff (CC or DC).
    Switches its move if the last round gave a bad payoff (CD or DD).
    """
    if len(my_history) == 0:
        return 'C'

    last_my = my_history[-1]
    last_opp = opp_history[-1]

    # Good outcomes: (C, C) -> 3 pts, (D, C) -> 5 pts
    if (last_my == 'C' and last_opp == 'C') or (last_my == 'D' and last_opp == 'C'):
        return last_my
    else:
        # Bad outcomes: (C, D) -> 0 pts, (D, D) -> 1 pt -> switch move
        if last_my == 'C':
            return 'D'
        else:
            return 'C'

ALL_STRATEGIES = {
    "Tit-for-Tat": tit_for_tat,
    "Grim Trigger": grim_trigger,
    "Always Defect": always_defect,
    "Always Cooperate": always_cooperate,
    "Generous TFT": generous_tit_for_tat,
    "Pavlov (WSLS)": pavlov,
}