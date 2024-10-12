# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2022 Mathieu Parent <math.parent@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import logging
from os.path import isdir
from typing import TYPE_CHECKING, Any, List, Optional
from urllib.parse import quote

from pygit2 import GIT_FETCH_PRUNE, GitError, RemoteCallbacks, Repository, init_repository

from gitlabracadabra.disk_cache import cache_dir
from gitlabracadabra.gitlab.connections import GitlabConnections
from gitlabracadabra.matchers import Matcher
from gitlabracadabra.objects.object import GitLabracadabraObject


if TYPE_CHECKING:
    from pygit2 import Reference


logger = logging.getLogger(__name__)


class MirrorsMixin(GitLabracadabraObject):
    """Object with mirrors."""

    def _init_repo(self) -> None:
        """Init the cache repository."""
        web_url_slug = quote(self.web_url(), safe='')
        repo_dir = str(cache_dir('') / web_url_slug)
        if isdir(repo_dir):
            self._repo = Repository(repo_dir)
        else:
            logger.debug(
                '[%s] Creating cache repository in %s',
                self._name,
                repo_dir,
            )
            self._repo = init_repository(repo_dir, bare=True)
        try:
            self._repo.remotes['gitlab']  # noqa: WPS428
        except KeyError:
            self._repo.remotes.create(
                'gitlab',
                self.web_url(),
                '+refs/heads/*:refs/remotes/gitlab/heads/*',
            )
            self._repo.remotes.add_fetch('gitlab', '+refs/tags/*:refs/remotes/gitlab/tags/*')
            self._repo.remotes.add_push('gitlab', '+refs/heads/*:refs/heads/*')
            self._repo.remotes.add_push('gitlab', '+refs/tags/*:refs/tags/*')
            self._repo.config['remote.gitlab.mirror'] = True

    def _fetch_remote(
        self,
        name: str,
        remote_callbacks: Optional[RemoteCallbacks] = None,
    ) -> None:  # noqa: WPS210,WPS231
        """Fetch the repo with the given name.

        Args:
            name: Remote name.
            remote_callbacks: Credentials and certificate check as pygit2.RemoteCallbacks.
        """
        try:
            # https://gitlab.com/gitlabracadabra/gitlabracadabra/-/issues/25
            self._repo.remotes[name].fetch(
                refspecs=self._repo.remotes[name].fetch_refspecs,
                callbacks=remote_callbacks,
                prune=GIT_FETCH_PRUNE,
                proxy=True,
            )
        except TypeError:
            self._repo.remotes[name].fetch(
                refspecs=self._repo.remotes[name].fetch_refspecs,
                callbacks=remote_callbacks,
                prune=GIT_FETCH_PRUNE,
            )

    def _push_remote(self, name: str, refs: List[str], remote_callbacks: Optional[RemoteCallbacks] = None) -> None:
        """Push to the repo with the given name.

        Args:
            name: Remote name.
            refs: refs list.
            remote_callbacks: Credentials and certificate check as pygit2.RemoteCallbacks.
        """
        try:
            try:  # noqa: WPS505
                # https://gitlab.com/gitlabracadabra/gitlabracadabra/-/issues/25
                self._repo.remotes[name].push(refs, callbacks=remote_callbacks, proxy=True)
            except TypeError:
                self._repo.remotes[name].push(refs, callbacks=remote_callbacks)
        except GitError as err:
            logger.error(  # noqa: G200
                '[%s] Unable to push remote=%s refs=%s: %s',
                self._name,
                name,
                ','.join(refs),
                err,
            )

    def _sync_ref(self, mirror: dict, ref: Reference, skip_ci: bool, dry_run: bool) -> None:  # noqa: WPS210,WPS231
        """Synchronize the given branch or tag.

        Args:
            mirror: Current mirror dict.
            ref: reference objects.
            skip_ci: skip_ci push option.
            dry_run: Dry run.
        """
        if ref.name.startswith('refs/heads/'):
            ref_type = 'head'
            ref_type_human = 'branch'
            ref_type_human_plural = 'branches'
        elif ref.name.startswith('refs/tags/'):
            ref_type = 'tag'
            ref_type_human = 'tag'
            ref_type_human_plural = 'tags'
        else:
            return
        shorthand = ref.name.split('/', 2)[2]

        # Ref mapping
        dest_shortand = shorthand
        if ref_type_human_plural in mirror:
            dest_shortand = None
            mappings: List[dict[str, str]] = mirror.get(ref_type_human_plural)  # type: ignore
            for mapping in mappings:
                matcher = Matcher(
                    mapping.get('from', ''),
                    None,
                    log_prefix='[{0}] {1} {2}'.format(
                        self._name,
                        mirror['url'],
                        ref_type_human_plural,
                    ),
                )
                matches = matcher.match([shorthand])
                if matches:
                    to_param = mapping.get('to', shorthand)
                    dest_shortand = matches[0].expand(to_param)
                    break

        if dest_shortand is None:
            return

        if skip_ci:
            # Note: Ignored by libgit2/PyGit2
            # https://github.com/libgit2/libgit2/issues/5335
            self._repo.config['push.pushOption'] = 'ci.skip'
        else:
            self._repo.config['push.pushOption'] = ''

        pull_commit = ref.peel().id
        gitlab_ref = self._repo.references.get(
            'refs/remotes/gitlab/{ref_type}s/{ref}'.format(ref_type=ref_type, ref=dest_shortand),
        )
        try:
            gitlab_commit = gitlab_ref.peel().id
        except AttributeError:
            gitlab_commit = None
        if pull_commit != gitlab_commit:
            if dry_run:
                logger.info(
                    '[%s] %s NOT Pushing %s %s to %s: %s -> %s (dry-run)',
                    self._name,
                    mirror['url'],
                    ref_type_human,
                    shorthand,
                    dest_shortand,
                    gitlab_commit,
                    str(pull_commit),
                )
            else:
                logger.info(
                    '[%s] %s Pushing %s %s to %s: %s -> %s',
                    self._name,
                    mirror['url'],
                    ref_type_human,
                    shorthand,
                    dest_shortand,
                    gitlab_commit,
                    str(pull_commit),
                )
                refspec = '{ref_name}:refs/{ref_type}s/{ref}'.format(
                    ref_name=ref.name,
                    ref_type=ref_type,
                    ref=dest_shortand,
                )
                self._push_remote(
                    'gitlab',
                    [refspec],
                    self.connection.pygit2_remote_callbacks,
                )

    def _pull_mirror(self, mirror: dict, skip_ci: bool, dry_run: bool) -> None:
        """Pull from the given mirror and push.

        Args:
            mirror: Current mirror dict.
            skip_ci: skip_ci push option.
            dry_run: Dry run.
        """
        try:
            self._repo.remotes['pull']  # noqa: WPS428
        except KeyError:
            self._repo.remotes.create('pull', mirror['url'], '+refs/heads/*:refs/heads/*')
            self._repo.remotes.add_fetch('pull', '+refs/tags/*:refs/tags/*')
            self._repo.config['remote.pull.mirror'] = True
        remote_callbacks = None
        pull_auth_id = mirror.get('auth_id')
        if pull_auth_id:
            remote_callbacks = GitlabConnections().get_connection(pull_auth_id).pygit2_remote_callbacks
        self._fetch_remote('pull', remote_callbacks)
        for ref in self._repo.references.objects:
            self._sync_ref(mirror, ref, skip_ci, dry_run)

    def _process_mirrors(
        self,
        param_name: str,
        param_value: Any,
        dry_run: bool = False,
        skip_save: bool = False,
    ) -> None:
        """Process the mirrors param.

        Args:
            param_name: "mirrors".
            param_value: List of mirror dicts.
            dry_run: Dry run.
            skip_save: False.
        """
        assert param_name == 'mirrors'  # noqa: S101
        assert not skip_save  # noqa: S101

        pull_mirror_count = 0
        self._init_repo()
        self._fetch_remote(
            'gitlab',
            self.connection.pygit2_remote_callbacks,
        )
        for mirror in param_value:
            direction = mirror.get('direction', 'pull')
            skip_ci = mirror.get('skip_ci', True)
            if direction == 'pull':
                if pull_mirror_count > 0:
                    logger.warning(
                        '[%s] NOT Pulling mirror: %s (Only first pull mirror is processed)',
                        self._name,
                        mirror['url'],
                    )
                    continue
                self._pull_mirror(mirror, skip_ci, dry_run)
                pull_mirror_count += 1
            else:
                logger.warning(
                    '[%s] NOT Push mirror: %s (Not supported yet)',
                    self._name,
                    mirror['url'],
                )
