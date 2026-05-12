const { test, expect } = require("@playwright/test");

test.use({ channel: "chrome" });

test("published site works in local Google Chrome", async ({ page }) => {
  await page.goto("https://ultima-ideia-vercel-deploy.vercel.app/", {
    waitUntil: "networkidle",
  });

  await expect(page).toHaveTitle(/A Última Ideia/);
  await expect(page.getByRole("heading", { name: /Sua marca/i })).toBeVisible();
  await expect(page.getByText("Submeta sua ideia").first()).toBeVisible();

  const heroImage = page.locator('img[src="./assets/hero-wall-v2.png"]');
  await expect(heroImage).toBeVisible();

  await page.getByPlaceholder("Seu nome").fill("Teste Chrome");
  await page.getByPlaceholder("Seu e-mail corporativo").fill("teste@empresa.com");
  await page.getByPlaceholder("Fale sobre sua marca").fill("Marca Teste");
  await page.getByRole("button", { name: /Submeta sua ideia/i }).click();
  await expect(page.getByText("Ideia recebida")).toBeVisible();

  await page.screenshot({ path: "_qa/chrome-desktop.png", fullPage: true });
});

test("published site is usable in Chrome mobile viewport", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 1200 });
  await page.goto("https://ultima-ideia-vercel-deploy.vercel.app/", {
    waitUntil: "networkidle",
  });

  await expect(page.getByRole("heading", { name: /Sua marca/i })).toBeVisible();
  await expect(page.getByPlaceholder("Seu nome")).toBeVisible();
  await page.screenshot({ path: "_qa/chrome-mobile.png", fullPage: true });
});
