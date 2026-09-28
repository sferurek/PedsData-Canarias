import {SourcesCatalog} from "@/components/SourcesCatalog";
import {sources} from "@/lib/provenance";
export default function SourcesPage(){return <><section className="semantic-hero"><span className="eyebrow">Catálogo de fuentes</span><h1>Every number<br/><em>must be traceable.</em></h1><p>Registro de las bases utilizadas, su escala real, versión, licencia, estado y uso dentro de PedsData Canarias.</p></section><div className="semantic-shell"><SourcesCatalog sources={sources}/></div></>}
