"use client";
import type {ChartType,MetricDefinition,TimePoint} from "@/lib/semantic";
import {islandLabels} from "@/lib/semantic";

const COLORS=["#176b68","#7d62a3","#dc765e","#2d6d96","#a87924","#3f7b52","#8b4f6c"];
const nf=new Intl.NumberFormat("es-ES",{maximumFractionDigits:2});
function seriesKey(point:TimePoint){return point.metric_id+"|"+point.geography_id+(point.dimension?"|"+point.dimension:"")}
function seriesLabel(key:string,metrics:MetricDefinition[]){const [metric,geo,dimension]=key.split("|");const def=metrics.find(item=>item.metric_id===metric);return [def?.label,islandLabels[geo]??geo,dimension].filter(Boolean).join(" · ")}
function extent(values:number[]){const min=Math.min(...values),max=Math.max(...values);return min===max?[min-1,max+1]:[min,max]}
function Empty(){return <div className="viz-empty" role="status">No hay observaciones para esta selección.</div>}

export function SemanticChart({points,metrics,type="line"}:{points:TimePoint[];metrics:MetricDefinition[];type?:ChartType}){
 if(!points.length)return <Empty/>;
 if(type==="table")return <div className="table-scroll semantic-table"><table><thead><tr><th>Territorio</th><th>Indicador</th><th>Periodo</th><th>Valor</th><th>Estado</th></tr></thead><tbody>{points.map((point,index)=><tr key={seriesKey(point)+"-"+point.period+"-"+index}><td>{islandLabels[point.geography_id]??point.geography_id}</td><td>{metrics.find(item=>item.metric_id===point.metric_id)?.label??point.metric_id}</td><td>{point.period}</td><td>{nf.format(point.value)} {point.unit}</td><td>{point.status}</td></tr>)}</tbody></table></div>;
 if(type==="small_multiples"){
  const groups=Object.groupBy(points,point=>point.geography_id);
  return <div className="small-multiples">{Object.entries(groups).map(([geo,items])=><article key={geo}><h3>{islandLabels[geo]??geo}</h3><SemanticChart points={items??[]} metrics={metrics} type="line"/></article>)}</div>;
 }
 if(type==="heatmap"){
  const periods=[...new Set(points.map(point=>point.period))].sort();
  const geos=[...new Set(points.map(point=>point.geography_id))];
  const [min,max]=extent(points.map(point=>point.value));
  const color=(value:number)=>{const ratio=(value-min)/(max-min);return "color-mix(in srgb, #176b68 "+Math.round(25+ratio*70)+"%, #f1eee5)"};
  return <div className="heatmap-wrap"><div className="heatmap" style={{gridTemplateColumns:"120px repeat("+periods.length+", minmax(34px,1fr))"}}><span/>{periods.map(period=><b key={period}>{period.slice(0,4)}</b>)}{geos.flatMap(geo=>[<strong key={geo+"-label"}>{islandLabels[geo]??geo}</strong>,...periods.map(period=>{const item=points.find(point=>point.geography_id===geo&&point.period===period);return <span key={geo+"-"+period} title={item?nf.format(item.value)+" "+item.unit:"Sin dato"} style={{background:item?color(item.value):"#e2e3dc"}}>{item?nf.format(item.value):"—"}</span>})])}</div></div>;
 }
 if(type==="scatter"&&metrics.length>1){
  const [first,second]=metrics;const matched:Record<string,{x?:TimePoint;y?:TimePoint}>={};
  for(const point of points){const key=point.geography_id+"|"+point.period;matched[key]??={};if(point.metric_id===first.metric_id)matched[key].x=point;if(point.metric_id===second.metric_id)matched[key].y=point}
  const pairs=Object.values(matched).filter(item=>item.x&&item.y) as {x:TimePoint;y:TimePoint}[];
  if(!pairs.length)return <Empty/>;
  const [xmin,xmax]=extent(pairs.map(item=>item.x.value)),[ymin,ymax]=extent(pairs.map(item=>item.y.value));
  return <svg className="semantic-chart" viewBox="0 0 760 360" role="img" aria-label={"Dispersión de "+first.label+" y "+second.label}><line x1="70" y1="310" x2="730" y2="310"/><line x1="70" y1="25" x2="70" y2="310"/>{pairs.map((item,index)=>{const x=70+(item.x.value-xmin)/(xmax-xmin)*660,y=310-(item.y.value-ymin)/(ymax-ymin)*285;return <circle key={index} cx={x} cy={y} r="5" fill={COLORS[index%COLORS.length]}><title>{`${islandLabels[item.x.geography_id]} · ${item.x.period}: ${nf.format(item.x.value)} / ${nf.format(item.y.value)}`}</title></circle>})}<text x="400" y="350" textAnchor="middle">{first.label}</text><text x="18" y="170" transform="rotate(-90 18 170)" textAnchor="middle">{second.label}</text></svg>;
 }
 const grouped=Object.groupBy(points,seriesKey);
 const periods=[...new Set(points.map(point=>point.period))].sort();
 const latest=periods.at(-1)!;
 if(type==="bar"){
  const values=points.filter(point=>point.period===latest);const max=Math.max(...values.map(point=>point.value));
  return <div className="bar-chart" role="img" aria-label={"Comparación en "+latest}>{values.map((point,index)=><div key={seriesKey(point)}><span>{islandLabels[point.geography_id]??point.geography_id}</span><i><b style={{width:(point.value/max*100)+"%",background:COLORS[index%COLORS.length]}}/></i><strong>{nf.format(point.value)} <small>{point.unit}</small></strong></div>)}</div>;
 }
 const [min,max]=extent(points.map(point=>point.value));const x=(period:string)=>periods.length===1?390:60+periods.indexOf(period)/(periods.length-1)*670;const y=(value:number)=>310-(value-min)/(max-min)*270;
 return <div><svg className="semantic-chart" viewBox="0 0 760 350" role="img" aria-label={"Serie temporal: "+metrics.map(metric=>metric.label).join(" y ")}><line x1="60" y1="310" x2="730" y2="310"/><line x1="60" y1="40" x2="60" y2="310"/><text x="60" y="335">{periods[0].slice(0,4)}</text><text x="730" y="335" textAnchor="end">{latest.slice(0,4)}</text><text x="52" y="45" textAnchor="end">{nf.format(max)}</text><text x="52" y="310" textAnchor="end">{nf.format(min)}</text>{Object.entries(grouped).map(([key,items],index)=>{const sorted=(items??[]).slice().sort((a,b)=>a.period.localeCompare(b.period));const d=sorted.map((point,i)=>(i?"L":"M")+x(point.period)+" "+y(point.value)).join(" ");return <g key={key}><path d={d} fill="none" stroke={COLORS[index%COLORS.length]} strokeWidth="3"/>{sorted.map(point=><circle key={point.period} cx={x(point.period)} cy={y(point.value)} r="3.5" fill={COLORS[index%COLORS.length]}><title>{`${seriesLabel(key,metrics)} · ${point.period}: ${nf.format(point.value)} ${point.unit}`}</title></circle>)}</g>})}</svg><div className="chart-legend">{Object.keys(grouped).map((key,index)=><span key={key}><i style={{background:COLORS[index%COLORS.length]}}/>{seriesLabel(key,metrics)}</span>)}</div></div>;
}
