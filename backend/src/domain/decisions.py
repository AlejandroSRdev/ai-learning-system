def decide_next_step(score: float) -> str:
    if score < 0.5:
        return "simplify"
    elif score < 0.75:
        return "reinforce"
    else:
        return "advance"
