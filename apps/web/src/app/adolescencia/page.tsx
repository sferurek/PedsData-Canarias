import {AdolescenceExplorer} from "@/components/AdolescenceExplorer";
import {Phase6BSurveys} from "@/components/Phase6BSurveys";

export const metadata={title:"Adolescencia"};

export default function Page(){
 return <><section className="clinical-hero">
  <span className="eyebrow">Adolescencia · encuestas diferenciadas</span>
  <h1>Escuchar la<br/><em>salud adolescente.</em></h1>
  <p>Hábitos y salud percibida conservando el universo de cada encuesta.</p>
 </section><div className="clinical-shell">
  <AdolescenceExplorer/>
  <Phase6BSurveys/>
 </div></>;
}
