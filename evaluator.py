import os

# Convert input string into tokens
def tokenise(expression):
    tokens = []
    i = 0
    length = len(expression)

    while i < length:
        ch = expression[i]

        if ch == ' ':
            i += 1
            continue

        # number (int or float)
        if ch.isdigit() or (ch == '.' and i+1 < length and expression[i+1].isdigit()):
            j = i
            dot_count = 0
            while j < length and (expression[j].isdigit() or expression[j] == '.'):
                if expression[j] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        return None
                j += 1
            tokens.append(('NUM', float(expression[i:j])))
            i = j

        # operators
        elif ch in '+-*/':
            tokens.append(('OP', ch))
            i += 1

        # parentheses
        elif ch == '(':
            tokens.append(('LPAREN', '('))
            i += 1

        elif ch == ')':
            tokens.append(('RPAREN', ')'))
            i += 1

        else:
            return None

    tokens.append(('END', None))
    return tokens

# format tokens for output
def format_tokens(tokens):
    if tokens is None:
        return "ERROR"

    parts = []
    for typ, val in tokens:
        if typ == 'NUM':
            if val == int(val):
                parts.append(f"[NUM:{int(val)}]")
            else:
                parts.append(f"[NUM:{val}]")
        elif typ == 'OP':
            parts.append(f"[OP:{val}]")
        elif typ == 'LPAREN':
            parts.append("[LPAREN:(]")
        elif typ == 'RPAREN':
            parts.append("[RPAREN:)]")
        elif typ == 'END':
            parts.append("[END]")
    return ' '.join(parts)

# format parse tree
def format_tree(node):
    if node is None:
        return "ERROR"

    if node[0] == 'NUM':
        val = node[1]
        return str(int(val)) if val == int(val) else str(val)

    elif node[0] == 'NEG':
        return f"(neg {format_tree(node[1])})"

    elif node[0] in ('+', '-', '*', '/'):
        return f"({node[0]} {format_tree(node[1])} {format_tree(node[2])})"

    return "ERROR"

# start parsing
def parse(tokens):
    node, pos = parse_expr(tokens, 0)
    if tokens[pos][0] != 'END':
        raise ValueError
    return node

# handle + and -
def parse_expr(tokens, pos):
    left, pos = parse_term(tokens, pos)

    while tokens[pos][0] == 'OP' and tokens[pos][1] in ('+', '-'):
        op = tokens[pos][1]
        pos += 1
        right, pos = parse_term(tokens, pos)
        left = (op, left, right)

    return left, pos

# handle * and /
def parse_term(tokens, pos):
    left, pos = parse_unary(tokens, pos)

    while tokens[pos][0] == 'OP' and tokens[pos][1] in ('*', '/'):
        op = tokens[pos][1]
        pos += 1
        right, pos = parse_unary(tokens, pos)
        left = (op, left, right)

    return left, pos

# handle unary minus
def parse_unary(tokens, pos):
    if tokens[pos][0] == 'OP' and tokens[pos][1] == '-':
        pos += 1
        operand, pos = parse_unary(tokens, pos)
        return ('NEG', operand), pos

    if tokens[pos][0] == 'OP' and tokens[pos][1] == '+':
        raise ValueError

    return parse_primary(tokens, pos)

# numbers, parentheses, implicit multiplication
def parse_primary(tokens, pos):
    tok = tokens[pos]

    if tok[0] == 'NUM':
        node = ('NUM', tok[1])
        pos += 1

    elif tok[0] == 'LPAREN':
        pos += 1
        node, pos = parse_expr(tokens, pos)

        if tokens[pos][0] != 'RPAREN':
            raise ValueError
        pos += 1

    else:
        raise ValueError

    # implicit multiplication
    if tokens[pos][0] in ('NUM', 'LPAREN'):
        right, pos = parse_primary(tokens, pos)
        node = ('*', node, right)

    return node, pos

# evaluate tree
def evaluate(node):
    if node[0] == 'NUM':
        return node[1]

    elif node[0] == 'NEG':
        return -evaluate(node[1])

    elif node[0] == '+':
        return evaluate(node[1]) + evaluate(node[2])

    elif node[0] == '-':
        return evaluate(node[1]) - evaluate(node[2])

    elif node[0] == '*':
        return evaluate(node[1]) * evaluate(node[2])

    elif node[0] == '/':
        right = evaluate(node[2])
        if right == 0:
            raise ZeroDivisionError
        return evaluate(node[1]) / right

    raise ValueError

# format result output
def format_result(val):
    if abs(val - round(val)) < 1e-10:
        return str(int(round(val)))
    return f"{val:.4f}"

# process single line
def process_expression(line):
    result = {"input": line, "tree": "ERROR", "tokens": "ERROR", "result": "ERROR"}

    try:
        tokens = tokenise(line)
        if tokens is None:
            return result

        result["tokens"] = format_tokens(tokens)

        tree = parse(tokens)
        result["tree"] = format_tree(tree)

        val = evaluate(tree)
        result["result"] = format_result(val)

    except:
        pass

    return result

# read file and write output
def evaluate_file(input_path: str) -> list:
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    results = []
    output_lines = []

    for line in lines:
        if not line.strip():
            continue

        r = process_expression(line)
        results.append(r)

        output_lines.append(f"Input: {r['input']}")
        output_lines.append(f"Tree: {r['tree']}")
        output_lines.append(f"Tokens: {r['tokens']}")
        output_lines.append(f"Result: {r['result']}")
        output_lines.append("")

    out_path = os.path.join(os.path.dirname(input_path), "output.txt")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    return results

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "sample_input.txt"
    results = evaluate_file(path)

    for r in results:
        print(f"Input: {r['input']}")
        print(f"Tree: {r['tree']}")
        print(f"Tokens: {r['tokens']}")
        print(f"Result: {r['result']}")
        print()