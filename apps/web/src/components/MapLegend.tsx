export type ContextLayer = "accessibility" | "income" | "density" | "degurba" | "pediatricians_ap" | "pediatric_frequentation" | "preterm_rate" | "PM10" | "PM2.5" | "NO2";
export const legendItems = [["under_5","<5 min"],["5_to_under_10","5–<10"],["10_to_under_15","10–<15"],["15_to_under_20","15–<20"],["20_to_under_30","20–<30"],["30_or_more","≥30"],["requires_interisland_transfer","Transferencia interinsular"],["not_evaluated","No evaluable"]] as const;
const labels: Record<ContextLayer,{label:string;unit:string;method:string}> = {
 accessibility:{label:"Accesibilidad pediátrica · 2024",unit:"minutos",method:"fixed_thresholds"},
 income:{label:"Renta media por persona · 2023",unit:"€/persona",method:"quantile"},
 density:{label:"Densidad infantil · 2024",unit:"niños/km²",method:"quantile"},
 degurba:{label:"Urbanización DEGURBA · 2021",unit:"categoría dominante",method:"categorical"},
 pediatricians_ap:{label:"Pediatras AP",unit:"profesionales",method:"equal_interval"},
 pediatric_frequentation:{label:"Frecuentación pediátrica",unit:"consultas/persona/año",method:"equal_interval"},
 preterm_rate:{label:"Prematuridad",unit:"%",method:"fixed_thresholds"},
 PM10:{label:"PM10 observado · 2025",unit:"µg/m³",method:"fixed_thresholds"},
 "PM2.5":{label:"PM2,5 observado · 2025",unit:"µg/m³",method:"fixed_thresholds"},
 NO2:{label:"NO₂ observado · 2025",unit:"µg/m³",method:"fixed_thresholds"}
};
export function MapLegend({layer="accessibility",year,breaks=[]}:{layer?:ContextLayer;year?:number;breaks?:number[]}){
 if(layer==="accessibility") return <div className="legend" aria-label="Leyenda de tiempo estimado">{legendItems.map(([key,label])=><span key={key}><i className={"swatch swatch-"+key}/>{label}</span>)}</div>;
 if(layer==="degurba") return <div className="legend context-legend" aria-label="Leyenda Urbanización DEGURBA"><strong>Urbanización DEGURBA · 2021 · categorical</strong>{[["#385e8d","Centro urbano"],["#6f91b8","Agrupación urbana"],["#c9a662","Rural"]].map(([color,label])=><span key={label}><i className="swatch" style={{background:color}}/>{label}</span>)}</div>;
 const selected=labels[layer],colors=["#d9e2f2","#9eb8d7","#607fae","#3f326d"];
 const text=(index:number)=>index===0?(breaks[0]===undefined?"Dato observado":"< "+breaks[0].toLocaleString("es-ES")):index===colors.length-1?(breaks[index-1]===undefined?"":"≥ "+breaks[index-1].toLocaleString("es-ES")):(breaks[index-1]?.toLocaleString("es-ES")??"")+"–"+(breaks[index]?.toLocaleString("es-ES")??"");
 return <div className="legend context-legend" aria-label={"Leyenda "+selected.label}><strong>{selected.label}{year?" · "+year:""} · {selected.method}</strong>{colors.map((color,index)=><span key={color}><i className="swatch" style={{background:color}}/>{text(index)} {selected.unit}</span>)}</div>;
}
