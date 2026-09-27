"use client";

import { useEffect, useRef, useState } from "react";
import * as maplibregl from "maplibre-gl";
import type { Map as MapLibreMap, MapLayerMouseEvent } from "maplibre-gl";
import type { MunicipalityProfile } from "@/lib/types";
import { MapLegend } from "./MapLegend";

const ISLAND_BOUNDS: Record<string, [[number, number], [number, number]]> = {
  "el-hierro": [[-18.2, 27.60], [-17.85, 27.90]], "la-gomera": [[-17.4, 28.0], [-17.0, 28.25]],
  "la-palma": [[-18.0, 28.45], [-17.65, 28.90]], "tenerife": [[-16.95, 27.95], [-16.0, 28.65]],
  "gran-canaria": [[-15.85, 27.70], [-15.35, 28.20]], "fuerteventura": [[-14.55, 28.0], [-13.75, 28.80]],
  "lanzarote": [[-13.90, 28.80], [-13.40, 29.32]],
};
const CANARY_BOUNDS: [[number, number], [number, number]] = [[-18.35, 27.45], [-13.25, 29.45]];
const BAND_LABELS: Record<string, string> = {
  under_5: "Menos de 5 min", "5_to_under_10": "5–<10 min", "10_to_under_15": "10–<15 min",
  "15_to_under_20": "15–<20 min", "20_to_under_30": "20–<30 min", "30_or_more": "30 min o más",
  requires_interisland_transfer: "Transferencia interinsular requerida", not_evaluated: "No evaluable",
};

