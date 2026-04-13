import java.util.Random;
import java.util.Scanner;

public class AlgebraSpellDuel {
    private static final Random RANDOM = new Random();

    private static int askInt(Scanner scanner, String prompt) {
        while (true) {
            System.out.print(prompt);
            if (scanner.hasNextInt()) {
                return scanner.nextInt();
            }
            System.out.println("Invalid input. Please enter an integer.");
            scanner.next();
        }
    }

    private static int[] makeEquation() {
        int x = RANDOM.nextInt(11) - 5;
        int a;
        do {
            a = RANDOM.nextInt(9) - 4;
        } while (a == 0);
        int b = RANDOM.nextInt(11) - 5;
        int c = a * x + b;
        return new int[] {a, b, c, x};
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int playerHp = 30;
        int rivalHp = 30;

        System.out.println("=== Algebra Spell Duel ===");
        System.out.println("Solve linear equations to cast spells.\n");

        for (int round = 1; round <= 8 && playerHp > 0 && rivalHp > 0; round++) {
            int[] eq = makeEquation();
            int a = eq[0], b = eq[1], c = eq[2], solution = eq[3];

            System.out.println("Round " + round + " | Your HP: " + playerHp + " | Rival HP: " + rivalHp);
            System.out.println("Solve for x: " + a + "x " + (b >= 0 ? "+ " : "- ") + Math.abs(b) + " = " + c);
            int answer = askInt(scanner, "x = ");

            if (answer == solution) {
                int damage = 6 + RANDOM.nextInt(5);
                rivalHp -= damage;
                System.out.println("Direct hit. You deal " + damage + " damage.\n");
            } else {
                int damage = 4 + RANDOM.nextInt(4);
                playerHp -= damage;
                System.out.println("Spell misfire. Correct answer was " + solution + ". Rival deals " + damage + " damage.\n");
            }
        }

        if (playerHp > rivalHp) {
            System.out.println("Victory. Your algebra held under pressure.");
        } else if (rivalHp > playerHp) {
            System.out.println("Defeat. Review isolating x and try again.");
        } else {
            System.out.println("Draw. Both mages are evenly matched.");
        }
        scanner.close();
    }
}
