package main

import (
	"fmt"
	"math/rand"
	"strings"
	"time"
)

type Direction struct {
	dr int
	dc int
}

var directions = []Direction{
	{0, 1},   // right
	{1, 0},   // down
	{1, 1},   // down-right
	{-1, 1},  // up-right
}

func makeGrid(size int) [][]rune {
	grid := make([][]rune, size)
	for i := range grid {
		grid[i] = make([]rune, size)
		for j := range grid[i] {
			grid[i][j] = '.'
		}
	}
	return grid
}

func canPlace(grid [][]rune, word string, row, col int, dir Direction) bool {
	size := len(grid)
	for _, ch := range word {
		if row < 0 || row >= size || col < 0 || col >= size {
			return false
		}
		if grid[row][col] != '.' && grid[row][col] != ch {
			return false
		}
		row += dir.dr
		col += dir.dc
	}
	return true
}

func placeWord(grid [][]rune, word string, row, col int, dir Direction) {
	for _, ch := range word {
		grid[row][col] = ch
		row += dir.dr
		col += dir.dc
	}
}

func tryPlaceWord(grid [][]rune, word string, rng *rand.Rand) bool {
	size := len(grid)
	for attempts := 0; attempts < 200; attempts++ {
		row := rng.Intn(size)
		col := rng.Intn(size)
		dir := directions[rng.Intn(len(directions))]
		if canPlace(grid, word, row, col, dir) {
			placeWord(grid, word, row, col, dir)
			return true
		}
	}
	return false
}

func fillEmpty(grid [][]rune, rng *rand.Rand) {
	for r := range grid {
		for c := range grid[r] {
			if grid[r][c] == '.' {
				grid[r][c] = rune('A' + rng.Intn(26))
			}
		}
	}
}

func printGrid(grid [][]rune) {
	for _, row := range grid {
		for _, ch := range row {
			fmt.Printf("%c ", ch)
		}
		fmt.Println()
	}
}

func main() {
	rng := rand.New(rand.NewSource(time.Now().UnixNano()))
	words := []string{"SPRITE", "PUZZLE", "QUEST", "CODING", "LEARN", "PIXEL"}
	size := 12

	grid := makeGrid(size)

	fmt.Println("Word Search Generator")
	fmt.Println("---------------------")

	for _, word := range words {
		upper := strings.ToUpper(word)
		ok := tryPlaceWord(grid, upper, rng)
		if !ok {
			fmt.Printf("Could not place word: %s\n", upper)
		}
	}

	fillEmpty(grid, rng)
	printGrid(grid)

	fmt.Println("\nFind these words:")
	for _, word := range words {
		fmt.Println("-", strings.ToUpper(word))
	}
}
