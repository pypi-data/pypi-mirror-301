"""
Packmon : Monitoring packages to increase quality and kill obsolescence
Author : Mindiell
License : APGLv3+
Package : https://framagit.org/Mindiell/packmon
Version : 0.3.1
"""

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import zip_longest
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.request import Request, urlopen


VERSION = "0.3.1"
BOT_URL = "https://framagit.org/Mindiell/packmon/-/blob/main/bot.md"
PYPI_STATUS = {
    "Development Status :: 1 - Planning": "planning",
    "Development Status :: 2 - Pre-Alpha": "pre-alpha",
    "Development Status :: 3 - Alpha": "alpha",
    "Development Status :: 4 - Beta": "beta",
    "Development Status :: 5 - Production/Stable": "stable",
    "Development Status :: 6 - Mature": "mature",
    "Development Status :: 7 - Inactive": "inactive",
}
PYPI_LICENSE = {
    "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication": "",
    "License :: CeCILL-B Free Software License Agreement (CECILL-B)": "",
    "License :: CeCILL-C Free Software License Agreement (CECILL-C)": "",
    "License :: DFSG approved": "DFSG approved",
    "License :: Eiffel Forum License (EFL)": "Eiffel Forum License (EFL)",
    "License :: Free For Educational Use": "Free For Educational Use",
    "License :: Free For Home Use": "Free For Home Use",
    "License :: Free To Use But Restricted": "Free To Use But Restricted",
    "License :: Free for non-commercial use": "Free for non-commercial use",
    "License :: Freely Distributable": "Freely Distributable",
    "License :: Freeware": "Freeware",
    "License :: GUST Font License 1.0": "GUST Font License 1.0",
    "License :: GUST Font License 2006-09-30": "GUST Font License 2006-09-30",
    "License :: Netscape Public License (NPL)": "Netscape Public License (NPL)",
    "License :: Nokia Open Source License (NOKOS)": "Nokia Open Source License (NOKOS)",
    "License :: OSI Approved": "OSI Approved",
    "License :: OSI Approved :: Academic Free License (AFL)": "Academic Free License (AFL)",
    "License :: OSI Approved :: Apache Software License": "Apache Software License",
    "License :: OSI Approved :: Apple Public Source License": "Apple Public Source License",
    "License :: OSI Approved :: Artistic License": "Artistic License",
    "License :: OSI Approved :: Attribution Assurance License": "Attribution Assurance License",
    "License :: OSI Approved :: BSD License": "BSD License",
    "License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)": "Boost Software License 1.0 (BSL-1.0)",
    "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)": "CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
    "License :: OSI Approved :: Common Development and Distribution License 1.0 (CDDL-1.0)": "Common Development and Distribution License 1.0 (CDDL-1.0)",
    "License :: OSI Approved :: Common Public License": "Common Public License",
    "License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)": "Eclipse Public License 1.0 (EPL-1.0)",
    "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)": "Eclipse Public License 2.0 (EPL-2.0)",
    "License :: OSI Approved :: Eiffel Forum License": "Eiffel Forum License",
    "License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)": "European Union Public Licence 1.0 (EUPL 1.0)",
    "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)": "European Union Public Licence 1.1 (EUPL 1.1)",
    "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)": "European Union Public Licence 1.2 (EUPL 1.2)",
    "License :: OSI Approved :: GNU Affero General Public License v3": "GNU Affero General Public License v3",
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)": "GNU Affero General Public License v3 or later (AGPLv3+)",
    "License :: OSI Approved :: GNU Free Documentation License (FDL)": "GNU Free Documentation License (FDL)",
    "License :: OSI Approved :: GNU General Public License (GPL)": "GNU General Public License (GPL)",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)": "GNU General Public License v2 (GPLv2)",
    "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)": "GNU General Public License v2 or later (GPLv2+)",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)": "GNU General Public License v3 (GPLv3)",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)": "GNU General Public License v3 or later (GPLv3+)",
    "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)": "GNU Lesser General Public License v2 (LGPLv2)",
    "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)": "GNU Lesser General Public License v2 or later (LGPLv2+)",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)": "GNU Lesser General Public License v3 (LGPLv3)",
    "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)": "GNU Lesser General Public License v3 or later (LGPLv3+)",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)": "GNU Library or Lesser General Public License (LGPL)",
    "License :: OSI Approved :: Historical Permission Notice and Disclaimer (HPND)": "Historical Permission Notice and Disclaimer (HPND)",
    "License :: OSI Approved :: IBM Public License": "IBM Public License",
    "License :: OSI Approved :: ISC License (ISCL)": "ISC License (ISCL)",
    "License :: OSI Approved :: Intel Open Source License": "Intel Open Source License",
    "License :: OSI Approved :: Jabber Open Source License": "Jabber Open Source License",
    "License :: OSI Approved :: MIT License": "MIT License",
    "License :: OSI Approved :: MIT No Attribution License (MIT-0)": "MIT No Attribution License (MIT-0)",
    "License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)": "MITRE Collaborative Virtual Workspace License (CVW)",
    "License :: OSI Approved :: MirOS License (MirOS)": "MirOS License (MirOS)",
    "License :: OSI Approved :: Motosoto License": "Motosoto License",
    "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)": "Mozilla Public License 1.0 (MPL)",
    "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)": "Mozilla Public License 1.1 (MPL 1.1)",
    "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)": "Mozilla Public License 2.0 (MPL 2.0)",
    "License :: OSI Approved :: Nethack General Public License": "Nethack General Public License",
    "License :: OSI Approved :: Nokia Open Source License": "Nokia Open Source License",
    "License :: OSI Approved :: Open Group Test Suite License": "Open Group Test Suite License",
    "License :: OSI Approved :: Open Software License 3.0 (OSL-3.0)": "Open Software License 3.0 (OSL-3.0)",
    "License :: OSI Approved :: PostgreSQL License": "PostgreSQL License",
    "License :: OSI Approved :: Python License (CNRI Python License)": "Python License (CNRI Python License)",
    "License :: OSI Approved :: Python Software Foundation License": "Python Software Foundation License",
    "License :: OSI Approved :: Qt Public License (QPL)": "Qt Public License (QPL)",
    "License :: OSI Approved :: Ricoh Source Code Public License": "Ricoh Source Code Public License",
    "License :: OSI Approved :: SIL Open Font License 1.1 (OFL-1.1)": "SIL Open Font License 1.1 (OFL-1.1)",
    "License :: OSI Approved :: Sleepycat License": "Sleepycat License",
    "License :: OSI Approved :: Sun Industry Standards Source License (SISSL)": "Sun Industry Standards Source License (SISSL)",
    "License :: OSI Approved :: Sun Public License": "Sun Public License",
    "License :: OSI Approved :: The Unlicense (Unlicense)": "The Unlicense (Unlicense)",
    "License :: OSI Approved :: Universal Permissive License (UPL)": "Universal Permissive License (UPL)",
    "License :: OSI Approved :: University of Illinois/NCSA Open Source License": "University of Illinois/NCSA Open Source License",
    "License :: OSI Approved :: Vovida Software License 1.0": "Vovida Software License 1.0",
    "License :: OSI Approved :: W3C License": "W3C License",
    "License :: OSI Approved :: X.Net License": "X.Net License",
    "License :: OSI Approved :: Zope Public License": "Zope Public License",
    "License :: OSI Approved :: zlib/libpng License": "zlib/libpng License",
    "License :: Other/Proprietary License": "Other/Proprietary License",
    "License :: Public Domain": "Public Domain",
    "License :: Repoze Public License": "Repoze Public License",
}


