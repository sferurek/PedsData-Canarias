import { expect, test } from "@playwright/test";

const islands = ["El Hierro", "La Gomera", "La Palma", "Tenerife", "Gran Canaria", "Fuerteventura", "Lanzarote"];

test("home exposes seven islands, bands and provenance", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Salud infantil/i })).toBeVisible();
  for (const island of islands) await expect(page.getByRole("heading", { name: island, exact: true })).toBeVisible();
  await page.locator("#mapa").scrollIntoViewIfNeeded();
  await expect(page.getByLabel("Mapa temático pediátrico de Canarias")).toBeVisible();
  await expect(page.getByText("Transferencia interinsular", { exact: true })).toBeVisible();
  await expect(page.getByText("Fuente y metodología").first()).toBeVisible();
  await expect(page.getByText(/Perfiles ZBS no publicados/i)).toBeVisible();
});

test("island filters and profiles remain navigable", async ({ page }) => {
  await page.goto("/#mapa");
  await page.locator("#mapa").scrollIntoViewIfNeeded();
  const islandFilter = page.getByLabel("Ámbito insular");
  await islandFilter.selectOption("el-hierro");
  await expect(islandFilter).toHaveValue("el-hierro");
  for (const slug of ["el-hierro", "la-gomera", "la-palma", "tenerife", "gran-canaria", "fuerteventura", "lanzarote"]) {
    await page.goto(`/islas/${slug}`);
    await expect(page.getByText("Perfil insular · acceso potencial")).toBeVisible();
    await expect(page.getByText("Fuente y metodología").first()).toBeVisible();
  }
});

test("Lanzarote treats La Graciosa as transfer, never a road time", async ({ page }) => {
  await page.goto("/islas/lanzarote");
  await expect(page.getByText("Transferencia interinsular requerida; tiempo terrestre no estimado.")).toBeVisible();
  await expect(page.getByText(/91 niños permanecen fuera del denominador evaluable/i)).toBeVisible();
});

test("small municipality keeps its profile but withholds detailed indicators", async ({ page }) => {
  await page.goto("/municipios/35007");
  await expect(page.getByRole("heading", { name: "Betancuria" })).toBeVisible();
  await expect(page.getByRole("heading", { name: /Detalle no publicable/i })).toBeVisible();
  await expect(page.getByText(/umbral conservador de 100/i)).toBeVisible();
});

test("visual QA has no horizontal clipping across home and seven profiles", async ({ page }, testInfo) => {
  await page.goto("/");
  await page.locator("#mapa").scrollIntoViewIfNeeded();
  await expect(page.locator(".map-shell")).toBeVisible();
  await expect(page.getByText("Cargando capa validada…")).toBeHidden({ timeout: 15000 });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1)).toBe(true);
  await page.screenshot({ path: `test-results/phase3-home-${testInfo.project.name}.png`, fullPage: true });
  await page.locator(".map-shell").screenshot({ path: `test-results/phase3-map-${testInfo.project.name}.png` });
  for (const slug of ["el-hierro", "la-gomera", "la-palma", "tenerife", "gran-canaria", "fuerteventura", "lanzarote"]) {
    await page.goto(`/islas/${slug}`);
    await expect(page.locator("h1")).toBeVisible();
    await expect(page.getByText("Cargando capa validada…")).toBeHidden({ timeout: 15000 });
    await page.waitForTimeout(650);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1)).toBe(true);
    if (testInfo.project.name === "desktop") await page.locator(".map-shell").screenshot({ path: `test-results/phase3-map-${slug}.png` });
  }
});


test("social and environmental layers remain navigable", async ({ page }) => {
  await page.goto("/#mapa");
  await page.locator("#mapa").scrollIntoViewIfNeeded();
  const layer = page.getByLabel("Capa principal", { exact: true });
  await layer.selectOption("income");
  await expect(page.getByText(/Renta media por persona/)).toBeVisible();
  await layer.selectOption("PM10");
  await expect(page.getByText(/PM10 observado/)).toBeVisible();
  await layer.selectOption("accessibility");
  await expect(page.getByText("Transferencia interinsular", { exact: true })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Meteorología y calima" })).toBeVisible();
});

test("municipal context keeps scale and provenance visible", async ({ page }) => {
  await page.goto("/municipios/35001");
  await expect(page.getByText("Renta por persona")).toBeVisible();
  await expect(page.getByText("Densidad infantil")).toBeVisible();
  await expect(page.getByText("Fuente y metodología").first()).toBeVisible();
});


test("clinical outcomes preserve geography and status", async ({ page }, testInfo) => {
  await page.goto("/resultados");
  await expect(page.getByRole("heading", { name: /Clínica con escala explícita/i })).toBeVisible();
  await expect(page.getByText(/Estos datos no permiten comparar islas/i)).toBeVisible();
  await page.getByLabel("Grupo diagnóstico").selectOption("asthma");
  await page.getByLabel("Edad hospitalización").selectOption("Y5T14");
  await expect(page.getByText("SURVEY_ESTIMATE", { exact: true })).toBeVisible();
  await expect(page.getByText(/Suprimido 1–4/).first()).toBeVisible();
  await expect(page.getByText("Fuente y metodología").first()).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1)).toBe(true);
  await page.screenshot({ path: `test-results/phase5-clinical-${testInfo.project.name}.png`, fullPage: true });
});

test("island and municipal profiles do not invent clinical geography", async ({ page }) => {
  await page.goto("/islas/el-hierro");
  await expect(page.getByRole("heading", { name: /Perinatalidad y mortalidad segura/i })).toBeVisible();
  await expect(page.getByText(/Hospitalización pediátrica disponible únicamente a nivel Canarias/i)).toBeVisible();
  await page.goto("/municipios/35001");
  await expect(page.getByText(/No se imputan hospitalización, mortalidad, prematuridad ni encuesta/i)).toBeVisible();
});
