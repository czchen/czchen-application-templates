#!/usr/bin/env python3
import pathlib
import sys

sys.path.append(str(pathlib.PurePath(__file__).parent.parent))

from omegaconf import OmegaConf
from testcontainers.postgres import PostgresContainer
import hydra

import utils


def main():
    config = pathlib.PosixPath(__file__).parent.parent / 'conf' / 'app' / 'override.yaml'

    with PostgresContainer(utils.POSTGRES_IMAGE) as postgres:
        with config.open('wt') as f:
            f.write(f'''
config:
  SQLALCHEMY_DATABASE_URI: {postgres.get_connection_url()}''')

        hydra.initialize(version_base=None, config_path='../conf')
        config = OmegaConf.to_container(hydra.compose(config_name='config'))
        print('Press any key to stop')
        input()


if __name__ == '__main__':
    sys.exit(main())
