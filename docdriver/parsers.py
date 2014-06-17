
import models as mo
from py.path import local

class Parser(object):
    tokens_map = {
        '%testcase%': mo.TestCase,
        '%teststep%': mo.TestStep,
        '%tc%': mo.TestCase,
        '%ts%': mo.TestStep,
    }

    testcase_tokens = set(['%testcase%', '%tc%'])
    teststep_tokens = set(['%teststep%', '%ts%'])

    def __init__(self):
        self.nodes = []
        self.node = None

    def parse(self, txt, reset_nodes=False):
        self.node = None

        if reset_nodes:
            self.nodes = []

        return self._parse(txt)

    def parse_file(self, filepath):
        return self._parse_file(filepath)

    def _parse_file(self, filepath):
        with file(filepath, 'r') as file_to_read:
            for self.curr_line_no, chunk in enumerate(file_to_read):
                _ = self.parse_chunk(chunk)

                if self.node:
                    self.node.lines.append(chunk)

                if _:
                    # let's return the node in the with the 'replace
                    # missing attributes mode' on so when trying to
                    # accessing missing attrs we'll return a nice placeholder
                    # instead of annoying attribute errors
                    _.replace_missing_attr = True
                    map(set_replace_missing_attr, _.steps)
                    yield _

            if self.node:
                self.node.replace_missing_attr = True
                map(set_replace_missing_attr, self.node.steps)
                yield self.node

    def _parse(self, txt, splitter='\n'):
        if splitter:
            chunks = txt.split('\n')

        for self.curr_line_no, chunk in enumerate(chunks):
            _ = self.parse_chunk(chunk)

            if self.node:
                self.node.lines.append(chunk)

            if _:
                # let's return the node in the with the 'replace
                # missing attributes mode' on so when trying to
                # accessing missing attrs we'll return a nice placeholder
                # instead of annoying attribute errors
                _.replace_missing_attr = True
                map(set_replace_missing_attr, _.steps)
                yield _

        if self.node:
            self.node.replace_missing_attr = True
            map(set_replace_missing_attr, self.node.steps)
            yield self.node

    def parse_chunk(self, chunk):
        if not chunk:
            return

        chunk = chunk.strip()
        cl = chunk.split(' ')
        chunk_head = cl[0]
        if chunk_head in self.tokens_map:
            if chunk_head in self.testcase_tokens:
                # line is related to a primary node. We need to check if it's:
                # - a new primary node declaration
                # or a new primary node field definition
                if len(cl) == 1:
                    # if it's only the token means it's a test case definition
                    if self.node:
                        # if we already have a node defined, replace it with
                        # the new one and return the previous one
                        prev_node = self.node

                        # we need to create the new node before returning the
                        # the previous one
                        self.node = self.create_node(chunk_head)
                        return prev_node

                    else:
                        # just need to define a node if we don't hae one yet
                        self.node = self.create_node(chunk_head)
                else:
                    print 'defining att', cl
                    # it's a node field definition
                    rest = u' '.join(cl[1:])
                    self.node.setattr_from_str(rest)

            elif chunk_head in self.teststep_tokens:
                # it's a secondary level node. It' means it's a child of the
                # current node.
                if not self.node:
                    raise ValueError("Test step token found but there's"
                                     " no test case defined yed")

                if len(cl) == 1:
                    # if it's only the token means it's a test step definition
                    step = self.create_node(chunk_head)
                    self.node.steps.append(step)

                else:
                    try:
                        rest = u' '.join(cl[1:])
                        self.node.steps[-1].setattr_from_str(rest)

                    except IndexError:
                        raise ValueError("Test step field definition found but"
                                         "but there's not test step defined yet!")


    def create_node(self, node_token):
        try:
            return self.tokens_map[node_token](line_no=self.curr_line_no)

        except KeyError:
            raise KeyError("Invalid node token found: %s" %node_token)



def set_replace_missing_attr(x):
    """
    convenience function to used to set a mode 'replace_missing_attr' attribute
    of an object to Tsrue
    """
    x.replace_missing_attr = True