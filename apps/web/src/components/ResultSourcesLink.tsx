import Link from "next/link";
import {traceHref} from "@/lib/provenance";
export function ResultSourcesLink({metricId,result,period,geography,className=""}:{metricId:string;result?:string;period?:string|number;geography?:string;className?:string}){
 return <Link className={"result-sources-link "+className} href={traceHref(metricId,{result,period,geography})}>Fuentes de este resultado <span aria-hidden="true">↗</span></Link>;
}
