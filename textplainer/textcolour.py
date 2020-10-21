
def get_coloured_text_string(text, colour):
    if colour=="red":
        return ("\033[31m" + text + "\033[0m")
    if colour=="green":
        return ("\033[32m" + text + "\033[0m")
    if colour=="yellow":
        return ("\033[33m" + text + "\033[0m")
    if colour=="blue":
        return ("\033[34m" + text + "\033[0m")
    if colour=="purple":
        return ("\033[35m" + text + "\033[0m")
    if colour=="cyan":
        return ("\033[36m" + text + "\033[0m")
    if colour=="white":
        return ("\033[37m" + text + "\033[0m")
    return text


