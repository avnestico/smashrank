

def get_position_points(position):
    score_table = {1:  48,
                   2:  40,
                   3:  34,
                   4:  29,
                   5:  25,
                   6:  22,
                   7:  20,
                   8:  19,
                   9:  18,
                   10: 17,
                   11: 16,
                   13: 15,
                   15: 14,
                   18: 13,
                   21: 12,
                   26: 11,
                   31: 10,
                   36:  9,
                   41:  8,
                   46:  7,
                   51:  6,
                   61:  5,
                   71:  4,
                   81:  3,
                   91:  2,
                   101: 1,
                   201: 0}

    try:
        position = int(position)
        return score_table[max(k for k in score_table if k <= position)]
    except ValueError:
        return None


def import_smashgg_tournament(url):
    pass


def set_tournament_score(dict):
    pass


def insert_tournament_to_database(dict):
    # database
    pass


def update_current_scores():
    pass
