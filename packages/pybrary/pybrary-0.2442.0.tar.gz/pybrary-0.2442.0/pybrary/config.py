from os import environ
from os.path import expanduser
from pathlib import Path
from subprocess import call

from pybrary import Dico


def create_config_py(path):
    with open(path, 'w') as out:
        out.write('config = dict(\n)\n')

def create_config_toml(path):
    with open(path, 'w') as out:
        out.write('[config]\n')

def create_config_yaml(path):
    with open(path, 'w') as out:
        out.write('config: {}\n')

def create_config_json(path):
    with open(path, 'w') as out:
        out.write('{"config": {}}\n')

creators = dict(
    py = create_config_py,
    toml = create_config_toml,
    yaml = create_config_yaml,
    json = create_config_json,
)


def load_config_py(path):
    from pybrary.modules import load
    return load('config', path).config

def load_config_toml(path):
    from tomllib import loads
    return loads(path.read_text())['config']

def load_config_yaml(path):
    from yaml import load, SafeLoader
    return load(open(path), Loader=SafeLoader)['config']

def load_config_json(path):
    from json import load
    return load(open(path))['config']

loaders = dict(
    py = load_config_py,
    toml = load_config_toml,
    yaml = load_config_yaml,
    json = load_config_json,
)


class Config(Dico):
    def __init__(self, app):
        path = Path('~/.config').expanduser()
        for ext, loader in loaders.items():
            full = path / f'{app}.{ext}'
            if full.is_file():
                config = loader(full)
                self.path = full
                break
        else:
            raise RuntimeError('Config not found')
        for key, val in config.items():
            setattr(self, key, val)

    @staticmethod
    def create(app, ext='py'):
        path = Path(f'~/.config/{app}.{ext}').expanduser()
        creators[ext](path)

    @staticmethod
    def edit(app, default='py'):
        path = Path('~/.config').expanduser()
        for ext in loaders:
            full = path / f'{app}.{ext}'
            if full.is_file(): break
        else:
            ext = default
            Config.create(app, ext)
        full = path / f'{app}.{ext}'
        editor = environ.get('EDITOR', 'vim')
        call([editor, full])


def get_app_config(app):
    path = Path(f'~/.config/{app}').expanduser()
    try:
        from pybrary.modules import load
        full = path / 'config.py'
        config = load('config', full)
        return full, config.config
    except: pass
    try:
        from tomllib import loads
        full = path / 'config.toml'
        config = loads(full.read_text())
        return full, config
    except: pass
    try:
        from yaml import load, SafeLoader
        full = path / 'config.yaml'
        config = load(full, loader=SafeLoader)
        return full, config
    except: pass
    try:
        from json import load
        full = path / 'config.json'
        config = load(full)
        return full, config
    except: pass
    return None, None
