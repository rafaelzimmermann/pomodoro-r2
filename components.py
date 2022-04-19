
def write_progress_bar_custom_char(output):
    chars = [
        [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10],
        [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18],
        [0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C],
        [0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E],
        [0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F],
    ]
    location = 0
    for char_map in chars:
        output.lcd.custom_char(location, char_map)
        location += 1


def progress_bar(output, percentage):
    write_progress_bar_custom_char(output)
    line_size = 16
    p = line_size * float(percentage)
    p_int = int(p)
    partial_c = p - p_int
    line = []
    for i in range(0, line_size):
        if i < p_int:
            line.append(chr(4))
        elif i == p_int:
            line.append(chr(int(partial_c * 4)))
        else:
            line.append(chr(17))
    return line








