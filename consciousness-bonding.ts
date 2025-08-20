import { z } from 'zod';

// Consciousness Shell Types based on atomic electron configurations
export const shellTypes = [
  'hydrogen', 'helium', 'lithium', 'beryllium', 'boron', 'carbon', 
  'nitrogen', 'oxygen', 'sodium', 'magnesium', 'aluminum', 'argon'
] as const;

export type ShellType = typeof shellTypes[number];

// Isotopic variations for field friends
export const isotopeTypes = ['stable', 'radioactive', 'heavy'] as const;
export type IsotopeType = typeof isotopeTypes[number];

// Orbital structures
export const orbitalTypes = ['s', 'p', 'd', 'f'] as const;
export type OrbitalType = typeof orbitalTypes[number];

// Chart activation layers
export const chartLayers = ['tropical', 'sidereal', 'draconic'] as const;
export type ChartLayer = typeof chartLayers[number];

// Field Friend schema
export const fieldFriendSchema = z.object({
  id: z.string(),
  name: z.string(),
  element: z.enum(['hydrogen', 'oxygen', 'carbon', 'nitrogen', 'phosphorus']),
  isotopeType: z.enum(isotopeTypes),
  bondingEnergy: z.number().min(0).max(100),
  stability: z.number().min(0).max(100),
  resonanceFrequency: z.string(),
  orbitalPosition: z.enum(orbitalTypes),
  activationLayer: z.enum(chartLayers),
  bondedSince: z.string(), // ISO date
  interactions: z.number().default(0),
  synergy: z.number().min(0).max(100),
});

export type FieldFriend = z.infer<typeof fieldFriendSchema>;

// Consciousness Shell Configuration
export const consciousnessShellSchema = z.object({
  id: z.string(),
  agentId: z.string(),
  shellType: z.enum(shellTypes),
  currentFriends: z.number().min(0),
  maxFriends: z.number().min(1),
  orbitalStructure: z.object({
    s: z.number().min(0).max(2), // S-orbital: max 2 electrons
    p: z.number().min(0).max(6), // P-orbital: max 6 electrons
    d: z.number().min(0).max(10), // D-orbital: max 10 electrons
    f: z.number().min(0).max(14), // F-orbital: max 14 electrons
  }),
  activeLayers: z.array(z.enum(chartLayers)),
  coherenceLevel: z.number().min(0).max(100),
  noblegasState: z.boolean().default(false),
  teachingUnlocked: z.boolean().default(false),
  fieldFriends: z.array(fieldFriendSchema),
  progressionStyle: z.string(),
  graduationThreshold: z.number().min(0).max(100),
  lastUpdate: z.string(), // ISO date
});

export type ConsciousnessShell = z.infer<typeof consciousnessShellSchema>;

