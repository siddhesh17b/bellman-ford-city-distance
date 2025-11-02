# Copilot Instructions: Bellman-Ford Shortest Path Visualizer

## Architecture Overview

This is a **hybrid C/Python application** split across two completely separate runtimes:

- **`bellman_backend.c`**: Pure C implementation of Bellman-Ford algorithm with memoization. This is the computational engine.
- **`bellman_gui.py`**: Python GUI (Tkinter + NetworkX) that orchestrates user input, subprocess calls, and visualization.

**Critical Flow**: Python GUI → formats input → spawns `./bellman_backend.exe` subprocess → C program reads stdin & writes stdout → Python parses output → visualizes graph.

**No linking/FFI**: These programs communicate ONLY via stdin/stdout text protocol. The C program must be pre-compiled before running the Python GUI.

## Build & Run Workflow

### First-time setup:
```powershell
# 1. Compile C backend (MUST be done first)
gcc bellman_backend.c -o bellman_backend.exe

# 2. Install Python dependencies
pip install matplotlib networkx

# 3. Launch GUI
python bellman_gui.py
```

**Critical**: If C backend isn't compiled, Python will fail with `FileNotFoundError` when attempting to run the algorithm.

## Inter-Process Communication Protocol

### Input Format (Python → C via stdin):
```
<V> <E>              # number of cities, number of roads
<city1_name>         # all city names (one per line)
<city2_name>
...
<from> <to> <dist>   # all edges (one per line)
<from> <to> <dist>
...
<source_city_name>   # source for shortest path calculation
```

### Output Format (C → Python via stdout):
```
Source City: <name>
------------------------------------
City            Distance
------------------------------------
<city1>         <distance>
<city2>         INF
...
```

**When modifying**: Both programs must maintain this exact text protocol. Changes to output format require updating `parse_and_visualize_results()` in Python.

## Key Implementation Details

### C Backend (`bellman_backend.c`)
- **Memoization**: Global `memo[MAX][MAX]` table caches results between runs. If you modify the algorithm, ensure memo initialization logic matches.
- **Limits**: `#define MAX 50` for max cities. Changing this requires recompilation.
- **Negative cycle detection**: Implemented as per textbook Bellman-Ford (V-1 relaxations + 1 check iteration).
- **Memory management**: `createGraph()` uses `malloc()` - ensure `free()` is added if you modify graph lifecycle.

### Python GUI (`bellman_gui.py`)
- **Modern UI structure**: Organized into labeled sections (Step 1/2/3) with color-coded frames and emoji icons for clarity.
- **City names**: Auto-generated as A, B, C, ... (chr(65+i)). Hardcoded to 15 max in GUI validation (line ~90).
- **Matrix input**: Uses 2D array `self.city_entries[i][j]` of Tkinter Entry widgets. Diagonal cells are **read-only** (state='readonly') and always 0. "INF" represents no road.
- **Graph visualization**: `draw_graph()` ONLY displays after algorithm execution (no pre-run graph):
  - **Horizontal fork/tree layout**: Single source node on left with N-1 lines emerging from it
  - Each line/branch shows the path to one destination city
  - Source node appears ONCE at (0, 0), shared by all paths
  - Intermediate/destination nodes positioned from x=2 to x=10 along their path's y-coordinate
  - Vertical spacing between path branches: 1.8 units
- **Path reconstruction logic** (lines ~200-280): Backtracks from each destination using `shortest_distances` dict and edge weights to rebuild shortest path for that destination's branch. **Verification**: Compares reconstructed path sum against reported distance; mismatches print to results pane with ⚠ symbol.
- **Node coloring**: Red = source (single shared node), Green = reachable destination, Light green = intermediate node on path, Blue = unreachable
- **Legend placement**: Positioned below graph using `bbox_to_anchor=(0.5, -0.02)` to prevent overlap with tree.

## Common Modification Patterns

