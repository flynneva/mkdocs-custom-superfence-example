import logging

from bs4 import BeautifulSoup

from pymdownx.superfences import SuperFencesBlockPreprocessor, SuperFencesCodeExtension


log = logging.getLogger('mkdocs')


def prefix_validator(language, inputs, options, attrs, md):
    """Custom validator."""
    log.info('Validating if this code block is a prefix code block')
    result = True
    
    for k, v in inputs.items():
        # Only accept option called `prefix`
        if k == 'prefix':
            options[k] = v
        elif bool(options):
            if 'prefix' in options:
                # Only use lines option if prefix is set
                if k == 'lines':
                    options[k] = v
        else:
            result = False

    if 'prefix' not in options:
        options['prefix'] = ''
        options['lines'] = -1  # this means do not apply prefix to any lines
    else:
        if 'lines' not in options:
            options['lines'] = 0  # this means to apply prefix to every line
    return result


def prefix_format(source, language, class_name, options, md, **kwargs):
    """Format a given code block with a given prefix as the prefix."""
    log.info('Custom prefix superfence detected!')
    num_lines = len(source.splitlines())

    try:
        if 'prefix' in options:
            prefix = options['prefix']
        else:
            prefix = ''
        if 'classes' in kwargs:
            classes = kwargs['classes']
        else:
            classes = []
        if options['lines'] == 0:
            # assume prefix to be set for every line in codeblock
            options['lines'] = f"1-{num_lines}"
        lines = options['lines']
        # handle the case where prefix and hl_lines are specified
        keep_hl = False
        if 'hl_lines' in options:
            keep_hl = True
        if 'hl_lines' not in classes:
            classes.append('hl_lines')
        # set hl_lines to lines to reuse hl_lines formatter logic
        options['hl_lines'] = lines
        # use linenum preprocessor to replace them later with prefix
        if 'linenums' not in options:
            options['linenums'] = '1'
        sf_ext = SuperFencesCodeExtension()
        config = sf_ext.getConfigs()
        preprocessor = SuperFencesBlockPreprocessor(md)
        preprocessor.config = config
        preprocessor.extension = sf_ext
        preprocessor.get_hl_settings()
        preprocessor.line_count = num_lines
        lines_int = preprocessor.parse_hl_lines(lines)
        soup = BeautifulSoup(
            preprocessor.highlight(
                src=source,
                language=language,
                options=options,
                md=md,
                classes=classes,
                id_value='',
                attrs=None),
            features='lxml')
        line_nums_col = soup.find("div", {"class": "linenodiv"})
        for index, row in enumerate(line_nums_col.findAll(class_='normal')):
            if (index + 1) in lines_int:  # index starts at 0, lines expected to start at 1
                row.string = prefix
            else:
                row.string = ''
        if not keep_hl:
            # remove highlight if hl_lines was not specified in markdown
            hl_div = soup.find("div", {"class": "hl_lines highlight"})
            hl_div.attrs['class'] = 'prefix'
    except Exception as err:
        log.error(err)
        raise
    return soup