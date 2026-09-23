"""Hegelese bootstrap 0.1: a bounded, dynamically checked functional evaluator."""

from dataclasses import dataclass
import json
import re

import hegelese as finite


@dataclass(frozen=True)
class Token:
    text: str
    line: int
    column: int


class Diagnostic(Exception):
    def __init__(self, token, message, status="Invalid"):
        self.token, self.message, self.status = token, message, status
        super().__init__(message)


@dataclass(frozen=True)
class Node:
    kind: str
    token: Token
    args: tuple


LEX = re.compile(r'(?P<space>\s+)|(?P<comment>\#[^\n]*)|(?P<string>"(?:[^"\\\n]|\\.)*")|(?P<int>[0-9]+)|(?P<name>[A-Za-z_][A-Za-z_0-9]*)|(?P<op>=>|==|!=|<=|>=|&&|\|\||[+*/%<>=!;:,.(){}\[\]-])')
RESERVED = finite.ALIASES | {"let", "rec", "fn", "if", "then", "else", "true", "false", "null", "process", "request", "from", "require", "into", "using", "occasion", "assumptions", "retain", "withdraw", "because", "match"}


def lex(source):
    result, pos, line, column = [], 0, 1, 1
    while pos < len(source):
        match = LEX.match(source, pos)
        if not match:
            raise Diagnostic(Token(source[pos], line, column), "Unexpected character.")
        text = match.group()
        if match.lastgroup not in ("space", "comment"):
            result.append(Token(text, line, column))
        line += text.count("\n")
        column = len(text.rsplit("\n", 1)[-1]) + 1 if "\n" in text else column + len(text)
        pos = match.end()
    result.append(Token("<eof>", line, column))
    return result


