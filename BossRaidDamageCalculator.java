/*
 * boss_raid_damage_calculator.java
 *
 * Estimates whether a team can defeat a raid boss before enrage.
 * Compile:
 *   javac BossRaidDamageCalculator.java
 * Run:
 *   java BossRaidDamageCalculator
 */

import java.util.ArrayList;
import java.util.List;

class Player {
    String name;
    double baseDps;
    double critBonusMultiplier;
    double buffMultiplier;

    Player(String name, double baseDps, double critBonusMultiplier, double buffMultiplier) {
        this.name = name;
        this.baseDps = baseDps;
        this.critBonusMultiplier = critBonusMultiplier;
        this.buffMultiplier = buffMultiplier;
    }

    double effectiveDps() {
        return baseDps * critBonusMultiplier * buffMultiplier;
    }
}

public class BossRaidDamageCalculator {
    public static void main(String[] args) {
        double bossHp = 2_500_000;
        int enrageSeconds = 180;

        List<Player> team = new ArrayList<>();
        team.add(new Player("Knight", 4200, 1.10, 1.15));
        team.add(new Player("Mage", 5100, 1.25, 1.08));
        team.add(new Player("Ranger", 4700, 1.18, 1.12));
        team.add(new Player("Cleric", 2600, 1.05, 1.05));

        double totalDps = 0.0;

        System.out.println("Raid Team Damage Report");
        System.out.println("-----------------------");

        for (Player player : team) {
            double dps = player.effectiveDps();
            totalDps += dps;
            System.out.printf("%s effective DPS: %.2f%n", player.name, dps);
        }

        double timeToKill = bossHp / totalDps;
        double totalDamageBeforeEnrage = totalDps * enrageSeconds;

        System.out.println();
        System.out.printf("Boss HP: %.0f%n", bossHp);
        System.out.printf("Team total DPS: %.2f%n", totalDps);
        System.out.printf("Estimated time to kill: %.2f seconds%n", timeToKill);
        System.out.printf("Damage before enrage: %.0f%n", totalDamageBeforeEnrage);

        if (timeToKill <= enrageSeconds) {
            System.out.println("Result: Clear is possible before enrage.");
        } else {
            double missingDamage = bossHp - totalDamageBeforeEnrage;
            System.out.printf("Result: Team wipes to enrage. Missing damage: %.0f%n", missingDamage);
        }
    }
}
