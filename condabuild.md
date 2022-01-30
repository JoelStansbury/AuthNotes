# Conda Build

## Cookiecutter
Building a conda package requires a specific directory structure. I don't know all of the specifics so I'm just going to share what worked for me.

`conda install cookiecutter`

`cookiecutter https://github.com/conda/cookiecutter-conda-python.git`

This will setup a template to use for the project (see [https://github.com/conda/cookiecutter-conda-python](https://github.com/conda/cookiecutter-conda-python) for more info, albeit not nearly enough info for a smooth-brain like me).

## meta.yaml
```yaml
{% set data = load_setup_py_data() %}

package:
  name: ipypdf
  version: {{ data['version'] }}

source:
  path: ..

build:
  # If the installation is complex, or different between Unix and Windows, use
  # separate bld.bat and build.sh files instead of this key.  Add the line
  # "skip: True  # [py<35]" (for example) to limit to Python 3.5 and newer, or
  # "skip: True  # [not win]" to limit to Windows.
```
This `script` declaration is how conda will install your package after it grabs all of the dependencies. `{{ PYTHON }} -m pip install -vv .` is more or less the same as `pip install .`
```yaml
  script: {{ PYTHON }} -m pip install -vv .
  noarch: python
  
  entry_points:
    {% for entry in data['entry_points']['console_scripts'] %}
      - {{ entry.split('=')[0].strip() }} = {{ entry.split('=')[1].strip() }}
    {% endfor %}
  

requirements:
  # if you need compilers, uncomment these
  #    read more at https://docs.conda.io/projects/conda-build/en/latest/resources/compiler-tools.html
  # build:
  #   - {{ compilers('c') }}
  host:
    - python
    - pip
    - setuptools
```
Here is where you declare all of the conda packages that your package requires to run.

Unfortunately I cannot find any example of requiring pypi dependencies. 
I'm pretty sure there is one, but people seem reluctant to elaborate as it is not recommended. 
The current answer seems to be, make a conda package for the dependency and upload it to conda-forge 
\**[forehead](https://www.urbandictionary.com/define.php?term=forehead)*, then you can require it in your package.
```yaml
  run:
    - python
    - pywin32 # [win]
    - spacy
    - ipycanvas
    - ipycytoscape
    - ipyevents
    - ipywidgets
    - ipytree
    - jupyterlab >=3.0
    - numpy <=1.19.3,>=1.13
    - opencv
    - pandas
    - pdf2image
    - pytesseract
    - tesseract
    - traitlets
    - spacy-model-en_core_web_lg
```
This seems to be a _"it might work if you're lucky"_ option. 
My understanding here is that setup.py searches on pip, 
so this will fail for packages which are named differently on conda 
(e.g. `opencv` on conda, vs `opencv-python` on pip) and for packages which are 
hosted on pypi but not conda-forge.
```yaml
    # dependencies are defined in setup.py
    # {% for dep in data['install_requires'] %}
    # - {{ dep.lower() }}
    # {% endfor %}

test:
  source_files:
    - tests
  requires:
    - pytest
    - pytest-cov
  commands:
    - pytest
```
This is a useful test to include. It literally just tries to import the package (albeit, the cookiecutter recipe I used here does this by default anyways).
```yaml
  imports:
    - ipypdf

about:
  home: https://github.com/JoelStansbury/ipypdf
  summary: Jupyter widget for applying nlp to pdf documents
  license: {{ data.get('license') }}
  license_file: LICENSE
```
## Building a package
`conda install conda-build`

`cd WHEREVER_YOU_RAN_COOKIECUTTER` (the folder above the folder that cookiecutter made for your package)

`conda build PACKAGE --output-folder="OUTPUT_PATH"` 
  * PACKAGE: is whatever name you gave your package in the cookiecutter config
  * OUTPUT_PATH: Where you want conda to dump everything (including the `.tar.bz2` file we're working for)

## Installing the package
You would think that this would be possible wouldn't you. I mean, you're literally making a set of instructions for how to build your project from scratch. Alas, this functionality actually is not supported for some reason.

There is a potential workaround involving a local conda channel, but it doesn't seem to work for me, so your mileage may vary.
https://github.com/conda/conda/issues/1884

> Note: The problem is with grabing dependencies, so if your package doesn't use any external libraries you can test it with <br>
> `conda install package_name-version-py....tar.bz2` <br>
> By external, I mean: not installed in the conda environment you are doing the manual testing

Regardless, the part that you would want to test (assuming you are new to conda build since you are reading this) is whether or not your meta.yaml instructions actually install the stuff your package needs. As far as I can tell, testing this is not supported. And judging by this comment https://github.com/conda/conda/issues/1884#issuecomment-181093847, I would not hold your breath for a fix.

