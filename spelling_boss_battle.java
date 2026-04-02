import java.util.*;

/**
 * spelling_boss_battle.java
 *
 * A simple ed-tech + gaming console program.
 * The player defeats enemies by spelling words correctly.
 *
 * Compile:
 *   javac spelling_boss_battle.java
 *
 * Run:
 *   java spelling_boss_battle
 */

public class spelling_boss_battle {

    static class WordChallenge {
        String clue;
        String answer;
        String hint;

        WordChallenge(String clue, String answer, String hint) {
            this.clue = clue;
            this.answer = answer;
            this.hint = hint;
        }
    }

    static class Player {
        String name;
        int hp = 30;
        int maxHp = 30;
        int score = 0;
        int potions = 2;

        Player(String name) {
            this.name = name;
        }

        void heal() {
            if (potions <= 0) {
                System.out.println("No potions left.");
                return;
            }
            potions--;
            hp = Math.min(maxHp, hp + 10);
            System.out.println("You used a potion. HP: " + hp + "/" + maxHp);
        }
    }

    static class Enemy {
        String name;
        int hp;
        int damage;

        Enemy(String name, int hp, int damage) {
            this.name = name;
            this.hp = hp;
            this.damage = damage;
        }
    }

    static final Scanner scanner = new Scanner(System.in);
    static final Random random = new Random();

    static final List<WordChallenge> WORDS = Arrays.asList(
        new WordChallenge("A place where books are kept", "library", "Starts with 'l'"),
        new WordChallenge("The number of days in a week", "seven", "Starts with 's'"),
        new WordChallenge("To learn how to do something", "practice", "Starts with 'p'"),
        new WordChallenge("A person who teaches students", "teacher", "Starts with 't'"),
        new WordChallenge("The opposite of difficult", "easy", "Starts with 'e'"),
        new WordChallenge("A strong wish to know something", "curiosity", "Starts with 'c'"),
        new WordChallenge("Words written in a book or article", "text", "Starts with 't'"),
        new WordChallenge("The planet we live on", "earth", "Starts with 'e'"),
        new WordChallenge("A short test of knowledge", "quiz", "Starts with 'q'"),
        new WordChallenge("The answer to a problem in maths", "solution", "Starts with 's'"),
        new WordChallenge("To speak clearly in front of people", "present", "Starts with 'p'"),
        new WordChallenge("The process of getting better through effort", "improvement", "Starts with 'i'")
    );

    static final String[] ENEMY_NAMES = {
        "Mistake Goblin",
        "Typo Slime",
        "Grammar Skeleton",
        "Dictionary Thief",
        "Boss of Blunders"
    };

    public static void main(String[] args) {
        System.out.println("=== SPELLING BOSS BATTLE ===");
        System.out.print("Enter your hero name: ");
        String name = scanner.nextLine().trim();
        if (name.isEmpty()) {
            name = "Scholar";
        }

        Player player = new Player(name);
        int round = 1;

        while (player.hp > 0) {
            Enemy enemy = createEnemy(round);
            System.out.println("\n--- Round " + round + " ---");
            System.out.println(enemy.name + " appears with " + enemy.hp + " HP.");

            boolean won = fightEnemy(player, enemy);
            if (!won) {
                break;
            }

            round++;
            if (round % 3 == 0) {
                player.hp = Math.min(player.maxHp, player.hp + 5);
                System.out.println("Rest bonus. HP restored to " + player.hp + "/" + player.maxHp);
            }
        }

        System.out.println("\n=== GAME OVER ===");
        System.out.println("Player: " + player.name);
        System.out.println("Score: " + player.score);
        System.out.println("Final HP: " + Math.max(player.hp, 0) + "/" + player.maxHp);
    }

    static Enemy createEnemy(int round) {
        String name = ENEMY_NAMES[Math.min(round - 1, ENEMY_NAMES.length - 1)];
        int hp = 10 + (round * 4);
        int damage = 3 + (round / 2);
        return new Enemy(name, hp, damage);
    }

    static boolean fightEnemy(Player player, Enemy enemy) {
        while (enemy.hp > 0 && player.hp > 0) {
            System.out.println("\n" + player.name + " HP: " + player.hp + "/" + player.maxHp);
            System.out.println(enemy.name + " HP: " + enemy.hp);
            System.out.println("Choose: [1] Spell word  [2] Use potion  [3] Quit");
            System.out.print("> ");
            String choice = scanner.nextLine().trim();

            if (choice.equals("3")) {
                return false;
            }

            if (choice.equals("2")) {
                player.heal();
                continue;
            }

            if (!choice.equals("1")) {
                System.out.println("Invalid choice.");
                continue;
            }

            WordChallenge challenge = WORDS.get(random.nextInt(WORDS.size()));

            System.out.println("Clue: " + challenge.clue);
            System.out.print("Spell the word: ");
            String answer = scanner.nextLine().trim().toLowerCase();

            if (answer.equals(challenge.answer)) {
                int damage = 6 + random.nextInt(4);
                enemy.hp -= damage;
                player.score += 10;
                System.out.println("Correct. You hit " + enemy.name + " for " + damage + " damage.");
            } else {
                player.hp -= enemy.damage;
                System.out.println("Wrong.");
                System.out.println("Hint: " + challenge.hint);
                System.out.println("Correct spelling: " + challenge.answer);
                System.out.println(enemy.name + " hits you for " + enemy.damage + " damage.");
            }
        }

        if (player.hp > 0) {
            System.out.println("You defeated " + enemy.name + "!");
            return true;
        }
        return false;
    }
}