@dataclass
class Header:
    slug: str
    name: str
    size: int
    min_size: int
    index: int
    reduced: bool


class Package:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.status = kwargs.get("status", "Unknown")
        self.license = kwargs.get("license", "Unknown")
        self.vulnerabilities_raw = kwargs.get("vulnerabilities", 0)
        self.version = kwargs.get("version", "Unknown")
        self.releases = kwargs.get("releases", [])
        self.release_limit = kwargs.get("release_limit", datetime.today())
        self.last_update = kwargs.get("last_update", datetime.today())
        if isinstance(self.last_update, str):
            self.last_update = datetime.strptime(self.last_update, "%Y-%m-%d")

    @property
    def has_problem(self) -> bool:
        if (
            self.status_level != ""
            or self.version_level != ""
            or self.release_level != ""
            or self.vulnerabilities_raw > 0
        ):
            return True
        return False

    @property
    def vulnerabilities(self) -> str:
        return str(self.vulnerabilities_raw)

    @property
    def last_version(self) -> str:
        return self.releases[-1]["release"]

    @property
    def next_version(self) -> str:
        for release_idx in range(len(self.releases) - 1):
            if self.releases[release_idx]["release"] == self.version:
                return self.releases[release_idx + 1]["release"]
        return self.version

    @property
    def last_release(self) -> str:
        return datetime.strptime(self.releases[-1]["release_date"], "%Y-%m-%dT%H:%M:%S")

    @property
    def last_release_human(self) -> str:
        return f"{self.last_release:%Y-%m-%d}"

    @property
    def status_level(self) -> str:
        if self.status in ("planning", "pre-alpha", "alpha", "inactive"):
            return "\033[1m\033[31m"
        elif self.status in ("", "beta"):
            return "\033[1m\033[33m"
        return ""

    @property
    def version_level(self) -> str:
        if self.version != self.last_version:
            versions = re.split(r"[.-]", self.version)[:-1]
            last_versions = re.split(r"[.-]", self.last_version)[:-1]
            for version, last_version in zip_longest(versions, last_versions):
                if version != last_version:
                    return "\033[1m\033[31m"
            return "\033[1m\033[33m"
        return ""

    @property
    def release_level(self) -> str:
        if self.last_release < self.release_limit:
            return "\033[1m\033[33m"
        return ""

    @property
    def vulnerabilities_level(self) -> str:
        if self.vulnerabilities_raw == 0:
            return "\033[92m"
        return "\033[1m\033[31m"

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "license": self.license,
            "vulnerabilities": self.vulnerabilities_raw,
            "releases": self.releases,
            "last_update": f"{self.last_update:%Y-%m-%d}",
        }


