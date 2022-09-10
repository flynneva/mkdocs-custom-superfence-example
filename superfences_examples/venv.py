import logging

from bs4 import BeautifulSoup

from pymdownx.superfences import SuperFencesBlockPreprocessor, SuperFencesCodeExtension

log = logging.getLogger('mkdocs')


def venv_validator(language, inputs, options, attrs, md):
    """Custom validator."""
    log.info('Validating if this code block is a valid venv code block')
    result = True
    
    return result


def venv_format(source, language, class_name, options, md, **kwargs):
    """Format a given code block with venv as the prefix."""
    log.info('Custom venv superfence detected!')

    num_lines = len(source.splitlines())
    
    prefix = 'venv'
    class_name = prefix  # default to name the class the same as the prefix

    try:
        for k, v in options.items():
            log.warn(f"{k}: {v}")
        if 'classes' in kwargs:
            classes = kwargs['classes']
        else:
            classes = []
        
        # append prefix to every line in code block
        lines = f"1-{num_lines}"
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
                hl_div.attrs['class'] = class_name
    except Exception as err:
        log.error(err)
        raise
    return soup