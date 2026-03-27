/*
GradeCalculator (Java)
A simple weighted grade calculator for students.

Compile:
    javac GradeCalculator.java
Run:
    java GradeCalculator
*/

import java.util.Scanner;

public class GradeCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Grade Calculator");
        System.out.println("Enter three category scores and their weights.");

        double homeworkScore = readDouble(scanner, "Homework score (0-100): ");
        double homeworkWeight = readDouble(scanner, "Homework weight %: ");

        double testScore = readDouble(scanner, "Test score (0-100): ");
        double testWeight = readDouble(scanner, "Test weight %: ");

        double projectScore = readDouble(scanner, "Project score (0-100): ");
        double projectWeight = readDouble(scanner, "Project weight %: ");

        double totalWeight = homeworkWeight + testWeight + projectWeight;
        if (Math.abs(totalWeight - 100.0) > 0.001) {
            System.out.println("Error: the weights must add up to 100.");
            scanner.close();
            return;
        }

        double finalGrade =
            (homeworkScore * homeworkWeight / 100.0) +
            (testScore * testWeight / 100.0) +
            (projectScore * projectWeight / 100.0);

        System.out.printf("\nFinal grade: %.2f%%\n", finalGrade);
        System.out.println("Letter grade: " + toLetterGrade(finalGrade));

        scanner.close();
    }

    private static double readDouble(Scanner scanner, String prompt) {
        while (true) {
            System.out.print(prompt);
            if (scanner.hasNextDouble()) {
                double value = scanner.nextDouble();
                if (value >= 0) {
                    return value;
                }
            } else {
                scanner.next();
            }
            System.out.println("Please enter a valid non-negative number.");
        }
    }

    private static String toLetterGrade(double grade) {
        if (grade >= 90) return "A";
        if (grade >= 80) return "B";
        if (grade >= 70) return "C";
        if (grade >= 60) return "D";
        return "F";
    }
}