def load_cache() -> list:
    home_path = Path.home().joinpath(".packmon")
    os.makedirs(home_path, exist_ok=True)
    cache_file = os.path.join(home_path, "packages.json")
    try:
        with open(cache_file) as file_handler:
            return [
                Package(
                    name=package["name"],
                    status=package["status"],
                    license=package["license"],
                    vulnerabilities=package["vulnerabilities"],
                    releases=package.get("releases", []),
                    last_update=package["last_update"],
                )
                for package in json.load(file_handler)
            ]
    except:
        return []


def save_cache(packages: list) -> None:
    home_path = Path.home().joinpath(".packmon")
    os.makedirs(home_path, exist_ok=True)
    cache_file = os.path.join(home_path, "packages.json")
    with open(cache_file, "wt") as file_handler:
        json.dump([package.to_json() for package in packages], file_handler, indent=2)


def display_cache_informations() -> None:
    packages = load_cache()
    oldest_update = None
    for package in packages:
        if package.last_update is not None:
            if oldest_update is None:
                oldest_update = package.last_update
            elif package.last_update < oldest_update:
                oldest_update = package.last_update
    print(f"Oldest update: {oldest_update:%Y-%m-%d}")
    print(f"Packages: {len(packages)}")
    names = sorted([package.name for package in packages], key=lambda x: x.lower())
    largest_name = len(max(names, key=lambda x: len(x)))
    columns = os.get_terminal_size().columns // (largest_name + 2)
    lines = len(names) // columns + 1
    for line in range(lines):
        for column in range(columns):
            try:
                print(f"{names[line + column*lines]:<{largest_name}} ", end="")
            except IndexError:
                # no data to display
                pass
        print()


def update_cache() -> None:
    packages = []
    cache_packages = load_cache()
    if len(cache_packages) == 0:
        print("No cache to update")
        return
    for idx, cache_package in enumerate(cache_packages):
        print(f"\r{idx+1}/{len(cache_packages)}", end="", file=sys.stderr, flush=True)
        package = get_datas_from_pypi(cache_package.name)
        if package is not None:
            packages.append(package)
        # Little pause in order not to spam pypi
        time.sleep(0.2)
    save_cache(packages)
    print()
    print("Cache updated!")


def get_datas_from_pypi(
    package_name: str,
    version: str = None,
    release_limit: datetime = datetime.today(),
) -> Package:
    datas = None
    request = Request(
        f"https://pypi.org/pypi/{package_name}/json",
        headers={"User-Agent": f"packmon/{VERSION} ({BOT_URL})"},
    )
    result = urlopen(request)
    if result.status == 200:
        datas = json.loads(result.read())
        name = datas["info"]["name"]
        status = "unknown"
        if datas["info"].get("license", "") != "":
            license = datas["info"]["license"] or "unknown"
        else:
            license = "unknown"
        for classifier in datas["info"]["classifiers"]:
            if classifier in PYPI_STATUS:
                status = PYPI_STATUS[classifier]
            if classifier in PYPI_LICENSE:
                license = PYPI_LICENSE[classifier]
        vulnerabilities = len(datas.get("vulnerabilities", []))
        releases = sorted(
            [
                {
                    "release": version,
                    "release_date": datas["releases"][version][0]["upload_time"],
                }
                for version in datas["releases"]
                if len(datas["releases"][version]) > 0
            ],
            key=lambda x: datetime.strptime(
                x["release_date"],
                "%Y-%m-%dT%H:%M:%S",
            ),
        )
        return Package(
            name=name,
            status=status,
            license=license,
            vulnerabilities=vulnerabilities,
            version=version,
            releases=releases,
            release_limit=release_limit,
        )
    return None


