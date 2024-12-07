#include <iostream>
#include <vector>
#include <set>
#include <fstream>
#include <string>
#include <tuple>
#include <chrono>
#include <thread>
#include <unordered_set>

using namespace std;

// Direction vectors for movements: UP, RIGHT, DOWN, LEFT
const vector<pair<int, int>> rotations = {
    {-1, 0},  // UP
    {0, 1},   // RIGHT
    {1, 0},   // DOWN
    {0, -1}   // LEFT
};

void prettyPrint(const vector<vector<char>> &grid) {
    const string RESET = "\033[0m";
    const string BLUE = "\033[34m";
    for (const auto &row : grid) {
        for (char c : row) {
            if (c == 'X') {
                cout << BLUE << c << RESET;
            } else {
                cout << c;
            }
        }
        cout << endl;
    }
    this_thread::sleep_for(chrono::milliseconds(100));
    cout << "\033[2J\033[H"; // Clear screen and move cursor to top-left
}


bool traverse(vector<vector<char>> &grid, int x, int y, int obsX, int obsY, int rotationID) {
    int rows = grid.size();
    int cols = grid[0].size();
    set<tuple<int, int, int>> seen;

    // Place obstacle
    grid[obsX][obsY] = '#';

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

        if (grid[nextX][nextY] == '#') {
            rotationID = (rotationID + 1) % 4; // Rotate clockwise
        } else {
            x = nextX;
            y = nextY;
        }
    }
}
// bool traverse(vector<vector<char>> &grid, int x, int y, int obsX, int obsY, int rotationID) {
//     int rows = grid.size();
//     int cols = grid[0].size();
//     set<tuple<int, int, int>> seen;
//     int TTL = 130 * 130; // Arbitrary loop prevention limit

//     // Place obstacle
//     grid[obsX][obsY] = '#';

//     while (TTL-- > 0) {
//         auto state = make_tuple(x, y, rotationID);
//         if (seen.find(state) != seen.end()) {
//             return true; // Loop detected
//         }
//         seen.insert(state);

//         int nextX = x + rotations[rotationID].first;
//         int nextY = y + rotations[rotationID].second;

//         if (nextX < 0 || nextX >= rows || nextY < 0 || nextY >= cols) {
//             return false; // Out of bounds
//         }

//         if (grid[nextX][nextY] == '#') {
//             rotationID = (rotationID + 1) % 4; // Rotate clockwise
//         } else {
//             x = nextX;
//             y = nextY;
//         }
//     }

//     return false; // Timeout
// }

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

    // Part One: Simulate guard route
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

    // Part Two: Find valid obstruction positions
    int valid_positions = 0;

    for (const auto &pos : visited_positions) {
        int obsX = pos.first;
        int obsY = pos.second;
        if ((obsX == startX && obsY == startY) || grid[obsX][obsY] == '#') {
            continue; // Skip starting position or existing walls
        }

        vector<vector<char>> temp_grid = grid; // Copy grid
        if (traverse(temp_grid, startX, startY, obsX, obsY, 0)) {
            ++valid_positions;
        }
    }

    // Final Results
    int visited_count = visited_positions.size();

    cout << string(50, '#') << endl;
    cout << "Advent of Code 2024\n\t- Day 06" << endl;
    cout << "\t\t★  Result: " << visited_count << endl;
    cout << "\t\t★★ Result: " << valid_positions << endl;
    cout << string(50, '#') << endl;

    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end_time - start_time;
    cout << "Execution Time: " << elapsed.count() << " seconds" << endl;

    return 0;
}
