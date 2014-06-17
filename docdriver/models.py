__author__ = 'fpliger'
from mako.template import Template
import datetime

class ModelBase(object):
    missing_attr_marker = '---'
    def __init__(self, replace_missing_attr=False, **kws):
        print 'setting, ', self, kws
        self.replace_missing_attr = replace_missing_attr
        map(lambda k, v: setattr(self, k, v), *zip(*kws.items()))
        self._initialize(**kws)

    def __getattr__(self, item):
        print self, item, self.__dict__.keys()
        value = self.__dict__.get(item, self.missing_attr_marker)

        if value == self.missing_attr_marker:
            print 'checking', self, self.replace_missing_attr
            if self.replace_missing_attr:
                return self.missing_attr_marker

            else:
                raise AttributeError(item)

        return value

    def setattr_from_str(self, txt):
        """
        Gets a string with the key=value format and sets the key attr to value

        i.e.:
        >>> model = ModelBase()
        >>> model.setattr_from_str('name=Bob')
        >>> model.name
            Bob
        """
        k, v = txt.strip().split('=')
        currvalue = getattr(self, k, u'')
        setattr(self, k, currvalue + v)
        print "just set", self, k, currvalue + v

    def _initialize(self, **kws):
        """Overwrite me to define model custom initialization"""
        pass


class Document(ModelBase):
    def __init__(self, test_cases=None):
        self.test_cases = test_cases

    def render(self, template, output=None):
        _templ = Template(filename=template)
        now = datetime.datetime.now()

        rendered = _templ.render(document=self, printing_timestamp=now)
        if output:
            with file(output, 'w') as fo:
                fo.write(rendered)

        return rendered


class TestCase(ModelBase):
    def _initialize(self, **kws):
        self.steps = []
        self.lines = []


class TestStep(ModelBase):
    pass