def update(
    requirements: list,
    days: int,
    no_cache: bool,
    no_update: bool,
    quiet: bool,
) -> list:
    release_limit = datetime.now() - timedelta(days=days)

    if no_cache:
        cache_packages = []
    else:
        cache_packages = load_cache()

    packages = []
    size = len(requirements)
    for idx, requirement in enumerate(requirements):
        try:
            if len(requirement.strip()) == 0 or requirement.strip()[0] == "#":
                continue
            if not quiet:
                print(f"\r{idx+1}/{size}", end="", file=sys.stderr, flush=True)
            result = re.match(
                "(?P<name>[^>~=<]+)((?P<condition>[>~=<]+)(?P<version>[^; ]+))?.*$",
                requirement,
            )
            name = result.group("name").lower()
            version = result.group("version") or "unkown"
            # Search in cache, if not present use the internet
            for cache_package in cache_packages:
                if name == cache_package.name.lower():
                    cache_package.version = version
                    cache_package.release_limit = release_limit
                    # If information is too old, update package
                    if not no_update and cache_package.last_update < (
                        datetime.now() - timedelta(days=20)
                    ):
                        continue
                    elif len(cache_package.releases) == 0:
                        continue
                    else:
                        packages.append(cache_package)
                        break
            else:
                packages.append(get_datas_from_pypi(name, version, release_limit))
                # Little pause in order not to spam pypi
                time.sleep(0.2)
        except Exception as e:
            print(
                f"Error while trying to find informations on {name}"
                f" with version {version}",
                file=sys.stderr,
            )
            print(e, file=sys.stderr)
            continue
    if not quiet:
        print()

    # Caching packages
    cache_modified = False
    new_cache = []
    # Adding updated or new packages
    for package in packages:
        for cache_package in cache_packages:
            if package.name.lower() == cache_package.name.lower():
                if cache_package.last_update != f"{package.last_update:%Y-%m-%d}":
                    new_cache.append(package)
                    cache_modified = True
                break
        else:
            new_cache.append(package)
            cache_modified = True
    if cache_modified:
        # Re-adding old packages to new cache
        for cache_package in cache_packages:
            for package in new_cache:
                if package.name.lower() == cache_package.name.lower():
                    break
            else:
                new_cache.append(cache_package)
        save_cache(new_cache)

    return packages


