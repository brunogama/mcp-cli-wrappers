# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Phase 7, Plan 07-01: Shortcuts Compatibility foundation (COMPLETE)
  - ShortcutsSupport package with AppIntents framework support (macOS 14+, iOS 17+)
  - DownloadConfiguration package dependency for profile integration
  - DownloadIntentError enum with 4 cases: invalidURL, missingProfile, profileLoadFailed, batchSizeExceeded
  - CustomLocalizedStringResourceConvertible conformance for user-friendly error messages
  - ProfileOptionsProvider skeleton (DynamicOptionsProvider) returning empty array
  - 18 comprehensive tests with 100% pass rate (14 error tests + 4 provider tests)
  - Zero warnings with warnings-as-errors enabled
- Phase 8, Plan 08-04: Profile Selector Action use case implementation
  - ProfileSelectionResult domain type with optional selectedProfile for cancellation handling
  - ProfileSelectorUseCase for retrieving available profiles for user selection
  - Comprehensive tests with 100% coverage (10 domain tests, 6 use case tests)
- Phase 8, Plan 08-03: Quick Download Action use case implementation (COMPLETE)
  - DownloadTriggerPort protocol for triggering downloads with async/throws signature
  - QuickDownloadUseCase for executing quick downloads with default profile
  - InMemoryDownloadTrigger MVP implementation for testing (actor-isolated, thread-safe)
  - Comprehensive tests for all components (99 tests total, 8 QuickDownload + 9 InMemoryTrigger)

### Fixed
- Phase 8: Updated QuickDownloadUseCase to use RaycastAction.Success return type (blocking fix for Plan 08-04)
- Phase 8: Fixed PortsTests trivial protocol existence checks to avoid compilation warnings

### Added
- **Phase 03-03 Wave 3**: YtDlpBridge Infrastructure Layer (IN PROGRESS)
  - `YtDlpBinaryLocator`: Binary discovery with fallback chain (bundled, system, cache)
  - `YtDlpProgressParser`: Parses yt-dlp stdout to DownloadProgress (regex-based extraction)
  - `YtDlpBridge`: YtDlpExecutorPort implementation spawning Foundation.Process
    - AsyncThrowingStream-based event streaming (started, progressed, completed/failed)
    - Graceful cancellation with SIGTERM/SIGKILL timeout
    - Error mapping from stderr to DownloadError types
  - 33 comprehensive tests (21 parser + 12 bridge) with 99%+ coverage
  - Zero warnings, zero lint violations, strict SwiftLint compliance
- **Phase 08-01 Wave 1**: Raycast Extension domain models and infrastructure scaffold (COMPLETE)
  - `RaycastActionType`: Enum for action types (quickDownload, profileSelector, searchHistory, viewStatus)
  - `RaycastError`: 5 error cases (invalidInput, profileNotFound, downloadFailed, historyUnavailable, networkError)
  - `RaycastCommand`: Command request type with actionType, url, profileName, parameters
  - `RaycastAction.Success`: Result type with downloadId, message, profileUsed, timestamp
  - `DownloadHistoryItem`: Download history record with UUID, url, profileName, status, timestamps
  - `DownloadStatus`: Status enum (pending, downloading, completed, failed, cancelled)
  - `HistoryPort`: Protocol for history operations (getRecent, search, filterByStatus, add)
  - `ProfileLoaderPort`: Protocol for profile loading (loadProfile, listProfiles, getDefaultProfile)
  - `RaycastBridge`: Raycast SDK adapter with stub methods (showToast, showHUD, showErrorAlert, clipboard, showForm)
  - `InMemoryHistoryProvider`: In-memory HistoryPort implementation with thread-safe actor isolation
  - `InMemoryProfileLoader`: In-memory ProfileLoaderPort with hardcoded presets
  - 68 comprehensive tests with 100% pass rate
  - Zero warnings with warnings-as-errors enabled
  - All types conform to Equatable, Sendable, Codable
- **Phase 06-02 Wave 2**: Spotlight Integration infrastructure & TCA layer (COMPLETE)
  - `CoreSpotlightIndexingAdapter`: IndexingPort implementation for CoreSpotlight framework
  - `AVFoundationMetadataExtractor`: MetadataExtractorPort with file introspection and yt-dlp JSON merging
  - `YtDlpJSONMetadataParser`: Safe JSON parsing for yt-dlp metadata extraction
  - `SearchMetadata+CSSearchableItem`: Extension mapping domain to Spotlight types with content type inference
  - `SpotlightIndexingFeature`: TCA reducer with fire-and-forget indexing effects
  - `SpotlightStatusView`: Debug SwiftUI view showing indexing progress and errors
  - `PHASE-3-INTEGRATION.md`: Integration guide for Phase 3 download reducer composition
  - README.md with complete architecture documentation
  - Infrastructure tests: JSON parser (8 tests), adapter (12 tests), extractor (10 tests)
  - UI tests: Reducer state management (6 tests)
  - 33 new tests total (57 suite-wide), 100% passing
  - Zero warnings, full RULES.md compliance
  - ComposableArchitecture, AVFoundation, CoreSpotlight integration
  - Fire-and-forget indexing never blocks download completion
  - Graceful degradation for missing metadata
