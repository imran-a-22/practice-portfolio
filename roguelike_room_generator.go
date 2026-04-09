// roguelike_room_generator.go
//
// Generates an ASCII roguelike room with walls, doors, enemies, treasure, and traps.
// Run:
//   go run roguelike_room_generator.go

package main

import (
	"fmt"
	"math/rand"
	"time"
)

const (
	width  = 18
	height = 10
)

type Point struct {
	row int
	col int
}

func createEmptyRoom() [][]rune {
	room := make([][]rune, height)

	for r := 0; r < height; r++ {
		room[r] = make([]rune, width)
		for c := 0; c < width; c++ {
			if r == 0 || r == height-1 || c == 0 || c == width-1 {
				room[r][c] = '#'
			} else {
				room[r][c] = '.'
			}
		}
	}

	return room
}

func placeDoor(room [][]rune, p Point) {
	room[p.row][p.col] = 'D'
}

func randomInteriorPoint() Point {
	return Point{
		row: rand.Intn(height-2) + 1,
		col: rand.Intn(width-2) + 1,
	}
}

func placeUniqueObjects(room [][]rune, symbol rune, count int) {
	placed := 0
	for placed < count {
		p := randomInteriorPoint()
		if room[p.row][p.col] == '.' {
			room[p.row][p.col] = symbol
			placed++
		}
	}
}

func printRoom(room [][]rune) {
	fmt.Println("Legend: # wall | . floor | D door | E enemy | T treasure | X trap")
	fmt.Println()

	for _, row := range room {
		for _, cell := range row {
			fmt.Printf("%c ", cell)
		}
		fmt.Println()
	}
}

func countSymbol(room [][]rune, symbol rune) int {
	total := 0
	for _, row := range room {
		for _, cell := range row {
			if cell == symbol {
				total++
			}
		}
	}
	return total
}

func main() {
	rand.Seed(time.Now().UnixNano())

	room := createEmptyRoom()

	doors := []Point{
		{row: 0, col: width / 2},
		{row: height - 1, col: width / 2},
		{row: height / 2, col: 0},
		{row: height / 2, col: width - 1},
	}

	for _, door := range doors {
		placeDoor(room, door)
	}

	placeUniqueObjects(room, 'E', 4)
	placeUniqueObjects(room, 'T', 2)
	placeUniqueObjects(room, 'X', 3)

	printRoom(room)

	fmt.Println()
	fmt.Printf("Enemies: %d\n", countSymbol(room, 'E'))
	fmt.Printf("Treasure chests: %d\n", countSymbol(room, 'T'))
	fmt.Printf("Traps: %d\n", countSymbol(room, 'X'))
}
