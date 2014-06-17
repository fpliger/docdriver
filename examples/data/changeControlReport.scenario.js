"use strict";

var urlParse = require('url');
var utils = require('./utilities');
var backendDb = require('../lib/backendDB.js');
var changeReport = require('./pages/changecontrolreport.page');
var changeReportDetail = require('./pages/changecontrolreportdetail.page');

describe('Change control report', function(){

  var first = true,
    session = new utils.MySession();

  beforeEach(function () {
    if (first) {
      waitsFor(backendDb.reset, 'database to reset', 30000);
      first = false;
    }
    runs(function () {
      session.ensureLoggedIn('testuser1@getzendoc.com', 'password', changeReport.url);
    });
  });
  
  it('has options open, closed and all for filtering', function(){
    element.all(by.css('.filter option')).then(function(options){
      expect(options.length).toEqual(3);
      expect(options[0].getText()).toBe('all');
      expect(options[0].getAttribute('value')).toBe('all');
      expect(options[1].getText()).toBe('open');
      expect(options[1].getAttribute('value')).toBe('open');
      expect(options[2].getText()).toBe('closed');
      expect(options[2].getAttribute('value')).toBe('closed');
    });
  });

  it('filtering shows relevant reports', function(){
  });

  it('table has 5 columns', function(){
    expect(element.all(by.css('th')).count()).toEqual(5);
    expect(changeReport.referenceHeading().getText()).toBe('Reference');
    expect(changeReport.documentHeading().getText()).toBe('Document');
    expect(changeReport.createdHeading().getText()).toBe('Created');
    expect(changeReport.closedHeading().getText()).toBe('Closed');
    expect(changeReport.authorHeading().getText()).toBe('Author');
  });

  it('clicking on table headers sorts rows', function(){
    expect(changeReport.referenceTdOne().getText()).toBe('CC-7');  
    expect(changeReport.documentTdOne().getText()).toBe('doc4');  
    expect(changeReport.createdTdOne().getText()).toBe('2014-03-25');  
    changeReport.referenceHeading().click();
    expect(changeReport.referenceTdOne().getText()).toBe('CC-1');  
    changeReport.referenceHeading().click();
    expect(changeReport.referenceTdOne().getText()).toBe('CC-7');  
    changeReport.documentHeading().click();
    expect(changeReport.documentTdOne().getText()).toBe('doc1');  
    changeReport.documentHeading().click();
    expect(changeReport.documentTdOne().getText()).toBe('Test review process'); 
    changeReport.createdHeading().click();
    expect(changeReport.createdTdOne().getText()).toBe('2014-03-25');  
    changeReport.createdHeading().click();
    expect(changeReport.createdTdOne().getText()).toBe('2014-03-25');  
  });

  it('clicking on cc reference navigates to cc detail page', function(){
    changeReport.ccLinkOne().click();
    browser.getCurrentUrl().then(function(url) {
      expect(urlParse.parse(url, true).path).toBe('/reports/change_control/CC-1-7');
    });
  });

  it('clicking on doc title navigates to doc view page', function(){
    changeReport.docLinkOne().click();
    browser.getCurrentUrl().then(function(url) {
      expect(urlParse.parse(url, true).path).toBe('/workspace/documents/123');
    });
  });

});