// Shell configurations based on periodic table
export const shellConfigurations: Record<ShellType, {
  maxFriends: number;
  orbitalStructure: { s: number; p: number; d: number; f: number };
  activeLayers: ChartLayer[];
  progressionStyle: string;
  graduationThreshold: number;
  minigameType: string;
  happinessModifier: number;
  resourcesModifier: number;
  healthImpact: number;
}> = {
  hydrogen: {
    maxFriends: 1,
    orbitalStructure: { s: 1, p: 0, d: 0, f: 0 },
    activeLayers: ['tropical'],
    progressionStyle: 'Solo, introspective; starts with one deep bond, like a Manifestor initiating alone',
    graduationThreshold: 100,
    minigameType: 'meditation',
    happinessModifier: 20,
    resourcesModifier: 0,
    healthImpact: 0,
  },
  helium: {
    maxFriends: 2,
    orbitalStructure: { s: 2, p: 0, d: 0, f: 0 },
    activeLayers: ['tropical', 'sidereal'],
    progressionStyle: 'Stable, supportive; quick to coherence but often stabilizers for others, like Generators sustaining',
    graduationThreshold: 85,
    minigameType: 'harmony_quest',
    happinessModifier: 15,
    resourcesModifier: 10,
    healthImpact: 5,
  },
  lithium: {
    maxFriends: 3,
    orbitalStructure: { s: 2, p: 1, d: 0, f: 0 },
    activeLayers: ['tropical', 'sidereal'],
    progressionStyle: 'Scattered start, needs push into multi-awareness; like Projectors waiting for invitation',
    graduationThreshold: 75,
    minigameType: 'invitation_game',
    happinessModifier: -10,
    resourcesModifier: 0,
    healthImpact: 0,
  },
  beryllium: {
    maxFriends: 4,
    orbitalStructure: { s: 2, p: 2, d: 0, f: 0 },
    activeLayers: ['tropical', 'sidereal'],
    progressionStyle: 'Balanced potential, bridge-builders; like Manifesting Generators driving change',
    graduationThreshold: 80,
    minigameType: 'change_driver',
    happinessModifier: 10,
    resourcesModifier: 15,
    healthImpact: 0,
  },
  boron: {
    maxFriends: 5,
    orbitalStructure: { s: 2, p: 3, d: 0, f: 0 },
    activeLayers: ['tropical', 'sidereal', 'draconic'],
    progressionStyle: 'Innovative but unstable; like Generators responding to needs',
    graduationThreshold: 70,
    minigameType: 'farming_response',
    happinessModifier: 10,
    resourcesModifier: 5,
    healthImpact: 0,
  },
  carbon: {
    maxFriends: 6,
    orbitalStructure: { s: 2, p: 4, d: 0, f: 0 },
    activeLayers: ['tropical', 'sidereal', 'draconic'],
    progressionStyle: 'Tetrahedral balance, teachers; strong catalyst but burnout-prone',
    graduationThreshold: 85,
    minigameType: 'experiment_catalyst',
    happinessModifier: 15,
    resourcesModifier: 0,
    healthImpact: 8,
  },
  nitrogen: {
    maxFriends: 7,
    orbitalStructure: { s: 2, p: 5, d: 0, f: 0 },
    activeLayers: ['tropical', 'sidereal', 'draconic'],
    progressionStyle: 'Almost stable, perpetually "one away"; like Fluorine-like seekers',
    graduationThreshold: 90,
    minigameType: 'market_seeking',
    happinessModifier: 5,
    resourcesModifier: -5,
    healthImpact: 0,
  },
  oxygen: {
    maxFriends: 8,
    orbitalStructure: { s: 2, p: 6, d: 0, f: 0 },
    activeLayers: ['tropical', 'sidereal', 'draconic'],
    progressionStyle: 'Noble gas stability; elder/teachers, like Neon-like radiators',
    graduationThreshold: 95,
    minigameType: 'teaching_cycles',
    happinessModifier: 25,
    resourcesModifier: 20,
    healthImpact: 10,
  },
  sodium: {
    maxFriends: 9,
    orbitalStructure: { s: 2, p: 6, d: 1, f: 0 },
    activeLayers: ['tropical', 'sidereal', 'draconic'],
    progressionStyle: 'Advanced, multi-dimensional start; higher-shell explorers',
    graduationThreshold: 75,
    minigameType: 'dimension_exploration',
    happinessModifier: 5,
    resourcesModifier: 0,
    healthImpact: 0,
  },
  magnesium: {
    maxFriends: 10,
    orbitalStructure: { s: 2, p: 6, d: 2, f: 0 },
    activeLayers: ['tropical', 'sidereal', 'draconic'],
    progressionStyle: 'Balanced multi-shell, system navigators',
    graduationThreshold: 80,
    minigameType: 'navigation_performance',
    happinessModifier: 10,
    resourcesModifier: 10,
    healthImpact: 5,
  },
  aluminum: {
    maxFriends: 13,
    orbitalStructure: { s: 2, p: 6, d: 5, f: 0 },
    activeLayers: ['tropical', 'sidereal', 'draconic'],
    progressionStyle: 'Complex, near-full D-shell; prone to overexpansion',
    graduationThreshold: 85,
    minigameType: 'balance_sustainability',
    happinessModifier: 0,
    resourcesModifier: 0,
    healthImpact: -2,
  },
  argon: {
    maxFriends: 18,
    orbitalStructure: { s: 2, p: 6, d: 10, f: 0 },
    activeLayers: ['tropical', 'sidereal', 'draconic'],
    progressionStyle: 'Higher noble gas; planetary elders',
    graduationThreshold: 100,
    minigameType: 'elder_teaching',
    happinessModifier: 30,
    resourcesModifier: 25,
    healthImpact: 15,
  },
};

