from contextlib import suppress
from os import walk
from pathlib import Path

from kalib.descriptors import cache, pin
from kalib.importer import optional, required, sort
from kalib.logging import Logging


class Git(Logging.Mixin):

    @pin.cls
    def Repo(cls):  # noqa: N802
        return required('git.Repo')

    @pin.root
    def root(cls):
        expect = suppress(required('git.exc.InvalidGitRepositoryError'))
        with expect, cls.Repo(
            Path.cwd().resolve(),
            search_parent_directories=True,
        ) as repo:
            return Path(repo.working_tree_dir).resolve()
        cls.log.verbose('not detected')

    @pin.root
    def repo(cls):
        if (path := cls.root):
            return cls.Repo(path, search_parent_directories=True)
        cls.log.verbose('not found')

    @pin.root
    def from_path(cls):
        root = cls.root

        if not root:
            cls.log.warning("feature disabled, git root isn't detected")
            return (lambda *args: None)  # noqa: ARG005

        @cache
        def resolver(path):
            for commit in cls.repo.iter_commits(paths=path, max_count=1):
                return commit
            cls.log.warning(f'{path=} not in repository {root!s} index')

        @cache
        def explorer(path):
            file = Path(path).resolve()

            if not file.is_file():
                cls.log.warning(f'{path=} ({file!s}) not found')
                return

            elif not str(file).startswith(str(root)):
                cls.log.warning(f'{path=} ({file!s}) not in {root!s}')
                return

            return resolver(str(file)[len(str(root)) + 1:])

        return explorer

    @pin.root
    def files(cls):
        result = []
        prefix = len(str(cls.root)) + 1
        for rt, _, fs in walk(cls.root):
            root = Path(rt)
            for f in fs:
                if f.endswith('.py'):
                    result.append(str(root / f)[prefix:])

        return tuple(sort(result))

    @pin.root
    def tree(cls):
        return {
            path: str(cls.from_path(path)) for path in cls.files
            if cls.from_path(path) is not None}

    @pin.root
    def tag(cls):
        with suppress(Exception), cls.repo as git:
            head = git.head.commit

            def get_distance(tag):
                return int(cli.rev_list(
                    '--count', f'{tag.commit.hexsha}..{head.hexsha}'))

            if git.tags:
                cli = required('git.Git')()
                distances = {
                    tag: get_distance(tag)
                    for tag in sort(git.tags, key=lambda x: x.name, reverse=True)}

                if distances:
                    return sorted(distances, key=lambda x: distances[x])[0]

    @pin.root
    def version(cls):
        with suppress(ImportError):
            if cls.tag and (version := optional('versioneer.get_version')):
                return version()
