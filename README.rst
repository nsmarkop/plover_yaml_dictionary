Plover YAML Dictionary
======================

YAML dictionary support for
`Plover <https://github.com/openstenoproject/plover>`__.

Installation
------------

Download the latest version of Plover for your operating system from the
`releases page <https://github.com/openstenoproject/plover/releases>`__.
Only versions 4.0.0.dev1 and higher are supported.

1. Open Plover
2. Navigate to the Plugin Manager tool
3. Select the “plover-yaml-dictionary” plugin entry in the list
4. Click install
5. Restart Plover

The same method can be used for updating and uninstalling the plugin.

Dictionary Format
-----------------

The YAML dictionary format used by this plugin maps translations to
strokes rather than strokes to translations which differs from the
default JSON dictionary format used by Plover. For a basic comparison,

JSON:

.. code:: json

    {
    "PHRO*EFR": "Plover",
    "PHRO*FR": "plover",
    "PHROFR": "Plover",
    }

YAML:

.. code:: yaml

    Plover:
    - PHRO*EFR
    - PHROFR
    plover:
    - PHRO*FR

Comments manually added within the YAML dictionary file are currently
not preserved due to performance limitations of the YAML package being
used.

Converting JSON dictionaries to YAML
------------------------------------

You can use the following script to take an input JSON dictionary file
path and output YAML dictionary file path to convert existing Plover
JSON dictionaries to the YAML format used by this plugin.

.. code:: python


    import json

    import ruamel.yaml


    JSON_FILENAME = r''
    YAML_FILENAME = r''

    # Load JSON dictionary
    with open(JSON_FILENAME, 'r', encoding='utf-8') as in_file:
        in_data = json.load(in_file)

    # Group dictionary by value, sorted alphabetically
    out_data = {}

    for key, value in sorted(in_data.items(), key=lambda x: x[1].casefold()):
        out_data.setdefault(value, []).append(key)
        out_data[value] = sorted(out_data[value])

    # Write dictionary to YAML
    with open(YAML_FILENAME, 'w', encoding='utf-8') as out_file:
        yaml = ruamel.yaml.YAML(typ='safe')
        yaml.allow_unicode = True
        yaml.default_flow_style = False
        yaml.indent(sequence=4, offset=2)
        yaml.dump(out_data, out_file)

