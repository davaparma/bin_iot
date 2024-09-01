const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
 
  await page.goto(`file://${process.cwd()}/hello_sit223.html`);
  

  const content = await page.$eval('h1', el => el.textContent);
  console.log('Running test to check correct header');
  
  if (content === 'Hello SIT223!') {
    console.log('Test passed!');
    process.exit(0); 
  } else {
    console.error('Test failed!');
    process.exit(1); 
  }

  await browser.close();
})();