class Parser:
    PRECEDENCE = {"||": 1, "&&": 2, "==": 3, "!=": 3, "<": 4, ">": 4, "<=": 4, ">=": 4, "+": 5, "-": 5, "*": 6, "/": 6, "%": 6}

    def __init__(self, source):
        self.tokens, self.i = lex(source), 0

    @property
    def at(self):
        return self.tokens[self.i]

    def take(self, expected=None):
        token = self.at
        if expected is not None and token.text != expected:
            raise Diagnostic(token, f"Expected {expected!r}; found {token.text!r}.")
        self.i += 1
        return token

    def accept(self, text):
        if self.at.text == text:
            self.take()
            return True
        return False

    def name(self):
        token = self.at
        if not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", token.text) or token.text in RESERVED:
            raise Diagnostic(token, "Expected an unreserved identifier.")
        return self.take().text

    def key(self):
        if self.at.text.startswith('"'):
            return self.string(self.take())
        return self.name()

    @staticmethod
    def string(token):
        try:
            return json.loads(token.text)
        except ValueError:
            raise Diagnostic(token, "Invalid string escape.") from None

    def program(self):
        nodes = []
        while self.at.text != "<eof>":
            token = self.at
            if self.accept("let"):
                recursive = self.accept("rec")
                name = self.name()
                self.take("=")
                nodes.append(Node("let", token, (name, self.expr(), recursive)))
            elif self.accept("process"):
                name = self.name()
                self.take("=")
                nodes.append(Node("process", token, (name, self.expr())))
            elif self.accept("request"):
                name = self.name()
                self.take("from")
                source = self.expr()
                self.take("require")
                nodes.append(Node("request", token, (name, source, self.expr())))
            elif token.text in finite.ALIASES:
                self.take()
                name = self.name()
                self.take("{")
                parts, dispositions = {}, {}
                while self.at.text != "}":
                    field = self.take()
                    if field.text in ("retain", "withdraw"):
                        key = self.key()
                        if key in dispositions:
                            raise Diagnostic(field, "Duplicate commitment disposition.")
                        self.take("because")
                        dispositions[key] = (field.text, self.expr(), field)
                    elif field.text in ("from", "into", "using", "occasion", "assumptions"):
                        if field.text in parts:
                            raise Diagnostic(field, "Duplicate Upheaval field.")
                        parts[field.text] = self.expr()
                    else:
                        raise Diagnostic(field, "Unknown Upheaval field.")
                    self.take(";")
                self.take("}")
                if set(parts) != {"from", "into", "using", "occasion", "assumptions"}:
                    raise Diagnostic(token, "Upheaval needs from, into, using, occasion, and assumptions.")
                nodes.append(Node("development", token, (name, parts, dispositions)))
            else:
                nodes.append(Node("expression", token, (self.expr(),)))
            self.take(";")
        return nodes

    def expr(self, minimum=0):
        token = self.take()
        text = token.text
        if text == "<eof>":
            raise Diagnostic(token, "Expected an expression.")
        if text == "fn":
            self.take("(")
            params = []
            if self.at.text != ")":
                params.append(self.name())
                while self.accept(","):
                    params.append(self.name())
            self.take(")")
            if len(set(params)) != len(params):
                raise Diagnostic(token, "Duplicate function parameter.")
            self.take("=>")
            node = Node("fn", token, (tuple(params), self.expr()))
        elif text == "if":
            condition = self.expr()
            self.take("then")
            yes = self.expr()
            self.take("else")
            node = Node("if", token, (condition, yes, self.expr()))
        elif text == "match":
            value = self.expr()
            self.take("{")
            branches = {}
            while self.at.text != "}":
                label = self.name()
                if label in branches:
                    raise Diagnostic(self.at, "Duplicate match branch.")
                self.take("(")
                name = self.name()
                self.take(")")
                self.take("=>")
                branches[label] = (name, self.expr())
                self.take(";")
            self.take("}")
            node = Node("match", token, (value, branches))
        elif text in ("-", "!"):
            node = Node("unary", token, (text, self.expr(7)))
        elif text == "(":
            node = self.expr()
            self.take(")")
        elif text == "[":
            items = []
            if self.at.text != "]":
                items.append(self.expr())
                while self.accept(","):
                    items.append(self.expr())
            self.take("]")
            node = Node("list", token, (items,))
        elif text == "{":
            fields = {}
            if self.at.text != "}":
                while True:
                    key = self.key()
                    if key in fields:
                        raise Diagnostic(self.at, "Duplicate record field.")
                    self.take(":")
                    fields[key] = self.expr()
                    if not self.accept(","):
                        break
            self.take("}")
            node = Node("record", token, (fields,))
        elif text.startswith('"'):
            node = Node("literal", token, (self.string(token),))
        elif text.isdigit():
            if len(text) > 1000:
                raise Diagnostic(token, "Integer literal exceeds 1000 digits.")
            node = Node("literal", token, (int(text),))
        elif text in ("true", "false", "null"):
            node = Node("literal", token, ({"true": True, "false": False, "null": None}[text],))
        elif re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", text) and text not in RESERVED:
            node = Node("name", token, (text,))
        else:
            raise Diagnostic(token, "Expected an expression.")
        while True:
            if self.accept("("):
                arguments = []
                if self.at.text != ")":
                    arguments.append(self.expr())
                    while self.accept(","):
                        arguments.append(self.expr())
                self.take(")")
                node = Node("call", token, (node, arguments))
            elif self.accept("."):
                node = Node("field", token, (node, self.name()))
            elif self.accept("["):
                index = self.expr()
                self.take("]")
                node = Node("index", token, (node, index))
            elif self.at.text in self.PRECEDENCE and self.PRECEDENCE[self.at.text] >= minimum:
                op = self.take()
                node = Node("binary", op, (op.text, node, self.expr(self.PRECEDENCE[op.text] + 1)))
            else:
                return node


@dataclass(frozen=True)
class Closure:
    params: tuple
    body: Node
    environment: dict


@dataclass(frozen=True)
class Builtin:
    name: str
    arity: int


@dataclass(frozen=True)
class Variant:
    tag: str
    value: object


@dataclass(frozen=True)
class Process:
    table: dict
    token: Token


@dataclass(frozen=True)
class Request:
    data: dict
    token: Token


@dataclass(frozen=True)
class Development:
    request: Request
    proposal: dict
    token: Token
    fields: dict


