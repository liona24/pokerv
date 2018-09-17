from deuces import Card


def serialize_card(card):
    suit_int = Card.get_suit_int(card)
    rank_int = Card.get_rank_int(card)

    s = Card.INT_SUIT_TO_CHAR_SUIT[suit_int]
    r = Card.STR_RANKS[rank_int]

    return s + r


def serialize_cards(cards):
    return list(map(serialize_card, cards))


def serialize_players(players, player_at_action):
    return [ {
        'name': p.name,
        'stack': p.stack,
        'bet': p.bet,
        'hand': serialize_cards(p.hand),
        'action_required': p == player_at_action,
        'has_folded': p.has_folded,
        'hand_score': p.hand_score,
        'is_allin': p.is_allin
    } for p in players ]


def serialize_summary(summary):
    return {
        'hands_played': summary.hands_played,
        'board': serialize_cards(summary.board),
        'winners': [ { 'name': w.name,
                       'hand': serialize_cards(w.hand),
                       'hand_score': w.hand_score,
                       'pot': pot } for w, pot in summary.winners ],
    }
