import java.util.Random;

class Fighter {
    String name;
    int health;
    int minDamage;
    int maxDamage;
    int critChance;

    Fighter(String name, int health, int minDamage, int maxDamage, int critChance) {
        this.name = name;
        this.health = health;
        this.minDamage = minDamage;
        this.maxDamage = maxDamage;
        this.critChance = critChance;
    }

    boolean isAlive() {
        return health > 0;
    }

    int attack(Random random) {
        int damage = random.nextInt(maxDamage - minDamage + 1) + minDamage;
        if (random.nextInt(100) < critChance) {
            damage *= 2;
            System.out.println(name + " lands a critical hit!");
        }
        return damage;
    }

    void takeDamage(int damage) {
        health = Math.max(0, health - damage);
    }
}

class TurnBasedBattleSimulator {
    public static void main(String[] args) {
        Random random = new Random();

        Fighter knight = new Fighter("Knight", 70, 8, 14, 20);
        Fighter slimeKing = new Fighter("Slime King", 80, 6, 16, 15);

        int round = 1;

        System.out.println("Turn-Based Battle Simulator");
        System.out.println("---------------------------");

        while (knight.isAlive() && slimeKing.isAlive()) {
            System.out.println("\nRound " + round);

            int knightDamage = knight.attack(random);
            slimeKing.takeDamage(knightDamage);
            System.out.println(
                knight.name + " deals " + knightDamage + " damage. " +
                slimeKing.name + " HP: " + slimeKing.health
            );

            if (!slimeKing.isAlive()) {
                break;
            }

            int slimeDamage = slimeKing.attack(random);
            knight.takeDamage(slimeDamage);
            System.out.println(
                slimeKing.name + " deals " + slimeDamage + " damage. " +
                knight.name + " HP: " + knight.health
            );

            round++;
        }

        System.out.println("\nBattle finished.");
        if (knight.isAlive()) {
            System.out.println(knight.name + " wins!");
        } else {
            System.out.println(slimeKing.name + " wins!");
        }
    }
}
