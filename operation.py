def add_value(curr_value, value):
    return 255 if curr_value + value > 255 else curr_value + value


def subtract_value(curr_value, value):
    return 0 if curr_value - value < 0 else curr_value - value


def multiply_value(curr_value, value):
    return 255 if curr_value * value > 255 else curr_value * value


def divide_value(curr_value, value):
    return 0 if value == 0 else int(curr_value / value)


def add_operation(rgb, blue_channel_enabled_get, green_channel_enabled_get, red_channel_enabled_get, value):
    (r, g, b) = rgb
    if red_channel_enabled_get == 1:
        r = add_value(r, value)
    if green_channel_enabled_get == 1:
        g = add_value(g, value)
    if blue_channel_enabled_get == 1:
        b = add_value(b, value)

    return r, g, b


def subtract_operation(rgb, blue_channel_enabled_get, green_channel_enabled_get, red_channel_enabled_get, value):
    (r, g, b) = rgb
    if red_channel_enabled_get == 1:
        r = subtract_value(r, value)
    if green_channel_enabled_get == 1:
        g = subtract_value(g, value)
    if blue_channel_enabled_get == 1:
        b = subtract_value(b, value)

    return r, g, b


def multiply_operation(rgb, blue_channel_enabled_get, green_channel_enabled_get, red_channel_enabled_get, value):
    (r, g, b) = rgb
    if red_channel_enabled_get == 1:
        r = multiply_value(r, value)
    if green_channel_enabled_get == 1:
        g = multiply_value(g, value)
    if blue_channel_enabled_get == 1:
        b = multiply_value(b, value)

    return r, g, b


def divide_operation(rgb, blue_channel_enabled_get, green_channel_enabled_get, red_channel_enabled_get, value):
    (r, g, b) = rgb
    if red_channel_enabled_get == 1:
        r = divide_value(r, value)
    if green_channel_enabled_get == 1:
        g = divide_value(g, value)
    if blue_channel_enabled_get == 1:
        b = divide_value(b, value)

    return r, g, b


def brightness_operation(rgb, value):
    (r, g, b) = rgb
    if value > 0:
        r = 255 if r + value > 255 else r + value
        g = 255 if g + value > 255 else g + value
        b = 255 if b + value > 255 else b + value
    else:
        r = 0 if r + value < 0 else r + value
        g = 0 if g + value < 0 else g + value
        b = 0 if b + value < 0 else b + value

    return r, g, b
