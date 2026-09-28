import {formatNumber} from "@/lib/format";
import {metricById} from "@/lib/semantic";
import {ResultSourcesLink} from "./ResultSourcesLink";
export function Metric({label,value,metricId,suffix,detail,period,geography}:{label:string;value:number|null|undefined;metricId:string;suffix?:string;detail?:string;period?:string|number;geography?:string}){
 const metric=metricById(metricId);if(!metric?.source_ids.length)return null;
 const rendered=value===null||value===undefined?"No disponible":formatNumber(value,1)+(suffix??"");
 return <div className="metric"><span className="metric-label">{label}</span><strong className="metric-value">{rendered}</strong>{detail&&<span className="metric-detail">{detail}</span>}<ResultSourcesLink metricId={metricId} result={label+": "+rendered} period={period} geography={geography}/></div>
}
