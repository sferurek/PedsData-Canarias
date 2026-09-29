import {expect,test} from "@playwright/test";

const islands=["el-hierro","la-gomera","la-palma","tenerife","gran-canaria","fuerteventura","lanzarote"];

test("home renders seven licensed island photographs with source and license links",async({page})=>{
 await page.goto("/");
 const cards=page.locator(".island-card");
 await expect(cards).toHaveCount(7);
 await expect(page.locator("[data-territory-image]")).toHaveCount(7);
 for(const card of await cards.all()){await expect(card.locator("img")).toBeVisible();await expect(card.getByText(/^Foto:/)).toBeVisible();await expect(card.locator('.photo-credit a')).toHaveCount(2)}
});

test("island profiles and reports expose licensed hero photography",async({page})=>{
 for(const slug of islands){await page.goto(`/islas/${slug}`);await expect(page.locator(`[data-territory-image="${slug}"] img`)).toBeVisible();await expect(page.locator(".profile-hero .photo-credit")).toBeVisible()}
 await page.goto("/informes/gran-canaria");
 await expect(page.locator('[data-territory-image="gran-canaria"] img')).toBeVisible();
 await expect(page.locator(".report-hero .photo-credit")).toBeVisible();
});

test("La Graciosa has its own licensed image and keeps transfer semantics",async({page})=>{
 await page.goto("/informes/la-graciosa");
 await expect(page.locator('[data-territory-image="la-graciosa"] img')).toBeVisible();
 await expect(page.getByText("Transferencia interinsular requerida",{exact:true}).first()).toBeVisible();
 await expect(page.getByText(/No se genera un mapa de tiempo terrestre/)).toBeVisible();
});

test("visual credits catalog exposes eight originals and licenses",async({page})=>{
 await page.goto("/creditos-visuales");
 await expect(page.getByRole("heading",{name:/Créditos de las fotografías territoriales/})).toBeVisible();
 await expect(page.locator(".visual-credits-grid article")).toHaveCount(8);
 await expect(page.getByRole("link",{name:/Abrir fuente original/})).toHaveCount(8);
});

test("licensed photography remains unclipped on mobile",async({page},testInfo)=>{
 test.skip(testInfo.project.name!=="iphone");
 for(const route of ["/","/islas/el-hierro","/informes/la-graciosa","/creditos-visuales"]){await page.goto(route);expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1),route).toBe(true)}
});
