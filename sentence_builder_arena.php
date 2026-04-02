<?php
/**
 * sentence_builder_arena.php
 *
 * Ed-tech + gaming console program.
 * The player builds correct sentences from shuffled words.
 * Correct answers damage enemies. Wrong answers reduce player health.
 *
 * Run:
 *   php sentence_builder_arena.php
 */

class Player {
    public string $name;
    public int $hp = 30;
    public int $maxHp = 30;
    public int $score = 0;
    public int $potions = 2;

    public function __construct(string $name) {
        $this->name = $name;
    }

    public function heal(): void {
        if ($this->potions <= 0) {
            echo "No potions left.\n";
            return;
        }

        $this->potions--;
        $this->hp = min($this->maxHp, $this->hp + 10);
        echo "Potion used. HP: {$this->hp}/{$this->maxHp}\n";
    }
}

class Enemy {
    public string $name;
    public int $hp;
    public int $damage;

    public function __construct(string $name, int $hp, int $damage) {
        $this->name = $name;
        $this->hp = $hp;
        $this->damage = $damage;
    }
}

$sentenceChallenges = [
    [
        "correct" => "She is reading a book",
        "shuffled" => ["book", "reading", "She", "a", "is"],
        "hint" => "Present continuous sentence about one girl."
    ],
    [
        "correct" => "They went to school early",
        "shuffled" => ["school", "went", "They", "early", "to"],
        "hint" => "Past tense sentence."
    ],
    [
        "correct" => "My brother plays football well",
        "shuffled" => ["well", "football", "plays", "brother", "My"],
        "hint" => "Present simple with third-person singular."
    ],
    [
        "correct" => "We are learning English today",
        "shuffled" => ["English", "today", "learning", "We", "are"],
        "hint" => "Present continuous with 'we'."
    ],
    [
        "correct" => "The cat slept on the chair",
        "shuffled" => ["chair", "slept", "the", "cat", "The", "on"],
        "hint" => "Past tense sentence about an animal."
    ],
    [
        "correct" => "I have finished my homework",
        "shuffled" => ["finished", "I", "my", "homework", "have"],
        "hint" => "Present perfect sentence."
    ],
    [
        "correct" => "The teacher asked a difficult question",
        "shuffled" => ["a", "question", "teacher", "asked", "The", "difficult"],
        "hint" => "Past tense sentence in class."
    ],
    [
        "correct" => "Our team won the final match",
        "shuffled" => ["won", "Our", "final", "the", "team", "match"],
        "hint" => "Past tense sentence about sport."
    ]
];

$enemyNames = [
    "Comma Crusher",
    "Tense Troll",
    "Word Order Wraith",
    "Syntax Serpent",
    "Grammar Overlord"
];

function inputLine(string $prompt): string {
    echo $prompt;
    return trim(fgets(STDIN));
}

function createEnemy(int $round, array $enemyNames): Enemy {
    $nameIndex = min($round - 1, count($enemyNames) - 1);
    $name = $enemyNames[$nameIndex];
    $hp = 12 + ($round * 5);
    $damage = 3 + intdiv($round, 2);
    return new Enemy($name, $hp, $damage);
}

function showChallenge(array $challenge): void {
    echo "\nArrange these words into a correct sentence:\n";
    echo implode(" | ", $challenge["shuffled"]) . "\n";
    echo "Hint: " . $challenge["hint"] . "\n";
}

function sentencesMatch(string $user, string $correct): bool {
    $normalize = function(string $text): string {
        $text = strtolower(trim($text));
        $text = preg_replace('/\s+/', ' ', $text);
        return $text;
    };

    return $normalize($user) === $normalize($correct);
}

echo "=== SENTENCE BUILDER ARENA ===\n";
echo "Build correct sentences to defeat grammar enemies.\n\n";

$name = inputLine("Enter your hero name: ");
if ($name === "") {
    $name = "Scholar";
}

$player = new Player($name);
$round = 1;

while ($player->hp > 0) {
    $enemy = createEnemy($round, $enemyNames);
    echo "\n--- Round {$round} ---\n";
    echo "{$enemy->name} appears with {$enemy->hp} HP.\n";

    while ($enemy->hp > 0 && $player->hp > 0) {
        echo "\n{$player->name} HP: {$player->hp}/{$player->maxHp}\n";
        echo "{$enemy->name} HP: {$enemy->hp}\n";
        echo "Score: {$player->score}\n";
        echo "Choose: [1] Build sentence  [2] Use potion  [3] Quit\n";

        $choice = inputLine("> ");

        if ($choice === "3") {
            echo "\nYou left the arena.\n";
            exit;
        }

        if ($choice === "2") {
            $player->heal();
            continue;
        }

        if ($choice !== "1") {
            echo "Invalid choice.\n";
            continue;
        }

        $challenge = $sentenceChallenges[array_rand($sentenceChallenges)];
        showChallenge($challenge);
        $answer = inputLine("Type the full correct sentence: ");

        if (sentencesMatch($answer, $challenge["correct"])) {
            $damage = rand(7, 11);
            $enemy->hp -= $damage;
            $player->score += 15;
            echo "Correct. You dealt {$damage} damage.\n";
        } else {
            $player->hp -= $enemy->damage;
            echo "Wrong.\n";
            echo "Correct sentence: {$challenge["correct"]}\n";
            echo "{$enemy->name} hits you for {$enemy->damage} damage.\n";
        }
    }

    if ($player->hp <= 0) {
        break;
    }

    echo "You defeated {$enemy->name}.\n";
    $round++;

    if ($round % 3 === 0) {
        $player->hp = min($player->maxHp, $player->hp + 6);
        $player->potions++;
        echo "Rest bonus. HP restored to {$player->hp}/{$player->maxHp}. You also found a potion.\n";
    }
}

echo "\n=== GAME OVER ===\n";
echo "Player: {$player->name}\n";
echo "Final score: {$player->score}\n";
echo "Rounds cleared: " . max(0, $round - 1) . "\n";
