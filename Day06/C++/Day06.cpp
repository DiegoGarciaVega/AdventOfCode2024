#include <iostream>
#include <vector>
#include <set>
#include <fstream>
#include <string>
#include <tuple>
#include <chrono>
#include <thread>
#include <unordered_set>
#include <omp.h>   // OpenMP header for parallelization
#include <atomic>  // For thread-safe counting

using namespace std;

// Direction vectors for movements: UP, RIGHT, DOWN, LEFT
const vector<pair<int, int>> rotations = {
    {-1, 0},  // UP
    {0, 1},   // RIGHT
    {1, 0},   // DOWN
    {0, -1}   // LEFT
};

// Function to print grid (removed colored output for simplicity)
void prettyPrint(const vector<vector<char>> &grid) {
    for (const auto &row : grid) {
        for (char c : row) {
            cout << c;
        }
        cout << endl;
    }
}

// Parallelized version of traverse function
bool traverse(const vector<vector<char>> &grid, int startX, int startY, int obsX, int obsY, int rotationID) {
    int rows = grid.size();
    int cols = grid[0].size();
    
    // Create a copy of the grid to modify
    vector<vector<char>> workGrid = grid;
    workGrid[obsX][obsY] = '#';
    
    set<tuple<int, int, int>> seen;
    int x = startX, y = startY;

    while (true) {
        auto state = make_tuple(x, y, rotationID);
        if (seen.find(state) != seen.end()) {
            return true; // Loop detected
        }
        seen.insert(state);

        int nextX = x + rotations[rotationID].first;
        int nextY = y + rotations[rotationID].second;

        if (nextX < 0 || nextX >= rows || nextY < 0 || nextY >= cols) {
            return false; // Out of bounds
        }

        if (workGrid[nextX][nextY] == '#') {
            rotationID = (rotationID + 1) % 4; // Rotate clockwise
        } else {
            x = nextX;
            y = nextY;
        }
    }
}

int main() {
    auto start_time = chrono::high_resolution_clock::now();

    // Read input from file
    ifstream infile("../input.txt");
    vector<string> file_lines;
    string line;

    while (getline(infile, line)) {
        file_lines.push_back(line);
    }

    int rows = file_lines.size();
    int cols = file_lines[0].size();
    vector<vector<char>> grid(rows, vector<char>(cols));
    int startX = 0, startY = 0;

    // Populate grid and find starting position
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            grid[i][j] = file_lines[i][j];
            if (grid[i][j] == '^') {
                startX = i;
                startY = j;
            }
        }
    }

    // Part One: Simulate guard route (same as original)
    int x = startX, y = startY, rotationID = 0;
    vector<pair<int, int>> obstacles;
    set<pair<int, int>> visited_positions;

    while (true) {
        grid[x][y] = 'X';
        visited_positions.insert({x, y});
        int nextX = x + rotations[rotationID].first;
        int nextY = y + rotations[rotationID].second;

        if (nextX < 0 || nextX >= rows || nextY < 0 || nextY >= cols) {
            break; // Out of bounds
        }

        if (grid[nextX][nextY] == '#') {
            rotationID = (rotationID + 1) % 4;
            obstacles.emplace_back(nextX, nextY);
            x = x + rotations[rotationID].first;
            y = y + rotations[rotationID].second;
        } else {
            x = nextX;
            y = nextY;
        }
    }

    // Part Two: Parallelize finding valid obstruction positions
    std::atomic<int> valid_positions(0);

    // Use OpenMP to parallelize the loop
    #pragma omp parallel
    {
        // Create thread-local grid to avoid race conditions
        vector<vector<char>> thread_grid = grid;

        // Distribute iterations across threads
        #pragma omp for
        for (int idx = 0; idx < visited_positions.size(); ++idx) {
            auto it = std::next(visited_positions.begin(), idx);
            int obsX = it->first;
            int obsY = it->second;

            // Skip starting position or existing walls
            if ((obsX == startX && obsY == startY) || thread_grid[obsX][obsY] == '#') {
                continue;
            }

            // Check if this position allows a valid traversal
            if (traverse(thread_grid, startX, startY, obsX, obsY, 0)) {
                valid_positions++;
            }
        }
    }

    // Final Results
    int visited_count = visited_positions.size();

    cout << string(50, '#') << endl;
    cout << "Advent of Code 2024\n\t- Day 06" << endl;
    cout << "\t\t★  Result: " << visited_count << endl;
    cout << "\t\t★★ Result: " << valid_positions.load() << endl;
    cout << string(50, '#') << endl;

    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end_time - start_time;
    cout << "Execution Time: " << elapsed.count() << " seconds" << endl;

    return 0;
}