export function AccessibilityMap({ municipalities, initialIsland = "all" }: {
  municipalities: MunicipalityProfile[];
  initialIsland?: string;
}) {
  const container = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MapLibreMap | null>(null);
  const [island, setIsland] = useState(initialIsland);
  const [municipality, setMunicipality] = useState("all");
  const [state, setState] = useState<"loading" | "ready" | "error">("loading");
  const [detail, setDetail] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    if (!container.current || mapRef.current) return;
    maplibregl.setWorkerUrl("/maplibre/maplibre-gl-worker.mjs");
    const map = new maplibregl.Map({
      container: container.current,
      style: { version: 8, sources: {}, layers: [{ id: "background", type: "background", paint: { "background-color": "#dfeae5" } }] },
      bounds: CANARY_BOUNDS, fitBoundsOptions: { padding: 28 }, attributionControl: false,
    });
    mapRef.current = map;
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    map.addControl(new maplibregl.AttributionControl({ customAttribution: "ISTAC · OpenStreetMap contributors · OSRM" }));
    const initializeLayers = () => {
      map.addSource("municipalities", { type: "geojson", data: "/data/municipalities.geojson" });
      map.addLayer({ id: "municipality-fill", type: "fill", source: "municipalities", paint: { "fill-color": "#f7faf7", "fill-opacity": 0.75 } });
      map.addLayer({ id: "municipality-line", type: "line", source: "municipalities", paint: { "line-color": "#78918b", "line-width": 0.8 } });
      map.addSource("accessibility", { type: "geojson", data: "/data/accessibility-grid.geojson" });
      map.addLayer({ id: "accessibility-fill", type: "fill", source: "accessibility", paint: {
        "fill-color": ["match", ["get", "band"], "under_5", "#08766b", "5_to_under_10", "#43a685",
          "10_to_under_15", "#8ac58d", "15_to_under_20", "#d2d87f", "20_to_under_30", "#e6b65f",
          "30_or_more", "#cf704e", "requires_interisland_transfer", "#7552a3", "#89928f"],
        "fill-opacity": 0.88, "fill-outline-color": "rgba(255,255,255,.3)" } });
      map.addSource("facilities", { type: "geojson", data: "/data/facilities.geojson" });
      map.addLayer({ id: "facilities", type: "circle", source: "facilities", paint: { "circle-radius": 3.5, "circle-color": "#102a36", "circle-stroke-color": "#fff", "circle-stroke-width": 1 } });
      map.on("click", "accessibility-fill", (event: MapLayerMouseEvent) => {
        const properties = event.features?.[0]?.properties;
        if (properties) setDetail(properties as Record<string, unknown>);
      });
      map.on("mouseenter", "accessibility-fill", () => { map.getCanvas().style.cursor = "pointer"; });
      map.on("mouseleave", "accessibility-fill", () => { map.getCanvas().style.cursor = ""; });
      map.once("idle", () => setState("ready"));
    };
    if (map.isStyleLoaded()) initializeLayers();
    else map.once("style.load", initializeLayers);
    map.on("error", (event) => {
      if (!map.isStyleLoaded()) setState("error");
      console.error("MapLibre error", event.error);
    });
    return () => { map.remove(); mapRef.current = null; };
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || state !== "ready") return;
    const filters: unknown[] = [];
    if (island !== "all") filters.push(["==", ["get", "island_id"], island]);
    if (municipality !== "all") filters.push(["==", ["get", "municipality_id"], municipality]);
    const filter = filters.length === 0 ? null : filters.length === 1 ? filters[0] : ["all", ...filters];
    map.setFilter("accessibility-fill", filter as never);
    map.setFilter("facilities", island === "all" ? null : ["==", ["get", "island_id"], island]);
    map.fitBounds(island === "all" ? CANARY_BOUNDS : ISLAND_BOUNDS[island], { padding: 38, duration: 400 });
    setDetail(null);
  }, [island, municipality, state]);

  const availableMunicipalities = municipalities.filter((item) => island === "all" || item.island_id === island);
  return <div className="map-shell">
    <div className="map-toolbar">
      <label>Ámbito insular<select value={island} onChange={(event) => { setIsland(event.target.value); setMunicipality("all"); }}>
        <option value="all">Canarias · 7 islas</option>
        {Object.entries({ "el-hierro": "El Hierro", "la-gomera": "La Gomera", "la-palma": "La Palma", tenerife: "Tenerife", "gran-canaria": "Gran Canaria", fuerteventura: "Fuerteventura", lanzarote: "Lanzarote" }).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
      </select></label>
      <label>Municipio<select value={municipality} onChange={(event) => setMunicipality(event.target.value)}>
        <option value="all">Todos los municipios</option>
        {availableMunicipalities.map((item) => <option key={`${item.island_id}-${item.municipality_id}`} value={item.municipality_id}>{item.municipality_name}{item.publication_status === "not_publishable" ? " · limitado" : ""}</option>)}
      </select></label>
      <span className="layer-label">Capa · Pediatría AP</span>
    </div>
    <div className="map-stage">
      <div ref={container} className="map" aria-label="Mapa de accesibilidad pediátrica de Canarias" />
      {state === "loading" && <div className="map-state" role="status">Cargando mapa validado…</div>}
      {state === "error" && <div className="map-state map-error" role="alert">El mapa no pudo cargarse. Los indicadores siguen disponibles.</div>}
      {detail && <aside className="map-detail" aria-live="polite"><button onClick={() => setDetail(null)} aria-label="Cerrar detalle">×</button>
        <span className="eyebrow">Detalle de celda</span><strong>{BAND_LABELS[String(detail.band)] ?? "Estado no disponible"}</strong>
        <dl><div><dt>Recurso más próximo</dt><dd>{String(detail.nearest_facility_name ?? "No asignado")}</dd></div>
          <div><dt>Distancia aproximada</dt><dd>{detail.distance_km == null ? "No disponible" : `${detail.distance_km} km`}</dd></div>
          <div><dt>Periodo</dt><dd>2024</dd></div></dl>
        <small>El conteo infantil exacto no se muestra por privacidad.</small>
      </aside>}
    </div>
    <MapLegend />
  </div>;
}
