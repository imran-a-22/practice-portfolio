type DamagePhase = {
  name: string;
  baseDamage: number;
  critChance: number;
  critMultiplier: number;
  vulnerabilityMultiplier: number;
};

type RaidBuild = {
  playerName: string;
  attackPower: number;
  skillMultiplier: number;
  elementalBonus: number;
  bossDefenseReduction: number;
  phases: DamagePhase[];
};

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function calculateExpectedPhaseDamage(build: RaidBuild, phase: DamagePhase): number {
  const critChance = clamp(phase.critChance, 0, 1);
  const expectedCritFactor = 1 + critChance * (phase.critMultiplier - 1);

  const rawDamage =
    (build.attackPower * build.skillMultiplier + phase.baseDamage) *
    (1 + build.elementalBonus);

  const defenseFactor = 1 + build.bossDefenseReduction;

  return rawDamage * expectedCritFactor * phase.vulnerabilityMultiplier * defenseFactor;
}

function main(): void {
  const build: RaidBuild = {
    playerName: "Arcturus",
    attackPower: 420,
    skillMultiplier: 2.1,
    elementalBonus: 0.35,
    bossDefenseReduction: 0.18,
    phases: [
      { name: "Opening Burst", baseDamage: 120, critChance: 0.32, critMultiplier: 1.8, vulnerabilityMultiplier: 1.15 },
      { name: "Shield Break Window", baseDamage: 260, critChance: 0.48, critMultiplier: 2.0, vulnerabilityMultiplier: 1.4 },
      { name: "Enrage Finish", baseDamage: 340, critChance: 0.40, critMultiplier: 2.2, vulnerabilityMultiplier: 1.3 }
    ]
  };

  let total = 0;
  console.log(`Raid damage estimate for ${build.playerName}`);
  console.log("=".repeat(40));

  for (const phase of build.phases) {
    const damage = calculateExpectedPhaseDamage(build, phase);
    total += damage;
    console.log(`${phase.name}: ${damage.toFixed(2)}`);
  }

  console.log("-".repeat(40));
  console.log(`Total expected damage: ${total.toFixed(2)}`);
}

main();
