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
I'm pretty sure there is one, but people seem reluctant to say how as it is not recommended. 
The current answer is, make a conda package for the dependency and upload it to conda-forge 
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
hosted on pypi but no one has spent the time to build and upload a conda package.
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

## Testing the package (sanity check)
> Note: I'm still working this part out. The windows section almost works, but it seems to ignore the requirement constraints in `meta.yaml`. I know it is not a problem with the `meta.yaml` during the test (automatically run at the end of the `conda build` command, you can see all of the package versions and they are correct)
### Windows
I think this is probably not how it is supposed to work (you'll see why in the linux section) but this is what works for me.

_from the same dir you ran `conda build`_

1. Open a new terminal with conda (Not sure why but if you do the next few steps in the same terminal you ran `conda build` then conda will not be able to pull any dependencies your package needs)
2. Create an empty test environment (with python)
    `conda create -n test python`
    `conda activate test`
3. Install your package: _starting from the same dir you ran `conda build`_
  ```
  cd build/noarch
  conda install --use-local FULL_TAR_FILENAME
  conda install --use-local PACKAGE -c conda-forge
  ```

Again, not sure why the two separate installs are necessary (and I cannot find any other reference saying this is how to do it), this is just what I need to do on my machine.

  * If you just run `conda install --use-local PACKAGE -c conda-forge` then conda will look for your package on conda-forge and say it couldn't find it
  * On the contrary, if you just run `conda install --use-local FULL_TAR_FILENAME` then the package doesn't get installed.
  * However, if your package doesn't need anything from conda-forge I think you can just use `conda install --use-local PACKAGE`

### Ubuntu
I think this should work, but I still need to test it again to make sure.

> Note: As I write this I'm remembering some issues I had (and couldn't solve) on my linux system, and am starting to think maybe it could be solved with new terminal workaround I needed in windows.

```
conda create - test python
conda activate test
cd build/noarch
conda install --use-local PACKAGE -c conda-forge
```

