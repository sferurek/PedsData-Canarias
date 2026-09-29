import imageCatalog from "@/data/island_hero_images.json";

export type IslandHeroImage = {
  image_id: string;
  territory_id: string;
  territory_name: string;
  title: string;
  author: string;
  source_url: string;
  license: string;
  license_url: string;
  original_dimensions: string;
  local_path: string;
  local_sha256: string;
  alt: string;
  commons_assessment: string;
  retrieved_at: string;
  derivative: string;
  license_validation: "VERIFIED";
};

export const islandHeroImages = imageCatalog as IslandHeroImage[];
export const islandHeroByTerritory = (territoryId: string) =>
  islandHeroImages.find((image) => image.territory_id === territoryId);
