/**
 * pricing_elasticity_lab.ts
 *
 * A small business/economics simulator that compares price points,
 * estimates demand from simple elasticity assumptions,
 * and finds the best expected monthly revenue/profit point.
 */

type Scenario = {
  price: number;
  demand: number;
  revenue: number;
  variableCost: number;
  contribution: number;
};

function estimateDemand(
  basePrice: number,
  baseDemand: number,
  trialPrice: number,
  elasticity: number
): number {
  const pctPriceChange = (trialPrice - basePrice) / basePrice;
  const pctDemandChange = elasticity * pctPriceChange;
  const rawDemand = baseDemand * (1 + pctDemandChange);
  return Math.max(0, Math.round(rawDemand));
}

function buildScenario(
  trialPrice: number,
  basePrice: number,
  baseDemand: number,
  elasticity: number,
  unitVariableCost: number
): Scenario {
  const demand = estimateDemand(basePrice, baseDemand, trialPrice, elasticity);
  const revenue = demand * trialPrice;
  const variableCost = demand * unitVariableCost;
  const contribution = revenue - variableCost;

  return {
    price: trialPrice,
    demand,
    revenue,
    variableCost,
    contribution,
  };
}

function currency(value: number): string {
  return `£${value.toFixed(2)}`;
}

function printTable(scenarios: Scenario[]): void {
  console.log("Price | Demand | Revenue | Variable Cost | Contribution");
  console.log("-------------------------------------------------------");
  for (const s of scenarios) {
    console.log(
      `${currency(s.price).padEnd(6)} | ` +
      `${String(s.demand).padEnd(6)} | ` +
      `${currency(s.revenue).padEnd(8)} | ` +
      `${currency(s.variableCost).padEnd(13)} | ` +
      `${currency(s.contribution)}`
    );
  }
}

function findBestScenario(scenarios: Scenario[]): Scenario {
  return scenarios.reduce((best, current) =>
    current.contribution > best.contribution ? current : best
  );
}

function main(): void {
  const basePrice = 10;
  const baseDemand = 1200;
  const elasticity = -1.4;
  const unitVariableCost = 2.4;

  const pricesToTest = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
  const scenarios = pricesToTest.map((price) =>
    buildScenario(price, basePrice, baseDemand, elasticity, unitVariableCost)
  );

  printTable(scenarios);

  const best = findBestScenario(scenarios);

  console.log("\nBest scenario by contribution:");
  console.log(`Price: ${currency(best.price)}`);
  console.log(`Demand: ${best.demand}`);
  console.log(`Revenue: ${currency(best.revenue)}`);
  console.log(`Contribution: ${currency(best.contribution)}`);
}

main();
