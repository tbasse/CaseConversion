import sublime_plugin
import re


def to_snake_case(text):
    text = re.sub('[-. _]+', '_', text)
    if text.isupper():
        # Entirely uppercase; assume case is insignificant.
        return text.lower()
    return re.sub('(?<=[^_])([A-Z])', r'_\1', text).lower()


def strip_wrapping_underscores(text):
    return re.sub("^(_*)(.*?)(_*)$", r'\2', text)


def to_pascal_case(text):
    callback = lambda pat: pat.group(1).upper()
    text = re.sub("_(\w)", callback, text)
    if text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def to_camel_case(text):
    text = to_pascal_case(text)
    return text[0].lower() + text[1:]


def to_dot_case(text):
    return text.replace("_", ".")


def to_dash_case(text):
    return text.replace("_", "-")


def to_separate_words(text):
    return text.replace("_", " ")


def toggle_case(word):
    pascalcase = re.search('^[A-Z][a-z]+(?:[A-Z][a-z]+)*$', word)
    snakecase = re.search('^[a-z]+(?:_[a-z]+)*$', word)
    camelcase = re.search('^[a-z]+(?:[A-Z][a-z]+)*$', word)
    if (pascalcase):
        return to_snake_case(word)
    elif (snakecase):
        return to_camel_case(word)
    elif (camelcase):
        return to_pascal_case(word)
    else:
        return word


def run_on_selections(view, edit, func):
    for s in view.sel():
        region = s if s else view.word(s)
        text = to_snake_case(view.substr(region))
        text = strip_wrapping_underscores(text)
        view.replace(edit, region, func(text))


def run_on_selections_togglecase(view, edit, func):
    for s in view.sel():
        region = s if s else view.word(s)
        text = view.substr(region)
        text = strip_wrapping_underscores(text)
        view.replace(edit, region, func(text))


class ToggleSnakeCamelPascalCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        run_on_selections_togglecase(self.view, edit, toggle_case)


class ConvertToSnakeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        run_on_selections(self.view, edit, lambda text: text)


class ConvertToCamel(sublime_plugin.TextCommand):
    def run(self, edit):
        run_on_selections(self.view, edit, to_camel_case)


class ConvertToPascal(sublime_plugin.TextCommand):
    def run(self, edit):
        run_on_selections(self.view, edit, to_pascal_case)


class ConvertToDot(sublime_plugin.TextCommand):
    def run(self, edit):
        run_on_selections(self.view, edit, to_dot_case)


class ConvertToDash(sublime_plugin.TextCommand):
    def run(self, edit):
        run_on_selections(self.view, edit, to_dash_case)


class ConvertToSeparateWords(sublime_plugin.TextCommand):
    def run(self, edit):
        run_on_selections(self.view, edit, to_separate_words)
