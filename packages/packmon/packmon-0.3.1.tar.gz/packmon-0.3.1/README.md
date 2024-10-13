packmon is a cli tool to monitor aging packages in order to see if somes become obsolete
or updates are availables.


# Philosophy

As a simple monitoring tool, packmon is pure-python in order to simplify its use.


# Usage

1. Install packmon globally on your system
2. Use it to detect obsolescence and vulnerabilities in any of your project (virtual
    environment or not)


## Example

System level installation:

    apt install packmon

Then use it:

    packmon myproject/requirements.txt

or

    pip freeze |packmon

event through pipes:

    curl -s https://raw.githubusercontent.com/AFPy/Potodo/master/requirements.txt |packmon

Result :

![sample](https://framagit.org/Mindiell/packmon/-/raw/main/media/sample.png)


## Options

### Cache management

Those options help you to manage packages informations from packmon's cache. Cache file
is stored into **HOME_USER/.packmon/packmon.json**.

#### clear-cache

Simply delete the cache file.

#### show-cache

Shows some informations about actual cache.

#### update-cache

Update each package from cache.

#### no-cache

Does not use cache when using packmon. With this option set, each package will call pypi
to retrieve informations.

#### no-update

Does not try to refresh a package information, even if it's over than the max dayslimit.

### Output management

#### no-color

Packmon will try to display colorized results to help user to see potential problems for
each package. With this option set, no color will be used.

#### quiet

With this option set, packmon will write nothing on the standard output (errors will
still be displayed using error output though).

#### only-problems

This option will limit the results only to obsolete packages.

### CI compatibility

#### ci

With this option set, packmon will return 1 if any package is obsolete or to update.
