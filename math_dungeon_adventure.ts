/**
 * math_dungeon_adventure.ts
 *
 * A TypeScript CLI game where the player solves maths questions
 * to defeat dungeon monsters, earn XP, and level up.
 *
 * Run with:
 *   ts-node math_dungeon_adventure.ts
 * or compile with:
 *   tsc math_dungeon_adventure.ts && node math_dungeon_adventure.js
 */

import * as readline from "readline";

type QuestionType = "addition" | "subtraction" | "multiplication" | "division" | "linear";

interface Question {
  prompt: string;
  answer: number;
  explanation: string;
  type: QuestionType;
}

class Player {
  name: string;
  hp = 20;
  maxHp = 20;
  level = 1;
  xp = 0;
  streak = 0;
  potions = 2;

  constructor(name: string) {
    this.name = name;
  }

  gainXp(amount: number): void {
    this.xp += amount;
    const nextLevelXp = this.level * 20;

    if (this.xp >= nextLevelXp) {
      this.xp -= nextLevelXp;
      this.level += 1;
      this.maxHp += 5;
      this.hp = this.maxHp;
      console.log(`\n✨ Level up! You are now level ${this.level}.`);
      console.log(`Your health is fully restored to ${this.hp}.`);
    }
  }

  heal(): void {
    if (this.potions <= 0) {
      console.log("You have no potions left.");
      return;
    }

    this.potions -= 1;
    const healAmount = 8;
    this.hp = Math.min(this.maxHp, this.hp + healAmount);
    console.log(`You used a potion and restored ${healAmount} HP.`);
    console.log(`HP: ${this.hp}/${this.maxHp}`);
  }
}

class Monster {
  name: string;
  hp: number;
  damage: number;

