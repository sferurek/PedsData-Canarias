"use client";
export default function ErrorPage({reset}:{reset:()=>void}){return <div className="page-state" role="alert"><span className="eyebrow">Error de carga</span><h1>No pudimos cargar esta vista</h1><p>Conservamos los estados nulos y no sustituimos datos por ceros. Puedes reintentar sin perder la navegación.</p><button className="retry-button" onClick={reset}>Reintentar</button></div>}
