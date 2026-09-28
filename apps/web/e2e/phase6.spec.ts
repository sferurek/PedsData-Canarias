import {test,expect} from "@playwright/test";
test("phase6 utilization preserves seven islands, filters and regional stock",async({page})=>{
 await page.goto("/utilizacion");
 await expect(page.getByRole("heading",{name:"Pediatría AP",exact:true})).toBeVisible();
 expect(await page.getByLabel("Isla SIAP").locator("option").count()).toBe(7);
 for(const island of ["el-hierro","la-gomera","la-palma","tenerife","gran-canaria","fuerteventura","lanzarote"]){await page.getByLabel("Isla SIAP").selectOption(island);await expect(page.getByTestId("siap-value")).not.toHaveText("No disponible");}
 await page.getByLabel("Año SIAP").selectOption("2007");
 await page.getByLabel("Lugar de consulta").selectOption("TELECONSULTA");
 await expect(page.getByTestId("siap-value")).toHaveText("No disponible");
 await page.getByLabel("Indicador SIAP").selectOption("frequentation");
 await expect(page.getByLabel("Lugar de consulta")).toBeDisabled();
 await page.getByLabel("Lista pediátrica").selectOption("surgical:CIRUGIA_PEDIATRICA");
 await expect(page.getByText(/Publicación insular en HOLD/)).toBeVisible();
 await page.getByLabel("Comparación Research V2").selectOption("distinct_persons");
 await page.getByText("Fuente y metodología",{exact:true}).first().click();
 await expect(page.getByRole("link",{name:"CSV oficial del indicador"})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
 await page.screenshot({path:"test-results/phase6-utilization-"+test.info().project.name+".png",fullPage:true});
});
test("phase6 adolescence and prevention keep admission boundaries",async({page})=>{
 await page.goto("/adolescencia");
 await page.getByLabel("Indicador HBSC").selectOption("perceived_health");
 await expect(page.getByRole("cell",{name:"17–18 años",exact:true})).toBeVisible();
 await expect(page.getByText(/ESdE y ESTUDES permanecen en HOLD/)).toBeVisible();
 await page.getByText("Fuente y metodología",{exact:true}).click();
 await expect(page.getByRole("link",{name:"Informe oficial HBSC"})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
 await page.screenshot({path:"test-results/phase6-adolescence-"+test.info().project.name+".png",fullPage:true});
 await page.goto("/prevencion");await expect(page.getByRole("heading",{name:"Vacunación",exact:true})).toBeVisible();
 await expect(page.getByText(/No se integra ningún porcentaje/)).toBeAttached();
});
test("mobile navigation reaches new modules",async({page},info)=>{test.skip(info.project.name!=="iphone");await page.goto("/");await page.getByText("Explorar",{exact:true}).click();await page.getByRole("navigation",{name:"Navegación móvil"}).getByRole("link",{name:"Utilización",exact:true}).click();await expect(page).toHaveURL(/utilizacion/);});
