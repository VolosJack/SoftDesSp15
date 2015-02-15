""" TODO: Put your header comment here """

import random
from PIL import Image
from math import pi, sin, cos, radians
from random import randint

operators = {
    "x": {
        "fn": lambda x: x,
        "arg": 0
    },
    "y": {
        "fn": lambda y: y,
        "arg": 0
    },
    "prod": {
        "fn": lambda a, b: a * b,
        "arg": 2
    },
    "cos_pi": {
        "fn": lambda a: cos(pi * a),
        "arg": 1
    },
    "sin_pi": {
        "fn": lambda a: sin(pi * a),
        "arg": 1
    },
    "cube": {
        "fn": lambda x: x ** 3,
        "arg": 1
    },
    "avg": {
        "fn": lambda a, b: (a + b) / 2,
        "arg": 2
    }
}


def prod(a, b):
    """ Multiplies the values provided in 'a' and 'b' and returns their product

    :param a: Input from a random function
    :param b: Input from a random function
    :return: The product of 'a' and 'b'

    >>> prod(1, 2)
    2.0

    >>> prod(1.5, 6)
    9.0
    """
    product = float(a) * float(b)

    return product

    pass


def sin_pi(a):
    """ Takes the sin of pi times 'a'

    :param a: Input from a random function
    :return: The sin of pi times 'a'
    >>> sin_pi(2)
    0.11

    >>> sin_pi(-0.5)
    -0.03
    """
    pi_a = pi * float(a)

    sin_pi_a = sin(radians(pi_a))

    return round(sin_pi_a, 2)

    pass


def cos_pi(a):
    """ Takes the sin of pi times 'a'

    :param a: Input from a random function
    :return: The sin of pi times 'a'
    >>> cos_pi(3)
    0.99

    >>> cos_pi(-0.7)
    1.0
    """
    pi_a = pi * float(a)

    cos_pi_a = cos(radians(pi_a))

    return round(cos_pi_a, 2)

    pass


def avg(a, b):
    """ Returns the average of 'a' and 'b'

    :param a: Input from a random function
    :param b: Input from a random function
    :return: One half time a plus b

    >>> avg(2, 4)
    3.0

    >>> avg(6.3, 7.7)
    7.0
    """
    a_and_b = float(a) + float(b)

    avg = 0.5 * a_and_b

    return round(avg, 2)

    pass


def square(a):
    """ Raises 'a' to the power of two

    :param a: Input from random function
    :return: 'a' squared
    >>> square(1)
    1.0

    >>> square(-0.25)
    0.06
    """

    return round(a * a, 2)

    pass


def x(a):
    """ Returns the value of 'a'

    :param a: Input from a random function
    :param b: Input from a random function
    :return: The value of 'a'
    >>> x(3)
    3.0

    >>> x(-0.24)
    -0.24
    """
    return round(a, 2)

    pass


def y(a):
    """ Returns the value of 'a'

    :param a: Input from a random function
    :param b: Input from a random function
    :return: The value of 'a'
    >>> y(4)
    4.0

    >>> y(2)
    2.0
    """
    return round(a, 2)

    pass


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)

    """
    # TODO: implement this

    ops = operators.keys()

    if max_depth == 1:
        return ["x"] if random < 0.5 else ["y"]
    else:
        if min_depth > 1:
            ops = [key for key in operators.keys() if not key in ["x", "y"]]
        func = ops[randint(0, len(ops)-1)]
        args = [build_random_function(min_depth-1, max_depth-1) for i in range(operators[func]["arg"])]

        if len(args):
            return [func] + args
        else:
            return [func]

    pass


def evaluate_random_function(f, a, b):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        a: the value of x to be used to evaluate the function
        b: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function("x",-0.5, 0.75)
        -0.5
        >>> evaluate_random_function("y",0.1,0.02)
        0.02
    """
    # TODO: implement this

    func = f[0]

    try:
        if not operators[func]["arg"]:
            if func == "x":
                return a
            else:
                return b
        elif operators[func]["arg"] == 1:
            return operators[func]["fn"](evaluate_random_function(f[1], a, b))
        else:
            return operators[func]["fn"](evaluate_random_function(f[1], a, b), evaluate_random_function(f[2], a, b))
    except KeyError:
        raise Exception("No function in list of bases")

    pass


def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # TODO: implement this
    input_interval_length = float(input_interval_end) - float(input_interval_start)
    output_interval_length = float(output_interval_end) - float(output_interval_start)

    input_dis_start = float(val) - input_interval_start

    input_percent = (input_dis_start / input_interval_length)

    output_dist_start = input_percent * output_interval_length

    output_val = float(output_interval_start) + output_dist_start

    return output_val

    pass


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y)),
                color_map(evaluate_random_function(green_function, x, y)),
                color_map(evaluate_random_function(blue_function, x, y))
            )

    im.save(filename)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
