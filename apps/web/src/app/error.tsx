"use client";
export default function ErrorPage({ reset }: { reset: () => void }) { return <div className="page-state" role="alert"><h1>No pudimos cargar esta vista</h1><p>Los datos no se sustituyen por valores vacíos.</p><button onClick={reset}>Reintentar</button></div>; }
