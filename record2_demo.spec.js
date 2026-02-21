const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: false
  });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3Dsaucelab%26oq%3Dsaucelab%26gs_lcrp%3DEgZjaHJvbWUyBggAEEUYOdIBCDE5MDRqMGoyqAIAsAIB%26sourceid%3Dchrome%26ie%3DUTF-8%26sei%3DbEqCadyLDdui5NoPnrzJsQE&q=EhAmAQFHS4CE8LAP7S-t0e1lGOyUicwGIjApKGfSAwZZNUvUDl5FeA-b1qhNBSbVCREgt88wup2oc5RC-ztS2FxUOwXnpn51FZwyAVJaAUM');

  // ---------------------
  await context.close();
  await browser.close();
})();