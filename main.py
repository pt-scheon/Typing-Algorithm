import math
st = input("Enter text to type: ")

home_input = input("Enter home keys for the 8 fingers (e.g., asdfjkl;), or type 'none' for default: ").strip()

default_home_chars = ['a', 's', 'd', 'f', 'j', 'k', 'l', ';']
if not home_input or home_input.lower() == 'none':
    home_chars = default_home_chars
else:
    home_chars = list(home_input[:8])
    while len(home_chars) < 8:
        home_chars.append(default_home_chars[len(home_chars)])

# --- KEYBOARD DICTIONARY ---
keys = {
    "fn": {"key": "fn", "row": 6, "col": 1, "coords": ((0.0, 0.0), (0.0, 16.5), (16.5, 0.0), (16.5, 16.5))},
    "control": {"key": "control", "row": 6, "col": 2, "coords": ((19.0, 0.0), (19.0, 16.5), (35.5, 0.0), (35.5, 16.5))},
    "option_left": {"key": "option_left", "row": 6, "col": 3, "coords": ((38.0, 0.0), (38.0, 16.5), (54.5, 0.0), (54.5, 16.5))},
    "cmd_left": {"key": "cmd_left", "row": 6, "col": 4, "coords": ((57.0, 0.0), (57.0, 16.5), (78.25, 0.0), (78.25, 16.5))},
    " ": {"key": "spacebar", "row": 6, "col": 5, "coords": ((80.75, 0.0), (80.75, 16.5), (173.25, 0.0), (173.25, 16.5))},
    "cmd_right": {"key": "cmd_right", "row": 6, "col": 6, "coords": ((175.75, 0.0), (175.75, 16.5), (197.0, 0.0), (197.0, 16.5))},
    "option_right": {"key": "option_right", "row": 6, "col": 7, "coords": ((199.5, 0.0), (199.5, 16.5), (216.0, 0.0), (216.0, 16.5))},
    "arrow_left": {"key": "arrow_left", "row": 6, "col": 8, "coords": ((218.5, 0.0), (218.5, 16.5), (235.0, 0.0), (235.0, 16.5))},
    "arrow_down": {"key": "arrow_down", "row": 6, "col": 9, "coords": ((237.5, 0.0), (237.5, 7.0), (254.0, 0.0), (254.0, 7.0))},
    "arrow_up": {"key": "arrow_up", "row": 6, "col": 9, "coords": ((237.5, 9.5), (237.5, 16.5), (254.0, 9.5), (254.0, 16.5))},
    "arrow_right": {"key": "arrow_right", "row": 6, "col": 10, "coords": ((256.5, 0.0), (256.5, 16.5), (273.0, 0.0), (273.0, 16.5))},
    "shift_left": {"key": "shift_left", "row": 5, "col": 1, "coords": ((0.0, 19.0), (0.0, 35.5), (40.25, 19.0), (40.25, 35.5))},
    "z": {"key": "z", "row": 5, "col": 2, "coords": ((42.75, 19.0), (42.75, 35.5), (59.25, 19.0), (59.25, 35.5))},
    "x": {"key": "x", "row": 5, "col": 3, "coords": ((61.75, 19.0), (61.75, 35.5), (78.25, 19.0), (78.25, 35.5))},
    "c": {"key": "c", "row": 5, "col": 4, "coords": ((80.75, 19.0), (80.75, 35.5), (97.25, 19.0), (97.25, 35.5))},
    "v": {"key": "v", "row": 5, "col": 5, "coords": ((99.75, 19.0), (99.75, 35.5), (116.25, 19.0), (116.25, 35.5))},
    "b": {"key": "b", "row": 5, "col": 6, "coords": ((118.75, 19.0), (118.75, 35.5), (135.25, 19.0), (135.25, 35.5))},
    "n": {"key": "n", "row": 5, "col": 7, "coords": ((137.75, 19.0), (137.75, 35.5), (154.25, 19.0), (154.25, 35.5))},
    "m": {"key": "m", "row": 5, "col": 8, "coords": ((156.75, 19.0), (156.75, 35.5), (173.25, 19.0), (173.25, 35.5))},
    ",": {"key": ",", "row": 5, "col": 9, "coords": ((175.75, 19.0), (175.75, 35.5), (192.25, 19.0), (192.25, 35.5))},
    ".": {"key": ".", "row": 5, "col": 10, "coords": ((194.75, 19.0), (194.75, 35.5), (211.25, 19.0), (211.25, 35.5))},
    "/": {"key": "/", "row": 5, "col": 11, "coords": ((213.75, 19.0), (213.75, 35.5), (230.25, 19.0), (230.25, 35.5))},
    "shift_right": {"key": "shift_right", "row": 5, "col": 12, "coords": ((232.75, 19.0), (232.75, 35.5), (282.5, 19.0), (282.5, 35.5))},
    "caps_lock": {"key": "caps_lock", "row": 4, "col": 1, "coords": ((0.0, 38.0), (0.0, 54.5), (30.75, 38.0), (30.75, 54.5))},
    "a": {"key": "a", "row": 4, "col": 2, "coords": ((33.25, 38.0), (33.25, 54.5), (49.75, 38.0), (49.75, 54.5))},
    "s": {"key": "s", "row": 4, "col": 3, "coords": ((52.25, 38.0), (52.25, 54.5), (68.75, 38.0), (68.75, 54.5))},
    "d": {"key": "d", "row": 4, "col": 4, "coords": ((71.25, 38.0), (71.25, 54.5), (87.75, 38.0), (87.75, 54.5))},
    "f": {"key": "f", "row": 4, "col": 5, "coords": ((90.25, 38.0), (90.25, 54.5), (106.75, 38.0), (106.75, 54.5))},
    "g": {"key": "g", "row": 4, "col": 6, "coords": ((109.25, 38.0), (109.25, 54.5), (125.75, 38.0), (125.75, 54.5))},
    "h": {"key": "h", "row": 4, "col": 7, "coords": ((128.25, 38.0), (128.25, 54.5), (144.75, 38.0), (144.75, 54.5))},
    "j": {"key": "j", "row": 4, "col": 8, "coords": ((147.25, 38.0), (147.25, 54.5), (163.75, 38.0), (163.75, 54.5))},
    "k": {"key": "k", "row": 4, "col": 9, "coords": ((166.25, 38.0), (166.25, 54.5), (182.75, 38.0), (182.75, 54.5))},
    "l": {"key": "l", "row": 4, "col": 10, "coords": ((185.25, 38.0), (185.25, 54.5), (201.75, 38.0), (201.75, 54.5))},
    ";": {"key": ";", "row": 4, "col": 11, "coords": ((204.25, 38.0), (204.25, 54.5), (220.75, 38.0), (220.75, 54.5))},
    "'": {"key": "'", "row": 4, "col": 12, "coords": ((223.25, 38.0), (223.25, 54.5), (239.75, 38.0), (239.75, 54.5))},
    "return": {"key": "return", "row": 4, "col": 13, "coords": ((242.25, 38.0), (242.25, 54.5), (282.5, 38.0), (282.5, 54.5))},
    "tab": {"key": "tab", "row": 3, "col": 1, "coords": ((0.0, 57.0), (0.0, 73.5), (26.0, 57.0), (26.0, 73.5))},
    "q": {"key": "q", "row": 3, "col": 2, "coords": ((28.5, 57.0), (28.5, 73.5), (45.0, 57.0), (45.0, 73.5))},
    "w": {"key": "w", "row": 3, "col": 3, "coords": ((47.5, 57.0), (47.5, 73.5), (64.0, 57.0), (64.0, 73.5))},
    "e": {"key": "e", "row": 3, "col": 4, "coords": ((66.5, 57.0), (66.5, 73.5), (83.0, 57.0), (83.0, 73.5))},
    "r": {"key": "r", "row": 3, "col": 5, "coords": ((85.5, 57.0), (85.5, 73.5), (102.0, 57.0), (102.0, 73.5))},
    "t": {"key": "t", "row": 3, "col": 6, "coords": ((104.5, 57.0), (104.5, 73.5), (121.0, 57.0), (121.0, 73.5))},
    "y": {"key": "y", "row": 3, "col": 7, "coords": ((123.5, 57.0), (123.5, 73.5), (140.0, 57.0), (140.0, 73.5))},
    "u": {"key": "u", "row": 3, "col": 8, "coords": ((142.5, 57.0), (142.5, 73.5), (159.0, 57.0), (159.0, 73.5))},
    "i": {"key": "i", "row": 3, "col": 9, "coords": ((161.5, 57.0), (161.5, 73.5), (178.0, 57.0), (178.0, 73.5))},
    "o": {"key": "o", "row": 3, "col": 10, "coords": ((180.5, 57.0), (180.5, 73.5), (197.0, 57.0), (197.0, 73.5))},
    "p": {"key": "p", "row": 3, "col": 11, "coords": ((199.5, 57.0), (199.5, 73.5), (216.0, 57.0), (216.0, 73.5))},
    "[": {"key": "[", "row": 3, "col": 12, "coords": ((218.5, 57.0), (218.5, 73.5), (235.0, 57.0), (235.0, 73.5))},
    "]": {"key": "]", "row": 3, "col": 13, "coords": ((237.5, 57.0), (237.5, 73.5), (254.0, 57.0), (254.0, 73.5))},
    "\\": {"key": "\\", "row": 3, "col": 14, "coords": ((256.5, 57.0), (256.5, 73.5), (282.5, 57.0), (282.5, 73.5))},
    "`": {"key": "`", "row": 2, "col": 1, "coords": ((0.0, 76.0), (0.0, 92.5), (16.5, 76.0), (16.5, 92.5))},
    "1": {"key": "1", "row": 2, "col": 2, "coords": ((19.0, 76.0), (19.0, 92.5), (35.5, 76.0), (35.5, 92.5))},
    "2": {"key": "2", "row": 2, "col": 3, "coords": ((38.0, 76.0), (38.0, 92.5), (54.5, 76.0), (54.5, 92.5))},
    "3": {"key": "3", "row": 2, "col": 4, "coords": ((57.0, 76.0), (57.0, 92.5), (73.5, 76.0), (73.5, 92.5))},
    "4": {"key": "4", "row": 2, "col": 5, "coords": ((76.0, 76.0), (76.0, 92.5), (92.5, 76.0), (92.5, 92.5))},
    "5": {"key": "5", "row": 2, "col": 6, "coords": ((95.0, 76.0), (95.0, 92.5), (111.5, 76.0), (111.5, 92.5))},
    "6": {"key": "6", "row": 2, "col": 7, "coords": ((114.0, 76.0), (114.0, 92.5), (130.5, 76.0), (130.5, 92.5))},
    "7": {"key": "7", "row": 2, "col": 8, "coords": ((133.0, 76.0), (133.0, 92.5), (149.5, 76.0), (149.5, 92.5))},
    "8": {"key": "8", "row": 2, "col": 9, "coords": ((152.0, 76.0), (152.0, 92.5), (168.5, 76.0), (168.5, 92.5))},
    "9": {"key": "9", "row": 2, "col": 10, "coords": ((171.0, 76.0), (171.0, 92.5), (187.5, 76.0), (187.5, 92.5))},
    "0": {"key": "0", "row": 2, "col": 11, "coords": ((190.0, 76.0), (190.0, 92.5), (206.5, 76.0), (206.5, 92.5))},
    "-": {"key": "-", "row": 2, "col": 12, "coords": ((209.0, 76.0), (209.0, 92.5), (225.5, 76.0), (225.5, 92.5))},
    "=": {"key": "=", "row": 2, "col": 13, "coords": ((228.0, 76.0), (228.0, 92.5), (244.5, 76.0), (244.5, 92.5))},
    "delete": {"key": "delete", "row": 2, "col": 14, "coords": ((247.0, 76.0), (247.0, 92.5), (282.5, 76.0), (282.5, 92.5))}
}

