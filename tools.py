import ast
import operator

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}

def safe_calculate(expr: str):
    def eval_node(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return OPS[type(node.op)](
                eval_node(node.left),
                eval_node(node.right)
            )
        else:
            raise ValueError("Ungültiger Ausdruck")

    tree = ast.parse(expr, mode='eval')
    return str(eval_node(tree.body))