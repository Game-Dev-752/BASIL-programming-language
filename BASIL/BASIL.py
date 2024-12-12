import os
import math
import sys

class BASIL:
    def __init__(self):
        self.code = {}
        self.variables = {}
        self.current_line = None
        self.execution_history = set()  # To track recently executed lines for loop detection

    def eval_expression(self, expression):
        """Evaluate an expression safely with support for ^ and real-only results."""
        try:
            # Replace ^ with Python's ** for exponentiation
            expression = expression.replace("^", "**")
            # Evaluate the expression
            result = eval(expression, {}, self.variables)
            # Check for imaginary results
            if isinstance(result, complex):
                raise ValueError("Imaginary number detected in expression.")
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")

    def set_variable(self, parts):
        try:
            name = parts[1]
            if parts[2] != "TO":
                print("Syntax error. Use: SET <name> TO <value>")
                return
            expression = " ".join(parts[3:])
            value = self.eval_expression(expression)
            self.variables[name] = value
        except Exception as e:
            print(f"Error: {e}")

    def print_expression(self, parts):
        try:
            expression = " ".join(parts[1:])
            value = self.eval_expression(expression)
            print(value)
        except Exception as e:
            print(f"Error: {e}")

    def if_condition(self, parts):
        condition = " ".join(parts[1:parts.index("THEN")])
        then_line = int(parts[parts.index("THEN") + 1])
        else_line = None
        if "ELSE" in parts:
            else_line = int(parts[parts.index("ELSE") + 1])

        try:
            condition_result = eval(condition, {}, self.variables)
            if condition_result:
                self.current_line = then_line
            elif else_line is not None:
                self.current_line = else_line
            else:
                self.current_line = self.get_next_line(self.current_line)
        except Exception as e:
            print(f"Error evaluating condition on line {self.current_line}: {e}")
            self.current_line = None

    def get_next_line(self, current):
        sorted_lines = sorted(self.code.keys())
        current_index = sorted_lines.index(current)
        return sorted_lines[current_index + 1] if current_index + 1 < len(sorted_lines) else None

    def input_statement(self, parts):
        prompt = parts[1][1:-1]  # Remove surrounding quotes
        variable_name = parts[2]

        # Display the prompt and take user input
        user_input = input(f"{prompt}: ")
        try:
            # Attempt to convert to integer or float if possible
            if '.' in user_input:
                value = float(user_input)
            else:
                value = int(user_input)
        except ValueError:
            value = user_input  # Treat as a string if conversion fails

        self.variables[variable_name] = value

    def remove_line(self, line_number):
        """Remove the specified code line."""
        if line_number in self.code:
            del self.code[line_number]
            print(f"Line {line_number} removed.")
        else:
            print(f"Error: Line {line_number} not found.")

    def reset(self):
        """Reset all code and variables."""
        self.code.clear()
        self.variables.clear()
        print("All code and variables have been reset.")

    def run(self):
        self.current_line = min(self.code.keys()) if self.code else None
        while self.current_line is not None:
            if self.current_line not in self.code:
                break  # Exit if there's no next line

            # Check for potential infinite loop
            if self.current_line in self.execution_history:
                print("Warning: Potential infinite loop detected.")
                break  # Exit the loop to avoid infinite execution

            # Add the current line to the execution history
            self.execution_history.add(self.current_line)

            try:
                parts = self.code[self.current_line].split()
                if parts[0] == "SET":
                    self.set_variable(parts)
                elif parts[0] == "PRINT":
                    self.print_expression(parts)
                elif parts[0] == "IF":
                    self.if_condition(parts)
                    continue  # Skip incrementing line number if conditional jumps
                elif parts[0] == "JUMP":
                    self.current_line = int(parts[1])
                    continue  # Skip incrementing line number, as we're jumping directly
                elif parts[0] == '"':
                    pass
                elif parts[0] == "INPUT":
                    self.input_statement(parts)
                elif parts[0] == "END":
                    break
                self.current_line = self.get_next_line(self.current_line)
            except KeyboardInterrupt:
                print("Loop ended.")
                break  # Exit the loop if interrupted by the user
            finally:
                # Clear the execution history after each iteration to avoid memory buildup
                self.execution_history.clear()

    def save(self, name):
        try:
            with open("./saves/" + name + ".basil", "w") as file:
                for line_num in sorted(self.code.keys()):
                    file.write(f"{line_num} {self.code[line_num]}\n")
            print(f"Code saved to ./saves/{name}.basil")
        except Exception as e:
            print(f"Error saving file: {e}")

    def load(self, name):
        try:
            with open("./saves/" + name + ".basil", "r") as file:
                self.code.clear()
                self.variables.clear()
                for line in file:
                    parts = line.strip().split(" ", 1)
                    self.code[int(parts[0])] = parts[1]
            print(f"Code loaded from ./saves/{name}.basil")
        except Exception as e:
            print(f"Error loading file: {e}")

    def view(self):
        if not self.code:
            print("No code to view.")
        else:
            for line_num in sorted(self.code.keys()):
                print(f"{line_num} {self.code[line_num]}")

def main():
    # Check for version flag
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("""
BASIL (Basic And Simple Interactive Language)
Version 1.7.3
December 10, 2024
""")
        return

    interpreter = BASIL()
    print("Welcome to BASIL")
    while True:
        command = input("> ").strip()
        if command.upper() == "EXIT":
            print("Exiting BASIL...")
            break
        elif command.upper() == "RUN":
            interpreter.run()
        elif command.upper() == "VIEW":
            interpreter.view()
        elif command.upper().startswith("SAVE"):
            _, name = command.split(maxsplit=1)
            interpreter.save(name)
        elif command.upper().startswith("LOAD"):
            _, name = command.split(maxsplit=1)
            interpreter.load(name)
        elif command.upper().startswith("REMOVE"):
            try:
                _, line_num = command.split()
                line_num = int(line_num)
                interpreter.remove_line(line_num)
            except ValueError:
                print("Invalid line number.")
        elif command.upper() == "RESET":
            interpreter.reset()
        elif command.upper() == "CLEAR":
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            try:
                parts = command.split(maxsplit=1)
                line_num = int(parts[0])
                rest = parts[1]
                interpreter.code[line_num] = rest
            except ValueError:
                print("Invalid line number or syntax.")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
