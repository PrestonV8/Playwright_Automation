const {test, expect} = require('@playwright/test');
const { chromium } = require('@playwright/test');

test('personal test real estate', async () => {
  const browser = await chromium.launch({
    headless: false
  });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://larizzare.com/');
  const page1Promise = page.waitForEvent('popup');
  await page.getByRole('link', { name: 'Go to Youtube page' }).click();
  const page1 = await page1Promise;

  // ---------------------
  await context.close();
  await browser.close();
});