from generator import nodes
from generator.nodes import *
from generator.globals import *


class NodeInterpreter:
    def __init__(self):
        self.start_node = nodes.Start()
        self.end_node = nodes.End()

    def execute(self):
        cur = self.start_node
        while not isinstance(cur, nodes.StopRuntime):
            cur.calculate()
            cur = cur.next_node()

    def flush(self):
        self.start_node.outputs["order_output"].disconnect()
        self.end_node.inputs["order_input"].disconnect()

    @property
    def start(self):
        return self.start_node.outputs['order_output']

    @property
    def end(self):
        return self.end_node.inputs['order_input']