  constructor(name: string, hp: number, damage: number) {
    this.name = name;
    this.hp = hp;
    this.damage = damage;
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function ask(text: string): Promise<string> {
  return new Promise((resolve) => rl.question(text, resolve));
}

function randInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function pickOne<T>(items: T[]): T {
  return items[randInt(0, items.length - 1)];
}

function generateQuestion(level: number): Question {
  const types: QuestionType[] =
    level < 2
      ? ["addition", "subtraction", "multiplication"]
      : ["addition", "subtraction", "multiplication", "division", "linear"];

  const type = pickOne(types);

  switch (type) {
    case "addition": {
      const a = randInt(2, 10 + level * 3);
      const b = randInt(2, 10 + level * 3);
      return {
        prompt: `What is ${a} + ${b}? `,
        answer: a + b,
        explanation: `${a} + ${b} = ${a + b}`,
        type,
      };
    }

    case "subtraction": {
      const a = randInt(8, 18 + level * 4);
      const b = randInt(2, a - 1);
      return {
        prompt: `What is ${a} - ${b}? `,
        answer: a - b,
        explanation: `${a} - ${b} = ${a - b}`,
        type,
      };
    }

    case "multiplication": {
      const a = randInt(2, 5 + level);
      const b = randInt(2, 5 + level);
      return {
        prompt: `What is ${a} × ${b}? `,
        answer: a * b,
        explanation: `${a} × ${b} = ${a * b}`,
        type,
      };
    }

    case "division": {
      const b = randInt(2, 5 + level);
      const answer = randInt(2, 6 + level);
      const a = b * answer;
      return {
        prompt: `What is ${a} ÷ ${b}? `,
        answer,
        explanation: `${a} ÷ ${b} = ${answer}`,
        type,
      };
    }

    case "linear": {
      const x = randInt(1, 8 + level);
      const a = randInt(2, 4 + level);
      const b = randInt(1, 10);
      const c = a * x + b;
      return {
        prompt: `Solve for x: ${a}x + ${b} = ${c}. x = `,
        answer: x,
        explanation: `${a}x + ${b} = ${c} → ${a}x = ${c - b} → x = ${(c - b) / a}`,
        type,
      };
    }
  }
}

function createMonster(stage: number): Monster {
  const names = [
    "Slime of Sums",
    "Goblin of Graphs",
    "Skeleton Scholar",
    "Fractions Phantom",
    "Algebra Warden",
    "Prime Number Beast",
    "Cave Troll of Tables",
  ];

  const name = pickOne(names);
  const hp = 8 + stage * 3;
  const damage = 2 + Math.floor(stage / 2);

  return new Monster(name, hp, damage);
}

async function battle(player: Player, monster: Monster): Promise<boolean> {
  console.log(`\n⚔️  A wild ${monster.name} appears!`);
  console.log(`${monster.name} HP: ${monster.hp}`);
  console.log(`${player.name} HP: ${player.hp}/${player.maxHp}`);

  while (monster.hp > 0 && player.hp > 0) {
    const action = (await ask("\nChoose: [a]nswer, [p]otion, [q]uit: ")).trim().toLowerCase();

    if (action === "q") {
      return false;
    }

    if (action === "p") {
      player.heal();
      continue;
    }

    if (action !== "a") {
      console.log("Invalid choice.");
      continue;
    }

    const question = generateQuestion(player.level);
    const raw = await ask(question.prompt);
    const userAnswer = Number(raw.trim());

    if (Number.isNaN(userAnswer)) {
      console.log("That was not a valid number.");
      continue;
    }

    if (userAnswer === question.answer) {
      player.streak += 1;
      const damage = 3 + player.level + Math.min(player.streak, 3);
      monster.hp -= damage;

      console.log(`✅ Correct. ${question.explanation}`);
      console.log(`You deal ${damage} damage.`);
      console.log(`${monster.name} HP: ${Math.max(0, monster.hp)}`);

      if (monster.hp <= 0) {
        const xpReward = 8 + player.level * 2;
        console.log(`\n🏆 You defeated ${monster.name}!`);
        console.log(`You gained ${xpReward} XP.`);
        player.gainXp(xpReward);

        if (randInt(1, 4) === 1) {
          player.potions += 1;
          console.log("You found a potion.");
        }

        return true;
      }
    } else {
      player.streak = 0;
      player.hp -= monster.damage;

      console.log(`❌ Incorrect. Correct answer: ${question.answer}`);
      console.log(`Explanation: ${question.explanation}`);
      console.log(`${monster.name} hits you for ${monster.damage} damage.`);
      console.log(`${player.name} HP: ${Math.max(0, player.hp)}/${player.maxHp}`);

      if (player.hp <= 0) {
        console.log("\n💀 You were defeated in the dungeon.");
        return false;
      }
    }
  }

  return player.hp > 0;
}

async function main(): Promise<void> {
  console.log("=== MATH DUNGEON ADVENTURE ===");
  console.log("Defeat monsters by solving maths problems.");
  console.log("Learn, level up, and survive.\n");

  const nameInput = (await ask("Enter your hero name: ")).trim();
  const player = new Player(nameInput || "Scholar");

  let stage = 1;

  while (true) {
    console.log(`\n--- Dungeon Room ${stage} ---`);
    const monster = createMonster(stage);
    const survived = await battle(player, monster);

    if (!survived) {
      break;
    }

    stage += 1;

    if (stage % 3 === 0) {
      console.log("\n📘 Rest room reached.");
      player.hp = Math.min(player.maxHp, player.hp + 5);
      console.log(`You recover some health. HP: ${player.hp}/${player.maxHp}`);
    }
  }

  console.log("\n=== Game Over ===");
  console.log(`Hero: ${player.name}`);
  console.log(`Level reached: ${player.level}`);
  console.log(`XP: ${player.xp}`);
  console.log(`Rooms cleared: ${Math.max(0, stage - 1)}`);
  rl.close();
}

main().catch((error) => {
  console.error("Unexpected error:", error);
  rl.close();
});
