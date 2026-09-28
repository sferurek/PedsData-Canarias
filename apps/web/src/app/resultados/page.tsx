import type {Metadata} from "next";
import {ClinicalExplorer} from "@/components/ClinicalExplorer";
import {SourceMethodPanel} from "@/components/SourceMethodPanel";
import {BDCAPExplorer} from "@/components/BDCAPExplorer";
export const metadata:Metadata={title:"Resultados de salud",description:"Hospitalización, perinatalidad, urgencias, mortalidad y Encuesta de Salud infantil con comparabilidad explícita."};
export default function OutcomesPage(){return <><section className="clinical-hero"><span className="eyebrow">Resultados de salud · RC4.1</span><h1>Clínica con<br/><em>escala explícita.</em></h1><p>Hospitalización, utilización y resultados pediátricos conservan la edad, geografía, periodo y definición de cada fuente.</p><nav aria-label="Dominios clínicos"><a href="#hospitalizacion">Hospitalización</a><a href="#bdcap">BDCAP</a><a href="#urgencias">Urgencias</a><a href="#perinatal">Perinatal</a><a href="#mortalidad">Mortalidad</a></nav></section><div className="clinical-shell"><ClinicalExplorer/><BDCAPExplorer/><SourceMethodPanel/></div></>}
