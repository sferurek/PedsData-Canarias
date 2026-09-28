import Link from "next/link";
export default function NotFound(){return <div className="page-state"><span className="eyebrow">Error 404</span><h1>Página no encontrada</h1><p>La ruta solicitada no existe o no forma parte de los datos validados.</p><Link className="primary-link" href="/">Volver al inicio</Link></div>}
