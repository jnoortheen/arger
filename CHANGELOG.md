# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [2.1.0](https://github.com/jnoortheen/arger/compare/v2.0.2...v2.1.0) (2025-07-03)


### Features

* update test dependencies ([e78ce7e](https://github.com/jnoortheen/arger/commit/e78ce7ee313ab49463f42ffcd853160f84449250))

## [2.0.2](https://github.com/jnoortheen/arger/compare/v2.0.1...v2.0.2) (2025-07-03)


### Bug Fixes

* PyPI release automation ([4d6227f](https://github.com/jnoortheen/arger/commit/4d6227f31fc997a8cac9221a156e0d86ca089885))

## [2.0.1](https://github.com/jnoortheen/arger/compare/v2.0.0...v2.0.1) (2025-07-03)


### Bug Fixes

* PyPI release by CI actions ([76cb5c0](https://github.com/jnoortheen/arger/commit/76cb5c07adbd4bd9411d19d18a574415a036eed5))

## [2.0.0](https://github.com/jnoortheen/arger/compare/v1.4.8...v2.0.0) (2025-07-03)


### ⚠ BREAKING CHANGES

* drop python 3.9 support

### Features

* support `X|None` optionals ([93a3c5f](https://github.com/jnoortheen/arger/commit/93a3c5f87b468a066ca0e02c81978ba7b33c6713))
* update release action ([fe93827](https://github.com/jnoortheen/arger/commit/fe938279ce9dd3b5ef518011e1cb8a49d2139f11))


### Bug Fixes

* **CI:** test action ([b9c3d1a](https://github.com/jnoortheen/arger/commit/b9c3d1a82b8833fbceb7643dda146b8c432b6540))
* failing tests ([8188486](https://github.com/jnoortheen/arger/commit/818848648c7c5bad7e30464c408c2ba699e3b7e6))
* ruff lint ([286d0b5](https://github.com/jnoortheen/arger/commit/286d0b5740502b328c16317140e3ae4965986294))
* use new pytest-lazy-fixtures ([b29d923](https://github.com/jnoortheen/arger/commit/b29d923fda1c63e6cc13d5866a0bda63301315f0))


### Documentation

* Update README.md ([6fb957b](https://github.com/jnoortheen/arger/commit/6fb957b347e9b6d4f110eb12c5061bfe1febb766))


### Code Refactoring

* drop python 3.9 support ([8a488cb](https://github.com/jnoortheen/arger/commit/8a488cbf55ba4f283888c106f5137da0b8fbffd7))

## [v1.4.8](https://github.com/jnoortheen/arger/releases/tag/v1.4.8) - 2022-11-09

<small>[Compare with v1.4.7](https://github.com/jnoortheen/arger/compare/v1.4.7...v1.4.8)</small>

### Bug Fixes
- Test action ([f393028](https://github.com/jnoortheen/arger/commit/f3930280fd915cd9e57652770597c4de19a9ce52) by Noortheen Raja).


## [v1.4.7](https://github.com/jnoortheen/arger/releases/tag/v1.4.7) - 2022-11-09

<small>[Compare with v1.4.6](https://github.com/jnoortheen/arger/compare/v1.4.6...v1.4.7)</small>


## [v1.4.6](https://github.com/jnoortheen/arger/releases/tag/v1.4.6) - 2022-11-09

<small>[Compare with v1.4.4](https://github.com/jnoortheen/arger/compare/v1.4.4...v1.4.6)</small>

### Code Refactoring
- Remove make,tox ([64e4133](https://github.com/jnoortheen/arger/commit/64e4133c327957cd6a367d93987e77efcf74e985) by Noortheen Raja).


## [v1.4.4](https://github.com/jnoortheen/arger/releases/tag/v1.4.4) - 2022-07-02

<small>[Compare with v1.4.2](https://github.com/jnoortheen/arger/compare/v1.4.2...v1.4.4)</small>

### Bug Fixes
- Set flags from docstring ([3d25821](https://github.com/jnoortheen/arger/commit/3d2582129497e3aafb5f8e79f98878a4bc9b688a) by Noortheen Raja).


## [v1.4.2](https://github.com/jnoortheen/arger/releases/tag/v1.4.2) - 2021-10-16

<small>[Compare with v1.3.8](https://github.com/jnoortheen/arger/compare/v1.3.8...v1.4.2)</small>

### Bug Fixes
- Handle py310 help out change ([cf3a570](https://github.com/jnoortheen/arger/commit/cf3a570be35f3a74fe155177a87c0322d9e8f1ec) by Noortheen Raja).
- Github py version ([04912ec](https://github.com/jnoortheen/arger/commit/04912ec1b862ab33e013740baf697b268b1be498) by Noortheen Raja).
- Qa errors ([2d53c81](https://github.com/jnoortheen/arger/commit/2d53c810dee14887786b12a66f6230f48bd270ee) by Noortheen Raja).


## [v1.3.8](https://github.com/jnoortheen/arger/releases/tag/v1.3.8) - 2021-04-11

<small>[Compare with v1.3.7](https://github.com/jnoortheen/arger/compare/v1.3.7...v1.3.8)</small>

### Bug Fixes
- Handle failing mkdocs build ([8d72d4d](https://github.com/jnoortheen/arger/commit/8d72d4db25ea39c52f1ddca31975f12db16ac2c8) by Noortheen Raja).


## [v1.3.7](https://github.com/jnoortheen/arger/releases/tag/v1.3.7) - 2021-04-11

<small>[Compare with v1.3.6](https://github.com/jnoortheen/arger/compare/v1.3.6...v1.3.7)</small>

### Bug Fixes
- Typing.optional kwarg handling ([76978c3](https://github.com/jnoortheen/arger/commit/76978c378ee8b706c7ed35e60cbd3b82137b4c29) by Noortheen Raja). Related issues/PRs: [#2](https://github.com/jnoortheen/arger/issues/2)


## [v1.3.6](https://github.com/jnoortheen/arger/releases/tag/v1.3.6) - 2021-02-17

<small>[Compare with v1.3.5](https://github.com/jnoortheen/arger/compare/v1.3.5...v1.3.6)</small>

### Bug Fixes
- Failing pytkdocs api docstring getter ([7f2222c](https://github.com/jnoortheen/arger/commit/7f2222c812c4171e342dfb2dec6571684849602b) by Noortheen Raja).


## [v1.3.5](https://github.com/jnoortheen/arger/releases/tag/v1.3.5) - 2021-02-16

<small>[Compare with v1.3.4](https://github.com/jnoortheen/arger/compare/v1.3.4...v1.3.5)</small>

### Bug Fixes
- Py36 compatibility for get_origin(annotated) ([20abc00](https://github.com/jnoortheen/arger/commit/20abc00734ead149d1dd9ef5228928c46bea15eb) by Noortheen Raja).


## [v1.3.4](https://github.com/jnoortheen/arger/releases/tag/v1.3.4) - 2021-02-16

<small>[Compare with v1.3.1](https://github.com/jnoortheen/arger/compare/v1.3.1...v1.3.4)</small>


## [v1.3.1](https://github.com/jnoortheen/arger/releases/tag/v1.3.1) - 2021-02-16

<small>[Compare with v1.3.0](https://github.com/jnoortheen/arger/compare/v1.3.0...v1.3.1)</small>

### Features
- Use annotated for arguments ([ddbdf38](https://github.com/jnoortheen/arger/commit/ddbdf381f772d505fe15ad577d8d57aa3a585ab9) by Noortheen Raja).


## [v1.3.0](https://github.com/jnoortheen/arger/releases/tag/v1.3.0) - 2021-02-16

<small>[Compare with v1.2.11](https://github.com/jnoortheen/arger/compare/v1.2.11...v1.3.0)</small>

### Bug Fixes
- Py-lint errors ([0fa651a](https://github.com/jnoortheen/arger/commit/0fa651a36e0c3d983b299a88fc4a4bb1e2431548) by Noortheen Raja).


## [v1.2.11](https://github.com/jnoortheen/arger/releases/tag/v1.2.11) - 2021-02-16

<small>[Compare with v1.2.10](https://github.com/jnoortheen/arger/compare/v1.2.10...v1.2.11)</small>

### Bug Fixes
- Py36 literal compatibilty ([2baf271](https://github.com/jnoortheen/arger/commit/2baf271f6b47ee2c1c36efe071e749a550afbe1f) by Noortheen Raja).


## [v1.2.10](https://github.com/jnoortheen/arger/releases/tag/v1.2.10) - 2021-02-16

<small>[Compare with v1.2.9](https://github.com/jnoortheen/arger/compare/v1.2.9...v1.2.10)</small>

### Features
- Add literal support for choices ([82322f7](https://github.com/jnoortheen/arger/commit/82322f791408a674e6c81f74a9cd4287a666d550) by Noortheen Raja). Related issues/PRs: [#1](https://github.com/jnoortheen/arger/issues/1)


## [v1.2.9](https://github.com/jnoortheen/arger/releases/tag/v1.2.9) - 2021-01-27

<small>[Compare with v1.2.8](https://github.com/jnoortheen/arger/compare/v1.2.8...v1.2.9)</small>

### Bug Fixes
- When `param:bool=true` used raises error ([1537b41](https://github.com/jnoortheen/arger/commit/1537b4189e0a4273ac33e469b1491560e2aafd05) by Noortheen Raja).


## [v1.2.8](https://github.com/jnoortheen/arger/releases/tag/v1.2.8) - 2021-01-02

<small>[Compare with v1.2.7](https://github.com/jnoortheen/arger/compare/v1.2.7...v1.2.8)</small>

### Code Refactoring
- Split __version__ to new module ([e60b059](https://github.com/jnoortheen/arger/commit/e60b0594ee14a110bede7b45ec5b4541d6e09262) by Noortheen Raja).


## [v1.2.7](https://github.com/jnoortheen/arger/releases/tag/v1.2.7) - 2020-12-23

<small>[Compare with v1.2.6](https://github.com/jnoortheen/arger/compare/v1.2.6...v1.2.7)</small>

### Features
- Add support for typing.optional <-> nargs="?" ([12ab8c7](https://github.com/jnoortheen/arger/commit/12ab8c771f9a91600b2e4695776f83973b7e4f9f) by Noortheen Raja).


## [v1.2.6](https://github.com/jnoortheen/arger/releases/tag/v1.2.6) - 2020-12-16

<small>[Compare with v1.2.5](https://github.com/jnoortheen/arger/compare/v1.2.5...v1.2.6)</small>


## [v1.2.5](https://github.com/jnoortheen/arger/releases/tag/v1.2.5) - 2020-12-16

<small>[Compare with v1.2.4](https://github.com/jnoortheen/arger/compare/v1.2.4...v1.2.5)</small>


## [v1.2.4](https://github.com/jnoortheen/arger/releases/tag/v1.2.4) - 2020-12-07

<small>[Compare with v1.2.3](https://github.com/jnoortheen/arger/compare/v1.2.3...v1.2.4)</small>


## [v1.2.3](https://github.com/jnoortheen/arger/releases/tag/v1.2.3) - 2020-12-07

<small>[Compare with v1.2.2](https://github.com/jnoortheen/arger/compare/v1.2.2...v1.2.3)</small>


## [v1.2.2](https://github.com/jnoortheen/arger/releases/tag/v1.2.2) - 2020-12-07

<small>[Compare with v1.2.1](https://github.com/jnoortheen/arger/compare/v1.2.1...v1.2.2)</small>


## [v1.2.1](https://github.com/jnoortheen/arger/releases/tag/v1.2.1) - 2020-12-07

<small>[Compare with v1.2.0](https://github.com/jnoortheen/arger/compare/v1.2.0...v1.2.1)</small>

### Features
- Support add arger.add_commands method ([a9cb3fa](https://github.com/jnoortheen/arger/commit/a9cb3faa34b1900c7bdb5093e04acb0ee07ea835) by Noortheen Raja).


## [v1.2.0](https://github.com/jnoortheen/arger/releases/tag/v1.2.0) - 2020-12-06

<small>[Compare with v1.1.0](https://github.com/jnoortheen/arger/compare/v1.1.0...v1.2.0)</small>


## [v1.1.0](https://github.com/jnoortheen/arger/releases/tag/v1.1.0) - 2020-12-05

<small>[Compare with v1.0.11](https://github.com/jnoortheen/arger/compare/v1.0.11...v1.1.0)</small>

### Features
- Option to customize sub-commands title ([982dab6](https://github.com/jnoortheen/arger/commit/982dab6ba19683ccd1bbf51c2eb98f3cb261f871) by Noortheen Raja).


## [v1.0.11](https://github.com/jnoortheen/arger/releases/tag/v1.0.11) - 2020-12-04

<small>[Compare with v1.0.10](https://github.com/jnoortheen/arger/compare/v1.0.10...v1.0.11)</small>

### Bug Fixes
- When *varargs used, it caused incorrect function dispatch ([0209820](https://github.com/jnoortheen/arger/commit/020982086c8e8a270510cabc4b61240f0dc0523f) by Noortheen Raja).


## [v1.0.10](https://github.com/jnoortheen/arger/releases/tag/v1.0.10) - 2020-11-28

<small>[Compare with v1.0.9](https://github.com/jnoortheen/arger/compare/v1.0.9...v1.0.10)</small>


## [v1.0.9](https://github.com/jnoortheen/arger/releases/tag/v1.0.9) - 2020-11-28

<small>[Compare with v1.0.8](https://github.com/jnoortheen/arger/compare/v1.0.8...v1.0.9)</small>

### Code Refactoring
- Use _init_subclass to register docstring parsers ([ac486bd](https://github.com/jnoortheen/arger/commit/ac486bd43866e24e6ae930bcb21b09e3f47456ab) by Noortheen Raja).

### Features
- Use prefix_chars settings to generate flags ([c9eabb2](https://github.com/jnoortheen/arger/commit/c9eabb203926910572c9e7946b7d15a7a7b2e1cf) by Noortheen Raja).


## [v1.0.8](https://github.com/jnoortheen/arger/releases/tag/v1.0.8) - 2020-11-11

<small>[Compare with v1.0.7](https://github.com/jnoortheen/arger/compare/v1.0.7...v1.0.8)</small>

### Bug Fixes
- Update numpy docstring parser ([b479611](https://github.com/jnoortheen/arger/commit/b479611ca0d3ae62cb359b28a4cf40af04debe52) by Noortheen Raja).


## [v1.0.7](https://github.com/jnoortheen/arger/releases/tag/v1.0.7) - 2020-11-09

<small>[Compare with v1.0.6](https://github.com/jnoortheen/arger/compare/v1.0.6...v1.0.7)</small>

### Code Refactoring
- Merge funcs and maian modules ([fd0ab1c](https://github.com/jnoortheen/arger/commit/fd0ab1c1d6dfb994c145c083de9ab89b879daacc) by Noortheen Raja).
- Remove parsedfunc type ([37810d6](https://github.com/jnoortheen/arger/commit/37810d6b1b7aa74d10a727659b846ebae8ab0ac2) by Noortheen Raja).
- Merge classes that handle argument and option creation ([023877d](https://github.com/jnoortheen/arger/commit/023877d72ddd1a5c22314594205ed371bbce60d4) by Noortheen Raja).
- Update typeaction handling vararg ([351979f](https://github.com/jnoortheen/arger/commit/351979fc37ef0b82df823e9105da25bc1a2746f9) by Noortheen Raja).
- Replace namedtuple param with inspect.parameter ([545cb80](https://github.com/jnoortheen/arger/commit/545cb803134c58602d9dda72c5853ba6e40053f7) by Noortheen Raja).
- Merge into single module parsers ([73e4f08](https://github.com/jnoortheen/arger/commit/73e4f0830bebb4e0bd4292ebd32fa2a1bcfd434d) by Noortheen Raja).
- Update argument update funcs ([08f9080](https://github.com/jnoortheen/arger/commit/08f90805f60caa4559bf480ba3109f2f638d58b7) by Noortheen Raja).
- Reduce number of modules ([ca4471f](https://github.com/jnoortheen/arger/commit/ca4471ffb180e5024f45f71f9b3fa6aa227285da) by Noortheen Raja).
- Update usage of types inside docstrings ([7e2f20a](https://github.com/jnoortheen/arger/commit/7e2f20aa88404ce8ac4276a75c7b3c98aa8b89bd) by Noortheen Raja).
- Move code from types to typing_utils ([b9c779c](https://github.com/jnoortheen/arger/commit/b9c779c4bc4ec06b94170e8e023b98d6ee06dc5e) by Noortheen Raja).

### Features
- Add version flag/action by passing version string to arger ([286328b](https://github.com/jnoortheen/arger/commit/286328bdcadf2dc8866cbe4b3202ba035bf54872) by Noortheen Raja).
- Create subcommands as soon as arger initiated ([9848e4e](https://github.com/jnoortheen/arger/commit/9848e4eb7c552e17624c32a9a3b53875fb93587a) by Noortheen Raja).
- Publish docs to github-pages ([57894fa](https://github.com/jnoortheen/arger/commit/57894fa5b7529283c3c23291e0350758a1ca413d) by Noortheen Raja).


## [v1.0.6](https://github.com/jnoortheen/arger/releases/tag/v1.0.6) - 2020-11-01

<small>[Compare with v1.0.5](https://github.com/jnoortheen/arger/compare/v1.0.5...v1.0.6)</small>

### Features
- Add python 3.9 support ([c647243](https://github.com/jnoortheen/arger/commit/c647243b1dc131b3b6d7b11a1e1c2118d3e08628) by Noortheen Raja).


## [v1.0.5](https://github.com/jnoortheen/arger/releases/tag/v1.0.5) - 2020-11-01

<small>[Compare with v1.0.3](https://github.com/jnoortheen/arger/compare/v1.0.3...v1.0.5)</small>


## [v1.0.3](https://github.com/jnoortheen/arger/releases/tag/v1.0.3) - 2020-11-01

<small>[Compare with v1.0.2](https://github.com/jnoortheen/arger/compare/v1.0.2...v1.0.3)</small>

### Features
- Implement skipping private arguments ([24d7404](https://github.com/jnoortheen/arger/commit/24d74047064071240244651475b57f00f1470426) by Noortheen Raja).


## [v1.0.2](https://github.com/jnoortheen/arger/releases/tag/v1.0.2) - 2020-11-01

<small>[Compare with v1.0.1](https://github.com/jnoortheen/arger/compare/v1.0.1...v1.0.2)</small>

### Features
- Add py39 to ci tests ([ec32e84](https://github.com/jnoortheen/arger/commit/ec32e84ab71d51be0771d29d1ab2d1ac117a033f) by Noortheen Raja).


## [v1.0.1](https://github.com/jnoortheen/arger/releases/tag/v1.0.1) - 2020-11-01

<small>[Compare with v0.4.1](https://github.com/jnoortheen/arger/compare/v0.4.1...v1.0.1)</small>

### Bug Fixes
- Py36 compat with re.pattern ([c695861](https://github.com/jnoortheen/arger/commit/c6958619da3423cdc4590c25a3767a2ed7589a1a) by Noortheen Raja).

### Code Refactoring
- Rewrite arger using new docstring parser ([9cd93a5](https://github.com/jnoortheen/arger/commit/9cd93a5b7de69765803e20efeafdf274e06867f4) by Noortheen Raja).
- Update docstring parser and add tests ([3d9d681](https://github.com/jnoortheen/arger/commit/3d9d681ad9875f0c0b632220b6415e2c9668dc3d) by Noortheen Raja).
- Remove external dependency to parse docstring ([ac72e9f](https://github.com/jnoortheen/arger/commit/ac72e9fb799d3c24b574ff6d7ff5f0dd4084f163) by Noortheen Raja).

### Features
- First stable release ([fc6e935](https://github.com/jnoortheen/arger/commit/fc6e935c50ac126d16b3811ee0d22545f6ad100b) by Noortheen Raja).
- Any level of nested commands will get dispatched ([9e579b1](https://github.com/jnoortheen/arger/commit/9e579b15dd42dd52fd88326c108c2af8cbe6c0b1) by Noortheen Raja).
- Use notebook for testing examples ([3ee4310](https://github.com/jnoortheen/arger/commit/3ee43103a8d43d1a057cc8ada76e60f0a978fe6d) by Noortheen Raja).


## [v0.4.1](https://github.com/jnoortheen/arger/releases/tag/v0.4.1) - 2020-04-18

<small>[Compare with v0.4.0](https://github.com/jnoortheen/arger/compare/v0.4.0...v0.4.1)</small>

### Bug Fixes
- Mypy errors ([09111b0](https://github.com/jnoortheen/arger/commit/09111b065cbc0a38b75ebe1984ffd47ce3714936) by Noortheen Raja).


## [v0.4.0](https://github.com/jnoortheen/arger/releases/tag/v0.4.0) - 2020-04-18

<small>[Compare with v0.3.0](https://github.com/jnoortheen/arger/compare/v0.3.0...v0.4.0)</small>

### Bug Fixes
- Py36 compatibility ([fe72990](https://github.com/jnoortheen/arger/commit/fe72990cd590183786984f369b06edd01c5efcba) by Noortheen Raja).
- Variable arg handling ([aaa7109](https://github.com/jnoortheen/arger/commit/aaa7109ae3ecfbbe714802928b3737efb4b008b3) by Noortheen Raja).

### Code Refactoring
- Inherit option from argument ([c581cb9](https://github.com/jnoortheen/arger/commit/c581cb9f2ea8efecbb111c3ecb926bebc9dffa9e) by Noortheen Raja).
- Update typing-utils to work on py36 ([ec6f40a](https://github.com/jnoortheen/arger/commit/ec6f40a81217926bc8528ac8de6579c55bf77fbf) by Noortheen Raja).
- Update parser functions ([3563223](https://github.com/jnoortheen/arger/commit/3563223c7718a631d1dc95f5f539dc1b4a7fae37) by Noortheen Raja).

### Features
- Add support for more complex types ([584e530](https://github.com/jnoortheen/arger/commit/584e53049a0e4a16b5193097052c3a2528ef3006) by Noortheen Raja).
- Add for tuple/list support ([895eb9c](https://github.com/jnoortheen/arger/commit/895eb9c015492c700125eb5c98bad2f45275cca3) by Noortheen Raja).


## [v0.3.0](https://github.com/jnoortheen/arger/releases/tag/v0.3.0) - 2020-04-16

<small>[Compare with v0.2.4](https://github.com/jnoortheen/arger/compare/v0.2.4...v0.3.0)</small>

### Code Refactoring
- Reduce complexity in parser function ([2c2d586](https://github.com/jnoortheen/arger/commit/2c2d58623ae4322bc4c2510f745a11655ee6bfb6) by Noortheen Raja).

### Features
- Implement mkdocs ([6ee7e70](https://github.com/jnoortheen/arger/commit/6ee7e700523ff5ad2765537b5e68ec321487f615) by Noortheen Raja).
- Add support for variadict arguments ([dc857c4](https://github.com/jnoortheen/arger/commit/dc857c427f86cf56403f0bc376317d723e4f0f1b) by Noortheen Raja).


## [v0.2.4](https://github.com/jnoortheen/arger/releases/tag/v0.2.4) - 2020-04-14

<small>[Compare with v0.2.3](https://github.com/jnoortheen/arger/compare/v0.2.3...v0.2.4)</small>

### Bug Fixes
- Setting flags only when not defined ([c9f63d0](https://github.com/jnoortheen/arger/commit/c9f63d0745d5d364f12f6f7192afd8f841886996) by Noortheen Raja).


## [v0.2.3](https://github.com/jnoortheen/arger/releases/tag/v0.2.3) - 2020-04-14

<small>[Compare with v0.2.2](https://github.com/jnoortheen/arger/compare/v0.2.2...v0.2.3)</small>

### Bug Fixes
- Using option to define arguments ([ed87eec](https://github.com/jnoortheen/arger/commit/ed87eecf49ab9da5de422498ef118dad3b67a14a) by Noortheen Raja).

### Code Refactoring
- Rename arger class module ([b8a45d1](https://github.com/jnoortheen/arger/commit/b8a45d11a228bba090aab40380698f678414387f) by Noortheen Raja).

### Features
- Use option for populating arguments ([aef46e7](https://github.com/jnoortheen/arger/commit/aef46e70aafadb8000a3e47c6a4144bed2fbc6d6) by Noortheen Raja).


## [v0.2.2](https://github.com/jnoortheen/arger/releases/tag/v0.2.2) - 2020-04-13

<small>[Compare with v0.2.1](https://github.com/jnoortheen/arger/compare/v0.2.1...v0.2.2)</small>


## [v0.2.1](https://github.com/jnoortheen/arger/releases/tag/v0.2.1) - 2020-04-13

<small>[Compare with v0.2.0](https://github.com/jnoortheen/arger/compare/v0.2.0...v0.2.1)</small>

### Bug Fixes
- Handle tests passing sys.argv ([9226d97](https://github.com/jnoortheen/arger/commit/9226d972553c023dbf4097e7637d88de65fc4367) by Noortheen Raja).


## [v0.2.0](https://github.com/jnoortheen/arger/releases/tag/v0.2.0) - 2020-04-13

<small>[Compare with v0.1.3](https://github.com/jnoortheen/arger/compare/v0.1.3...v0.2.0)</small>

### Features
- Sub-command with a root context function ([0c9d19d](https://github.com/jnoortheen/arger/commit/0c9d19d05c70520b065ecef44863f7355e3da8aa) by Noortheen Raja).
- Add python < 37 compatible type checks ([f478771](https://github.com/jnoortheen/arger/commit/f4787716a8c0c7fbfa384d8a55c22eebba913078) by Noortheen Raja).
- Call nested commands ([662d05a](https://github.com/jnoortheen/arger/commit/662d05ab0fc7ab969e87fe4543dba2d04ab2da45) by Noortheen Raja).
- Add ability to add nested commands ([923a4a0](https://github.com/jnoortheen/arger/commit/923a4a0c34f1e248d8301d2705c2e6d07296eb08) by Noortheen Raja).


## [v0.1.3](https://github.com/jnoortheen/arger/releases/tag/v0.1.3) - 2020-04-11

<small>[Compare with v0.1.2](https://github.com/jnoortheen/arger/compare/v0.1.2...v0.1.3)</small>


## [v0.1.2](https://github.com/jnoortheen/arger/releases/tag/v0.1.2) - 2020-04-11

<small>[Compare with v0.1.1](https://github.com/jnoortheen/arger/compare/v0.1.1...v0.1.2)</small>


## [v0.1.1](https://github.com/jnoortheen/arger/releases/tag/v0.1.1) - 2020-04-11

<small>[Compare with 0.1](https://github.com/jnoortheen/arger/compare/0.1...v0.1.1)</small>


## [0.1](https://github.com/jnoortheen/arger/releases/tag/0.1) - 2020-04-11

<small>[Compare with first commit](https://github.com/jnoortheen/arger/compare/0e07f27250630f02ddfb3d9cc515c724ef30395b...0.1)</small>

### Bug Fixes
- Recognise type from typehint and default value ([405cfad](https://github.com/jnoortheen/arger/commit/405cfad716aa4361232de2df3af9127ef80c7e3b) by Noortheen Raja).
- Mypy type errors ([522954c](https://github.com/jnoortheen/arger/commit/522954cb1fd0be7f52b464d56b9c6b3d985a1551) by Noortheen Raja).
- Test workflow ([951e23e](https://github.com/jnoortheen/arger/commit/951e23efbdd498d669619607ef5f941a6dd5a583) by Noortheen Raja).

### Code Refactoring
- Add arger structs ([6722d7a](https://github.com/jnoortheen/arger/commit/6722d7a267088b6ff905f452a9ab9a373dd5794e) by Noortheen Raja).
- Remove notebooks folder ([d7f303b](https://github.com/jnoortheen/arger/commit/d7f303b2f670e03376c03cdaa4c84eadfddddc22) by Noortheen Raja).
- Move out docstring to sub functions ([e7ecd49](https://github.com/jnoortheen/arger/commit/e7ecd49956eee72891dd793fbffe9493b7265ae2) by Noortheen Raja).

### Features
- Implement single function dispatch ([171e871](https://github.com/jnoortheen/arger/commit/171e871282e2263075d1b548c138970688a8af25) by Noortheen Raja).
- Make arger work with single or multi functions ([5299fba](https://github.com/jnoortheen/arger/commit/5299fbaf5e13edd86bb92991fcfd6683b4d52cf7) by Noortheen Raja).
- Implement parser ([1fd04ad](https://github.com/jnoortheen/arger/commit/1fd04ad5a01d23c4d0cd4e59e366a30e1e5f44ac) by Noortheen Raja).
- Add action to publish package ([e85fe08](https://github.com/jnoortheen/arger/commit/e85fe081cba967b5268d3bb80fbc4424a2e439b1) by Noortheen Raja).
- Add github actions for testing and linting ([d9ea90d](https://github.com/jnoortheen/arger/commit/d9ea90d21aff1214c1b0d61639a1ca19ee7ff19d) by Noortheen Raja).
- Add boilerplate from ([0e07f27](https://github.com/jnoortheen/arger/commit/0e07f27250630f02ddfb3d9cc515c724ef30395b) by Noortheen Raja).
