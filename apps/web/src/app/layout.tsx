import type {Metadata, Viewport} from "next";
import Link from "next/link";
import {Geist} from "next/font/google";
import "maplibre-gl/dist/maplibre-gl.css";
import "./globals.css";
import {SiteHeader} from "@/components/SiteHeader";

const geist=Geist({subsets:["latin"],variable:"--font-geist"});
const publicUrl="https://web-sferureks-projects.vercel.app";

export const metadata:Metadata={
 metadataBase:new URL(publicUrl),
 title:{default:"PedsData Canarias · Salud infantil con datos públicos",template:"%s · PedsData Canarias"},
 description:"Observatorio independiente de salud infantil en Canarias basado en datos públicos, metodología reproducible y trazabilidad explícita.",
 applicationName:"PedsData Canarias",
 authors:[{name:"PedsData Canarias",url:"https://github.com/sferurek/PedsData-Canarias"}],
 creator:"PedsData Canarias",
 publisher:"PedsData Canarias",
 category:"health",
 openGraph:{type:"website",locale:"es_ES",url:publicUrl,siteName:"PedsData Canarias",title:"PedsData Canarias · Beta pública",description:"Salud infantil en las siete islas con datos públicos, método reproducible y fuentes trazables.",images:[{url:"/opengraph-image",width:1200,height:630,alt:"PedsData Canarias, observatorio independiente de salud infantil"}]},
 twitter:{card:"summary_large_image",title:"PedsData Canarias · Beta pública",description:"Salud infantil en las siete islas con datos públicos y trazabilidad explícita.",images:["/opengraph-image"]},
 robots:{index:true,follow:true},
};
export const viewport:Viewport={width:"device-width",initialScale:1,themeColor:"#031522",colorScheme:"dark"};

export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="es" data-scroll-behavior="smooth"><body className={geist.variable}>
 <a className="skip-link" href="#contenido">Saltar al contenido principal</a>
 <SiteHeader/><main id="contenido" tabIndex={-1}>{children}</main>
 <footer><div className="footer-project"><strong>PedsData Canarias · Beta pública</strong><p>Proyecto independiente basado en datos públicos. No es una herramienta clínica ni implica afiliación institucional.</p></div><nav aria-label="Información legal y científica"><Link href="/aviso">Aviso</Link><Link href="/licencias">Licencias</Link><Link href="/creditos-visuales">Créditos visuales</Link><Link href="/citar">Cómo citar</Link><Link href="/fuentes">Fuentes</Link><a href="https://github.com/sferurek/PedsData-Canarias">GitHub</a></nav><p>Sin perfiles ZBS hasta disponer de geometría oficial vigente.</p></footer>
 </body></html>}
