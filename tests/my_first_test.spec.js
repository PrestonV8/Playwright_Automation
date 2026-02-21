const {test, expect} = require('@playwright/test')
// const {hello, helloworld} = require('./demo/hello')
import {hello, helloworld} from './demo/hello'

console.log(hello());
console.log(helloworld());

/*
 * 'async' before a function makes the function return a promise (not happening at the same time)
 * 'await' before a function makes the function wait for a promise 
 */

// 'goto' is to enter a website page

// test block: browser test
test('My first test ', async ({page}) => {
    
    await page.goto('http://google.com') 
    await expect(page).toHaveTitle('Google')
})