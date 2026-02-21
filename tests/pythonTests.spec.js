const {test, expect} = require('@playwright/test');
const {chromium} = require('@playwright/test');

test("smoke: demo test runs", async ({page}) => {
    const env = process.env.ENV || "staging";

    await page.goto("https://example.com");

    await expect(page).toHaveTitle(/Example Domain/);
});