# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.0.0] - 2026-09-15

### Added
- Add Postman collection for API testing.
- Add `join_cycle` API to allow System Manager users to add clients to a cycle.
- Add `api_error` helper for API error handling.
- Add Cycle Membership workspace with number cards.
- Add Cycle Overview report.
- Add Cycle DocType validation and submission logic.
- Add Cycle and Cycle Member DocTypes.
- Add ElGameya Settings DocType.
- Add ElGameya Client DocType for cycle membership.
- Add validation utilities for Egyptian phone numbers and National IDs.
- Add language switcher to the navbar.
- Add missing Arabic translations for Frappe system messages.

### Changed
- Update README installation instructions with the correct app repository link.
- Use the `All` role instead of the `Client` role for Cycle and Client read permissions.
- Enhance Client List View columns and filters.
- Remove ERPNext from required apps.

### Fixed
- Add missing `time_zone` configuration to System Settings during installation.

### Internationalization
- Add missing Arabic translations.