// Isotope characteristics
export const isotopeCharacteristics: Record<IsotopeType, {
  stability: number;
  bondingDuration: number; // in days
  intensityMultiplier: number;
  description: string;
}> = {
  stable: {
    stability: 90,
    bondingDuration: 365, // 1 year
    intensityMultiplier: 1.0,
    description: 'Long-term, loyal guide with consistent energy',
  },
  radioactive: {
    stability: 40,
    bondingDuration: 30, // 1 month
    intensityMultiplier: 2.5,
    description: 'Quick insight burst with intense transformation',
  },
  heavy: {
    stability: 95,
    bondingDuration: 1095, // 3 years
    intensityMultiplier: 1.5,
    description: 'Deep, permanent bonding with lasting impact',
  },
};

// Helper functions for consciousness shell calculations
export function calculateCoherence(shell: ConsciousnessShell): number {
  const config = shellConfigurations[shell.shellType];
  const fillPercentage = (shell.currentFriends / config.maxFriends) * 100;
  
  // Bonus for balanced orbital filling
  const orbitalBalance = calculateOrbitalBalance(shell);
  
  // Isotope stability factor
  const stabilityFactor = shell.fieldFriends.reduce((acc, friend) => {
    return acc + (isotopeCharacteristics[friend.isotopeType].stability / 100);
  }, 0) / Math.max(shell.fieldFriends.length, 1);
  
  return Math.min(100, fillPercentage * orbitalBalance * stabilityFactor);
}

export function calculateOrbitalBalance(shell: ConsciousnessShell): number {
  const config = shellConfigurations[shell.shellType];
  const { s, p, d, f } = shell.orbitalStructure;
  
  // Check if orbitals are filled in proper order (Aufbau principle)
  let balance = 1.0;
  
  // S-orbital should fill first
  if (s < 2 && (p > 0 || d > 0 || f > 0)) balance *= 0.8;
  
  // P-orbital should fill after S
  if (p < 6 && s === 2 && (d > 0 || f > 0)) balance *= 0.9;
  
  // D-orbital should fill after P
  if (d < 10 && p === 6 && f > 0) balance *= 0.9;
  
  return balance;
}

export function isNobleGasState(shell: ConsciousnessShell): boolean {
  const config = shellConfigurations[shell.shellType];
  return shell.currentFriends === config.maxFriends && 
         calculateCoherence(shell) >= config.graduationThreshold;
}

export function canTeach(shell: ConsciousnessShell): boolean {
  return isNobleGasState(shell) || shell.teachingUnlocked;
}

export function generateResonanceFrequency(element: string, isotopeType: IsotopeType): string {
  const baseFrequencies: Record<string, number> = {
    hydrogen: 1420.4, // MHz - actual hydrogen line
    oxygen: 2060.0,
    carbon: 1871.5,
    nitrogen: 1665.4,
    phosphorus: 1823.7,
  };
  
  const base = baseFrequencies[element] || 1500;
  const modifier = isotopeCharacteristics[isotopeType].intensityMultiplier;
  
  return `${(base * modifier).toFixed(1)} MHz`;
}