@dataclass(frozen=True)
class Evidence:
    report: dict


class Evaluator:
    def __init__(self, source_name, fuel, budget):
        self.source_name, self.fuel, self.budget = source_name, fuel, budget
        self.last = Token("", 1, 1)

    def spend(self, token):
        self.last = token
        if self.fuel <= 0:
            raise Diagnostic(token, "Evaluation fuel exhausted; no conclusion.", "Unknown")
        self.fuel -= 1

    def need(self, condition, token, message):
        if not condition:
            raise Diagnostic(token, message)

    def location(self, token):
        return {"file": self.source_name, "line": token.line, "column": token.column, "spelling": token.text}

    def evaluate(self, node, env):
        self.spend(node.token)
        kind, args, token = node.kind, node.args, node.token
        if kind == "literal":
            return args[0]
        if kind == "name":
            self.need(args[0] in env, token, "Undefined name: " + args[0])
            return env[args[0]]
        if kind == "fn":
            return Closure(args[0], args[1], dict(env))
        if kind == "list":
            return [self.evaluate(x, env) for x in args[0]]
        if kind == "record":
            return {k: self.evaluate(v, env) for k, v in args[0].items()}
        if kind == "if":
            condition = self.evaluate(args[0], env)
            self.need(type(condition) is bool, token, "Condition must be Boolean.")
            return self.evaluate(args[1] if condition else args[2], env)
        if kind == "match":
            value = self.evaluate(args[0], env)
            self.need(isinstance(value, Variant), token, "Match requires a tagged value.")
            self.need(value.tag in args[1], token, "No branch for tag " + value.tag)
            name, body = args[1][value.tag]
            return self.evaluate(body, dict(env, **{name: value.value}))
        if kind == "call":
            function = self.evaluate(args[0], env)
            values = [self.evaluate(x, env) for x in args[1]]
            return self.call(function, values, token)
        if kind in ("field", "index"):
            value = self.evaluate(args[0], env)
            if isinstance(value, Evidence):
                value = value.report
            key = args[1] if kind == "field" else self.evaluate(args[1], env)
            if type(value) is dict:
                self.need(type(key) is str and key in value, token, "Record key is absent or not a string.")
            else:
                self.need(type(value) in (list, str) and type(key) is int and 0 <= key < len(value), token, "Invalid sequence index.")
            return value[key]
        if kind == "unary":
            value = self.evaluate(args[1], env)
            self.need(type(value) is (int if args[0] == "-" else bool), token, "Wrong unary operand type.")
            return -value if args[0] == "-" else not value
        if kind == "binary":
            op, left, right = args
            a = self.evaluate(left, env)
            if op in ("&&", "||"):
                self.need(type(a) is bool, token, "Logical operands must be Boolean.")
                if (op == "&&" and not a) or (op == "||" and a):
                    return a
                b = self.evaluate(right, env)
                self.need(type(b) is bool, token, "Logical operands must be Boolean.")
                return b
            b = self.evaluate(right, env)
            if op in ("==", "!="):
                equal = self.equal(a, b, token)
                return equal if op == "==" else not equal
            if op == "+" and type(a) is type(b) and type(a) in (str, list):
                self.need(len(a) + len(b) <= 10000, token, "Sequence exceeds 10000 elements.")
                return a + b
            self.need(type(a) is int and type(b) is int, token, "Arithmetic and ordering require integers.")
            if op in ("/", "%"):
                self.need(b != 0, token, "Division by zero.")
            result = {"+": lambda: a+b, "-": lambda: a-b, "*": lambda: a*b,
                      "/": lambda: a//b, "%": lambda: a%b, "<": lambda: a<b,
                      ">": lambda: a>b, "<=": lambda: a<=b, ">=": lambda: a>=b}[op]()
            self.need(type(result) is bool or result.bit_length() <= 4096, token, "Integer exceeds 4096 bits.")
            return result
        raise Diagnostic(token, "Unsupported expression.")

    def equal(self, a, b, token):
        self.spend(token)
        allowed = (int, bool, str, type(None), list, dict, Variant)
        self.need(type(a) in allowed and type(b) in allowed, token, "Equality is defined only on data values.")
        if type(a) is not type(b):
            return False
        if type(a) is list:
            return len(a) == len(b) and all(self.equal(x, y, token) for x, y in zip(a, b))
        if type(a) is dict:
            return a.keys() == b.keys() and all(self.equal(a[k], b[k], token) for k in a)
        if isinstance(a, Variant):
            return a.tag == b.tag and self.equal(a.value, b.value, token)
        return a == b

    def call(self, function, values, token):
        self.spend(token)
        self.need(isinstance(function, (Closure, Builtin)), token, "Value is not callable.")
        arity = len(function.params) if isinstance(function, Closure) else function.arity
        self.need(len(values) == arity, token, f"Expected {arity} arguments; received {len(values)}.")
        if isinstance(function, Closure):
            return self.evaluate(function.body, dict(function.environment, **dict(zip(function.params, values))))
        name = function.name
        if name == "len":
            self.need(type(values[0]) in (list, str, dict), token, "len requires a sequence or record.")
            return len(values[0])
        if name == "int":
            value = values[0]
            self.need(type(value) is str and re.fullmatch(r"-?[0-9]{1,1000}", value), token, "int requires a decimal string of at most 1000 digits.")
            return int(value)
        if name == "str":
            self.need(type(values[0]) is int, token, "str requires an integer.")
            return str(values[0])
        if name == "variant":
            self.need(type(values[0]) is str and re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", values[0]) and values[0] not in RESERVED, token, "Tag must be an unreserved identifier.")
            return Variant(*values)
        if name == "map":
            self.need(type(values[1]) is list, token, "map requires a function and list.")
            return [self.call(values[0], [x], token) for x in values[1]]
        if name == "fold":
            function, result, items = values
            self.need(type(items) is list, token, "fold requires a function, initial value, and list.")
            for item in items:
                result = self.call(function, [result, item], token)
            return result
        if name == "inspect":
            value = values[0]
            self.need(isinstance(value, (Process, Request, Development)), token, "inspect requires a process, request, or Upheaval.")
            if isinstance(value, Process):
                return value.table
            if isinstance(value, Request):
                return value.data
            return value.proposal
        if name == "check":
            value = values[0]
            self.need(isinstance(value, Development), token, "check requires an Upheaval declaration.")
            report = finite.check(value.request.data, value.proposal, self.budget)
            report["source_location"] = self.location(value.token)
            report["request_location"] = self.location(value.request.token)
            for diagnostic in report.get("diagnostics", []):
                path = diagnostic["path"]
                field = value.fields.get(path, value.token)
                diagnostic["location"] = self.location(field)
            return Evidence(report)
        raise Diagnostic(token, "Unknown built-in.")

    def make_process(self, name, record, token):
        self.need(type(record) is dict and set(record) == {"version", "states", "inputs", "initial", "step", "observe"}, token, "Process needs version, states, inputs, initial, step, and observe.")
        finite.names(record["states"], "/states", 1000)
        finite.names(record["inputs"], "/inputs", 64)
        observations = record["observe"]
        self.need(type(observations) is dict and len(observations) <= 32, token, "observe requires at most 32 named functions.")
        table = {k: record[k] for k in ("version", "states", "inputs", "initial")}
        table["name"] = name
        table["transitions"] = {s: {i: self.call(record["step"], [s, i], token) for i in record["inputs"]} for s in record["states"]}
        table["observations"] = {n: {s: self.call(f, [s], token) for s in record["states"]} for n, f in observations.items()}
        finite.process(table, "/process/" + name)
        return Process(table, token)

    def program(self, nodes):
        env = {name: Builtin(name, arity) for name, arity in {"len": 1, "int": 1, "str": 1, "map": 2, "fold": 3, "variant": 2, "inspect": 1, "check": 1}.items()}
        result = None
        for node in nodes:
            self.spend(node.token)
            kind, args, token = node.kind, node.args, node.token
            if kind == "expression":
                result = self.evaluate(args[0], env)
                continue
            name = args[0]
            self.need(name not in env, token, "Duplicate top-level name: " + name)
            if kind == "let":
                result = self.evaluate(args[1], env)
                if args[2]:
                    self.need(isinstance(result, Closure), token, "let rec requires a function.")
                    result.environment[name] = result
            elif kind == "process":
                result = self.make_process(name, self.evaluate(args[1], env), token)
            elif kind == "request":
                source = self.evaluate(args[1], env)
                self.need(isinstance(source, Process), token, "Request source must be a process.")
                required = self.evaluate(args[2], env)
                self.need(type(required) is list and all(type(x) is str and x in source.table["observations"] for x in required) and len(set(required)) == len(required), token, "Required observations must be distinct source observation names.")
                result = Request({"schema": "hegelese-request/0.1", "source": source.table, "required_observations": required}, token)
            elif kind == "development":
                parts, dispositions = args[1:]
                request = self.evaluate(parts["from"], env)
                target = self.evaluate(parts["into"], env)
                function = self.evaluate(parts["using"], env)
                self.need(isinstance(request, Request) and isinstance(target, Process), token, "from requires a request; into requires a process.")
                proposal = {"schema": "hegelese-proposal/0.1", "operation": token.text,
                            "request_sha256": finite.digest(request.data), "target": target.table,
                            "occasion": self.evaluate(parts["occasion"], env),
                            "assumptions": self.evaluate(parts["assumptions"], env),
                            "mapping": {s: self.call(function, [s], token) for s in request.data["source"]["states"]},
                            "dispositions": {k: {"action": action, "reason": self.evaluate(reason, env)} for k, (action, reason, _) in dispositions.items()}}
                locations = {"/proposal/dispositions/" + k: t for k, (_, _, t) in dispositions.items()}
                result = Development(request, proposal, token, locations)
            env = dict(env, **{name: result})
        return result


def display(value, evaluator):
    evaluator.spend(evaluator.last)
    if isinstance(value, Evidence):
        return display(value.report, evaluator)
    if isinstance(value, Variant):
        return {"tag": value.tag, "value": display(value.value, evaluator)}
    if isinstance(value, (Closure, Builtin)):
        return {"kind": "Function"}
    if isinstance(value, Process):
        return {"kind": "Process", "definition": display(value.table, evaluator)}
    if isinstance(value, Request):
        return {"kind": "Request", "definition": display(value.data, evaluator)}
    if isinstance(value, Development):
        return {"kind": "UncheckedDevelopment", "proposal": display(value.proposal, evaluator)}
    if type(value) is list:
        return [display(x, evaluator) for x in value]
    if type(value) is dict:
        return {k: display(v, evaluator) for k, v in value.items()}
    return value


def run(source, filename="<input>", fuel=100000, budget=100000):
    evaluator = Evaluator(filename, fuel, budget)
    try:
        if type(fuel) is not int or not 0 <= fuel <= 1_000_000:
            raise Diagnostic(evaluator.last, "Fuel must be an integer from 0 through 1000000.")
        if type(budget) is not int or not 0 <= budget <= 1_000_000:
            raise Diagnostic(evaluator.last, "Check budget must be an integer from 0 through 1000000.")
        if len(source.encode("utf-8")) > 2_000_000:
            raise Diagnostic(evaluator.last, "Source exceeds 2 MB.")
        value = evaluator.program(Parser(source).program())
        return {"language": "hegelese-bootstrap/0.1", "status": value.report["status"] if isinstance(value, Evidence) else "Evaluated", "value": display(value, evaluator), "fuel_remaining": evaluator.fuel}
    except finite.Invalid as error:
        diagnostic = Diagnostic(evaluator.last, error.message)
        path = error.path
    except Diagnostic as error:
        diagnostic, path = error, None
    except RecursionError:
        diagnostic, path = Diagnostic(evaluator.last, "Bootstrap nesting limit reached; no conclusion.", "Unknown"), None
    return {"language": "hegelese-bootstrap/0.1", "status": diagnostic.status,
            "diagnostics": [{"message": diagnostic.message, "location": evaluator.location(diagnostic.token), "path": path}]}
