# Copyright The Aliyun Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging
import subprocess
import sys

import pkg_resources

from aliyun.bootstrap.bootstrap_gen import (
    default_instrumentations,
    libraries,
)
import requests
import os
import shutil

import tarfile
import glob
from aliyun.bootstrap.version import __version__
from aliyun.bootstrap.acm import get_agent_url_from_acm

logger = logging.getLogger(__name__)


def _syscall(func):
    def wrapper(package=None):
        try:
            if package:
                return func(package)
            return func()
        except subprocess.SubprocessError as exp:
            cmd = getattr(exp, "cmd", None)
            if cmd:
                msg = f'Error calling system command "{" ".join(cmd)}"'
            if package:
                msg = f'{msg} for package "{package}"'
            raise RuntimeError(msg)

    return wrapper


@_syscall
def _sys_pip_install(package):
    # explicit upgrade strategy to override potential pip config
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-U",
            "--upgrade-strategy",
            "only-if-needed",
            package,
        ]
    )


file_path = 'aliyun-python-agent.tar.gz'
whl_path = "./aliyun-python-agent"


def _download_agent_file():
    url = os.getenv("PYTHON_AGENT_PATH")
    if url is None:
        url = get_agent_url_from_acm()
    if url is None:
        logger.error(f"get agent url err! ")
        return
    # 下载文件
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)


def _remove_agent_file():
    os.remove(file_path)
    shutil.rmtree(whl_path)


def _extract_whl():
    os.makedirs(whl_path, exist_ok=True)
    # 打开并解压缩 tar.gz 文件
    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(path=whl_path)  # 设置解压缩目录，默认是当前目录

    # 找到所有的 .whl 文件
    whl_files = glob.glob(f'{whl_path}/*/*.whl')
    return whl_files


def _pip_check():
    """Ensures none of the instrumentations have dependency conflicts.
    Clean check reported as:
    'No broken requirements found.'
    Dependency conflicts are reported as:
    'opentelemetry-instrumentation-flask 1.0.1 has requirement opentelemetry-sdk<2.0,>=1.0, but you have opentelemetry-sdk 0.5.'
    To not be too restrictive, we'll only check for relevant packages.
    """
    with subprocess.Popen(
            [sys.executable, "-m", "pip", "check"], stdout=subprocess.PIPE
    ) as check_pipe:
        pip_check = check_pipe.communicate()[0].decode()
        pip_check_lower = pip_check.lower()
    for package_tup in libraries:
        for package in package_tup:
            if package.lower() in pip_check_lower:
                raise RuntimeError(f"Dependency conflict found: {pip_check}")


def _is_installed(req):
    if req in sys.modules:
        return True

    try:
        pkg_resources.get_distribution(req)
    except pkg_resources.DistributionNotFound:
        return False
    except pkg_resources.VersionConflict as exc:
        logger.warning(
            "instrumentation for package %s is available but version %s is installed. Skipping.",
            exc.req,
            exc.dist.as_requirement(),  # pylint: disable=no-member
        )
        return False
    return True


def _find_installed_libraries():
    for lib in default_instrumentations:
        yield lib

    for lib in libraries:
        if _is_installed(lib["library"]):
            yield lib["instrumentation"]


def _run_requirements():
    logger.setLevel(logging.ERROR)
    print("\n".join(_find_installed_libraries()), end="")


def _run_install():
    # for lib in _find_installed_libraries():
    #     _sys_pip_install(lib)
    _download_agent_file()
    agent_whls = _extract_whl()
    for whl in agent_whls:
        _sys_pip_install(whl)
    _pip_check()
    _remove_agent_file()


def run() -> None:
    action_install = "install"
    action_requirements = "requirements"

    parser = argparse.ArgumentParser(
        description="""
        aliyun-bootstrap detects installed libraries and automatically
        installs the relevant instrumentation packages for them.
        """
    )
    parser.add_argument(
        "--version",
        help="print version information",
        action="version",
        version="%(prog)s " + __version__,
    )
    parser.add_argument(
        "-uid",
        "--user_id",
        help="aliyun user id, detail link: ",
    )
    parser.add_argument(
        "-a",
        "--action",
        choices=[action_install, action_requirements],
        default=action_requirements,
        help="""
        install - uses pip to install the new requirements using to the
                  currently active site-package.
        requirements - prints out the new requirements to stdout. Action can
                       be piped and appended to a requirements.txt file.
        """,
    )
    args = parser.parse_args()

    cmd = {
        action_install: _run_install,
        action_requirements: _run_requirements,
    }[args.action]
    cmd()
