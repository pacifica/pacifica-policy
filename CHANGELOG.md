# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Endpoints for status
- Endpoints for reporting

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
