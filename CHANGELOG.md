# Changelog

All notable changes to this project will be documented in this file.

## [Roadmap]
- Consider renaming the project...
- Add some(??) interoperability with TypedDict.
- Add multiply dunders as intersection operation.
- Add divide dunders as symmetric difference operation.

## [0.2.0]  - 2024-07-27
### Changed
- Change class name to `Dynamic` to better match conventions.

### Fixed
- Strict Typing doesn't break in various ways when interacting with `None`. (re-implemented using a separate dictionary of types)
- Arithmetic `+`/`-` operations now preserve parameter states from the left-hand dynamic.

## [0.1.7] - 2024-07-26
- Add optional _strict_typing parameter that enforces type matching for attributes.

## [0.1.6] - 2024-07-26
### Added
- Added some missing copyright notices.

### Changed
- Improve clarity of 'reserved' keys line in docstring/readme.
- Add missing simple usage examples to docstring.

## [0.1.5] - 2024-07-26
### Removed
- Removed extra/unnecessary key renaming logic when setting `_dict` directly. It is covered by `__setattr__` already.

## [0.1.4] - 2024-07-26
### Added
- Initial draft of the changelog file.
- Library imports dynamic for easier importing.
- Key Renaming: Key names automatically substitute non-alphanumeric with underscores.

### Fixed
- Tests work out of the box now. (added pytest.ini, changed import)

### Changed
- Setting `_dict` now uses constructor-like logic to rename keys.
- Docstring/Readme updated to reflect key renaming.
- Unit tests added to cover key renaming.

## [0.1.3] - 2024-07-25
### Added
- Initial(ish) release of DynamicDict.
- Publishing details improved.
- Library imports dynamic for easier importing.