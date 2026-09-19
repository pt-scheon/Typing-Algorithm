import math
import tkinter as tk
from tkinter import simpledialog, messagebox
from collections import deque

u = 19.0
keys = {
    "`": {"x": 0.5 * u, "y": 38.0}, "1": {"x": 1.5 * u, "y": 38.0}, "2": {"x": 2.5 * u, "y": 38.0},
    "3": {"x": 3.5 * u, "y": 38.0}, "4": {"x": 4.5 * u, "y": 38.0}, "5": {"x": 5.5 * u, "y": 38.0},
    "6": {"x": 6.5 * u, "y": 38.0}, "7": {"x": 7.5 * u, "y": 38.0}, "8": {"x": 8.5 * u, "y": 38.0},
    "9": {"x": 9.5 * u, "y": 38.0}, "0": {"x": 10.5 * u, "y": 38.0}, "-": {"x": 11.5 * u, "y": 38.0},
    "=": {"x": 12.5 * u, "y": 38.0}, "delete": {"x": 13.75 * u, "y": 38.0},

    "tab": {"x": 0.75 * u, "y": 19.0}, "q": {"x": 2.0 * u, "y": 19.0}, "w": {"x": 3.0 * u, "y": 19.0},
    "e": {"x": 4.0 * u, "y": 19.0}, "r": {"x": 5.0 * u, "y": 19.0}, "t": {"x": 6.0 * u, "y": 19.0},
    "y": {"x": 7.0 * u, "y": 19.0}, "u": {"x": 8.0 * u, "y": 19.0}, "i": {"x": 9.0 * u, "y": 19.0},
    "o": {"x": 10.0 * u, "y": 19.0}, "p": {"x": 11.0 * u, "y": 19.0}, "[": {"x": 12.0 * u, "y": 19.0},
    "]": {"x": 13.0 * u, "y": 19.0}, "\\": {"x": 14.0 * u, "y": 19.0},

    "caps": {"x": 0.875 * u, "y": 0.0}, "a": {"x": 2.25 * u, "y": 0.0}, "s": {"x": 3.25 * u, "y": 0.0},
    "d": {"x": 4.25 * u, "y": 0.0}, "f": {"x": 5.25 * u, "y": 0.0}, "g": {"x": 6.25 * u, "y": 0.0},
    "h": {"x": 7.25 * u, "y": 0.0}, "j": {"x": 8.25 * u, "y": 0.0}, "k": {"x": 9.25 * u, "y": 0.0},
    "l": {"x": 10.25 * u, "y": 0.0}, ";": {"x": 11.25 * u, "y": 0.0}, "'": {"x": 12.25 * u, "y": 0.0},
    "return": {"x": 13.625 * u, "y": 0.0},

    "l_shift": {"x": 1.125 * u, "y": -19.0}, "z": {"x": 2.75 * u, "y": -19.0}, "x": {"x": 3.75 * u, "y": -19.0},
    "c": {"x": 4.75 * u, "y": -19.0}, "v": {"x": 5.75 * u, "y": -19.0}, "b": {"x": 6.75 * u, "y": -19.0},
    "n": {"x": 7.75 * u, "y": -19.0}, "m": {"x": 8.75 * u, "y": -19.0}, ",": {"x": 9.75 * u, "y": -19.0},
    ".": {"x": 10.75 * u, "y": -19.0}, "/": {"x": 11.75 * u, "y": -19.0}, "r_shift": {"x": 13.375 * u, "y": -19.0},

    "fn": {"x": 0.5 * u, "y": -38.0}, "ctrl": {"x": 1.5 * u, "y": -38.0}, "opt": {"x": 2.5 * u, "y": -38.0},
    "cmd": {"x": 3.625 * u, "y": -38.0}, "space": {"x": 6.75 * u, "y": -38.0}, "r_cmd": {"x": 9.875 * u, "y": -38.0},
    "r_opt": {"x": 11.0 * u, "y": -38.0}, "left": {"x": 12.0 * u, "y": -38.0}, 
    "up": {"x": 13.0 * u, "y": -33.25}, "down": {"x": 13.0 * u, "y": -42.75}, 
    "right": {"x": 14.0 * u, "y": -38.0},
}
keys[" "] = keys["space"]

# --- 2. PHYSICS PRE-CALCULATIONS ---
width_mults = {
    "delete": 1.5, "tab": 1.5, "caps": 1.75, "return": 1.75, 
    "l_shift": 2.25, "r_shift": 2.25, "cmd": 1.25, "r_cmd": 1.25, "space": 5.0
}
height_mults = {"up": 0.5, "down": 0.5}

