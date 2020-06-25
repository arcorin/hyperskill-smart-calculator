# Smart Calculator
# Stage 7/7
# I've got the power

# Defined functions in order of execution:
# A: main
# B: validate_input
# C: check_infix
# D: construct_infix
# E: infix_to_postfix
# F: precedence
# G: calculate_postfix
# H: binary_operations

import string

# create lists with valid char: ...
# ... numbers, letters (valid char for variables), ...
# ... math signs and parenthesis
operators = ["+", "-", "*", "/", "//", "%", "^"]
paren = ["(", ")"]
digits = list(string.digits)
letters = list(string.ascii_letters)

valid_chars = ["+", "-", "*", "/", "//", "%", "^"]
valid_chars.extend(digits)
valid_chars.extend(letters)
valid_chars.extend(paren)
valid_chars.extend(".")

variables = dict()


# H: the eight function to execute -> binary math operations
def binary_operations(a, b, x):
    if x == "+":
        return a + b
    elif x == "-":
        return a - b
    elif x == "*":
        return a * b
    elif x == "^":
        return a ** b
    elif x == "/":
        if b == 0:
            print("ZeroDivision")
        else:
            return a / b
    elif x == "%":
        if b == 0:
            print("ZeroDivision")
        else:
            return a % b


# G: seventh function to execute -> calculate postfix expression
def calculate_postfix(a):
    stack = []
    for x in a:
        # if x in variables:
            # x = variables[x]
        if x not in operators:
            stack.append(x)
        if x in operators:
            b, c = stack.pop(), stack.pop()
            stack.append(binary_operations(c, b, x))
    return stack[0]


# F: sixth function to execute -> calculate precedence
def precedence(a):
    p_ = 0

    if a in ["+", "-"]:
        p_ = 1
    elif a in ["*", "/", "%"]:
        p_ = 2
    elif a == "^":
        p_ = 3
    return p_


# E: fifth function to execute -> transform infix notation to postfix notation
def infix_to_postfix(exp):
    e_postfix = []
    stack = []

    for e in exp:
        if e not in ["+", "-", "*", "/", "%", "^", "(", ")"]:
            e_postfix.append(e)
        if e in operators:
            if stack == [] or stack[-1] == "(":
                stack.append(e)
            elif stack[-1] in operators and precedence(stack[-1]) < precedence(e):
                stack.append(e)
            else:
                while stack and ((stack[-1] in operators and precedence(stack[-1]) >= precedence(e)) or stack[-1] != "("):
                    e_postfix.append(stack.pop())
                stack.append(e)
        if e == "(":
            stack.append(e)
        if e == ")":
            while stack[-1] != "(":
                e_postfix.append(stack.pop())
            stack.pop()

    while stack:
        e_postfix.append(stack.pop())

    return e_postfix


# D: fourth function to execute -> create and check infix expression from string
def construct_infix(s):
    # create infix expression as a list of operands, operators and parentheses
    expression = []
    n = len(s)
    i = 0
    while i < n:
        value = ""
        # append to expression operands (variables or numbers) with 1 or more chars
        if s[i].isalpha():
            k = 0
            while i + k < n and s[i + k] not in ["+", "-", "*", "/", "%", "^", "(", ")"]:
                value += s[i + k]
                k += 1
            i += k
        elif s[i].isdigit():
            k = 0
            while i + k < n and s[i + k] not in ["+", "-", "*", "/", "%", "^", "(", ")"]:
                value += s[i + k]
                k += 1
            i += k

        # check if operands are variables and if they are replace them
        if value.isalpha():
            if value in variables:
                expression.append(variables[value])
                # print(f"the variable {value} was replaced with it's value")
            else:
                print("Unknown variable")
                main()
        if value.isdigit():
            expression.append(int(value))

        # append to expression operators + and -
        if i < n and s[i] in ["+", "-"]:
            sign = "+"
            minus = 2
            j = 0
            while i + j < n and s[i + j] in operators:
                if s[i + j] == "-":
                    minus += 1
                j += 1
            i += j

            if minus % 2 != 0:
                sign = "-"
            expression.append(sign)

        # append to expression operators *, /, %, ^ and parenthesis
        if i < n and s[i] in ["*", "/", "%", "^", "(", ")"]:
            expression.append(s[i])
            i += 1

    # print(expression)
    return expression


# C: third function to execute -> check infix expression
def check_expression(s):
    # check if the expression is correct
    correct = True

    # check parentheses: number and chars around them
    if s.count("(") != s.count(")") or s.count("(") == 1 and len(s) < 3:
        correct = False

    # check start and end of the string for wrong operators or parentheses
    elif s[0] in ["*", "/", "%", "^", ")"]:
        correct = False
    elif s[-1] in [operators, "("]:
        correct = False

    # check the rest of the string for wrong parentheses or operators
    else:
        for x in range(0, len(s) - 1):
            if s[x] == "(" and s[x + 1] in ["*", "/", "%", "^", ")"]:
                correct = False
            if s[x] in ["*", "/", "%", "^", ")"] and s[x + 1] in operators:
                correct = False
            if s[x] in operators and s[x + 1] in ["*", "/", "%", "^", ")"]:
                correct = False
        for x in range(1, len(s)):
            if s[x] == ")" and s[x - 1] in ["*", "/", "%", "^", "("]:
                correct = False

    if not correct:
        print("Invalid input")
        main()
    if correct:
        return s


# B: second function to execute -> input string, evaluate string and, ....
# ... if the string is correct, pass it to main()
def validate_input():
    s = input().replace(" ", "")

    # check input string
    # case 1: check if it is an empty string
    if s in ["", " "]:
        main()

    # case 2: check for a known command
    if s.startswith("/"):
        if s == "/exit":
            print("Bye!")
            exit()
        elif s == "/help":
            print("The program calculates the expression")
            main()
        else:
            print("Unknown command")
            main()

    # case 3: check for an assignment
    elif "=" in s:
        if s.count("=") > 1:
            print("Invalid assignment")
            main()
        elif s.count("=") == 1:
            n = s.index("=")
            left = s[:n]
            right = s[n + 1:]

            # check if the name of the variable contains only letters
            if left.isalpha():
                # check if the right part contains only digits
                if right.isdigit():
                    # save variable to the dictionary
                    variables[left] = int(right)

                # check if the right part is a variable from the dictionary
                elif right.isalpha():
                    if right in variables:
                        variables[left] = variables[right]
                    else:
                        print("Unknown variable")
                        main()
                else:
                    print("Invalid assignment")
                    main()

            # if the name of the variable doesn't contains only letters return to main
            else:
                print("Invalid identifier")
                main()

        # print(variables)
        main()

    # case 4: check if all chars are valid
    elif not all([x in valid_chars for x in s]):
        print("Invalid expression")
        main()

    # case 5: when all chars are valid ...
    # ... create expression as a list of operands, operators and parentheses
    else:
        return s


# A: first function to execute
def main():
    correct_string = validate_input()  # function B
    # print("the correct string is:", correct_string)

    checked_string = check_expression(correct_string) # function C
    # print("the checked string is:", checked_string)

    infix_expression = construct_infix(checked_string)  # function D
    # print("the infix expression is:", infix_expression)

    postfix_expression = infix_to_postfix(infix_expression)  # functions E, F
    # print("the postfix expression is:", postfix_expression)

    result = calculate_postfix(postfix_expression)  # functions G, H

    print(round(result, 2))
    main()


main()