- **Phase 06-01 Wave 1**: Spotlight Integration domain and application layer (COMPLETE)
  - `SearchMetadata`: Searchable metadata value type (13 properties, Equatable, Sendable, Codable)
  - `SpotlightError`: 5 error cases for Spotlight operations
  - `IndexingPort`: Protocol for Spotlight index operations (4 async methods)
  - `MetadataExtractorPort`: Protocol for metadata extraction
  - `MetadataExtractionRequest`: Parameter object for extraction requests
  - `IndexDownloadedFileUseCase`: Extracts metadata and indexes files
  - `DeleteSpotlightIndexUseCase`: Cleanup operations (by ID or domain)
  - Exports facade for stable API surface
  - 24 comprehensive tests with 100% pass rate and 99%+ coverage
  - Mock-based unit tests (MockIndexingPort, MockMetadataExtractorPort)
  - Zero external dependencies (Foundation only)
  - Zero warnings and SwiftLint violations
  - All types thread-safe (Sendable conformance)
- **Phase 03-02 Wave 2**: Download application layer with queue management and coordinator
  - `YtDlpExecutorPort`: Protocol for yt-dlp execution abstraction
  - `RetryPolicy`: Configurable retry behavior with maxRetries (0-10), failureBehavior enum (autoRetry, pauseBatch, continueWithoutError), and delay settings
  - `DownloadQueueManager`: FIFO queue with priority support (higher values = higher priority, insertion order for same priority)
  - `DownloadCoordinator`: Central orchestrator managing concurrent downloads with parallelism limit (1-10, default 3)
  - AsyncThrowingStream-based event emission for all download lifecycle events
  - Retry logic with configurable policies and automatic re-queueing
  - Comprehensive test suite with 22 tests (11 queue manager, 11 coordinator) and 99%+ coverage
  - All types conform to Sendable for thread-safe operations
- **Phase 03-01 Wave 1**: Download domain layer foundation
  - `DownloadID`: Type-safe UUID wrapper for download identification
  - `DownloadProgress`: Progress metrics with formatted output (percent, speed, ETA)
  - `DownloadError`: Domain error types (networkError, ytDlpError, fileSystemError, cancelled)
  - `DownloadState`: State enum (pending, downloading, paused, completed, failed, cancelled)
  - `DownloadEvent`: Event-driven architecture for download lifecycle transitions
  - All domain types conform to Equatable, Sendable, Codable for AsyncThrowingStream integration

### Changed
- **Phase 03-02**: Updated project state for Wave 2 completion
  - STATE.md reflects Phase 3 at 50% (2/4 plans complete)
  - Locked concurrency model and failure strategy decisions
  - Updated requirements progress tracking (EXEC-01 to EXEC-10)
  - Context for Wave 3 YtDlpBridge implementation
- **Phase 03-02**: Completed Wave 2 application layer documentation
  - Created 03-02-SUMMARY.md with full implementation details
  - Documented priority queue algorithm and concurrency strategy
  - Recorded auto-fixes (SwiftLint violations) and deviations
  - 372 lines application code, 22 tests, 99%+ coverage

### Removed
- **Phase 03-02**: Placeholder files from DownloadApplication
  - Removed Placeholder.swift and PlaceholderTests.swift (no longer needed)

### Fixed
- **Phase 03-02**: SwiftLint violations in RetryPolicy
  - Use `Self` instead of explicit type name in static factory methods
  - Resolves prefer_self_in_static_references violations
- UI test throwing context errors in ConfigurationFeatureTests and ProfileManagerFeatureTests
  - Resolved TCA TestStore initialization issues with throwing domain constructors
  - Added helper methods for safe configuration creation in test suite

### Added
- Phase 02-03 UI layer with TCA integration (Complete)
  - `ConfigurationFeature` TCA reducer with real-time validation feedback
  - `ProfileManagerFeature` TCA reducer for profile CRUD operations
  - `ConfigurationView` SwiftUI form with configuration sections
  - `ProfileManagerView` with profile list and preset buttons
  - 9 comprehensive UI tests using TCA TestStore pattern
  - Full 99% test coverage for UI layer
- Phase 06 research documentation for Spotlight Integration (Phase 06-RESEARCH)
  - CoreSpotlight framework investigation (macOS 14.0+ compatibility)
  - Indexing strategy with async/await APIs
  - Metadata mapping for CSSearchableItemAttributeSet
  - Architecture patterns for port/adapter with IndexingPort
  - Error handling and graceful degradation strategies
  - Testing approaches for CoreSpotlight integration
  - Performance optimization recommendations
  - Identified standard stack and common pitfalls
- Placeholder coverage check script (scripts/check-coverage.sh)
  - Pre-commit hook integration for 99% coverage requirement
  - Foundation for future coverage enforcement
