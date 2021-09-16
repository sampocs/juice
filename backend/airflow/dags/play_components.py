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

DISTANCES = [
    r"[-]?\d+ yard[s]?",
    r"no gain"
]

PLAYER = r"[a-zA-Z, .'-]+[a-zA-Z]" # can't end with a space