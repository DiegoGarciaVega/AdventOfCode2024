# 🌟 Day 2: Red-Nosed Reports 🌟

Fortunately, the first location The Historians want to search isn't far from the Chief Historian's office. At the **Red-Nosed Reindeer nuclear fusion/fission plant**, there’s no sign of the Chief Historian, but the engineers need your help analyzing some **unusual data**.

The data consists of reports, each containing several levels. A report is **safe** if:

1. Levels are either all **increasing** or all **decreasing**.
2. Any two adjacent levels differ by at least 1 and at most 3.

Your task is to determine how many reports are safe.

---

## 📏 Part One: Determining Safe Reports

Analyze each report to check if it meets the safety rules.

**Example Data:**

- **7 6 4 2 1**
- **1 2 7 8 9**
- **9 7 6 2 1**
- **1 3 2 4 5**
- **8 6 4 4 1**
- **1 3 6 7 9**


**Analysis:**

- **7 6 4 2 1**: Safe (all levels decreasing by 1 or 2).
- **1 2 7 8 9**: Unsafe (increase of 5 between 2 and 7).
- **9 7 6 2 1**: Unsafe (decrease of 4 between 6 and 2).
- **1 3 2 4 5**: Unsafe (1 → 3 is increasing, but 3 → 2 is decreasing).
- **8 6 4 4 1**: Unsafe (4 → 4 is neither an increase nor a decrease).
- **1 3 6 7 9**: Safe (all levels increasing by 1, 2, or 3).

**Result:**  
In this example, **2 reports are safe**.

For this input, the number of safe reports is: **230**

---

## 🛠️ Part Two: The Problem Dampener

The engineers introduce the **Problem Dampener**, a module that allows the reactor safety systems to ignore one "bad" level in a report. If removing a single level makes the report safe, the report is considered **safe**.

**Reanalysis of Example Data:**

- **7 6 4 2 1**: Safe (no change needed).
- **1 2 7 8 9**: Unsafe (no single removal fixes it).
- **9 7 6 2 1**: Unsafe (no single removal fixes it).
- **1 3 2 4 5**: Safe (removing **3** makes it increasing).
- **8 6 4 4 1**: Safe (removing the first **4** makes it decreasing).
- **1 3 6 7 9**: Safe (no change needed).

**Result:**  
In this example, **4 reports are safe**.

For this input, the number of safe reports with the Problem Dampener is: **301**

---

### ⭐ Outcome

Both parts of the puzzle are complete, earning **two gold stars**! 🎉  

---

