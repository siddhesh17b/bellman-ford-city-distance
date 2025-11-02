# Bellman-Ford Shortest Path Visualizer

A hybrid C/Python application that finds shortest paths between cities using the Bellman-Ford algorithm with interactive GUI visualization.

![Version](https://img.shields.io/badge/version-1.0-blue)
![Language](https://img.shields.io/badge/language-C%20%2B%20Python-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🎯 Features

- **Pure C Backend**: Bellman-Ford algorithm implementation with memoization for fast repeat calculations
- **Modern Interactive GUI**: Professional step-by-step Tkinter interface with color-coded sections
- **Horizontal Fork Tree Visualization**: Single source node with N-1 branches showing routes to each destination
- **Negative Cycle Detection**: Automatically detects and reports negative weight cycles
- **Random Test Generator**: One-click random distance matrix generation for quick testing
- **Path Verification**: Built-in validation comparing reconstructed paths against calculated distances
- **Informative Display**: Real-time statistics showing path count and reachable cities

## 📋 Prerequisites

- **GCC Compiler** (MinGW for Windows)
- **Python 3.x**
- **Required Python packages**:
  ```bash
  pip install matplotlib networkx
  ```

## 🚀 Quick Start

### 1. Compile the C Backend

```powershell
gcc bellman_backend.c -o bellman_backend.exe
```

### 2. Run the GUI

```powershell
python bellman_gui.py
```

## 📖 How to Use

### Step-by-Step Guide:

**Step 1: City Configuration**
1. Enter number of cities (2-15) in the input box
2. Click "Create Matrix" to generate the distance grid
3. City names are auto-generated as A, B, C, etc.

**Step 2: Distance Matrix**
1. Fill in distances between cities:
   - Enter positive integers for road distances
   - Use "INF" or leave blank for no direct road
   - Diagonal cells (0) are read-only (city to itself)
2. OR click "🎲 Generate Random Distances" for instant test data

**Step 3: Run Algorithm**
1. Select source city from dropdown menu
2. Click "▶ Run Algorithm" button
3. View results in the results pane and graph visualization

### Understanding the Results:

- **Results Pane**: Shows distance from source to each city
- **Graph Visualization** (Horizontal Fork Tree):
  - 🔴 Single red node on left = Source city (all paths start here)
  - N-1 branches emerge from source (fork shape)
  - Each branch = Complete path to one destination city
  - 🟢 Green nodes = Reachable destination cities (at the end of their branch)
  - 🟢 Light green nodes = Intermediate cities along a branch
  -  Blue nodes = Unreachable destination cities (distance = ∞)
  - Green arrows with `[weight]` = Edges on shortest paths
  - All branches share the same source node (no duplication)

## 🔧 Project Structure

```
bellman-ford-city-distance/
├── bellman_backend.c       # C implementation of Bellman-Ford
├── bellman_gui.py          # Python GUI (Tkinter + NetworkX)
├── bellman_backend.exe     # Compiled C program (auto-generated)
├── README.md               # This file
├── LICENSE                 # MIT License
├── .gitignore              # Git ignore rules
└── VERIFICATION_REPORT.md  # Extensive testing report
```

## 🎨 Visual Features

### Graph Visualization (Horizontal Fork Tree)

The graph displays like a horizontal fork/tree with **1 source and N-1 branches**:

```
Example with 4 cities (A=source):

                  ──[5]──> B ──[3]──> C  (Branch to C: distance 8)
                 /
        A ──────┤──────────[10]──────> D  (Branch to D: distance 10)
                 \
                  ──[5]──> B             (Branch to B: distance 5)
```

**Key Characteristics:**
- **Single source node**: One red source node at left (x=0, y=0)
- **Fork shape**: N-1 branches emerge from the source (like a tree fork)
- **One branch per destination**: Each branch shows complete shortest path to that destination
- **No source duplication**: Source appears only once, shared by all branches
- **Intermediate nodes unique**: Cities can appear in multiple branches (e.g., B appears in branches to C and to B)
- **Horizontal layout**: Nodes arranged left-to-right showing traversal order

**Nodes:**
- 🔴 **Red with dark border**: Source city (single node, all branches start here)
- 🟢 **Green with dark border**: Destination cities (reachable, at end of their branch)
- 🟢 **Light green**: Intermediate cities along the path
- 🔵 **Blue with dark border**: Unreachable destination cities (distance = ∞)
- **Label format**: `CityName\n(distance)` where distance is from source

**Edges:**
- **Bold green arrows (3px)**: Path edges with weights shown as `[10]`
- **Gray dashed arrows**: Edges for unreachable paths
- **First edge of each branch**: Connects from shared source node to first intermediate/destination

**Legend:**
- Positioned below graph to avoid overlap
- Shows node types and edge types
- Title displays: "Horizontal Tree: Shortest Paths from X | N paths shown | Reachable: Y/Z cities"

### GUI Layout
- **Step 1**: Blue section for city configuration
- **Step 2**: Purple section for distance matrix input  
- **Step 3**: Green section for algorithm execution
- **Results**: Clean scrollable text output with monospace font
- **Graph**: Professional horizontal fork tree visualization with informative title

## ⚙️ How It Works

### Architecture

```
┌─────────────────┐
│   Python GUI    │  Collects user input
│  (bellman_gui)  │  Formats data
└────────┬────────┘
         │
         │ subprocess call
         ↓
┌─────────────────┐
│   C Backend     │  Runs Bellman-Ford
│ (bellman_backend)│ Calculates paths
└────────┬────────┘
         │
         │ stdout output
         ↓
┌─────────────────┐
│   Python GUI    │  Displays results
│                 │  Visualizes graph
└─────────────────┘
```

### Input Format (C Program)

The GUI sends data to C program in this format:

```
<number_of_cities> <number_of_edges>
<city1_name>
<city2_name>
...
<from_city> <to_city> <distance>
<from_city> <to_city> <distance>
...
<source_city_name>
```

### Example

```
3 3
A
B
C
A B 10
B C 5
A C 20
A
```

## 🧪 Testing

### Manual Testing
1. Create a simple 3-city network
2. Test with known shortest paths
3. Verify output matches expected results

### Automated Testing
Run the verification script:
```powershell
python verify_integration.py
```

## 📊 Example Use Cases

### Case 1: Finding Shortest Route
- **Cities**: A, B, C
- **Roads**: A→B (10), B→C (5), A→C (20)
- **Result**: Shortest A→C is 15 (via B), not 20 (direct)

### Case 2: Unreachable Cities
- **Cities**: A, B, C
- **Roads**: A→B (5), B→C (3)
- **From B**: Can reach C (3), but not A (INF)

### Case 3: Negative Cycle Detection
- **Cities**: A, B, C
- **Roads**: A→B (1), B→C (2), C→A (-5)
- **Result**: Error - negative weight cycle detected

## 🔍 Algorithm Details

**Bellman-Ford Algorithm Steps:**
1. Initialize distances to infinity
2. Set source distance to 0
3. Relax all edges V-1 times
4. Check for negative cycles
5. Return shortest distances

**Time Complexity**: O(V × E)  
**Space Complexity**: O(V²) with memoization

## ⚠️ Limitations

- Maximum 15 cities (GUI constraint - for readability)
- Maximum 50 cities (C backend `MAX` constant - can be increased by recompiling)
- Single source at a time (run again for different sources)
- Windows-specific (uses `.exe` extension - modify for Linux/Mac)
- Graph visualization only shows after algorithm execution (no pre-run preview)

## 🛠️ Customization

### Change Maximum Cities (C Backend)
Edit `MAX` constant in `bellman_backend.c`:
```c
#define MAX 100  // Change from 50 to 100
```
Then recompile: `gcc bellman_backend.c -o bellman_backend.exe`

### Change GUI City Limit
Edit validation in `bellman_gui.py` (around line 90):
```python
if not 2 <= self.city_count <= 20:  # Change from 15 to 20
```

### Customize Color Scheme
Edit color codes in `bellman_gui.py`:
- Title bar: `bg='#2c3e50'` (dark blue-gray)
- Buttons: `bg='#3498db'` (blue), `bg='#27ae60'` (green), `bg='#9b59b6'` (purple)
- Node colors: `'#FF4444'` (red), `'#44FF44'` (green), `'#4488FF'` (blue)

### Adjust Graph Layout
Modify spacing in `draw_graph()` method:
```python
y_spacing = 1.8  # Vertical spacing between branches (increase for more space)
self.fig = Figure(figsize=(7, 7), dpi=100)  # Graph canvas size
```

**Understanding the horizontal fork structure:**
- Source node appears ONCE at coordinates (0, 0)
- Each destination branch emerges from this single source
- Intermediate/destination nodes positioned from x=2 to x=10 along their branch
- Nodes use unique keys `"CityName_DestinationName"` except source which uses `"SourceName_SOURCE"`

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Developed for DAA Lab Project
- Algorithm Implementation: C (Bellman-Ford)
- GUI Development: Python (Tkinter + NetworkX)

## 🙏 Acknowledgments

- Bellman-Ford algorithm based on standard textbook implementation
- NetworkX library for graph visualization
- Matplotlib for embedding graphs in Tkinter

## 📞 Support

For questions or issues:
1. Check `VERIFICATION_REPORT.md` for detailed testing
2. Review code comments for implementation details
3. Ensure C backend is compiled before running GUI

## 🔮 Future Enhancements

- [ ] Support for bidirectional roads (auto-fill symmetric matrix)
- [ ] Highlight actual path sequence with step-by-step animation
- [ ] Multiple source comparison (side-by-side view)
- [ ] Save/load graph configurations (JSON format)
- [ ] Export results and graph to PDF/PNG
- [ ] Dark mode theme toggle
- [ ] Undo/redo for matrix edits
- [ ] Import from CSV file

---

**Note**: This is an educational project demonstrating algorithm implementation and GUI integration. The Bellman-Ford algorithm runs entirely in C, while Python provides the user interface.
