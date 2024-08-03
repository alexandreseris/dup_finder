# dup_finder

A small script used to retrieve duplicates file, either by name, size and/or content (content mode works by reading the file as binary so you can use it to check binary-like files)

Support Unix style pattern matching (check [this](https://docs.python.org/3.10/library/fnmatch.html) for more information about the synthax)

tested with python 3.10, no dependencies, you can use it as is :)

## Usage from command line

```sh
usage: dup_finder [-h] [-c [{content,name,size} ...]] [-p [PATTERNS ...]] [-x [EXCLUDE ...]] [-i] folders [folders ...]

program to find and remove file duplicates in a directory

positional arguments:
  folders               folder used to search

options:
  -h, --help            show this help message and exit
  -c [{content,name,size} ...], --comparison-type [{content,name,size} ...]
                        comparison used to target duplicates. Defaults to name and size
  -p [PATTERNS ...], --file-pattern [PATTERNS ...]
                        file pattern used to restrict search
  -x [EXCLUDE ...], --exclude-file-pattern [EXCLUDE ...]
                        file pattern used to exclude from search
  -i, --interactive-remove
                        interactively ask for which file to remove instead of just printing the paths

usage example: python3 dup_finder -c content -p '*.csv' '*.json' -i -- folder1 folder2
```
