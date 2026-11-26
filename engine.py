import random

# Standard Axelrod Payoff Matrix: (Player 1 score, Player 2 score)
PAYOFFS = {
    ('C', 'C'): (3, 3),  # Reward for mutual cooperation
    ('C', 'D'): (0, 5),  # Sucker's payoff / Temptation
    ('D', 'C'): (5, 0),  # Temptation / Sucker's payoff
    ('D', 'D'): (1, 1),  # Punishment for mutual defection
}


def apply_noise(move, noise):
    """Flips a move ('C' <-> 'D') with probability equal to noise."""
    if noise > 0.0 and random.random() < noise:
        if move == 'C':
            return 'D'
        else:
            return 'C'
    return move


def play_match(strategy1, strategy2, rounds=200, noise=0.0):
    """
    Runs a single repeated match between two strategies.
    Returns (score1, score2, coop_rate1, coop_rate2).
    """
    history1 = []
    history2 = []
    score1 = 0
    score2 = 0
    coop1 = 0
    coop2 = 0

    for _ in range(rounds):
        intended1 = strategy1(history1, history2)
        intended2 = strategy2(history2, history1)

        move1 = apply_noise(intended1, noise)
        move2 = apply_noise(intended2, noise)

        history1.append(move1)
        history2.append(move2)

        if move1 == 'C':
            coop1 += 1
        if move2 == 'C':
            coop2 += 1

        p1_pts, p2_pts = PAYOFFS[(move1, move2)]
        score1 += p1_pts
        score2 += p2_pts

    coop_rate1 = (coop1 / rounds) * 100.0
    coop_rate2 = (coop2 / rounds) * 100.0

    return score1, score2, coop_rate1, coop_rate2


def run_tournament(strategies, rounds=200, noise=0.0, trials=1):
    """
    Runs a full round-robin tournament where every strategy plays every other
    strategy (including a clone of itself). Averages results across `trials`.
    """
    names = list(strategies.keys())
    total_scores = {name: 0.0 for name in names}
    total_coop = {name: 0.0 for name in names}
    pairwise_matrix = {n1: {n2: 0.0 for n2 in names} for n1 in names}

    for _ in range(trials):
        for i in range(len(names)):
            for j in range(i, len(names)):
                n1 = names[i]
                n2 = names[j]
                s1, s2, c1, c2 = play_match(
                    strategies[n1], strategies[n2], rounds=rounds, noise=noise
                )

                if i == j:
                    # Playing against a clone
                    avg_self_score = (s1 + s2) / 2.0
                    avg_self_coop = (c1 + c2) / 2.0
                    total_scores[n1] += avg_self_score
                    total_coop[n1] += avg_self_coop
                    pairwise_matrix[n1][n1] += avg_self_score
                else:
                    total_scores[n1] += s1
                    total_scores[n2] += s2
                    total_coop[n1] += c1
                    total_coop[n2] += c2
                    pairwise_matrix[n1][n2] += s1
                    pairwise_matrix[n2][n1] += s2

    # Average across trials
    for n1 in names:
        total_scores[n1] = total_scores[n1] / trials
        total_coop[n1] = total_coop[n1] / (trials * len(names))
        for n2 in names:
            pairwise_matrix[n1][n2] = pairwise_matrix[n1][n2] / trials

    return total_scores, total_coop, pairwise_matrix