physical_gap_x = 3.0  
physical_gap_y = 3.5  

for k, v in keys.items():
    v["key"] = k
    w = width_mults.get(k, 1.0) * u - physical_gap_x
    h = height_mults.get(k, 1.0) * u - physical_gap_y
    cx, cy = v["x"], v["y"]
    v["coords"] = (
        (cx - w/2, cy - h/2), (cx - w/2, cy + h/2), 
        (cx + w/2, cy - h/2), (cx + w/2, cy + h/2)
    )

def calc_dist(f_data, target):
    if f_data["key"] == target["key"]: return 0.0
    t_xmin, t_xmax = target["coords"][0][0], target["coords"][2][0]
    t_ymin, t_ymax = target["coords"][0][1], target["coords"][1][1]
    f_xmin, f_xmax = f_data["coords"][0][0], f_data["coords"][2][0]
    f_ymin, f_ymax = f_data["coords"][0][1], f_data["coords"][1][1]
    dx = max(0.0, max(t_xmin, f_xmin) - min(t_xmax, f_xmax))
    dy = max(0.0, max(t_ymin, f_ymin) - min(t_ymax, f_ymax))
    return math.hypot(dx, dy)

FINGERS_NAMES = ["left pinky", "left ring", "left middle", "left index", 
                 "right index", "right middle", "right ring", "right pinky"]

def calculate_optimal_path(target_string, initial_state):
    valid_str = "".join([c.lower() for c in target_string if c.lower() in keys])
    if not valid_str: return None

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
                
                transition_cost = calc_dist(keys[state[f_idx]], keys[char])
                new_cost = cost + transition_cost
                
                if new_state not in next_layer or new_cost < next_layer[new_state][0]:
                    next_layer[new_state] = (new_cost, state, f_idx)
        
        if not next_layer: return None
        
        if len(next_layer) > BEAM_WIDTH:
            sorted_states = sorted(next_layer.items(), key=lambda item: item[1][0])
            next_layer = dict(sorted_states[:BEAM_WIDTH])
            
        layer = next_layer
        history.append(layer)

    best_final_state = min(layer, key=lambda s: layer[s][0])
    path = []
    curr_state = best_final_state
    
    for t in range(len(valid_str), 0, -1):
        _, prev_state, finger_used = history[t][curr_state]
        char_typed = valid_str[t-1]
        finger_name = FINGERS_NAMES[finger_used]
        path.append((char_typed, finger_name))
        curr_state = prev_state

    path.reverse()
    return path