# --- HELPERS & CONSTRAINTS ---

def get_center(char):
    if char not in keys: return (0, 0)
    c = keys[char]["coords"]
    return ((c[0][0] + c[2][0]) / 2, (c[0][1] + c[1][1]) / 2)

FINGERS_NAMES = ["Left Pinky", "Left Ring", "Left Middle", "Left Index", 
                 "Right Index", "Right Middle", "Right Ring", "Right Pinky"]

def is_valid(state_tuple):
    """
    All anatomical constraints removed. 
    Fingers can cross, stretch infinitely, and teleport across the keyboard.
    """
    return True

def calculate_move_cost(finger_curr_key, target_key):
    """
    Calculates movement cost using the tilted rotation matrix without gravity pull.
    """
    if finger_curr_key == target_key:
        return 0.0

    t_center = get_center(target_key)
    f_center = get_center(finger_curr_key)
    
    dx = t_center[0] - f_center[0]
    dy = t_center[1] - f_center[1]

    # Rotational mapping (Ergonomic Grid Tilt)
    tilt_angle = 0.08
    nx = -math.sin(tilt_angle)
    ny = math.cos(tilt_angle)

    parallel = abs(dx * ny - dy * nx)
    orthogonal = abs(dx * nx + dy * ny)

    move_dist = parallel + (1.2 * orthogonal)
    
    return move_dist

