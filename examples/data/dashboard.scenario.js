/2 global describe, beforeEach, browser, element, by, it, expect */

'use strict';

var urlParse = require('url');
var utils = require('./utilities');
var backendDb = require('../lib/backendDB.js');

describe('dashboard page', function () {


  it('redirects to desired state after login', function () {
    var targetUrl = '/home';

   /*
  %testcase%
  %testcase% title=Test User Dashboard
  %testcase% description=Tests if user is redirected to dashboard after login in
  */

    /*
    %ts%
    %ts% description=try to access homepage
    %ts% expected_result=The user login page with email/ password text boxes
    %ts% expected_result=displays as user is not logged in with a proper session
    */
    browser.get(targetUrl);
    browser.getCurrentUrl().then(function(url) {
      expect(urlParse.parse(url, true).path).toBe('/login');
    });

    /*
    %teststep%
    %teststep% description=Insert valid username and password in the related page
    %teststep% description=fields and click the 'login' link button
    */

    loginPage.emailField().sendKeys('testuser1@getzendoc.com');
    loginPage.passwordField().sendKeys('password');
    loginPage.submitButton().click();
    // Fixed sleep here because it's using regular POST (not ajax / angular thing)
    browser.sleep(1000);


    // %teststep% expected_result=The user is redirected to his related dashboard page
    browser.getCurrentUrl().then(function(url) {
      expect(urlParse.parse(url, true).path).toBe(targetUrl);
    });
  })


  it('should not navigate and display error if email incorrect', function () {
  /*
  %testcase%
  %testcase% title=Test user credentials check (prevent access with wrong emails)
  %testcase% description=Tests login negative case of when user tries to access the system
  %testcase% description=with a wrong email. The test should ensure that user receives a
  %testcase% description=message informing that email user is incorrect
  */

    /*
    %ts%
    %ts% description=try to access homepage
    %ts% expected_result=The user login page with email/ password text boxes
    %ts% expected_result=displays as user is not logged in with a proper session
    */
    var targetUrl = '/home';

    browser.get(targetUrl);
    browser.getCurrentUrl().then(function(url) {
      expect(urlParse.parse(url, true).path).toBe('/login');
    });


    /*
    %ts%
    %ts% description=Insert invalid email and a valid password
    %ts% description=in the related page fields and click the
    %ts% description='login' link button
    */
    var error = element(by.binding('errors.email'));
    loginPage.emailField().sendKeys('wrong@getzendoc.com');
    loginPage.passwordField().sendKeys('password');
    element(by.id('login-btn')).click();

    /*
    %teststep% expected_result=The user sees a message box with the following
    %teststep% expected_result=message: 'This email address is not registered'
    */
    browser.getCurrentUrl().then(function(url){
      expect(urlParse.parse(url, true).path).toBe('/login');
      expect(error.getText()).toEqual('This email address is not registered');
    });
  });

  it('should not navigate and display error if password incorrect', function () {
    browser.get('/login');
    var error = element(by.binding('errors.password'));
    loginPage.emailField().sendKeys('testuser1@getzendoc.com');
    loginPage.passwordField().sendKeys('cobbler');
    element(by.id('login-btn')).click();
    browser.getCurrentUrl().then(function(url){
      expect(urlParse.parse(url, true).path).toBe('/login');
      expect(error.getText()).toEqual('Incorrect password');
    });
  });
});
