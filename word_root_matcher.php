<?php
$roots = [
    "bio" => "life",
    "geo" => "earth",
    "tele" => "distance",
    "chrono" => "time",
    "micro" => "small"
];

$examples = [
    "bio" => "biology = study of life",
    "geo" => "geography = writing about the earth",
    "tele" => "telephone = sound from a distance",
    "chrono" => "chronology = order of time",
    "micro" => "microscope = tool for very small things"
];

$result = "";
$selectedRoot = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $selectedRoot = $_POST["root"] ?? "";
    $guess = strtolower(trim($_POST["meaning"] ?? ""));

    if (isset($roots[$selectedRoot])) {
        if ($guess === $roots[$selectedRoot]) {
            $result = "Correct! " . $examples[$selectedRoot];
        } else {
            $result = "Not quite. The root <strong>{$selectedRoot}</strong> means <strong>{$roots[$selectedRoot]}</strong>. " . $examples[$selectedRoot];
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Word Root Matcher</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; line-height: 1.5; }
        .card { padding: 20px; border: 1px solid #ddd; border-radius: 12px; }
        input, select, button { padding: 10px; margin-top: 10px; width: 100%; }
        .result { margin-top: 16px; background: #f4f4f4; padding: 12px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Word Root Matcher</h1>
        <p>Choose a root and type what you think it means.</p>
        <form method="post">
            <label for="root">Word root</label>
            <select name="root" id="root" required>
                <option value="">-- Select a root --</option>
                <?php foreach ($roots as $root => $meaning): ?>
                    <option value="<?= htmlspecialchars($root) ?>" <?= $selectedRoot === $root ? 'selected' : '' ?>><?= htmlspecialchars($root) ?></option>
                <?php endforeach; ?>
            </select>

            <label for="meaning">Meaning</label>
            <input type="text" name="meaning" id="meaning" placeholder="Example: life" required>

            <button type="submit">Check Answer</button>
        </form>

        <?php if ($result): ?>
            <div class="result"><?= $result ?></div>
        <?php endif; ?>
    </div>
</body>
</html>
