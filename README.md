### Rez-packages

This is a collection of [Rez](http://nerdvegas.github.io/rez/) packages to help download, build and deploy various applications and open source projects often used in the Film, VFX and Animation.

_Note that this currently only includes packages for **Windows** see [Different OS implementations](#different-os-implementations)_

**WIP** 

This is a work in progress and under heavy development repository. 
Feel free to test and create issues for any issues you're facing, however at this stage I would not using these in production without thorough testing.


## Quick Start Guide

1. clone this repository.
2. `cd` into the package you would like to build and install.
3. `rez build --install` to do a full install of that package.
4. `rez env {package}` to run an environment with that package, e.g. `rez env maya`

_Note that some package will require additional packages to be available to `rez` for building, see [Missing required packages](#missing-required-packages)_

## Build, install or reference packages

**Build from source, install precompiled libraries or reference packages**

Some packages need to build from source (e.g. `openexr` or `zlib`) and in some cases we download precompiled binaries/installers (e.g. `mtoa` or `redshift`). 
For other cases we only generate ["reference packages"](https://github.com/mottosso/rez-for-projects#q-why-reference-packages) for applications we'll just have the Artist still install locally, this the case for DCCs like `maya`, `fusion`, `houdini`.

#### Build from source

- When building from source the generator is currently forced to build using `Visual Studio 15 2017 Win64` in the `rezbuild.py` scripts for the package.
- When `cmake` is available for the source we build and compile through `cmake`

Packages that did not lend themselves to a simple rez-build are build using simple bash scripts, these can be spotted by the build.sh in the root directory.  These packages require you to set some environment variables in build.sh to specify where packages should be released to.  

#### Reference packages

The reference packages reference the default installation locations for the applications and all the reference package does is set the relevant environment variables for the Application to run as expected.


## Additional notes

#### Different OS implementations

Currently this repository contains **only!** rez-packages that build and distribute the *Windows* variants. This could be expanded to support *Mac OS* and *Linux* however as for us internall there's no rush to support that feel free to submit PRs to implement this behavior.

#### Missing required packages

In some cases packages require certain packages to be available that are not in this repository, e.g. `7zip`. 
In those cases we recommend install [`rez-pipz`](https://github.com/mottosso/rez-pipz) and [`rez-scoopz`](https://github.com/mottosso/rez-scoopz) to easily install these packages, so that one can for example do:

```python
# Install some dependencies of this repository
rez env pipz -- install jinja2
rez env scoopz -- install python
rez env scoopz -- install cmake
rez env scoopz -- install make
rez env scoopz -- install 7zip

# Or to install for a specific Python version
rez env python-3.7 pipz -- install PySide2
```

In other cases it requires that you have some of the other packages available that *are* inside this rez packages repository. In those cases you'll need to `rez build --install` those first to make sure they are available.

#### Other rez-packages repositories

If you're looking for more references on Rez packages here are some other repositories you can look into:

- https://github.com/UTS-AnimalLogicAcademy/open-source-rez-packages
- https://github.com/predat/rez-packages
- [Rez Issue #673: Recipe Repositories](https://github.com/nerdvegas/rez/issues/673) (not a package repository, but shows some thoughts about the future for package repositories)