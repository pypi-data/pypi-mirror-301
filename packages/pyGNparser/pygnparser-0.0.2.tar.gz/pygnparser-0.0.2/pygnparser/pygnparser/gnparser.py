from pygnparser.utils.pygnparser_utils import gnp_post, gnp_url


def gnparser(names, with_details='on', cultivars='off', diaereses='off'):
    """
    Parse scientific names

    :param names: [str] Human name(s) separated by \\r\\n
    :param with_details: [str] Turn detailed information about the name on or off
    :param cultivars: [str] Turn cultivar handling on or off
    :param diaereses: [str] Turn diaereses handling on or off

    Usage::

        from pygnparser import gnparser
        gnparser('Puma concolor\\nPanthera leo\\nPanthera onca\\nPanthera tigris\\nPanthera pardus\\nPanthera uncia')
    """
    url = gnp_url()
    args = {
        "names": names,
        "with_details": with_details,
        "cultivars": cultivars,
        "diaereses": diaereses,
        "format": 'json'
    }
    out = gnp_post(url, args)
    return out