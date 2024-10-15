# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.19] - 2024-10-11

### Changed
- `lastmodified` in `MoodleContentInfo` now datetime

### Removed
- Integration with Sync removed

## [0.1.18] - 2024-10-11

### Added
- `title` property to `MoodleSection`

## [0.1.17] - 2024-10-10

### Added
- Inline attachment (webdav) download method (same as regular)

## [0.1.16] - 2024-10-10

### Fixed
- Prevent conflicts with other resource type enums

## [0.1.14] - 2024-10-10

### Added
- Add convenience `MoodleContentHandler` model

## [0.1.13] - 2024-10-10

### Added
- Add `body` property to `MoodleSection`
- More Module Types
- Optional description property in Module

## [0.1.12] - 2024-10-10

### Fixed
- Allow None in some API model properties

### Added
- `MoodleBadge` model

## [0.1.11] - 2024-10-10

### Fixed
- Remove space in content fileName property

## [0.1.10] - 2024-10-09

### Added
- Download method in session

## [0.1.9] - 2024-10-09

### Changed
- Improve MoodleContent integration with sync

## [0.1.8] - 2024-10-09

### Changed
- Improve integration with sync

### Added
- Extended API

## [0.1.7] - 2024-10-09

### Changed
- Make content attributes optional

### Added
- Content type enum

## [0.1.6] - 2024-10-09

### Changed
- Empty lists by default in some responses

## [0.1.5] - 2024-10-09

### Changed
- Rename `MoodleContent` and `MoodleInContent`

## [0.1.4] - 2024-10-09

### Added
- Add `courseid` query parameter to `core_course_get_contents`

## [0.1.3] - 2024-10-09

### Added
- Implicitly convert some timestamp fields to datetime

## [0.1.2] - 2024-10-09

### Added
- Add `userid` query parameter to `core_enrol_get_users_courses`

## [0.1.1] - 2024-10-09

### Added
- `MoodleLogin` to login with user/pass

## [0.1.0] - 2024-10-09

### Added
- Initial release
