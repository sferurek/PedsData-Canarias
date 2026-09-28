# Configuración Vercel — beta pública

Auditoría: 28/09/2026.

| Campo | Valor validado |
|---|---|
| Team/scope | `sferureks-projects` |
| Proyecto | `web` (`prj_3LHGO4uW0PKuJyv8xHABUyRXFSK8`) |
| Repositorio | `sferurek/PedsData-Canarias` |
| Production Branch | `main` |
| Root Directory | `apps/web` |
| Framework | Next.js |
| Node | 24.x |
| Variables de entorno | ninguna |
| GitHub integration | activa |
| Preview protection | Vercel Authentication |

## Incidencia corregida

GitHub desplegaba desde la raíz del monorepo y no encontraba Next.js. Se fijó `rootDirectory=apps/web`; el preview de PR #2 volvió a estado `Ready` y el check Vercel pasó.

## Política de apertura

Los previews permanecen protegidos. Vercel Authentication quedó fijada en `deploymentType=preview`: protege previews y deja producción accesible. No se promueve un preview anterior ni se reutiliza un alias de RC. La producción `https://web-sferureks-projects.vercel.app` se verificó con `curl` sin bypass en Home, sitemap, robots y rutas críticas; 11 rutas devolvieron HTTP 200.
