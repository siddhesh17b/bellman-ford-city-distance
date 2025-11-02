import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess  # To run our C program
import random      # For generating random distances
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import networkx as nx  # For graph visualization

class BellmanFordGUI:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Bellman-Ford Shortest Path Visualizer")
        self.root.geometry("1400x850")
        self.root.configure(bg='#f0f0f0')

        # Variables to store our data
        self.city_entries, self.city_names, self.city_count, self.graph_data = [], [], 0, None

        # Create title label at the top with better styling
        title_frame = tk.Frame(root, bg='#2c3e50', pady=15)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="🗺️ Bellman-Ford Shortest Path Visualizer", 
                font=("Arial", 18, "bold"), bg='#2c3e50', fg='white').pack()

        # Main container to hold left and right panels
        main_container = tk.Frame(root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel: for all the controls and inputs
        left_frame = tk.Frame(main_container, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Right panel: for graph visualization
        right_frame = tk.Frame(main_container, relief=tk.SOLID, borderwidth=2, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Section 1: Input for number of cities (with better styling)
        input_section = tk.LabelFrame(left_frame, text="📊 Step 1: City Configuration", 
                                      font=("Arial", 11, "bold"), bg='#f0f0f0', 
                                      relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
        input_section.pack(pady=5, fill=tk.X)
        
        frame_top = tk.Frame(input_section, bg='#f0f0f0')
        frame_top.pack(pady=5)
        tk.Label(frame_top, text="Number of Cities (2-15):", font=("Arial", 10), 
                bg='#f0f0f0').grid(row=0, column=0, padx=5, sticky='w')
        self.entry_cities = tk.Entry(frame_top, width=10, font=("Arial", 10))
        self.entry_cities.grid(row=0, column=1, padx=5)
        tk.Button(frame_top, text="Create Matrix", command=self.create_matrix, 
                 bg='#3498db', fg='white', font=("Arial", 10, "bold"), 
                 relief=tk.RAISED, padx=10, pady=5).grid(row=0, column=2, padx=5)

        # Section 2: Distance matrix container (with better styling)
        matrix_section = tk.LabelFrame(left_frame, text="📝 Step 2: Distance Matrix", 
                                       font=("Arial", 11, "bold"), bg='#f0f0f0', 
                                       relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
        matrix_section.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.matrix_frame = tk.Frame(matrix_section, bg='#f0f0f0')
        self.matrix_frame.pack(pady=5)

        # Button to generate random distances (disabled until matrix is created)
        self.random_btn = tk.Button(matrix_section, text="🎲 Generate Random Distances", 
                                    command=self.randomize_matrix, state="disabled",
                                    bg='#9b59b6', fg='white', font=("Arial", 10, "bold"),
                                    relief=tk.RAISED, padx=10, pady=5)
        self.random_btn.pack(pady=5)

        # Section 3: Source selection and algorithm execution
        control_section = tk.LabelFrame(left_frame, text="🚀 Step 3: Run Algorithm", 
                                       font=("Arial", 11, "bold"), bg='#f0f0f0', 
                                       relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
        control_section.pack(pady=5, fill=tk.X)
        
        source_frame = tk.Frame(control_section, bg='#f0f0f0')
        source_frame.pack(pady=5)
        tk.Label(source_frame, text="Select Source City:", font=("Arial", 10), 
                bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        self.source_var = tk.StringVar()
        self.source_menu = tk.OptionMenu(source_frame, self.source_var, [])
        self.source_menu.config(font=("Arial", 10), width=8)
        self.source_menu.pack(side=tk.LEFT, padx=5)

        # Button to run the algorithm
        tk.Button(control_section, text="▶ Run Algorithm", command=self.run_algorithm,
                 bg='#27ae60', fg='white', font=("Arial", 11, "bold"),
                 relief=tk.RAISED, padx=20, pady=8).pack(pady=10)

        # Section 4: Results display (with better styling)
        results_section = tk.LabelFrame(left_frame, text="📋 Results", 
                                       font=("Arial", 11, "bold"), bg='#f0f0f0', 
                                       relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
        results_section.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.txt_output = scrolledtext.ScrolledText(results_section, width=50, height=12, 
                                                    font=("Consolas", 9), bg='#ffffff',
                                                    relief=tk.SUNKEN, borderwidth=2)
        self.txt_output.pack(pady=5, fill=tk.BOTH, expand=True)

        # Section 5: Graph visualization area (improved styling)
        graph_header = tk.Frame(right_frame, bg='#34495e', pady=10)
        graph_header.pack(fill=tk.X)
        tk.Label(graph_header, text="🗺️ Network Graph Visualization", 
                font=("Arial", 13, "bold"), bg='#34495e', fg='white').pack()
        
        # Create a matplotlib figure for drawing the graph with more space
        self.fig = Figure(figsize=(7, 7), dpi=100, facecolor='white')
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Show initial message before any graph is created
        self.ax.text(0.5, 0.5, 'Run algorithm to see shortest path visualization', 
                    ha='center', va='center', fontsize=12, color='#7f8c8d', style='italic')
        self.ax.set_xlim(0, 1); self.ax.set_ylim(0, 1); self.ax.axis('off'); self.canvas.draw()

    def create_matrix(self):
        """Creates the distance matrix based on user input"""
        try:
            # Get the number of cities from the entry box and validate
            self.city_count = int(self.entry_cities.get())
            if not 2 <= self.city_count <= 15:
                messagebox.showerror("Error", "Enter 2-15 cities"); return
        except ValueError:
            messagebox.showerror("Error", "Invalid number"); return

        # Clear any existing matrix
        for widget in self.matrix_frame.winfo_children(): widget.destroy()
        self.city_entries.clear()

        # Auto-generate city names: A, B, C, D, etc. (chr(65) = 'A')
        self.city_names = [chr(65 + i) for i in range(self.city_count)]

        # Add instruction label and column headers
        tk.Label(self.matrix_frame, text="Enter distances (0 = same city, INF = no direct road)", 
                font=("Arial", 9, "italic"), bg='#f0f0f0', fg='#555').grid(
                row=0, column=0, columnspan=self.city_count+1, pady=5)
        # Column headers
        tk.Label(self.matrix_frame, text="", bg='#f0f0f0').grid(row=1, column=0)  # Empty corner
        for j, name in enumerate(self.city_names):
            tk.Label(self.matrix_frame, text=name, font=("Arial", 10, "bold"), 
                    bg='#3498db', fg='white', width=5, relief=tk.RAISED).grid(
                    row=1, column=j+1, padx=1, pady=1)

        # Create the matrix grid with entry boxes (improved styling)
        for i, name in enumerate(self.city_names):
            # Row headers
            tk.Label(self.matrix_frame, text=name, font=("Arial", 10, "bold"), 
                    bg='#3498db', fg='white', width=5, relief=tk.RAISED).grid(
                    row=i+2, column=0, padx=1, pady=1)
            row_entries = []
            for j in range(self.city_count):
                e = tk.Entry(self.matrix_frame, width=6, justify="center", font=("Arial", 9))
                e.grid(row=i+2, column=j+1, padx=1, pady=1)
                if i == j:
                    e.insert(0, "0")
                    e.config(state='readonly', readonlybackground='#ecf0f1')  # Diagonal is read-only
                else:
                    e.insert(0, "")
                row_entries.append(e)
            self.city_entries.append(row_entries)

        # Update the source city dropdown menu
        self.source_var.set(self.city_names[0])
        menu = self.source_menu["menu"]
        menu.delete(0, "end")
        for name in self.city_names:
            menu.add_command(label=name, command=lambda v=name: self.source_var.set(v))
        self.random_btn.config(state="normal")  # Enable the random button

    def draw_graph(self, highlight_source=None, shortest_distances=None):
        """Draw a horizontal binary-tree-like graph with n-1 separate paths.

        This method ONLY displays results after algorithm execution - no pre-run visualization.
        
        Layout concept (like a horizontal binary tree):
        - Source city on the LEFT side
        - N-1 horizontal lines emerge from source (one for each destination city)
        - Each line shows the complete shortest path from source to that destination
        - Each path is independent (nodes can be duplicated across paths)
        - Path nodes are arranged horizontally from left (source) to right (destination)
        - Each path has its own vertical slot/row for clarity
        
        Example with 4 cities (A, B, C, D) where A is source:
        
        Row 1:  A ─→ B ─→ C          [Path to C via B, distance shown]
        Row 2:  A ────────→ D         [Direct path to D]
        Row 3:  A ─→ B               [Path to B]
        
        Verification: Sum of edge weights along each path is compared to reported distance.
        """
        self.ax.clear()
        self.txt_output.tag_config("warn", foreground="red")

        # Only draw graph after algorithm has been run
        if not (highlight_source and shortest_distances):
            self.ax.text(0.5, 0.5, 'Run algorithm to see shortest path visualization', 
                        ha='center', va='center', fontsize=12, color='#7f8c8d', style='italic')
            self.ax.set_xlim(0, 1); self.ax.set_ylim(0, 1); self.ax.axis('off'); self.canvas.draw(); return

        # Build a dictionary of all directed edges present in the matrix: (u,v)->weight
        all_edges = {}
        for i in range(self.city_count):
            for j in range(self.city_count):
                val = self.city_entries[i][j].get().strip().upper()
                if val and val != "INF":
                    try:
                        w = int(val)
                    except ValueError:
                        continue
                    if not (i == j and w == 0):
                        all_edges[(self.city_names[i], self.city_names[j])] = w

        source = highlight_source

        # Get n-1 destinations (excluding source) - each gets its own horizontal path/row
        destinations = [c for c in self.city_names if c != source]
        n_dest = len(destinations)
        y_spacing = 1.8  # vertical spacing between path rows
        
        # We'll create completely separate paths for each destination
        # Using a custom graph to draw each path independently
        all_paths = []  # List of (destination, path_nodes, path_edges, y_position)
        verification_messages = []

        for idx, dest in enumerate(destinations):
            # Calculate y-position for this path (centered around 0)
            y_pos = (idx - (n_dest - 1) / 2) * y_spacing
            
            dest_dist = shortest_distances.get(dest, float('inf'))
            
            # If destination unreachable, create a simple unreachable marker
            if dest_dist == float('inf'):
                all_paths.append((dest, [source, dest], [], y_pos, dest_dist))
                continue

            # Reconstruct shortest path by backtracking from destination
            path = [dest]
            current = dest
            safe_break = 0
            while current != source and safe_break < (self.city_count * 2):
                safe_break += 1
                found = False
                for p in self.city_names:
                    if p == current: continue
                    if (p, current) in all_edges:
                        w = all_edges[(p, current)]
                        p_dist = shortest_distances.get(p, float('inf'))
                        cur_dist = shortest_distances[current]
                        if p_dist != float('inf') and p_dist + w == cur_dist:
                            path.insert(0, p)
                            current = p
                            found = True
                            break
                if not found:
                    break

            # Verify path starts from source
            if path[0] != source:
                # Path reconstruction failed
                all_paths.append((dest, [source, dest], [], y_pos, dest_dist))
                continue

            # Build edges for this path
            path_edges = [(path[i], path[i+1], all_edges.get((path[i], path[i+1]), 0)) 
                         for i in range(len(path) - 1)]

            # Verification: sum edge weights
            sum_w = sum(w for _, _, w in path_edges)
            if sum_w != dest_dist:
                verification_messages.append(
                    f"⚠ Path to {dest}: sum={sum_w} vs reported={dest_dist}")

            all_paths.append((dest, path, path_edges, y_pos, dest_dist))

        # Now draw all paths
        # Create NetworkX graph for drawing (we'll add nodes/edges for each path)
        G = nx.DiGraph()
        pos = {}
        node_info = {}  # Track node appearances: node_key -> (city_name, distance, is_source, is_dest, is_reachable)
        edge_list = []
        edge_labels_dict = {}

        # Add source node ONCE (shared by all paths)
        source_key = f"{source}_SOURCE"
        pos[source_key] = (0.0, 0.0)  # Center vertically at y=0
        node_info[source_key] = (source, 0, True, False, True)
        G.add_node(source_key)

        for dest, path_nodes, path_edges, y_pos, dest_dist in all_paths:
            is_reachable = dest_dist != float('inf')
            path_len = len(path_nodes)
            
            # Skip the source node (already added) and position remaining nodes
            for i, node_name in enumerate(path_nodes):
                if i == 0:  # This is the source node
                    continue  # Skip, already added
                
                # Create unique node key for this path: "CityName_rowIndex"
                node_key = f"{node_name}_{dest}"
                
                # Calculate x position (spread from 2 to 10, leaving gap after source at 0)
                remaining_nodes = path_len - 1  # Exclude source
                if remaining_nodes == 1:
                    x_pos = 10.0
                else:
                    # Position intermediate and destination nodes
                    x_pos = 2.0 + (8.0 * (i - 1)) / (remaining_nodes - 1)
                
                pos[node_key] = (x_pos, y_pos)
                
                # Track node information
                is_destination = (node_name == dest)
                node_distance = shortest_distances.get(node_name, float('inf'))
                
                node_info[node_key] = (node_name, node_distance, False, is_destination, is_reachable)
                G.add_node(node_key)
            
            # Add edges for this path
            for i in range(len(path_nodes) - 1):
                # First edge is from the shared source to first intermediate/destination
                if i == 0:
                    src_key = source_key  # Use the shared source
                else:
                    src_key = f"{path_nodes[i]}_{dest}"
                
                dst_key = f"{path_nodes[i+1]}_{dest}"
                weight = path_edges[i][2] if i < len(path_edges) else 0
                
                G.add_edge(src_key, dst_key)
                edge_list.append((src_key, dst_key))
                edge_labels_dict[(src_key, dst_key)] = f"[{weight}]" if is_reachable else ""

        # Draw all edges (all are part of shortest paths in this design)
        reachable_edges = [(u, v) for (u, v) in edge_list 
                          if node_info.get(v, (None, None, None, None, False))[4]]
        unreachable_edges = [(u, v) for (u, v) in edge_list 
                            if not node_info.get(v, (None, None, None, None, False))[4]]
        
        # Draw reachable path edges (green, prominent)
        if reachable_edges:
            nx.draw_networkx_edges(G, pos, edgelist=reachable_edges, edge_color='#00AA00',
                                  arrows=True, arrowsize=20, ax=self.ax, alpha=0.9, width=3,
                                  arrowstyle='->', connectionstyle='arc3,rad=0')
        
        # Draw unreachable path edges (gray, dashed)
        if unreachable_edges:
            nx.draw_networkx_edges(G, pos, edgelist=unreachable_edges, edge_color='#CCCCCC',
                                  arrows=True, arrowsize=15, ax=self.ax, alpha=0.4, width=1.5,
                                  style='dashed', arrowstyle='->', connectionstyle='arc3,rad=0')

        # Draw nodes with appropriate colors
        node_colors = []
        node_edge_colors = []
        for node_key in G.nodes():
            city_name, node_dist, is_source, is_dest, is_reachable = node_info[node_key]
            
            if is_source:
                node_colors.append('#FF4444')  # Red for source
                node_edge_colors.append('#CC0000')
            elif is_dest and is_reachable:
                node_colors.append('#44FF44')  # Green for reachable destinations
                node_edge_colors.append('#00AA00')
            elif is_dest and not is_reachable:
                node_colors.append('#4488FF')  # Blue for unreachable
                node_edge_colors.append('#0066CC')
            elif is_reachable:
                node_colors.append('#90EE90')  # Light green for intermediate nodes
                node_edge_colors.append('#00AA00')
            else:
                node_colors.append('#CCCCCC')  # Gray for unreachable intermediates
                node_edge_colors.append('#999999')

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000, 
                              edgecolors=node_edge_colors, linewidths=2.5, ax=self.ax, alpha=0.95)

        # Draw node labels showing city name and distance
        labels = {}
        for node_key in G.nodes():
            city_name, node_dist, is_source, is_dest, is_reachable = node_info[node_key]
            dtext = '∞' if node_dist == float('inf') else str(int(node_dist))
            labels[node_key] = f"{city_name}\n({dtext})"
        
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=9, font_weight='bold', 
                               font_family='sans-serif', ax=self.ax)

        # Draw edge weight labels
        if edge_labels_dict:
            # Only show labels for reachable paths
            reachable_labels = {k: v for k, v in edge_labels_dict.items() if v and k in reachable_edges}
            if reachable_labels:
                nx.draw_networkx_edge_labels(G, pos, reachable_labels, font_size=9, 
                                            font_color='#006400', font_weight='bold', ax=self.ax, 
                                            bbox=dict(boxstyle='round,pad=0.4', facecolor='#E8F8E8', 
                                            edgecolor='#00AA00', alpha=0.9, linewidth=1.5))

        # Legend - positioned outside the plot area to avoid overlap
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF4444', 
                      markersize=10, label='Source City', markeredgewidth=1.5, markeredgecolor='#CC0000'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#44FF44', 
                      markersize=10, label='Destination (Reachable)', markeredgewidth=1.5, markeredgecolor='#00AA00'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#90EE90', 
                      markersize=10, label='Intermediate Node', markeredgewidth=1.5, markeredgecolor='#00AA00'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4488FF', 
                      markersize=10, label='Unreachable', markeredgewidth=1.5, markeredgecolor='#0066CC'),
            plt.Line2D([0], [0], color='#00AA00', linewidth=2.5, label='Path Edge')
        ]
        
        # Position legend outside the plot area (below the graph)
        self.ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.02),
                      ncol=3, frameon=True, fancybox=True, shadow=True, fontsize=9,
                      framealpha=0.95, edgecolor='#34495e', facecolor='white')

        # Add informative title with statistics
        reachable_count = sum(1 for d in shortest_distances.values() if d != float('inf')) - 1  # Exclude source
        total_cities = len(self.city_names) - 1  # Exclude source
        title_text = f"Horizontal Tree: Shortest Paths from {source}\n"
        title_text += f"{n_dest} paths shown | Reachable: {reachable_count}/{total_cities} cities"
        self.ax.set_title(title_text, fontsize=12, fontweight='bold', pad=15, color='#2c3e50')

        # If verification messages exist, print them to the results pane in red
        if verification_messages:
            self.txt_output.insert(tk.END, "\n", "warn")
            for msg in verification_messages:
                self.txt_output.insert(tk.END, msg + "\n", "warn")

        # Adjust plot margins to accommodate legend at bottom
        self.ax.margins(0.15)
        self.ax.axis('off')
        self.fig.tight_layout()
        self.canvas.draw()

    def randomize_matrix(self):
        """Fill the matrix with random distances for quick testing"""
        for i in range(self.city_count):
            for j in range(self.city_count):
                if i != j:  # Skip diagonal (read-only)
                    self.city_entries[i][j].delete(0, tk.END)
                    self.city_entries[i][j].insert(0, str(random.randint(1, 50)))
        # Don't draw graph yet - only after running algorithm
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, "Random distances generated. Select source city and run algorithm.\n")

    def run_algorithm(self):
        """Main function to run the Bellman-Ford algorithm using C backend"""
        if not self.city_names:
            messagebox.showerror("Error", "Create city matrix first"); return

        # Build list of edges from the matrix
        edges = []
        for i in range(self.city_count):
            for j in range(self.city_count):
                val = self.city_entries[i][j].get().strip().upper()
                if val and val not in ["", "INF", "0"]:
                    try: edges.append(f"{self.city_names[i]} {self.city_names[j]} {int(val)}")
                    except ValueError: continue

        if not edges:
            messagebox.showerror("Error", "No valid distances"); return

        # Prepare input data in the format C program expects
        src_city = self.source_var.get()
        V, E = self.city_count, len(edges)
        data = f"{V} {E}\n" + "\n".join(self.city_names) + "\n" + "\n".join(edges) + "\n" + src_city + "\n"

        try:
            # Run the C program using subprocess - THIS IS WHERE ALGORITHM RUNS
            result = subprocess.run(["./bellman_backend.exe"], input=data, text=True, capture_output=True)
            self.txt_output.delete("1.0", tk.END); self.txt_output.insert(tk.END, result.stdout)  # Display C output
            self.parse_and_visualize_results(result.stdout, src_city)  # Parse and visualize
        except FileNotFoundError:
            messagebox.showerror("Error", "Compile C program: gcc bellman_backend.c -o bellman_backend.exe")

    def parse_and_visualize_results(self, output, source_city):
        """Parse the C program output and update graph with results"""
        shortest_distances = {}
        lines = [ln for ln in output.strip().split('\n') if ln.strip()]
        parsing = False
        for line in lines:
            if 'Source City:' in line:
                # next lines include table heading; start parsing after the next '----' line
                parsing = False
                continue
            if '------------------------------------' in line:
                parsing = not parsing
                continue
            if parsing and line.strip():
                parts = line.split()
                if len(parts) >= 2 and parts[0] in self.city_names:
                    city, dist_str = parts[0], parts[1]
                    shortest_distances[city] = float('inf') if dist_str == 'INF' else int(dist_str) if dist_str.lstrip('-').isdigit() else None

        # As a fallback if parsing failed to capture the distances (some C outputs vary), try a simple extraction
        if not shortest_distances:
            for n in self.city_names:
                # try to find a line like: "A              0"
                for line in lines:
                    if line.strip().startswith(n + ' '):
                        parts = line.split()
                        if len(parts) >= 2 and parts[0] == n:
                            d = parts[1]
                            shortest_distances[n] = float('inf') if d == 'INF' else int(d) if d.lstrip('-').isdigit() else None

        # ensure source included
        if source_city not in shortest_distances:
            shortest_distances[source_city] = 0

        self.graph_data = True; self.draw_graph(highlight_source=source_city, shortest_distances=shortest_distances)

# Main program starts here
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = BellmanFordGUI(root)  # Create our GUI application
    root.mainloop()  # Start the GUI event loop