def output(packages: list, no_color: bool, only_problems: bool, quiet: bool) -> None:
    if quiet:
        return
    if no_color:
        HEADER = ""
        NORMAL = ""
    else:
        HEADER = "\033[96m"
        NORMAL = "\033[0m"

    # Computing columns sizes
    terminal_width = os.get_terminal_size().columns
    headers = [
        Header("name", "name", 5, 5, 0, False),
        Header("status", "status", 7, 7, 1, False),
        Header("license", "license", 8, 8, 2, False),
        Header("version", "version", 8, 8, 3, False),
        Header("next_version", "next version", 13, 13, 4, False),
        Header("last_version", "last version", 13, 13, 5, False),
        Header("last_release_human", "last release", 13, 13, 6, False),
        Header("vulnerabilities", "vulnerabilities", 15, 15, 7, False),
    ]
    for header in headers:
        for package in packages:
            if len(getattr(package, header.slug)) >= header.size:
                header.size = len(getattr(package, header.slug)) + 1
    if sum([h.min_size for h in headers]) < terminal_width:
        while sum([h.size for h in headers]) > terminal_width:
            largest = sorted(
                filter(lambda h: not h.reduced, headers),
                key=lambda h: h.size,
                reverse=True,
            )[0].index
            # Reduce largest column
            headers[largest].size -= min(
                sum([h.size for h in headers]) - terminal_width,
                headers[largest].size - headers[largest].min_size,
            )
            headers[largest].reduced = True

    # Printing values
    def display_value(value: str, header: Header, level: str = "") -> str:
        if header.reduced and len(value) > header.size - 1:
            result = value[: (header.size - 2)] + "\u2026"
        else:
            result = value
        return f"{level}{result: <{header.size}}{NORMAL}"

    # specific for windows in order to enable coloration by escape sequences
    os.system("")
    line = HEADER
    for header in headers:
        line += f"{header.name: <{header.size}}"
    print(f"{line}{NORMAL}")
    for package in packages:
        if only_problems and not package.has_problem:
            continue
        line = display_value(package.name, headers[0])
        line += display_value(
            package.status,
            headers[1],
            "" if no_color else package.status_level,
        )
        line += display_value(package.license, headers[2])
        line += display_value(
            package.version,
            headers[3],
            "" if no_color else package.version_level,
        )
        line += display_value(package.next_version, headers[4])
        line += display_value(package.last_version, headers[5])
        line += display_value(
            package.last_release_human,
            headers[6],
            "" if no_color else package.release_level,
        )
        line += display_value(
            package.vulnerabilities,
            headers[7],
            "" if no_color else package.vulnerabilities_level,
        )
        print(line)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse requirements FILE(s).")
    # version
    parser.add_argument(
        "--version",
        action="store_const",
        const=True,
        default=False,
        help="output version information and exit",
    )
    # clear cache
    parser.add_argument(
        "--clear-cache",
        action="store_const",
        const=True,
        default=False,
        help="delete cache file and exit",
    )
    # display informations about cache
    parser.add_argument(
        "--show-cache",
        action="store_const",
        const=True,
        default=False,
        help="display informations about cache and exit",
    )
    # clear cache
    parser.add_argument(
        "--update-cache",
        action="store_const",
        const=True,
        default=False,
        help="update information of each package in cache and exit",
    )
    # requirement file
    parser.add_argument(
        "FILE",
        nargs="*",
        help="files to analyse; if no file given, read standard input",
    )
    # colorize output
    parser.add_argument(
        "--no-color",
        action="store_const",
        const=True,
        default=False,
        help="output is displayed without ANSI escapes colors",
    )
    # delay (in days)
    parser.add_argument(
        "--delay",
        default=360,
        type=int,
        help=(
            "delay, in days, after which last release is considered obsolete "
            "(default to 360)"
        ),
    )
    # display only lines with problematic packages
    parser.add_argument(
        "--only-problems",
        action="store_const",
        const=True,
        default=False,
        help="output is limited to obsolete or aging packages",
    )
    # CI output : exit with -1
    parser.add_argument(
        "--ci",
        action="store_const",
        const=True,
        default=False,
        help="if any package has a problem exit with -1 error code",
    )
    # Quiet output
    parser.add_argument(
        "--quiet",
        action="store_const",
        const=True,
        default=False,
        help="no output",
    )
    # no cache
    parser.add_argument(
        "--no-cache",
        action="store_const",
        const=True,
        default=False,
        help=(
            "does not use cache (each package needs a request to pypi to retrieve its "
            "informations)"
        ),
    )
    # no update
    parser.add_argument(
        "--no-update",
        action="store_const",
        const=True,
        default=False,
        help=(
            "does not try to update package informations from pypi, even if it's old"
        ),
    )
    args = parser.parse_args()
    if args.version:
        print(f"Version {VERSION}")
    elif args.clear_cache:
        # Clear cache
        home_path = Path.home().joinpath(".packmon")
        os.makedirs(home_path, exist_ok=True)
        cache_file = os.path.join(home_path, "packages.json")
        try:
            os.remove(cache_file)
        except FileNotFoundError:
            # No cache present
            pass
    elif args.show_cache:
        display_cache_informations()
    elif args.update_cache:
        update_cache()
    else:
        requirements = []
        if len(args.FILE) == 0:
            line = input()
            try:
                while line != "":
                    if len(line.strip()) != 0 and line.strip()[0] != "#":
                        requirements.append(line)
                    line = input()
            except EOFError:
                pass
        else:
            for filename in args.FILE:
                with open(filename) as file_handler:
                    for line in file_handler.read().splitlines():
                        if len(line.strip()) != 0 and line.strip()[0] != "#":
                            requirements.extend([line])

        packages = update(
            requirements, args.delay, args.no_cache, args.no_update, args.quiet
        )
        output(packages, args.no_color, args.only_problems, args.quiet)
        if args.ci:
            for package in packages:
                if package.has_problem:
                    sys.exit(1)
