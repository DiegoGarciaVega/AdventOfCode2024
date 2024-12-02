const fs = require('node:fs');

fs.readFile('../input.txt', 'utf8', (err, data) => {
    if (err) {
        console.error("Error reading the file:", err);
        return;
    }

    const splitted = data.split("\n").filter(line => line.trim() !== ""); // Ensure no empty lines
    let leftList = [];
    let rightList = [];

    splitted.forEach(element => {
        const aux = element.split("   "); // Adjust delimiter if needed
        if (aux.length >= 2) { // Ensure there are at least two parts
            leftList.push(parseFloat(aux[0])); // Convert to number
            rightList.push(parseFloat(aux[1])); // Convert to number
        }
    });

    leftList.sort((a, b) => a - b); // Numeric sort
    rightList.sort((a, b) => a - b); // Numeric sort

    let sum = 0;
    let similarityScore = 0;

    for (let i = 0; i < leftList.length; i++) {
        // Use leftList[i] as the left element
        const leftElement = leftList[i];
        
        // Count occurrences of leftElement in rightList
        const frequency = rightList.filter(item => item === leftElement).length;
        
        // Add to similarity score
        similarityScore += frequency * leftElement;

        // Calculate sum (existing logic)
        if (i < rightList.length) {
            sum += Math.abs(leftElement - rightList[i]);
        }
    }

    console.log("#".repeat(50));
    console.log("Advent of Code 2024");
    console.log("\t- Day 01\n\t\t★  Result: " + sum + "\n\t\t★★ Result: " + similarityScore);
    console.log("#".repeat(50));
});
