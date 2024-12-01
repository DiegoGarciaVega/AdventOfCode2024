package main

import (
	"fmt"
	"os"
)

func ReadFile() string {
	fmt.Println("Reading file")
	fileName := "../input.txt"
	data, err := os.ReadFile(fileName)
	if err != nil {
		panic(err)
	}

	fmt.Println("File name " + fileName)
	fmt.Printf("File size %d\n", len(data))
	// fmt.Printf("file content : %s\n", data)

	return string(data)
}

func main() {
	data := ReadFile()
	fmt.Println(data)

	for i, val := range data {
		fmt.Printf("Line %d, Text: %v\n", i, val)
	}
}