# --- VITERBI DYNAMIC PROGRAMMING ENGINE ---

def calculate_optimal_path(target_string, home_setup):
    valid_str = "".join([c.lower() for c in target_string if c.lower() in keys])
    if not valid_str:
        return "No valid keys to type."

    safe_home = [k if k in keys else default_home_chars[i] for i, k in enumerate(home_setup)]
    initial_state = tuple(safe_home)

    layer = {initial_state: (0.0, None, None)}
    history = [layer]
    
    BEAM_WIDTH = 3000  

    for char in valid_str:
        next_layer = {}
        
        for state, (cost, _, _) in layer.items():
            for f_idx in range(8):
                temp_state = list(state)
                temp_state[f_idx] = char
                new_state = tuple(temp_state)
                
                transition_cost = calculate_move_cost(state[f_idx], char)
                new_cost = cost + transition_cost
                
                if new_state not in next_layer or new_cost < next_layer[new_state][0]:
                    next_layer[new_state] = (new_cost, state, f_idx)
        
        if not next_layer:
            return f"Pathfinding failed at '{char}'."
            
        if len(next_layer) > BEAM_WIDTH:
            sorted_states = sorted(next_layer.items(), key=lambda item: item[1][0])
            next_layer = dict(sorted_states[:BEAM_WIDTH])
            
        layer = next_layer
        history.append(layer)

    # --- TRACEBACK ---
    best_final_state = min(layer, key=lambda s: layer[s][0])
    
    path = []
    curr_state = best_final_state

    for t in range(len(valid_str), 0, -1):
        _, prev_state, finger_used = history[t][curr_state]
        
        char_typed = valid_str[t-1]
        finger_name = FINGERS_NAMES[finger_used]
        
        display_char = "Spacebar" if char_typed == " " else char_typed
        path.append((display_char, finger_name))
        
        curr_state = prev_state

    path.reverse()
    return path

# --- EXECUTION ---
result = calculate_optimal_path(st, home_chars)

print("\n--- VITERBI OPTIMAL PATH ---")
if isinstance(result, str):
    print(result)
else:
    for step_num, (ch, f_name) in enumerate(result, 1):
        print(f"Step {step_num}: '{ch}' pressed by {f_name}")
