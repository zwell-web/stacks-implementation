# evaluate_expressions.py
# Author: Annie Sesay

class Stack:
    def _init_(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0


def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def apply_op(a, b, op):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a / b


def evaluate(expression):
    values = Stack()
    ops = Stack()
    i = 0
    expression = expression.replace(" ", "")

    while i < len(expression):
        if expression[i] == '(':
            ops.push(expression[i])

        elif expression[i].isdigit():
            val = 0
            while i < len(expression) and expression[i].isdigit():
                val = (val * 10) + int(expression[i])
                i += 1
            values.push(val)
            i -= 1

        elif expression[i] == ')':
            while not ops.is_empty() and ops.peek() != '(':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.push(apply_op(val1, val2, op))
            ops.pop()

        elif expression[i] in ['+', '-', '*', '/']:
            while not ops.is_empty() and precedence(ops.peek()) >= precedence(expression[i]):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.push(apply_op(val1, val2, op))
            ops.push(expression[i])
        i += 1

    while not ops.is_empty():
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        values.push(apply_op(val1, val2, op))

    return values.pop()


def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    results = []
    for line in lines:
        line = line.strip()
        if line == "-----":
            results.append("-----")
        elif line == "":
            continue
        else:
            try:
                result = evaluate(line)
                # convert float to int if whole number
                result = int(result) if result == int(result) else result
                results.append(str(result))
            except Exception:
                results.append("Error")

    with open(output_file, 'w') as f:
        for item in results:
            f.write(item + '\n')


if __name__ == "_main_":
    process_file("input.txt", "output.txt")
    print("✅ Evaluation complete! Check output.txt for results.")
