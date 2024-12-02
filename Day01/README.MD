# 🌟 Day 1: Historian Hysteria 🌟

The Chief Historian is always present for the big Christmas sleigh launch, but nobody has seen him in months! Last anyone heard, he was visiting locations that are historically significant to the North Pole. A group of Senior Historians has asked you to accompany them as they check the places they think he was most likely to visit.

To save Christmas, you must **collect fifty stars** by solving puzzles before Santa takes off on December 25th. Two puzzles are available each day in the Advent calendar, and solving each grants one star. Good luck!

---

## 🕵️ Mystery in the Chief Historian's Office

The Historians' search begins at the Chief Historian's office, but they find only an assortment of notes and lists of **historically significant locations**. These locations are identified by **location IDs**. The problem? Two groups of Historians made their own lists from the notes, but the lists don't match.

Your task is to reconcile these two lists.

---

### 📏 Part One: Measuring the Distance

By comparing the two lists side by side, you can calculate the total "distance" between them:

1. Pair the smallest number from the left list with the smallest from the right, the second smallest with the second smallest, and so on.
2. For each pair, calculate the absolute difference (distance).
3. Sum these distances to get the total.

**Example:**

| Left List | Right List | Pair   | Distance |
|-----------|------------|--------|----------|
| 3         | 4          | 1 ↔ 3  | 2        |
| 4         | 3          | 2 ↔ 3  | 1        |
| 2         | 5          | 3 ↔ 3  | 0        |
| 1         | 3          | 3 ↔ 4  | 1        |
| 3         | 9          | 3 ↔ 5  | 2        |
| 3         | 3          | 4 ↔ 9  | 5        |

**Total Distance:**  
2 + 1 + 0 + 1 + 2 + 5 = **11**

For this input, the total distance is: **1223326**

---

### 🧮 Part Two: Calculating Similarity

The Historians notice that some location IDs appear in both lists, which might indicate mistakes in transcription. This time, calculate a **similarity score**:

1. For each number in the left list:
   - Multiply it by the number of times it appears in the right list.
2. Sum these values to get the similarity score.

**Example:**

| Left List | Right List | Count in Right | Contribution to Score |
|-----------|------------|----------------|------------------------|
| 3         | 4          | 3              | 3 × 3 = 9             |
| 4         | 3          | 1              | 4 × 1 = 4             |
| 2         | 5          | 0              | 2 × 0 = 0             |
| 1         | 3          | 0              | 1 × 0 = 0             |
| 3         | 9          | 3              | 3 × 3 = 9             |
| 3         | 3          | 3              | 3 × 3 = 9             |

**Similarity Score:**  
9 + 4 + 0 + 0 + 9 + 9 = **31**

For this input, the similarity score is: **21070419**

---

### ⭐ Outcome

Both parts of the puzzle are complete, earning **two gold stars**! 🎉  