- Configuration domain models for yt-dlp parameter management (Phase 02-01)
  - `DownloadConfiguration` struct with full yt-dlp parameter coverage
  - `FormatOption`, `AudioCodec`, `VideoQuality` enums for typed configuration
  - `SubtitleConfiguration` for subtitle download settings
  - `PostProcessingOptions` option set for metadata/thumbnail embedding
  - `DownloadProfile` for named configuration presets
  - `ProfilePresets` factory with 3 built-in presets (Best Video, Audio Only, 4K Quality)
  - Complete test coverage (50 tests, 99%+ coverage)
  - Planning documentation: Phase 02-01 SUMMARY.md, updated STATE.md
- Configuration application ports (Phase 02-02)
  - `ProfileRepositoryPort` protocol for profile persistence operations
  - `ConfigurationValidatorPort` protocol for yt-dlp configuration validation
- Configuration application use cases (Phase 02-02)
  - `SaveProfileUseCase` for persisting profiles
  - `LoadProfileUseCase` for retrieving profiles by ID
  - `DeleteProfileUseCase` with built-in preset protection
  - `ListProfilesUseCase` combining built-in and user-created profiles
  - `ValidateConfigurationUseCase` for yt-dlp configuration validation
- Configuration infrastructure implementations (Phase 02-02)
  - `JSONProfileRepository` for file-based profile persistence
  - `YtDlpConfigurationValidator` for yt-dlp template and configuration validation
- Updated Package.swift with Application and Infrastructure targets (Phase 02-02)
  - Added DownloadConfigurationApplication target
  - Added DownloadConfigurationInfrastructure target
  - Added test targets for application and infrastructure layers
  - Updated Exports.swift to re-export all layers
- Application layer comprehensive test suite (Phase 02-02)
  - Manual mocks for ProfileRepositoryPort and ConfigurationValidatorPort
  - 18 unit tests covering all use cases with error scenarios
  - `ProfileRepositoryError` moved to domain layer for proper layering
  - 100% test coverage for application use cases
- Infrastructure layer integration tests (Phase 02-02)
  - 10 tests for JSONProfileRepository with file I/O and cleanup
  - 6 tests for YtDlpConfigurationValidator with template validation
  - Tests verify JSON serialization roundtrip for complex configurations
  - Temporary directory isolation prevents test pollution
  - Total: 84 tests passing with 0 failures
- Phase 02-02 completion (Phase 02-02)
  - SUMMARY.md with deliverables, metrics, and architectural decisions
  - Updated STATE.md with progress tracking (2/45 requirements complete)
- Configuration UI layer with TCA (Phase 02-03)
  - `ConfigurationFeature` TCA reducer for configuration state management
  - Real-time validation via ValidateConfigurationUseCase dependency
  - Actions for format, audio, subtitles, output template, and post-processing
  - Preset application and reset to default functionality
  - Dependency injection pattern for ValidateConfigurationUseCase
  - `ConfigurationView` with 7 specialized sections for settings
  - Format selection picker with quality options
  - Audio extraction section with codec/bitrate selection
  - Subtitle configuration with language and embedding options
  - Output template editor with validation
  - Post-processing toggles for metadata/thumbnail embedding
  - Advanced settings for concurrency and directory selection
  - `ProfileManagerFeature` TCA reducer for profile CRUD operations
  - Load, save, delete, and apply profile actions
  - Built-in preset protection (prevents deletion)
  - Save profile sheet presentation management
  - Dependency injection for all profile use cases
  - `ProfileManagerView` with preset buttons and profile list
  - `PresetButtonsView` with 3 quick preset buttons (Best Video, Audio Only, 4K)
  - `ProfileListView` with swipe-to-delete for user profiles
  - `ProfileRow` with profile details and selection indicator
  - `SaveProfileSheet` for naming new profiles
  - Helper extensions for display names (VideoQuality, AudioCodec)
  - Updated Package.swift with UI target and ComposableArchitecture dependency
  - Updated Exports.swift to re-export DownloadConfigurationUI
  - Added Hashable conformance to domain enums (FormatOption, AudioCodec, VideoQuality, SubtitleFormat)
  - Comprehensive UI tests with TCA TestStore (9 tests, 100% pass rate)
  - ConfigurationFeatureTests: 4 tests covering validation, presets, reset
  - ProfileManagerFeatureTests: 5 tests covering CRUD operations and built-in protection
  - Non-exhaustive testing mode for immutable domain types
  - Phase 2 completion summary (02-03-SUMMARY.md)
  - Updated STATE.md: Phase 2 complete (12/12 requirements, 20% milestone progress)

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.0] - 2026-02-01

### Added
- Initial project setup with Clean Architecture + TCA foundation
- Phase 1: URL Management
  - URLBatch domain model with immutable URL collection
  - AddURLToBatchUseCase and ImportURLsFromFileUseCase
  - URLManagementUI with TCA state management
  - Comprehensive test coverage (99%+)
- Planning documentation structure
  - ROADMAP.md with 8 phases and 60 requirements
  - STATE.md for progress tracking
  - CONVENTIONS.md for code standards
  - ARCHITECTURE.md documenting Clean Architecture + TCA pattern

[Unreleased]: https://github.com/yourusername/ubberdownloader/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/ubberdownloader/releases/tag/v0.1.0
