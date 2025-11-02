#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
#include <limits.h>

// Define max limits for our arrays
#define MAX 50        // Maximum number of cities we can handle
#define NAME_LEN 30   // Maximum length for a city name

// Structure to store an edge (road)
// Each edge represents a road from one city to another with a distance
struct Edge {
    int src, dest, weight;  // source city index, destination city index, and distance
};

// Structure to represent the graph
// A graph is basically all the cities and roads connecting them
struct Graph {
    int V, E;              // V = number of vertices (cities), E = number of edges (roads)
    struct Edge* edge;     // Pointer to array of edges (dynamically allocated)
};

// Global memoization table for caching shortest paths
// This stores previously calculated results so we don't recalculate
int memo[MAX][MAX];  

// Initialize memo table with INT_MAX (means uncomputed/infinite)
void initializeMemo(int V) {
    // Loop through all possible source and destination combinations
    for (int i = 0; i < V; i++)
        for (int j = 0; j < V; j++)
            memo[i][j] = INT_MAX;  // Set to infinity initially
}

// Create a new graph dynamically
// We allocate memory based on how many cities and roads we have
struct Graph* createGraph(int V, int E) {
    // Allocate memory for the graph structure itself
    struct Graph* graph = (struct Graph*) malloc(sizeof(struct Graph));
    graph->V = V;  // Store number of vertices (cities)
    graph->E = E;  // Store number of edges (roads)
    
    // Allocate memory for all the edges
    graph->edge = (struct Edge*) malloc(E * sizeof(struct Edge));
    return graph;
}

// Print all distances from the given source city
void printDistances(int src, int dist[], char cityNames[][NAME_LEN], int V) {
    printf("Source City: %s\n", cityNames[src]);
    printf("------------------------------------\n");
    printf("%-15s Distance\n", "City");  // %-15s means left-align with 15 characters
    printf("------------------------------------\n");

    // Print distance to each city
    for (int i = 0; i < V; i++) {
        if (dist[i] == INT_MAX)
            printf("%-15s INF\n", cityNames[i]);  // INF means unreachable
        else
            printf("%-15s %d\n", cityNames[i], dist[i]);  // Print actual distance
    }
}

// Bellman-Ford algorithm with memoization
// This finds the shortest path from source city to all other cities
void BellmanFord(struct Graph* graph, int src, char cityNames[][NAME_LEN]) {
    int V = graph->V;  // Number of cities
    int E = graph->E;  // Number of roads
    int dist[V];       // Array to store shortest distances

    // Check if results are already computed (memoization optimization)
    // If we already calculated shortest paths from this source, use cached results
    int memoized = 1;
    for (int i = 0; i < V; i++) {
        if (memo[src][i] == INT_MAX) {
            memoized = 0;  // Not cached yet
            break;
        }
    }

    // If we found cached results, just print them and return
    if (memoized) {
        printf("Using cached results for %s\n\n", cityNames[src]);
        printDistances(src, memo[src], cityNames, V);
        return;
    }

    // Step 1: Initialize distances from source to all vertices as infinite
    for (int i = 0; i < V; i++)
        dist[i] = INT_MAX;
    dist[src] = 0;  // Distance from source to itself is 0

    // Step 2: Relax all edges |V| - 1 times
    // This is the core of Bellman-Ford algorithm
    for (int i = 1; i <= V - 1; i++) {
        for (int j = 0; j < E; j++) {
            int u = graph->edge[j].src;      // Source city of this edge
            int v = graph->edge[j].dest;     // Destination city of this edge
            int w = graph->edge[j].weight;   // Distance of this road
            
            // If we found a shorter path to v through u, update it
            if (dist[u] != INT_MAX && dist[u] + w < dist[v])
                dist[v] = dist[u] + w;
        }
    }

    // Step 3: Check for negative weight cycles
    // If we can still relax an edge, there's a negative cycle
    for (int j = 0; j < E; j++) {
        int u = graph->edge[j].src;
        int v = graph->edge[j].dest;
        int w = graph->edge[j].weight;
        if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
            printf("Error: Graph contains a negative weight cycle!\n");
            return;
        }
    }

    // Store results in memo table for future use
    for (int i = 0; i < V; i++)
        memo[src][i] = dist[i];

    // Display results
    printDistances(src, dist, cityNames, V);
}

// Find index of a city by name
// Returns the index if found, -1 if not found
int findCityIndex(char cityNames[][NAME_LEN], int count, char name[]) {
    for (int i = 0; i < count; i++)
        if (strcmp(cityNames[i], name) == 0)  // strcmp returns 0 if strings match
            return i;
    return -1;  // City not found
}

int main() {
    int V, E;
    // Read number of vertices (cities) and edges (roads)
    scanf("%d %d", &V, &E);

    // Create the graph structure
    struct Graph* graph = createGraph(V, E);
    char cityNames[MAX][NAME_LEN];  // Array to store all city names

    // Read city names
    for (int i = 0; i < V; i++)
        scanf("%s", cityNames[i]);

    // Read all the roads (edges)
    for (int i = 0; i < E; i++) {
        char srcName[NAME_LEN], destName[NAME_LEN];
        int dist;
        scanf("%s %s %d", srcName, destName, &dist);  // Read: from_city to_city distance
        
        // Convert city names to indices
        int src = findCityIndex(cityNames, V, srcName);
        int dest = findCityIndex(cityNames, V, destName);
        
        // Store this edge in our graph
        graph->edge[i].src = src;
        graph->edge[i].dest = dest;
        graph->edge[i].weight = dist;
    }

    // Initialize the memoization table
    initializeMemo(V);

    // Read the source city name
    char srcCity[NAME_LEN];
    scanf("%s", srcCity);

    // Find the index of source city
    int srcIndex = findCityIndex(cityNames, V, srcCity);
    if (srcIndex == -1) {
        printf("Invalid source city.\n");
        return 0;
    }

    // Run Bellman-Ford algorithm
    BellmanFord(graph, srcIndex, cityNames);
    return 0;
}
