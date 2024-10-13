"""
bibliograpy process module
"""
import json
import logging
from argparse import Namespace
from pathlib import Path

import yaml

from bibliograpy.api import Institution

LOG = logging.getLogger(__name__)

def _process(ns: Namespace):
    """config
    """
    LOG.info("dependencies")

    in_extension = ns.file.split('.')[-1]
    output_dir = Path(Path.cwd(), ns.output)
    output_file = ns.output_file
    out_extension = output_file.split('.')[-1]

    LOG.info('open configuration file %s', ns.file)
    with open(ns.file, encoding=ns.encoding) as s:

        if in_extension == 'yml':
            content = yaml.safe_load(s)
        elif in_extension == 'json':
            content = json.load(s)
        else:
            raise ValueError(f'unsupported configuration format {in_extension}')

        with open(Path(output_dir, output_file), 'w', encoding=ns.encoding) as o:
            if out_extension == 'py':
                o.write('from bibliograpy.api import Institution\n')
                o.write('\n')
                for ref in content:
                    ref_type = ref['type']
                    if ref_type == 'institution':
                        o.write(f'{Institution.from_dict(ref).to_source_bib()}\n')
            elif out_extension in ['yml', 'yaml']:
                yaml.dump(content, o, sort_keys=False)
