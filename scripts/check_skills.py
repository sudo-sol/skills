#!/usr/bin/env python3
"""Validate the complete distributable package without network access."""
import json
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit('Install check dependencies: python3 -m pip install -r requirements-dev.txt')

ROOT = Path(__file__).resolve().parent.parent


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of silently accepting the last value."""


def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def yaml_map(text):
    value = yaml.load(text, Loader=UniqueLoader)
    require(isinstance(value, dict), 'YAML must be a mapping')
    return value


def check_skill(path):
    text = path.read_text()
    lines = text.splitlines()
    require(lines and lines[0] == '---', 'missing opening front-matter delimiter')
    require('---' in lines[1:], 'missing closing front-matter delimiter')
    end = lines.index('---', 1)
    fm = yaml_map('\n'.join(lines[1:end]))
    name = fm.get('name')
    require(isinstance(name, str) and name == path.parent.name, 'name must match folder')
    require(len(name) <= 64 and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name), 'invalid skill name')
    description = fm.get('description')
    require(isinstance(description, str) and 0 < len(description.strip()) <= 1024, 'invalid description')
    require(fm.get('license') == 'MIT', 'license must be MIT')
    explicit = fm.get('disable-model-invocation', False)
    require(isinstance(explicit, bool), 'disable-model-invocation must be a boolean')
    metadata = yaml_map((path.parent / 'agents/openai.yaml').read_text())
    interface = metadata.get('interface')
    require(isinstance(interface, dict), 'missing interface metadata')
    for key in ('display_name', 'short_description'):
        require(isinstance(interface.get(key), str) and interface[key].strip(), f'missing interface.{key}')
    require(25 <= len(interface['short_description']) <= 64, 'short_description must be 25–64 characters')
    policy = metadata.get('policy', {})
    require(isinstance(policy, dict), 'policy must be a mapping')
    implicit = policy.get('allow_implicit_invocation', True)
    require(isinstance(implicit, bool), 'allow_implicit_invocation must be a boolean')
    require(explicit == (not implicit), 'invocation settings out of sync')
    for ref in re.findall(r'`(references/[A-Za-z0-9._/-]+)`', text):
        target = (path.parent / ref).resolve()
        require(target.is_relative_to(path.parent.resolve()) and target.is_file(), f'missing or unsafe reference: {ref}')


def check_package(paths):
    for filename in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        require((ROOT / filename).is_file() and (ROOT / filename).read_text().strip(), f'missing or empty root notice: {filename}')
    manifest = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
    market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
    registered = manifest.get('skills')
    require(isinstance(registered, list) and all(isinstance(p, str) for p in registered), 'skills must be a path array')
    actual = {'./' + str(p.parent.relative_to(ROOT)) for p in paths}
    require(actual and len(actual) == len(paths), 'no skills or duplicate paths')
    require(len(registered) == len(set(registered)) and set(registered) == actual, 'manifest registrations differ from disk')
    require(manifest.get('name') == market.get('name') == 'skills', 'collection name must be skills')
    require(isinstance(manifest.get('version'), str) and re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']), 'invalid release version')
    require(manifest.get('license') == 'MIT', 'manifest license must be MIT')
    require(manifest.get('repository') == 'https://github.com/sudo-sol/skills', 'wrong repository')
    entries = market.get('plugins')
    require(isinstance(entries, list) and len(entries) == 1 and entries[0].get('name') == 'skills' and entries[0].get('source') == './', 'marketplace must register the root plugin once')
    require(market.get('owner', {}).get('name') == 'sudo-sol', 'wrong marketplace owner')
    readme = (ROOT / 'README.md').read_text()
    listed = re.findall(r'\]\(\./(skills/[^)]+/SKILL\.md)\)', readme)
    require(len(listed) == len(set(listed)) and set(listed) == {str(p.relative_to(ROOT)) for p in paths}, 'README skill list differs from disk')
    # Validate relative Markdown links throughout the public package.
    for doc in [*ROOT.glob('*.md'), *ROOT.glob('skills/**/*.md')]:
        for ref in re.findall(r'\]\(([^\s)]+)\)', doc.read_text()):
            if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', ref) or ref.startswith('#'):
                continue
            target = (doc.parent / ref.split('#', 1)[0]).resolve()
            require(target.is_relative_to(ROOT) and target.exists(), f'{doc.relative_to(ROOT)}: broken link {ref}')


def main():
    paths = sorted((ROOT / 'skills').rglob('SKILL.md'))
    errors = []
    for path in paths:
        try:
            require(len(path.relative_to(ROOT).parts) == 4, 'skill must be skills/<bucket>/<name>/SKILL.md')
            check_skill(path)
        except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
            errors.append(f'{path.relative_to(ROOT)}: {exc}')
    try:
        check_package(paths)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        errors.append(f'package: {exc}')
    for error in errors:
        print(f'FAIL: {error}')
    if not errors:
        print(f'All skill checks passed ({len(paths)} skills).')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
