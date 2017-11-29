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


def bs3_cols(sizes):
    """
    Convert a BS3 column sizes dict into a css class string.

    The `sizes` may be a list of tuples instead of a dict.

        >>> bs3_cols({'md': '6', 'xs': '8'})
        'col-md-6 col-xs-8'
    """
    if not isinstance(sizes, dict):
        sizes = OrderedDict(sizes)

    return ' '.join([
        'col-{k}-{v}'.format(k=k, v=v)
        for k, v in sizes.items()
    ])


def bs3_inverse_cols(sizes, *, offset=False, grid=12):
    """
    Convert a BS3 column sizes dict into a css class string,
    but calculate the inverse used for the labels on the left.

    The `sizes` may be a list of tuples instead of a dict.

    The `offset` argument is useful when a label is not present,
    and space needs to be padded.

    Set `grid` for a non-standard number of grid columns.

        >>> bs3_inverse_cols({'md': '6', 'xs': '8'})
        'col-md-6 col-xs-4'

        >>> bs3_inverse_cols({'md': '6', 'xs': '8'}, offset=True)
        'col-md-offset-6 col-xs-offset-4'

        >>> bs3_inverse_cols({'md': '6', 'xs': '8'}, grid=16)
        'col-md-10 col-xs-8'
    """
    if not isinstance(sizes, dict):
        sizes = OrderedDict(sizes)

    fmt = 'col-{k}-{v}' if not offset else 'col-{k}-offset-{v}'

    return ' '.join([
        fmt.format(k=k, v=grid - int(v))
        for k, v in sizes.items()
    ])
