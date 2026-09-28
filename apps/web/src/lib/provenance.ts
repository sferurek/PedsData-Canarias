import sourcesRaw from "@/data/sources-catalog.json";
import {metricById} from "./semantic";
export type SourceDefinition={source_id:string;name:string;organization:string;domain:string;description:string;contains:string;universe_age:string;geographic_disaggregation:string;available_period:string;update_frequency:string;format:string;license:string;version_used:string;integration_status:string;last_acquired_at:string;official_url:string;used_in:string[];checksum:string|null};
export const sources=(sourcesRaw as {sources:SourceDefinition[]}).sources;
export function sourceById(id:string){return sources.find(source=>source.source_id===id)}
export function sourcesForMetric(metricId:string){const metric=metricById(metricId);return (metric?.source_ids??[]).map(sourceById).filter(Boolean) as SourceDefinition[]}
export function traceHref(metricId:string,params:Record<string,string|number|undefined>={}){
 const query=new URLSearchParams();
 Object.entries(params).forEach(([key,value])=>{if(value!==undefined)query.set(key,String(value))});
 const suffix=query.toString();return "/trazabilidad/"+encodeURIComponent(metricId)+(suffix?"?"+suffix:"");
}
