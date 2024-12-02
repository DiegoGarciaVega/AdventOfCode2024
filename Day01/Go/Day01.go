package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	// Open the file
	fileName := "../input.txt"
	file, err := os.Open(fileName)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	var leftList, rightList []int

	// Read the file line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.Fields(scanner.Text()) // Split the line into fields
		if len(line) >= 2 {                    // Ensure there are at least 2 elements
			leftVal, err1 := strconv.Atoi(line[0])
			rightVal, err2 := strconv.Atoi(line[1])
			if err1 == nil && err2 == nil { // Add to respective lists if parsing is successful
				leftList = append(leftList, leftVal)
				rightList = append(rightList, rightVal)
			} else {
				fmt.Println("Error parsing line:", line)
			}
		}
	}

	if err := scanner.Err(); err != nil {
		panic(err)
	}

	// Sort the lists
	sort.Ints(leftList)
	sort.Ints(rightList)

	// Calculate total distance
	totalDistance := 0
	similarityScore := 0
	for i := 0; i < len(leftList) && i < len(rightList); i++ {
		totalDistance += abs(leftList[i] - rightList[i])
		similarityScore += leftList[i] * freq(leftList[i], rightList)
	}

	// Print result
	fmt.Println(strings.Repeat("#", 50))
	fmt.Printf("Advent of Code 2024\n\t- Day 01\n\t\t★  Result: %d\n\t\t★★ Result: %d\n", totalDistance, similarityScore)
	fmt.Println(strings.Repeat("#", 50))
}

// Helper function to compute absolute value
func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

// Helper function to compute frequency of elements
func freq(element int, data []int) int {
	counter := 0
	for _, val := range data {
		if val == element {
			counter += 1
		}
	}
	return counter
}
