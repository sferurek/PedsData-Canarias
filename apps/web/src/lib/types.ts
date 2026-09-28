export type DataStatus = "VALIDATED" | "PARTIAL" | "PENDING OFFICIAL GEOMETRY" | "COMPLETE" | "ESTIMATED" | "PROVISIONAL" | "NOT AVAILABLE";
export type ContextFields = {
  income_mean_per_person_2023: number;
  income_mean_per_household_2023: number;
  income_median_per_consumption_unit_2023: number;
  child_density_per_km2: number;
  rural_children_pct: number;
  territorial_status: "ESTIMATED";
};
export type IslandProfile = {
  island_id:string; name:string; slug:string; children_0_14:number; population_total:number;
  population_evaluable:number; population_routed:number; population_requires_interisland_transfer:number;
  population_no_route:number; population_not_evaluated:number; eligible_pediatric_facilities:number;
  children_per_verified_pediatric_facility:number|null; pediatricians_ap_2024:number;
  median_travel_minutes:number|null; p90_travel_minutes:number|null; pct_under_15_total:number;
  pct_20_or_more_total:number; pct_30_or_more_total:number; pct_requires_interisland_transfer_total:number;
  pct_not_evaluated_total:number; income_mean_per_person_2023:number; child_density_per_km2:number;
  rural_children_pct:number; air_station_count:number; weather_station_count:number;
};
export type MunicipalityProfile = Partial<IslandProfile> & Partial<ContextFields> & {
  island_id:string; municipality_id:string; municipality_name:string;
  publication_status:"publishable"|"not_publishable"; publication_reason:string; slug:string;
};
export type ProfilesData = {
  summary:{children_0_14:number;eligible_pediatric_facilities:number;median_travel_minutes:number;pct_under_15_total:number;pct_30_or_more_total:number;pediatricians_ap_2024:number};
  islands:IslandProfile[]; municipalities:MunicipalityProfile[];
  metadata:{source_period:number;catalog_date:string;engine:string;engine_version:string;osm_snapshot:string;status:string;income_period:number;air_period:number;territorial_period:string;weather_status:string;calima_status:string};
};