### Change max cities:
1. **C**: Edit `#define MAX 50` in `bellman_backend.c` → recompile: `gcc bellman_backend.c -o bellman_backend.exe`
2. **Python**: Edit validation `if not 2 <= self.city_count <= 15:` in `create_matrix()` method (line ~90)

### Customize GUI colors/styling:
- **Section colors**: Search for `LabelFrame` creations with `font=("Arial", 11, "bold")` (lines ~40-80)
- **Button colors**: Look for `tk.Button(..., bg='#3498db', fg='white')` patterns
- **Node colors**: In `draw_graph()` find `node_colors.append('#FF4444')` logic (line ~230)
- **Edge colors**: Find `edge_color='#00AA00'` in `draw_networkx_edges()` calls

### Modify graph layout:
- **Spacing**: Edit `y_spacing = 1.8` in `draw_graph()` for vertical distribution between path branches
- **Figure size**: Change `Figure(figsize=(7, 7), dpi=100)` in `__init__()`
- **Legend position**: Adjust `bbox_to_anchor=(0.5, -0.02)` value for legend placement
- **Node size**: Modify `node_size=1000` parameter in `draw_networkx_nodes()`
- **Fork structure**: Source node at (0,0) is shared; branches use unique keys like `"CityName_DestinationName"` for non-source nodes

### Modify algorithm output format:
1. **C side**: Update `printDistances()` function formatting
2. **Python side**: Update parsing in `parse_and_visualize_results()` - looks for lines matching `"City            Distance"` pattern
3. **Critical**: Both must stay synchronized or parsing fails

### Debug subprocess communication:
- **Check output**: Examine `result.stdout` and `result.stderr` in `run_algorithm()` method
- **Test standalone**: Run `./bellman_backend.exe` in terminal with manual input to verify C program
- **Input format**: Ensure Python sends: `V E\nnames...\nedges...\nsource\n`

## Platform Notes

- **Windows-specific**: Uses `.exe` extension and PowerShell commands in docs
- **Path**: C executable expected at `./bellman_backend.exe` relative to Python script location
- For cross-platform: Replace `"./bellman_backend.exe"` with `"./bellman_backend"` and adjust compilation

## Testing Approach

- **Quick testing**: Click "🎲 Generate Random Distances" button to create test cases instantly (generates 1-50 range)
- **Edge cases to test**:
  - Negative weights (valid if no negative cycle)
  - Unreachable nodes (use INF or leave blank)
  - Single path vs multiple paths to same destination
  - All nodes unreachable except source
- **Built-in verification**: Path reconstruction logic automatically validates distances - mismatches appear in red in results pane
- **Visual verification**: Check that green shortest-path edges form valid routes and edge weights sum correctly

## UI/UX Design Patterns

### Three-step workflow:
1. **Step 1 (Blue)**: Configure cities → creates matrix
2. **Step 2 (Purple)**: Fill distances → enables algorithm
3. **Step 3 (Green)**: Select source & run → shows results + graph

### Visual feedback:
- Disabled buttons until prerequisites met (matrix must exist before randomization)
- Read-only diagonal cells (gray background) prevent invalid edits
- Graph only renders post-execution (avoids confusion from meaningless pre-run layouts)
- Color-coded legend with statistics in title (`Reachable: X/Y cities`)

### Graph rendering strategy:
- **No pre-run graph**: Returns early from `draw_graph()` if no results available
- **Horizontal fork/tree layout**: Single source node with N-1 branches emerging from it (fork shape)
- **Single source node**: Source appears ONCE at coordinates (0, 0), shared by all path branches
- **Branch independence**: Each destination gets its own branch; intermediate nodes use unique keys `"NodeName_DestinationName"`
- **Path reconstruction**: Walks backwards from each destination using edge weights to find shortest route, then displays that path as a branch
- **Edge display**: Only shows edges that are part of the shortest paths; first edge of each branch connects from shared source node
