const test = require('@playwright/test');
const { chromium } = require('@playwright/test');

test('personal test', async () => {
  const browser = await chromium.launch({
    headless: false
  });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://www.radenta.com/home/welcome');
  await page.getByRole('navigation').getByRole('link', { name: 'About Us' }).click();
  await page.getByRole('navigation').getByRole('link', { name: 'Solutions' }).click();
  await page.getByRole('navigation').getByRole('link', { name: 'Services' }).click();
  await page.getByRole('navigation').getByRole('link', { name: 'Articles' }).click();
  await page.getByRole('link', { name: 'Start 2026 Strong with Microsoft 365 Business Premium', exact: true }).click();
  await page.getByRole('link', { name: 'Radenta, Vantiq bring' }).click();

  // ---------------------
  await context.close();
  await browser.close();
});