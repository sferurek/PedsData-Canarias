import rawProfiles from "@/data/profiles.json";
import type { ProfilesData } from "./types";

export const profiles = rawProfiles as ProfilesData;

export const islandBySlug = (slug: string) =>
  profiles.islands.find((island) => island.slug === slug);

export const municipalityById = (id: string) =>
  profiles.municipalities.find((municipality) => municipality.municipality_id === id);

export const islandName = (id: string) =>
  profiles.islands.find((island) => island.island_id === id)?.name ?? id;
