# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Endpoints for status
- Endpoints for reporting

## [0.8.2] - 2020-01-22
### Updated
- Pull #116 Add Python 3.7 and 3.8 by [@dmlb2000](https://github.com/dmlb2000)
- Pull #115 Update Pylint 2.0+ by [@dmlb2000](https://github.com/dmlb2000)
- Pull #114 Remove Python 2.7 support by [@dmlb2000](https://github.com/dmlb2000)

## [0.8.1] - 2019-11-08
### Updated
- Pull #112 Allow admins to see all events by [@dmlb2000](https://github.com/dmlb2000)

## [0.8.0] - 2019-09-03
### Removed
- Deprecated SearchSync (closed #107 and #95) functionality by [@dmlb2000](https://github.com/dmlb2000)
- Pull #110 Refactored testing suite by [@dmlb2000](https://github.com/dmlb2000)

## [0.7.0] - 2019-06-21
### Changed
- Fix #100 add better exclude command line by [@dmlb2000](https://github.com/dmlb2000)
- Fix #102 add config file caching by [@dmlb2000](https://github.com/dmlb2000)
- Fix #99 add searchsync performance testing by [@dmlb2000](https://github.com/dmlb2000)

## [0.6.7] - 2019-06-21
### Changed
- Fix #93 add exclude searchsync options by [@dmlb2000](https://github.com/dmlb2000)
- Fix #91 add better docs by [@dmlb2000](https://github.com/dmlb2000)

## [0.6.6] - 2019-05-30
### Changed
- Add field data flag to the has doi metadata attribute by [@plithnar](https://github.com/plithnar)

## [0.6.5] - 2019-05-23
### Changed
- Fix #84 make the elasticsearch endpoint not constant
- Fix #85 verify event policy is of type ingest

## [0.6.4] - 2019-05-22
### Added
- Allowed for Elasticsearch sniffing to be configurable (Pull #78)

### Changed
- Fix #79 Change Web Root to be Status
- Fix #81 Modify Elasticsearch Mappings to include more fields

## [0.6.1] - 2019-05-18
### Added
- Events policy endpoint
- Ingest policy endpoint
- Uploader policy endpoint
- ElasticSearch synchronization
- Data release management

### Changed
