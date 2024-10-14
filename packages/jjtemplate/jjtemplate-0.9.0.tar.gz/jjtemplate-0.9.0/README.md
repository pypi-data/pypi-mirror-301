# jjtemplate

Jinja2 Templating with JSON files

## Example

`example.txt.jinja`:

```
Hello, {{ name }}.

```

`example.json`:

```json
{
    "name": "world"
}
```

You run:

```console
$ jjtemplate -o result.txt example.txt.jinja example.json
```

Then you get `result.txt`:

```
Hello, world.

```

## Install

```console
$ pip install jjtemplate
```


## Usage


```
usage: jjtemplate [-h] [-i IMPORT_NAME] [-o OUTPUT] template_file [json_files ...]

positional arguments:
  template_file         Jinja2 template file
  json_files            JSON files loaded to the context (top-level object must
                        be a dictionary)

optional arguments:
  -h, --help            show this help message and exit
  -i IMPORT_NAME, --import IMPORT_NAME
                        import Python module to the context (can be put
                        multiple times)
  -o OUTPUT, --output OUTPUT
                        output file name
```

Installed `jjtemplate` command runs `main` function of `jjtemplate.py`, which
is the sole entire content of the module.

You can copy `jjtemplate.py` and add it to your project freely.  See the
License section bellow.

## References

- [Template Designer Documentation — Jinja Documentation (3.1.x)][1]
- [JSON][2]

[1]:https://jinja.palletsprojects.com/en/3.1.x/templates/
[2]:https://www.json.org/

## License

jjtemplate is marked with CC0 1.0. To view a copy of
this license, visit &lt;https://creativecommons.org/publicdomain/zero/1.0/&gt;.

(In other words, public domain.)
