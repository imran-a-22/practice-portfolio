package main

import (
    "bufio"
    "fmt"
    "math/rand"
    "os"
    "sort"
    "strconv"
    "strings"
    "time"
)

type Event struct {
    Name string
    Year int
}

var events = []Event{
    {"Magna Carta signed", 1215},
    {"Printing press spreads in Europe", 1450},
    {"Columbus reaches the Americas", 1492},
    {"French Revolution begins", 1789},
    {"Telephone patented", 1876},
    {"First powered flight", 1903},
    {"World Wide Web proposed", 1989},
}

func askOrder(reader *bufio.Reader) []int {
    for {
        fmt.Print("Enter order as three numbers from oldest to newest: ")
        line, _ := reader.ReadString('\n')
        fields := strings.Fields(line)
        if len(fields) != 3 {
            fmt.Println("Please enter exactly three numbers.")
            continue
        }
        seen := map[int]bool{}
        result := make([]int, 0, 3)
        ok := true
        for _, field := range fields {
            value, err := strconv.Atoi(field)
            if err != nil || value < 1 || value > 3 || seen[value] {
                ok = false
                break
            }
            seen[value] = true
            result = append(result, value)
        }
        if ok {
            return result
        }
        fmt.Println("Invalid order.")
    }
}

func main() {
    rand.Seed(time.Now().UnixNano())
    reader := bufio.NewReader(os.Stdin)
    score := 0

    fmt.Println("=== Timeline Tactician ===")
    fmt.Println("Place events in the correct chronological order.\n")

    for mission := 1; mission <= 5; mission++ {
        picks := rand.Perm(len(events))[:3]
        chosen := []Event{events[picks[0]], events[picks[1]], events[picks[2]]}
        fmt.Printf("Mission %d\n", mission)
        for i, event := range chosen {
            fmt.Printf("%d. %s\n", i+1, event.Name)
        }
        answer := askOrder(reader)
        sorted := make([]Event, len(chosen))
        copy(sorted, chosen)
        sort.Slice(sorted, func(i, j int) bool { return sorted[i].Year < sorted[j].Year })

        correct := true
        for i, pick := range answer {
            if chosen[pick-1].Year != sorted[i].Year {
                correct = false
                break
            }
        }

        if correct {
            score += 20
            fmt.Println("Correct.\n")
        } else {
            fmt.Println("Not quite. Correct order:")
            for _, event := range sorted {
                fmt.Printf("- %s (%d)\n", event.Name, event.Year)
            }
            fmt.Println()
        }
    }
    fmt.Printf("Final score: %d / 100\n", score)
}
