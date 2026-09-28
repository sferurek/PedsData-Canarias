export type ContextLayer = "accessibility" | "income" | "density" | "PM10" | "PM2.5" | "NO2";
export const legendItems = [["under_5","<5 min"],["5_to_under_10","5–<10"],["10_to_under_15","10–<15"],["15_to_under_20","15–<20"],["20_to_under_30","20–<30"],["30_or_more","≥30"],["requires_interisland_transfer","Transferencia interinsular"],["not_evaluated","No evaluable"]] as const;
const context:Record<Exclude<ContextLayer,"accessibility">,{label:string;unit:string;items:[string,string][]}>={
 income:{label:"Renta neta media por persona · 2023",unit:"€/persona",items:[["context-1","<10.000"],["context-2","10.000–12.000"],["context-3","12.000–14.000"],["context-4","≥14.000"]]},
 density:{label:"Densidad infantil · 2024",unit:"niños/km²",items:[["context-1","<25"],["context-2","25–100"],["context-3","100–300"],["context-4","≥300"]]},
 PM10:{label:"Última observación validada PM10 · 2025",unit:"µg/m³",items:[["air-1","<10"],["air-2","10–20"],["air-3","20–40"],["air-4","≥40"]]},
 "PM2.5":{label:"Última observación validada PM2,5 · 2025",unit:"µg/m³",items:[["air-1","<5"],["air-2","5–10"],["air-3","10–20"],["air-4","≥20"]]},
 NO2:{label:"Última observación validada NO₂ · 2025",unit:"µg/m³",items:[["air-1","<10"],["air-2","10–20"],["air-3","20–40"],["air-4","≥40"]]},
};
export function MapLegend({layer="accessibility"}:{layer?:ContextLayer}){
 if(layer==="accessibility") return <div className="legend" aria-label="Leyenda de tiempo estimado">{legendItems.map(([key,label])=><span key={key}><i className={`swatch swatch-${key}`}/>{label}</span>)}</div>;
 const selected=context[layer]; return <div className="legend context-legend" aria-label={`Leyenda ${selected.label}`}><strong>{selected.label}</strong>{selected.items.map(([key,label])=><span key={key}><i className={`swatch swatch-${key}`}/>{label} {selected.unit}</span>)}</div>;
}
