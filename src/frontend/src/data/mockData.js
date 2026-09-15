export const gridOverview = {
  riskScore: 72,
  riskLevel: "High",
  assetsMonitored: 128,
  criticalAssets: 7,
  highRiskAssets: 18,
  outageProneAreas: 4,
  affectedCustomers: 12480,
};

export const criticalAssets = [
  {
    id: "TR-002",
    name: "Central Grid Transformer",
    type: "Power Transformer",
    location: "Vadodara Central",
    riskScore: 92,
    failureProbability: 87,
    status: "Critical",
  },
  {
    id: "TR-017",
    name: "Industrial Feeder Transformer",
    type: "Power Transformer",
    location: "Makarpura",
    riskScore: 86,
    failureProbability: 74,
    status: "High",
  },
  {
    id: "CB-041",
    name: "North Substation Breaker",
    type: "Circuit Breaker",
    location: "Nizampura",
    riskScore: 81,
    failureProbability: 68,
    status: "High",
  },
  {
    id: "TX-031",
    name: "East Distribution Transformer",
    type: "Distribution Transformer",
    location: "Waghodia",
    riskScore: 78,
    failureProbability: 61,
    status: "High",
  },
];

export const outageAreas = [
  {
    name: "Vadodara Central",
    riskLevel: "Critical",
    assetsAtRisk: 3,
    customersAffected: 5200,
  },
  {
    name: "Makarpura Industrial Zone",
    riskLevel: "High",
    assetsAtRisk: 5,
    customersAffected: 3400,
  },
  {
    name: "Nizampura",
    riskLevel: "High",
    assetsAtRisk: 4,
    customersAffected: 2180,
  },
  {
    name: "Waghodia",
    riskLevel: "Medium",
    assetsAtRisk: 2,
    customersAffected: 1700,
  },
];
