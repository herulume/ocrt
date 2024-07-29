# OCRT

Python script to generate openers for [OpenerCreator](https://github.com/herulume/OpenerCreator) from images.

Currently supported classes: SGE, RPR.

## About

To get started, run the following (skip `nix develop` if you have nix-direv):

```
$ nix develop
$ poetry run python ocrt <path_to_opener_image>
```
`<path_to_opener_image>` should be an opener's PNG from The Balance, which will be exported as a JSON file to `output/<job>_opener.json`. 

Openers with a high number of skills can take a bit to generate.



Thank you [JetBrains](https://www.jetbrains.com/pycharm/) for the [open-source license](https://www.jetbrains.com/community/opensource/).