# --- 5. VISUALIZER APP ---(VC)
class ManualInteractiveTracer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mac M2 Finger Tracer - Unconstrained Auto-Solver")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.scale = 5.0
        self.offset_x = 25
        self.offset_y = 150

        # Control Panel
        top_frame = tk.Frame(root, bg="#1e1e1e")
        top_frame.pack(fill=tk.X, pady=10, padx=25)
        
        btn = tk.Button(top_frame, text="🤖 Auto-Calculate Mathematically Fastest Path", 
                        font=("Arial", 12, "bold"), bg="#2ecc71", fg="black", command=self.auto_solve)
        btn.pack(side=tk.LEFT)
        
        # --- NEW: GRAND TOTAL TRACKER ---
        self.grand_total_var = tk.StringVar()
        self.grand_total_var.set("Grand Total: 0.0 u")
        lbl_total = tk.Label(top_frame, textvariable=self.grand_total_var, font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#3498db")
        lbl_total.pack(side=tk.LEFT, expand=True)
        
        btn_clear = tk.Button(top_frame, text="🧹 Clear Traces", font=("Arial", 12), command=self.clear_traces)
        btn_clear.pack(side=tk.RIGHT)

        btn_home = tk.Button(top_frame, text="🏠 Return to Home", font=("Arial", 12), command=self.return_to_home)
        btn_home.pack(side=tk.RIGHT, padx=10)

        self.canvas = tk.Canvas(root, bg="#1e1e1e")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.fingers = {
            "left pinky": {"pos": keys["a"], "color": "#9b59b6", "total_dist": 0.0, "key": "a", "history": deque(maxlen=2)},
            "left ring": {"pos": keys["s"], "color": "#f1c40f", "total_dist": 0.0, "key": "s", "history": deque(maxlen=2)},
            "left middle": {"pos": keys["d"], "color": "#3498db", "total_dist": 0.0, "key": "d", "history": deque(maxlen=2)},
            "left index": {"pos": keys["f"], "color": "#2ecc71", "total_dist": 0.0, "key": "f", "history": deque(maxlen=2)},
            "right index": {"pos": keys["j"], "color": "#e67e22", "total_dist": 0.0, "key": "j", "history": deque(maxlen=2)},
            "right middle": {"pos": keys["k"], "color": "#e74c3c", "total_dist": 0.0, "key": "k", "history": deque(maxlen=2)},
            "right ring": {"pos": keys["l"], "color": "#1abc9c", "total_dist": 0.0, "key": "l", "history": deque(maxlen=2)},
            "right pinky": {"pos": keys[";"], "color": "#ecf0f1", "total_dist": 0.0, "key": ";", "history": deque(maxlen=2)},
        }

        self.start_key = None
        self.active_finger_name = None
        self.temp_line = None

        self.info_var = tk.StringVar()
        self.update_status_display()

        self.label = tk.Label(
            root, textvariable=self.info_var, font=("Consolas", 11, "bold"),
            bg="#2d2d2d", fg="white", justify=tk.LEFT, pady=8, padx=20
        )
        self.label.pack(fill=tk.X, side=tk.BOTTOM)

        self.draw_keyboard()

        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def get_canvas_coords(self, x, y):
        cx = x * self.scale + self.offset_x
        cy = (50 - y) * self.scale + self.offset_y
        return cx, cy

    def draw_keyboard(self):
        self.key_coords = {}
        for char, pos in keys.items():
            if char == "space": continue 
            
            cx, cy = self.get_canvas_coords(pos["x"], pos["y"])
            c = pos["coords"]
            x1, y1 = self.get_canvas_coords(c[0][0], c[0][1])
            x2, y2 = self.get_canvas_coords(c[3][0], c[3][1])
            
            self.canvas.create_rectangle(
                x1, y1, x2, y2, 
                fill="#333333", outline="#555", width=2
            )
            
            display_char = char.upper() if char != " " else "SPACE"
            font_size = 14 if len(display_char) <= 2 else 9
            self.canvas.create_text(
                cx, cy, text=display_char, fill="white", font=("Arial", font_size, "bold")
            )
            self.key_coords[char] = (cx, cy)
            
        self.redraw_finger_markers()

    def redraw_finger_markers(self):
        self.canvas.delete("marker")
        for name, data in self.fingers.items():
            k = data["key"]
            cx, cy = self.key_coords[k]
            
            self.canvas.create_oval(
                cx - 18, cy - 18, cx + 18, cy + 18,
                outline=data["color"], width=4, tags="marker",
            )

    def find_closest_key(self, x, y):
        closest = None
        min_dist = float("inf")
        for char, (cx, cy) in self.key_coords.items():
            d = math.hypot(x - cx, y - cy)
            if d < min_dist and d < 40:
                min_dist = d
                closest = char
        return closest

    def update_status_display(self):
        # Update Grand Total
        grand_total = sum(data["total_dist"] for data in self.fingers.values())
        self.grand_total_var.set(f"Grand Total: {grand_total:.1f} u")

        # Update per-finger Breakdown
        status_lines = ["⚡ Click & drag to trace, Auto-Calculate optimized paths, or Return to Home! (ESC to exit)"]
        for name, data in self.fingers.items():
            history_str = " ➔ ".join([f"{m['from']}->{m['to']} ({m['dist']:.1f}u)" for m in data["history"]]) if data["history"] else "No moves yet"
            status_lines.append(f"[{name.title():<13}] Total: {data['total_dist']:>6.1f}u | Last 2: [{history_str}]")

        self.info_var.set("\n".join(status_lines))

    def clear_traces(self):
        self.canvas.delete("path")
        self.canvas.delete("path_text")
        for data in self.fingers.values():
            data["total_dist"] = 0.0
            data["history"].clear()
        self.update_status_display()

    def return_to_home(self):
        home_keys = {
            "left pinky": "a", "left ring": "s", "left middle": "d", "left index": "f",
            "right index": "j", "right middle": "k", "right ring": "l", "right pinky": ";"
        }
        
        for f_name, data in self.fingers.items():
            start_key = data["key"]
            end_key = home_keys[f_name]
            
            if start_key != end_key:
                step_dist = calc_dist(keys[start_key], keys[end_key])
                data["total_dist"] += step_dist
                data["history"].append({
                    "from": start_key.upper() if start_key != " " else "SPC",
                    "to": "HOME",
                    "dist": step_dist
                })
                data["pos"] = keys[end_key]
                data["key"] = end_key
                
                scx, scy = self.key_coords[start_key]
                ecx, ecy = self.key_coords[end_key]
                
                if step_dist > 0:
                    self.canvas.create_line(scx, scy, ecx, ecy, fill=data["color"], width=2, dash=(4, 4), tags="path")
                    mid_x = (scx + ecx) / 2
                    mid_y = (scy + ecy) / 2 - 15
                    self.canvas.create_text(mid_x, mid_y, text=f"🏠{step_dist:.1f}", fill="orange", font=("Arial", 9, "bold"), tags="path_text")
                    
        self.redraw_finger_markers()
        self.update_status_display()

    def auto_solve(self):
        target = simpledialog.askstring("Auto Solver", "Enter text to optimize (ignores human constraints):")
        if not target: return
        
        # Start the solver from wherever the fingers currently are!
        current_state = (
            self.fingers["left pinky"]["key"], self.fingers["left ring"]["key"],
            self.fingers["left middle"]["key"], self.fingers["left index"]["key"],
            self.fingers["right index"]["key"], self.fingers["right middle"]["key"],
            self.fingers["right ring"]["key"], self.fingers["right pinky"]["key"]
        )
        
        path = calculate_optimal_path(target, current_state)
        if not path:
            messagebox.showerror("Error", "Could not calculate path.")
            return
            
        for char, f_name in path:
            start_key = self.fingers[f_name]["key"]
            end_key = char
            
            step_dist = calc_dist(keys[start_key], keys[end_key])
            f_data = self.fingers[f_name]
            f_data["total_dist"] += step_dist
            f_data["history"].append({
                "from": start_key.upper() if start_key != " " else "SPC",
                "to": end_key.upper() if end_key != " " else "SPC",
                "dist": step_dist
            })
            f_data["pos"] = keys[end_key]
            f_data["key"] = end_key
            
            scx, scy = self.key_coords[start_key]
            ecx, ecy = self.key_coords[end_key]
            
            # Don't draw lines for 0.0 distance
            if step_dist > 0:
                self.canvas.create_line(scx, scy, ecx, ecy, fill=f_data["color"], width=3, tags="path")
                mid_x = (scx + ecx) / 2
                mid_y = (scy + ecy) / 2 - 15
                self.canvas.create_text(mid_x, mid_y, text=f"{step_dist:.1f}", fill="white", font=("Arial", 9, "bold"), tags="path_text")
                
        self.redraw_finger_markers()
        self.update_status_display()

    # --- MANUAL TRACE LOGIC ---
    def on_press(self, event):
        clicked_key = self.find_closest_key(event.x, event.y)
        if clicked_key:
            active_finger = None
            for name, data in self.fingers.items():
                if data["key"] == clicked_key:
                    active_finger = (name, data)
                    break
            
            if active_finger:
                self.start_key = clicked_key
                self.active_finger_name = active_finger[0]
                color = active_finger[1]["color"]
                cx, cy = self.key_coords[self.start_key]
                self.temp_line = self.canvas.create_line(cx, cy, event.x, event.y, fill=color, width=4, dash=(4, 2))
            else:
                self.start_key = None

    def on_drag(self, event):
        if self.temp_line and self.start_key:
            cx, cy = self.key_coords[self.start_key]
            self.canvas.coords(self.temp_line, cx, cy, event.x, event.y)

    def on_release(self, event):
        if self.temp_line:
            self.canvas.delete(self.temp_line)
            self.temp_line = None

        if self.start_key:
            end_key = self.find_closest_key(event.x, event.y)
            if end_key and end_key != self.start_key:
                step_dist = calc_dist(keys[self.start_key], keys[end_key])
                f_data = self.fingers[self.active_finger_name]
                f_data["total_dist"] += step_dist
                f_data["history"].append({
                    "from": self.start_key.upper() if self.start_key != " " else "SPC",
                    "to": end_key.upper() if end_key != " " else "SPC",
                    "dist": step_dist,
                })
                f_data["pos"] = keys[end_key]
                f_data["key"] = end_key

                scx, scy = self.key_coords[self.start_key]
                ecx, ecy = self.key_coords[end_key]
                self.canvas.create_line(scx, scy, ecx, ecy, fill=f_data["color"], width=4, tags="path")

                mid_x = (scx + ecx) / 2
                mid_y = (scy + ecy) / 2 - 18
                self.canvas.create_text(
                    mid_x, mid_y, text=f"{step_dist:.1f}", fill="yellow",
                    font=("Arial", 12, "bold"), tags="path_text"
                )

                self.redraw_finger_markers()
                self.update_status_display()

            self.start_key = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ManualInteractiveTracer(root)
    root.mainloop()
