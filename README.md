# ⌨️ Typing Algorithm

A physics-inspired typing simulation that models how human fingers move across a keyboard. Instead of using hardcoded finger-to-key assignments, this algorithm **dynamically selects the optimal finger** for each keystroke based on physical distance, hand tilt geometry, and (optionally) home-row gravity.

Two prototypes explore different strategies — **greedy** vs **globally optimal** — for solving the finger-assignment problem.

## 📁 Branch Structure

| Branch | Description |
|---|---|
| `main` | Documentation only |
| [`prototype-1-greedy`](../../tree/prototype-1-greedy) | Greedy, character-by-character finger selection with home-row gravity |
| [`prototype-2-viterbi`](../../tree/prototype-2-viterbi) | Viterbi dynamic programming with beam search for globally optimal paths |

## 🧠 How It Works

Typing is treated as a **cost-minimization problem**. Given a string to type, the algorithm decides which of 8 fingers should press each key to minimize total finger travel distance.

### Cost Function

For each finger `f` moving from its current key to a target key `t`:

$$
\text{cost} = \lvert \text{parallel}\rvert + 1.2 \cdot \lvert\text{orthogonal}\rvert
$$

Where parallel and orthogonal are projections of the finger→target vector onto **tilted hand axes** (tilt angle ≈ 0.08 rad), reflecting that lateral finger movement is easier than vertical reach.

| Factor | Description |
|---|---|
| **Hand tilt angle** | A rotational offset (0.08 rad) decomposes movement into parallel and orthogonal components, modeling the natural inward rotation of hands on the keyboard |
| **Orthogonal weighting** | Vertical movement is penalized 1.2× more than horizontal movement |
| **Home-row gravity** *(Prototype 1 only)* | A tunable penalty for how far a finger has drifted from its home position |

## 📂 Prototypes

### Prototype 1 — Greedy, Character-by-Character · [`prototype-1-greedy`](../../tree/prototype-1-greedy)

Processes input **one character at a time**. For each keystroke, it evaluates all 8 fingers and picks the one with the **lowest immediate cost** — a greedy approach.

**Key features:**
- Full Mac keyboard layout with **shifted characters** (e.g., `!` / `@` / uppercase letters)
- **Home-row gravity** parameter (γ) — penalizes fingers that have drifted far from home, modeling the natural tendency to return

$$
\text{total\_cost} = \text{move\_cost} + \gamma \cdot d_{\text{home}}
$$

- Per-finger **movement history** logging
- Configurable home keys

**How to run:**
```bash
git checkout prototype-1-greedy
python main.py
```

**Example output:**
```
h pressed by right index
e pressed by left middle
l pressed by right ring
l pressed by right ring
o pressed by right ring

--- History for right index ---
Pressed 'h'.
```

---

### Prototype 2 — Viterbi Dynamic Programming · [`prototype-2-viterbi`](../../tree/prototype-2-viterbi)

Instead of making greedy per-character decisions, this prototype finds the **globally optimal finger assignment** for the entire input string using the [Viterbi algorithm](https://en.wikipedia.org/wiki/Viterbi_algorithm).

**How it works:**

1. **State space** — Each state is a tuple of 8 keys representing where each finger currently rests. The initial state is the home row.
2. **Transitions** — For each character, the algorithm branches into 8 possible futures (one per finger that could press the key), computing the cumulative cost for each.
3. **Beam search pruning** — To keep the search tractable, only the top **3,000 lowest-cost states** are kept at each step.
4. **Traceback** — After processing all characters, the algorithm traces back from the lowest-cost final state to reconstruct the optimal finger sequence.

**Key features:**
- **Globally optimal** path (within beam width) — avoids the short-sighted mistakes of greedy selection
- Viterbi DP with **beam width of 3,000**
- Clean step-by-step output of the optimal sequence

**How to run:**
```bash
git checkout prototype-2-viterbi
python main.py
```

**Example output:**
```
--- VITERBI OPTIMAL PATH ---
Step 1: 'h' pressed by Right Index
Step 2: 'e' pressed by Left Middle
Step 3: 'l' pressed by Right Ring
Step 4: 'l' pressed by Right Ring
Step 5: 'o' pressed by Right Middle
```

## ⚖️ Prototype Comparison

| | Prototype 1 (Greedy) | Prototype 2 (Viterbi DP) |
|---|---|---|
| **Strategy** | Greedy — best finger *right now* | Global — best finger *overall* |
| **Optimality** | Locally optimal | Globally optimal (within beam) |
| **Time complexity** | O(n × 8) | O(n × B × 8) where B = beam width |
| **Gravity parameter** | ✅ Yes | ❌ No |
| **Shifted / uppercase** | ✅ Yes | ❌ Lowercase only |
| **Per-finger history** | ✅ Yes | ❌ No |
| **Best for** | Quick simulation, experimentation | Finding the true optimal path |

## ⚙️ Configuration

| Parameter | Prototype | Default | Description |
|---|---|---|---|
| Gravity (γ) | 1 only | — | How strongly fingers pull back to home row (`0.0`–`1.0`). Recommended: `0.03`–`0.08` |
| Home keys | Both | `asdfjkl;` | Custom home-row keys for the 8 fingers (left pinky → right pinky) |
| Tilt angle | Both | `0.08` rad | Models the natural inward rotation of the hands (hardcoded) |
| Orthogonal weight | Both | `1.2` | Penalty multiplier for vertical vs horizontal movement (hardcoded) |
| Beam width | 2 only | `3000` | Max states kept per DP layer (hardcoded) |

## 🗺️ Keyboard Model

The keyboard is modeled as a **coordinate grid** based on a standard Mac laptop layout. Every key is stored with:
- **Row and column** identifiers
- **Bounding box coordinates** — 4 corner points `(x, y)` in millimeters
- Prototype 1 includes both **lowercase and shifted** variants mapped to the same physical key

Rows are numbered bottom-up:

| Row | Keys |
|---|---|
| 6 | Bottom modifiers — fn, control, option, cmd, space, arrows |
| 5 | Shift row — z, x, c, v, b, n, m, punctuation |
| 4 | Home row — a, s, d, f, g, h, j, k, l, semicolon |
| 3 | Top letter row — q, w, e, r, t, y, u, i, o, p, brackets |
| 2 | Number row — 1–0, symbols, delete |

## 🛠️ Tech Stack

- **Language:** Python 3
- **Dependencies:** `math` (standard library only — zero external packages)

## 🚀 Future Ideas

- [ ] Visualize finger paths on a keyboard heatmap
- [ ] Merge gravity into the Viterbi prototype
- [ ] Add shifted / uppercase character support to Prototype 2
- [ ] Benchmark against real typing data (WPM correlation)
- [ ] Support non-QWERTY layouts (Dvorak, Colemak)
- [ ] Add anatomical constraints (finger crossing, max stretch)
- [ ] Extend to mobile / thumb-typing models

## 📄 License

<!-- Add your preferred license here -->
