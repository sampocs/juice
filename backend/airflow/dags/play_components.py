PLAYER = r"[a-zA-Z, .'-]+[a-zA-Z]" # can't end with a space

RUN_DIRECTIONS = [
    r"up the middle", 
    r"left guard", 
    r"right guard", 
    r"left tackle", 
    r"right tackle", 
    r"left end", 
    r"right end"
]

PASS_DIRECTIONS = [
    r"short left",
    r"short middle",
    r"short right",
    r"deep left",
    r"deep middle",
    r"deep right",
]

# Ex: 40 yards
DISTANCES = [
    r"[-]?\d+ yard[s]?",
    r"no gain"
]

# Ex: CHI-10
YARDAGE = r"[A-Z]{2,3}-[\d]{1,2}"

FIELD_GOAL_STATUSES = [
    r"good",
    r"no good"
]

PENALTY = r"[a-zA-Z \d()]+"

NO_PLAY = r"no play"