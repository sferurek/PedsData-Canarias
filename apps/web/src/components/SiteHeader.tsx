import Link from "next/link";

const links=[
 ["/#mapa","Accesibilidad"],["/#entorno","Entorno"],
 ["/#desigualdad","Desigualdad"],["/resultados","Resultados"],
 ["/utilizacion","Utilización"],["/prevencion","Prevención"],
 ["/adolescencia","Adolescencia"],["/#islas","Islas"],
 ["/utilizacion#research","Research"],["/#metodologia","Método"]
];

export function SiteHeader(){
 return <header className="site-header">
  <Link className="brand" href="/" aria-label="PedsData Canarias, inicio">
   <span className="brand-mark">P</span><span>PedsData <b>Canarias</b></span>
  </Link>
  <nav className="desktop-nav" aria-label="Navegación principal">
   {links.map(([url,label])=><Link key={url} href={url}>{label}</Link>)}
  </nav>
  <details className="mobile-navigation"><summary>Explorar</summary>
   <nav aria-label="Navegación móvil">
    {links.map(([url,label])=><a key={url} href={url}>{label}</a>)}
   </nav>
  </details>
  <span className="rc-badge">RC4.1 · preview</span>
 </header>;
}
