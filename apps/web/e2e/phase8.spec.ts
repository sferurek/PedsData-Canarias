import {expect,test} from "@playwright/test";

test("temporal explorer compares registered island series with provenance",async({page})=>{
 await page.goto("/evolucion");
 await expect(page.getByText("Evolución temporal",{exact:true}).first()).toBeVisible();
 await expect(page.getByLabel("Indicador")).toBeVisible();
 await expect(page.getByText("Fuentes de este resultado").first()).toBeVisible();
 await page.goto("/comparar");
 await expect(page.getByText(/selecciona entre 1 y 7/i)).toBeVisible();
});

test("thematic map keeps one scale and exposes method",async({page})=>{
 await page.goto("/#mapa");
 await page.locator("#mapa").scrollIntoViewIfNeeded();
 const layer=page.getByLabel("Capa principal",{exact:true});
 await layer.selectOption("income");
 await expect(page.getByText(/Renta media por persona/)).toBeVisible();
 await expect(page.getByText(/quantile/).first()).toBeVisible();
 await layer.selectOption("pediatricians_ap");
 await expect(page.getByLabel("Año de la capa")).toBeEnabled();
 await layer.selectOption("PM10");
 await expect(page.getByText(/PM10 observado/)).toBeVisible();
 await layer.selectOption("accessibility");
 await expect(page.getByText("Transferencia interinsular",{exact:true})).toBeVisible();
});

test("Ask PedsData returns deterministic provenance and controlled errors",async({page})=>{
 await page.goto("/pregunta");
 await page.getByLabel("Pregunta a PedsData").fill("Evolución de pediatras en Lanzarote");
 await page.getByRole("button",{name:"Consultar"}).click();
 await expect(page.getByText("Fuentes registradas")).toBeVisible();
 await expect(page.getByText("Fuentes de este resultado").first()).toBeVisible();
 await page.getByLabel("Pregunta a PedsData").fill("Mapa de hospitalización regional por municipio");
 await page.getByRole("button",{name:"Consultar"}).click();
 await expect(page.locator(".ask-error")).toBeVisible();
});

test("source and metric registries are navigable",async({page})=>{
 await page.goto("/fuentes");
 await expect(page.getByText("Catálogo de fuentes",{exact:true}).first()).toBeVisible();
 await expect(page.getByText(/15 fuentes registradas/)).toBeVisible();
 await page.getByLabel("Dominio").selectOption("Atención Primaria");
 await expect(page.getByRole("heading",{name:"Profesionales de Atención Primaria"})).toBeVisible();
 await page.goto("/indicadores/accessibility_ap");
 await expect(page.getByText("OSRM:5.27.1",{exact:true})).toBeVisible();
 await page.getByText("Fuentes de este resultado").first().click();
 await expect(page).toHaveURL(/\/trazabilidad\/accessibility_ap/);
 await expect(page.getByRole("heading",{name:"OpenStreetMap Canarias congelado"})).toBeVisible();
});

test("mobile semantic routes do not clip",async({page},testInfo)=>{
 test.skip(testInfo.project.name!=="iphone","mobile-only check");
 for(const route of ["/evolucion","/comparar","/explorar","/pregunta","/fuentes"]){await page.goto(route);expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1)).toBe(true)}
});
