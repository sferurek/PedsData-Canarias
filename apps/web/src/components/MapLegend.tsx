export type ContextLayer =
 | "accessibility"
 | "facilities"
 | "child_population_assigned_0_14"
 | "pediatricians_ap"
 | "assigned_children_per_pediatrician"
 | "pediatric_consultations"
 | "pediatric_frequentation"
 | "births"
 | "income"
 | "density"
 | "degurba"
 | "preterm_rate"
 | "PM10"
 | "PM2.5"
 | "NO2";

export const legendItems = [
 ["under_5","<5 min"],
 ["5_to_under_10","5–<10"],
 ["10_to_under_15","10–<15"],
 ["15_to_under_20","15–<20"],
 ["20_to_under_30","20–<30"],
 ["30_or_more","≥30"],
 ["requires_interisland_transfer","Transferencia interinsular"],
 ["not_evaluated","No evaluable"]
] as const;

const labels: Record<Exclude<ContextLayer,"accessibility"|"facilities"|"degurba">,{label:string;unit:string;method:string}> = {
 child_population_assigned_0_14:{label:"Población asignada 0–14",unit:"personas",method:"equal_interval"},
 pediatricians_ap:{label:"Pediatras AP",unit:"profesionales",method:"equal_interval"},
 assigned_children_per_pediatrician:{label:"Población asignada por pediatra",unit:"personas/profesional",method:"equal_interval"},
 pediatric_consultations:{label:"Consultas de Pediatría AP",unit:"consultas",method:"equal_interval"},
 pediatric_frequentation:{label:"Frecuentación pediátrica",unit:"consultas/persona/año",method:"equal_interval"},
 births:{label:"Nacimientos",unit:"nacimientos",method:"equal_interval"},
 income:{label:"Renta media por persona",unit:"€/persona",method:"quantile"},
 density:{label:"Densidad infantil",unit:"niños/km²",method:"quantile"},
 preterm_rate:{label:"Prematuridad",unit:"%",method:"fixed_thresholds"},
 PM10:{label:"PM10 observado",unit:"µg/m³",method:"fixed_thresholds"},
 "PM2.5":{label:"PM2,5 observado",unit:"µg/m³",method:"fixed_thresholds"},
 NO2:{label:"NO₂ observado",unit:"µg/m³",method:"fixed_thresholds"}
};

export function MapLegend({layer="accessibility",year,breaks=[]}:{layer?:ContextLayer;year?:number;breaks?:number[]}){
 if(layer==="accessibility") return <div className="legend" aria-label="Leyenda de tiempo estimado">{legendItems.map(([key,label])=><span key={key}><i className={"swatch swatch-"+key}/>{label}</span>)}</div>;
 if(layer==="facilities") return <div className="legend context-legend" aria-label="Leyenda de centros pediátricos"><strong>Recursos pediátricos AP verificados · {year}</strong><span><i className="swatch" style={{background:"#2de2e6",borderRadius:"50%"}}/>Centro verificado</span></div>;
 if(layer==="degurba") return <div className="legend context-legend" aria-label="Leyenda Urbanización DEGURBA"><strong>Urbanización DEGURBA · 2021 · categorical</strong>{[["#247ea0","Centro urbano"],["#45b8b6","Agrupación urbana"],["#c9a662","Rural"]].map(([color,label])=><span key={label}><i className="swatch" style={{background:color}}/>{label}</span>)}</div>;
 const selected=labels[layer],colors=["#0f4c6d","#087f9d","#12b8c4","#4fe1d2"];
 const text=(index:number)=>index===0?(breaks[0]===undefined?"Dato observado":"< "+breaks[0].toLocaleString("es-ES")):index===colors.length-1?(breaks[index-1]===undefined?"":"≥ "+breaks[index-1].toLocaleString("es-ES")):(breaks[index-1]?.toLocaleString("es-ES")??"")+"–"+(breaks[index]?.toLocaleString("es-ES")??"");
 return <div className="legend context-legend" aria-label={"Leyenda "+selected.label}><strong>{selected.label}{year?" · "+year:""} · {selected.method}</strong>{colors.map((color,index)=><span key={color}><i className="swatch" style={{background:color}}/>{text(index)} {selected.unit}</span>)}</div>;
}
