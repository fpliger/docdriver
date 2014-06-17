import docdriver
from py.path import local

import click

@click.command()
@click.option('--testsdir',
              prompt='Test folder to parse',
              default='data',
              help='Path to the folder containing the test files to parse'
)
@click.option('--test_files_extension',
            prompt='Extension of the tests files to parse',
              default="*.js",
              help='extension of the tests files to parse'
)
@click.option('--output_file_template',
              prompt='template file to use',
              default='testdoc_template.html',
              help='''Path to the template file to use to generate output

NOTE: docdriver only supports mako templates for now...'''
)
@click.option('--output_file',
              prompt='Output file',
              default='testcases_report.html',
              help='Path to the output file',
)
def parse_tests(
        testsdir='data',
        test_files_extension="*.js",
        output_file_template='testdoc_template.html',
        output_file='testcases_report.html'
    ):

    datadir = local(testsdir)

    parser = docdriver.Parser()

    for testfile in datadir.listdir(test_files_extension):
        print 'parsing file ', testfile

        testdoc = docdriver.Document(parser.parse_file(str(testfile)))
        content = testdoc.render(output_file_template, output_file)

    print 'done'

if __name__ == '__main__':
    parse_tests()