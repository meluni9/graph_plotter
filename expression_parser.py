import numpy as np
from sympy import symbols, sympify, lambdify

class ExpressionParser:
    def __init__(self):
        self.threshold = 50

    def parse_expression(self, expr, x_min, x_max):
        try:
            x = symbols('x')
            sym_expr = sympify(expr)
            f = lambdify(x, sym_expr, 'numpy')

            x_values = np.linspace(x_min, x_max, 10000)
            y_values = f(x_values)

            mask = np.isfinite(y_values)

            segments = []
            current_x = []
            current_y = []

            for i in range(1, len(x_values)):
                if mask[i] and mask[i - 1]:
                    if abs(y_values[i] - y_values[i - 1]) < self.threshold:
                        current_x.append(x_values[i])
                        current_y.append(y_values[i])
                    else:
                        if current_x:
                            segments.append((np.array(current_x), np.array(current_y)))
                        current_x = [x_values[i]]
                        current_y = [y_values[i]]
                else:
                    if current_x:
                        segments.append((np.array(current_x), np.array(current_y)))
                    current_x = []
                    current_y = []

            if current_x:
                segments.append((np.array(current_x), np.array(current_y)))

            return segments

        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
