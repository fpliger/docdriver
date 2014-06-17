
import docdriver


class TestParser:
    def setup(self):
        self.parser = docdriver.Parser()

    def test_parse_doc(self, monkeypatch, tmpdir):
        txt = '''describe('homepage login page', function () {
  /*
  %testcase%
  %testcase% title=Test User Login
  %testcase% description=This should test that user login works well when user provides correct credentials

  */
  var session = new utils.MySession(),

    it('redirects to desired state after login', function () {

        var targetUrl = '/home;
        browser.get(targetUrl);
        /*
        %teststep%
        %teststep% description=Access login page
        %teststep% aspected_result=The user login pate with email/ password text boxes displays
        */
        browser.getCurrentUrl().then(function(url) {
          expect(urlParse.parse(url, true).path).toBe('/login');
        });
        /*
        %teststep%
        %teststep% description=Type in valid user credentials in the email/ password text boxes
        */
        loginPage.emailField().sendKeys('johndoe@gmail.com');
        loginPage.passwordField().sendKeys('password');
        loginPage.submitButton().click();

        // %teststep% aspected_result=User gets redirected to his homepage view
        browser.getCurrentUrl().then(function(url) {
          expect(urlParse.parse(url, true).path).toBe(targetUrl);
        });
      })

    runs(function () {
      session.ensureLoggedIn('johndoe@gmail.com');
    });

  });
'''
        test_cases = self.parser.parse(txt)

        #assert len(test_cases) == 1

        test_case = test_cases.next()
        assert test_case.title == 'Test User Login'
        assert test_case.description == 'This should test that user login ' \
                                        'works well when user provides correct' \
                                        ' credentials'

        t1, t2 = test_case.steps

        assert t1.description == 'Access login page'
        assert t1.aspected_result == 'The user login pate with email/ password text boxes displays'


        assert t2.description == 'Type in valid user credentials in the email/ password text boxes'
        assert t2.aspected_result == 'User gets redirected to his homepage view'

    def test_parse_test_case(self, monkeypatch):
        pass

    def test_parse_test_step(self, monkeypatch, tmpdir):
        pass

