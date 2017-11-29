from collections import OrderedDict


def add_css_classes(boundfield, css_classes):
    """
    Add a single or multiple css classes to a form widget. To add multiple classes, pass
    them as a whitespace delimited string or a list. eg, `add_classes(boundfield, 'foo bar')`
    """
    if not css_classes:
        return

    if isinstance(css_classes, str):
        css_classes = css_classes.split()

    widget = boundfield.field.widget
    classes = OrderedDict.fromkeys(widget.attrs.get('class', '').split())
    classes.update(OrderedDict.fromkeys(css_classes))

    widget.attrs['class'] = " ".join(classes)


def try_classmro(fn, cls):
    """
    Try `fn` with the `cls` by walking its MRO until a result is returned.
    eg, `try_classmro(field_dict.get, forms.CharField)`
    """
    for cls in cls.mro():
        result = fn(cls)
        if result is not None:
            return result
