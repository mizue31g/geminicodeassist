# Changelog

## [1.10.0](https://github.com/googleapis/python-genai/compare/v1.9.0...v1.10.0) (2025-04-09)


### ⚠ BREAKING CHANGES

* remove Part.from_video_metadata

### Features

* Add adapter size 2 for Gemini 2.0 Tuning ([959df89](https://github.com/googleapis/python-genai/commit/959df89e322efd4ed74f1c186a293b6f8fb7ee6e))
* Add domain to Web GroundingChunk ([9a75d48](https://github.com/googleapis/python-genai/commit/9a75d4885056771625f1af9ae735d61db9e7dc3c))
* Add session resumption. ([6e80ae7](https://github.com/googleapis/python-genai/commit/6e80ae77eba78607b91429168da20d618af9d3f0))
* Add thinking_budget to ThinkingConfig for Gemini Thinking Models ([71863e0](https://github.com/googleapis/python-genai/commit/71863e00c187c4eb9a379780f0a871235768a555))
* Add traffic type to GenerateContentResponseUsageMetadata ([925f983](https://github.com/googleapis/python-genai/commit/925f9836e1a6baf65adb5de5154870c1ec2621db))
* Add transcription support for MLDev ([c0a1b5c](https://github.com/googleapis/python-genai/commit/c0a1b5cdc169bfed61c69ffd8a08c0bffaaa80ce))
* Add types for configurable speech detection ([ae4ecee](https://github.com/googleapis/python-genai/commit/ae4ecee9562b71a292b61c63d33853568ab37f14))
* Add types to support continuous sessions with a sliding window ([7099e1e](https://github.com/googleapis/python-genai/commit/7099e1e99ce9e80a3b1080dcd1141a51e1990fea))
* Add UsageMetadata to LiveServerMessage ([018846a](https://github.com/googleapis/python-genai/commit/018846ae3e1f73d91522b8606e611152b7f63002))
* Added support for Context Window Compression ([e5c646c](https://github.com/googleapis/python-genai/commit/e5c646c106407a6c424a5d7fc6d022a395bac430))
* Populate X-Server-Timeout header when a request timeout is set. ([2af7b67](https://github.com/googleapis/python-genai/commit/2af7b67e811ae2b2e920c090006b2054193b404b))
* Remove experimental warnings for generate_videos and operations ([fa6007a](https://github.com/googleapis/python-genai/commit/fa6007ae9fb755e7cafb518985c96d54dd572a43))
* Remove experimental warnings from live api. ([007d1b1](https://github.com/googleapis/python-genai/commit/007d1b15e31000366352449c39679848dd7f622a))
* Support media resolution ([ef64f8a](https://github.com/googleapis/python-genai/commit/ef64f8a49171f2e05765ed7141d8ee51409a1ac7))


### Bug Fixes

* Remove Part.from_video_metadata ([c0947ab](https://github.com/googleapis/python-genai/commit/c0947ab20f75ed1c67985f7a2fdea04a5959de68))
* Upload file should support timeout (in milliseconds) configuration from http_options per request or from client ([5f3e895](https://github.com/googleapis/python-genai/commit/5f3e895276c94536ed797bcdca7fb913f95ddb01))


### Miscellaneous Chores

* Release 1.10.0 ([c136e41](https://github.com/googleapis/python-genai/commit/c136e4164d0c26530871c56653e21fc30caee511))

## [1.9.0](https://github.com/googleapis/python-genai/compare/v1.8.0...v1.9.0) (2025-04-01)


### Features

* Add specialized `send` methods to the live api ([9c4e4dc](https://github.com/googleapis/python-genai/commit/9c4e4dcdff508230f635c5d174486b08b87f86c9))
* Expose generation_complete, input/output_transcription & input/output_audio_transcription to SDK for Vertex Live API ([e5685ad](https://github.com/googleapis/python-genai/commit/e5685adc7a064b511ddb490ef0aaf27f3070775f))
* Merge GenerationConfig into LiveConnectConfig ([d22535e](https://github.com/googleapis/python-genai/commit/d22535e700178f27e458a02868cd2c06d5470e34))


### Bug Fixes

* Make response arg in APIError class constructor optional. [#572](https://github.com/googleapis/python-genai/issues/572) ([7b3f4a4](https://github.com/googleapis/python-genai/commit/7b3f4a4c50646c29293c0196b471b7bf3a29f102))


### Documentation

* Docstring improvements ([77f5356](https://github.com/googleapis/python-genai/commit/77f53566bbff3a715d2c7e5e83ada61ffd80ac96))

## [1.8.0](https://github.com/googleapis/python-genai/compare/v1.7.0...v1.8.0) (2025-03-26)


### Features

* Add engine to VertexAISearch ([21f0394](https://github.com/googleapis/python-genai/commit/21f03941e23173d5c4bfce8551e9f64410a4cd95))
* Add IMAGE_SAFTY enum value to FinishReason ([3a65fb0](https://github.com/googleapis/python-genai/commit/3a65fb0e841b183d42023aef37e22207cdc9829f))
* Add MediaModalities for ModalityTokenCount ([fb2509c](https://github.com/googleapis/python-genai/commit/fb2509c471a42a3144d7b25e63be54d32608851c))
* Add Veo 2 generate_videos support in Go SDK ([55b2923](https://github.com/googleapis/python-genai/commit/55b2923de0b925ad5487d1584331cb093773a325))
* Allow title property to be sent to Gemini API. Gemini API now supports the title property, so it's ok to pass this onto both Vertex and Gemini API. ([f2f92a7](https://github.com/googleapis/python-genai/commit/f2f92a739a764f1eae20e932fdea6a3305305f77))
* **chats:** Allow user to create chat session with list of ContentDict ([43c5379](https://github.com/googleapis/python-genai/commit/43c5379aa0a6da1f742ab0eada72cbff0b2bed40)), closes [#467](https://github.com/googleapis/python-genai/issues/467)
* Move set event loop into try except logic when setting auth lock ([d04b6a6](https://github.com/googleapis/python-genai/commit/d04b6a65129960d6e70acec2879afbd8f7c5b0e0))
* Save prompt safety attributes in dedicated field for generate_images ([e5bbb0e](https://github.com/googleapis/python-genai/commit/e5bbb0e6b77f12e7e6877ae0e976fda3f8beb604))
* Support new UsageMetadata fields ([122cdc8](https://github.com/googleapis/python-genai/commit/122cdc86f1c7381f04f6c8ab3ea86409fcb85661))


### Bug Fixes

* Improve logging for response.parsed (fixes [#455](https://github.com/googleapis/python-genai/issues/455)) ([64012dd](https://github.com/googleapis/python-genai/commit/64012dd6a6c1877114100f52c10a45a7f7ff885e))
* Schema transformer logic fix. ([f64bcba](https://github.com/googleapis/python-genai/commit/f64bcba552156c1f344f8c03932a24c0a4f9c222))
* Set event loop before asyncio.Lock() to ensure threading safety ([be2d9c6](https://github.com/googleapis/python-genai/commit/be2d9c61176f8330166e7912e233fb07fa82e4a8))
* Surface complete error details from backend ([38f5beb](https://github.com/googleapis/python-genai/commit/38f5bebba79182f78c4aa921861151626c79a84d))
* **chats:** Raise error when `types.Content` is passed to `send_message()` to correctly adhere to type annotation. To migrate code previously passing `content = types.Content(...)` to `send_message()`, pass `content.parts` instead.

### Documentation

* Log warning to users that Part.from_video_metadata will be deprecated. ([2d12f54](https://github.com/googleapis/python-genai/commit/2d12f544bc3f8d1e2720855f0fe3519881baaeb0))

## [1.7.0](https://github.com/googleapis/python-genai/compare/v1.6.0...v1.7.0) (2025-03-18)


### Features

* Bump up the websockets version for proxy support ([b996c4b](https://github.com/googleapis/python-genai/commit/b996c4b62be8c4d108dbe572372a2c31661e9bcc))
* Leverage httpx connection pooling and avoid instantiation of httpx.Client or httpx.AsyncClient for each call ([2ac5129](https://github.com/googleapis/python-genai/commit/2ac5129d4005d797f29df0a213e2455d7d730b43))


### Bug Fixes

* **chats:** Fix duplicate history when appending AFC history ([e4b1d8a](https://github.com/googleapis/python-genai/commit/e4b1d8af03be5579ff6cb0ba42dd0d3d65126892))
* **chats:** Raise error when `types.Content` is passed to `send_message()` to correctly adhere to type annotation. To migrate code previously passing `content = types.Content(...)` to `send_message()`, pass `content.parts` instead.
* Fix incorrect casing of upload status and url headers in Files API. httpx.Response returns 'x-goog-upload-status', but we were checking for 'X-Goog-Upload-Status'. Also clean up upload_file and download_file requests. ([2ac5129](https://github.com/googleapis/python-genai/commit/2ac5129d4005d797f29df0a213e2455d7d730b43))


### Documentation

* Use consistent terminology for Gemini Developer API and Vertex AI ([7f1cc22](https://github.com/googleapis/python-genai/commit/7f1cc22e6220d4550726bd75c0dff922698d674e))

## [1.5.0](https://github.com/googleapis/python-genai/compare/v1.4.0...v1.5.0) (2025-03-07)


### Features

* Determine mime_type from local images ([5e84ddc](https://github.com/googleapis/python-genai/commit/5e84ddc8d4265069e6a03c9a99ff6891cc641297))
* Enable generate_videos for Gemini Developer API ([4a242f6](https://github.com/googleapis/python-genai/commit/4a242f6f759a5e3fd1435b548d8dda38091b9cee))
* Enable image to video for generate_videos ([787354b](https://github.com/googleapis/python-genai/commit/787354bf96d7a4fc479d9e8bd432e76ab54ab54c))
* Expand files.download to work on Video and GeneratedVideo objects ([8d4d6fd](https://github.com/googleapis/python-genai/commit/8d4d6fd6271b3f74d3efae676fc08418b9bb5cda))
* Support asynchronously upload and download files using httpx ([498c01d](https://github.com/googleapis/python-genai/commit/498c01da1d2820b97b2218022b7e42840453e739))


### Bug Fixes

* Fix incorrect unit for `timeout_in_seconds` in HttpOptions. ([a9be9a2](https://github.com/googleapis/python-genai/commit/a9be9a20691249bacf162d97ef6664883102edc7))
* Fix Video.show() when uri and video_bytes are provided ([3477c40](https://github.com/googleapis/python-genai/commit/3477c40cf89eb8006b6a0877710ec77cdb1edeff))

## [1.4.0](https://github.com/googleapis/python-genai/compare/v1.3.0...v1.4.0) (2025-03-05)


### Features

* Add response_id and create_time to GenerateContentResponse ([b46ed36](https://github.com/googleapis/python-genai/commit/b46ed361d9c0845880a1447ee42dd3c0f6f7a886))
* Allow non-content types in generate_content ([cbaaf4a](https://github.com/googleapis/python-genai/commit/cbaaf4ae19e17f4fafb48e8671c10786095e2936))
* Enable Live API initial connect to accept functions directly, in addition to just FunctionDeclaration ([91b1d3e](https://github.com/googleapis/python-genai/commit/91b1d3ee85fd32e9243e3a2da4d10a763e4d0005))
* Enable minItem, maxItem, nullable for Schema type when calling Gemini API. ([867ce70](https://github.com/googleapis/python-genai/commit/867ce70cf4a7ebd52554af3d494f73fd3cd4f6b6))
* Implement get history to return comprehensive or curated chat history ([92deda1](https://github.com/googleapis/python-genai/commit/92deda1b86c27c4f93691d4f4056ed64ba84d6a8))
* Support aspect ratio for edit_image ([5423a58](https://github.com/googleapis/python-genai/commit/5423a58f3abea2b468973c0c071ced6547f6cef1))


### Bug Fixes

* Allow user do batch generate content when passing a list of strings ([cbaaf4a](https://github.com/googleapis/python-genai/commit/cbaaf4ae19e17f4fafb48e8671c10786095e2936))
* Fix chats.send_message_stream curated history ([bcf2be0](https://github.com/googleapis/python-genai/commit/bcf2be03ae6d51957052cacfb8ed905045cc6f77))
* Log warn instead of raise error for GenerateContentResponse.text quick accessor when there are mixed part types ([55a0638](https://github.com/googleapis/python-genai/commit/55a0638075d89b873aea581e2012a0951cbcf7fb))
* Remove the keyword parameter requirement for UserContent and ModelContent ([0cc292f](https://github.com/googleapis/python-genai/commit/0cc292f5b61dcc2756c2110038c93c0c23b29c1d))

## [1.3.0](https://github.com/googleapis/python-genai/compare/v1.2.0...v1.3.0) (2025-02-24)


### Features

* Add generate_videos (Veo 2) support for Python ([e9e2be7](https://github.com/googleapis/python-genai/commit/e9e2be73d5a2f6a03d6a2a665cf35e96f2ed97cd))
* Add sdk logger instance (fixes [#278](https://github.com/googleapis/python-genai/issues/278)) ([cf281b5](https://github.com/googleapis/python-genai/commit/cf281b58195be1dd374e4754e432603ac215202f))
* Introduce response.executable_code and response.code_execution_result quick accessors for GenerateContentResponse class ([3725ddf](https://github.com/googleapis/python-genai/commit/3725ddf44a0df04f6fac0bd5295f45ed20b4a8fe))
* Introduce UserContent and ModelContent to facilitate easier content creation ([c8cfef8](https://github.com/googleapis/python-genai/commit/c8cfef85ca1f7901e802800f580915a14340cae7))
* Native async client support using httpx ([c38da8d](https://github.com/googleapis/python-genai/commit/c38da8d4425a92bd6ba483abccc3dbeafbf8daa4))
* Provide a public property for determining the module backend. ([8e561de](https://github.com/googleapis/python-genai/commit/8e561de04965bb8766db87ad8eea7c57c1040442))


### Bug Fixes

* Enable sending empty input to Live API as turn complete ([99a5510](https://github.com/googleapis/python-genai/commit/99a55100e1c4e91f53b22881fbff67e62f6fb99d))
* Fix automatic function calling warning message logic. ([b99da95](https://github.com/googleapis/python-genai/commit/b99da95ae0b986d77853c917931bdfa94c6b7714))
* Fix duplicate get_function_response_parts in (async) generate_content_stream and ensure chunk isn't empty before get_function_response_parts ([d4193e6](https://github.com/googleapis/python-genai/commit/d4193e6eb22d62c61b2727600171eb06780bfa18))
* Properly handle empty json response with headers for list models ([859ebc3](https://github.com/googleapis/python-genai/commit/859ebc3dc51aab9834b9034b5a1a205bcc72d25d))


### Documentation

* Add docs for error handling ([#317](https://github.com/googleapis/python-genai/issues/317)) ([6e1cb82](https://github.com/googleapis/python-genai/commit/6e1cb82704f6cb05b67191a319190c5ce0f67d9c))
* Add instruction on how to disable automatic function calling. ([f8b12d5](https://github.com/googleapis/python-genai/commit/f8b12d53567585094f7e7b1d015b89c993f480de))
* Regenerate docs for 1.2.0 ([30a3493](https://github.com/googleapis/python-genai/commit/30a34931d200feb12da54e978ea1f4a4a3d1e82e))
* Remove negative_prompt from image samples (fixes [#339](https://github.com/googleapis/python-genai/issues/339)) ([81e18f0](https://github.com/googleapis/python-genai/commit/81e18f053048ff4b3d2c5dde0726234d51cc8290))
* Update docs for models modules ([d96bba2](https://github.com/googleapis/python-genai/commit/d96bba29326113dba46ff16932deeb50618b8d8c))

## [1.2.0](https://github.com/googleapis/python-genai/compare/v1.1.0...v1.2.0) (2025-02-12)


### Features

* Enable Media resolution for Gemini API. ([6cdf61d](https://github.com/googleapis/python-genai/commit/6cdf61d09f0dec0b27f2be6a0487ec5f4792d62f))
* Support property_ordering in response_schema (fixes [#236](https://github.com/googleapis/python-genai/issues/236)) ([01b15e3](https://github.com/googleapis/python-genai/commit/01b15e32d3823a58d25534bb6eea93f30bf82219))


### Bug Fixes

* Default to list base models for async models list ([d3226b7](https://github.com/googleapis/python-genai/commit/d3226b7ce9fde115e503da7f9108d735fc89325c))
* Remove Type import from types.py that get's shadowed by API Type type. (fixes [#310](https://github.com/googleapis/python-genai/issues/310)) ([78f58c3](https://github.com/googleapis/python-genai/commit/78f58c3f63ec1d9fb916e81f9b962d5b65b13ec2))
* Use typing_extensions.TypedDict for TypedDict types (fixes [#189](https://github.com/googleapis/python-genai/issues/189)) ([996562a](https://github.com/googleapis/python-genai/commit/996562afed6d19b20bef343262e4c8820559c2d6))


### Documentation

* Client initialization using environmental variables. ([e4c2ffc](https://github.com/googleapis/python-genai/commit/e4c2ffcdb5ddd68ded5f3e2b98c0b44afe91ca1b))
* Fix File.expiration_time description (fixes [#318](https://github.com/googleapis/python-genai/issues/318)) ([729f619](https://github.com/googleapis/python-genai/commit/729f619bdc88f0d775fda3b9f1a75a527ddf90ac))
* Fix files.upload docs to use 'file' instead of 'path' (fixes [#306](https://github.com/googleapis/python-genai/issues/306)) ([2b35d0c](https://github.com/googleapis/python-genai/commit/2b35d0ca4e74b67f98e64da88286148370be9b6f))

## [1.1.0](https://github.com/googleapis/python-genai/compare/v1.0.0...v1.1.0) (2025-02-10)


### Features

* Add support for typing.Literal in response_schema (fixes [#264](https://github.com/googleapis/python-genai/issues/264)) ([384c4eb](https://github.com/googleapis/python-genai/commit/384c4eb7bac7ac867db8f19777c33e01daff89ef))
* Allow converting a function into FunctionDeclaration with api option ([408e28f](https://github.com/googleapis/python-genai/commit/408e28fc9892996eb1cb617de3cf7ce658deed16))
* Support generate content config for each chat turn ([ca19100](https://github.com/googleapis/python-genai/commit/ca1910026d7e425c1f9adb13779ec43bc2b9d99e))
* Tuning - `Tuning.tune` for Gemini API no longer blocks until the tuning operation is resolved ([fcf8888](https://github.com/googleapis/python-genai/commit/fcf88881698eabfa7d808df0f1353aa6bcc54cb8))


### Bug Fixes

* Remove duplicate function invocations and ensure automatic function calling can be disabled in generate_content_stream ([0958fbe](https://github.com/googleapis/python-genai/commit/0958fbe4ce68c09a6b665fcacb2e3a16dfd822d2))
* Response_schema generation for pydantic fields with type Optional[list] and Optional[MyBaseModel] now work correctly (fixes [#246](https://github.com/googleapis/python-genai/issues/246)) ([8330561](https://github.com/googleapis/python-genai/commit/833056195bb7fe7c7e45095df2eea748f48de49c))
* Support dict response_schema with 'any_of' key ([75f5056](https://github.com/googleapis/python-genai/commit/75f505637c89df50120e3ea25c6379fa49b54abf))
* Common - Do not fail when server returns unknown enum values on Python &lt;3.11 ([843d86d](https://github.com/googleapis/python-genai/commit/843d86d38699be5f6acc58e5e5a915acab8018be))


### Documentation

* Add docs on how to structure `contents` (fixes [#274](https://github.com/googleapis/python-genai/issues/274)) ([da356cb](https://github.com/googleapis/python-genai/commit/da356cb12d9b68fe9ccae0fec1c059399e7f9685))
* Regenerate docs for 1.0 ([fbee816](https://github.com/googleapis/python-genai/commit/fbee81625178fe9d39c7856bcae01ebf570b154c))
* Update model names in README, fix function calling example ([11c0274](https://github.com/googleapis/python-genai/commit/11c0274fbac5c82e39dac4e99ac7237cd9705e0b))

## [1.0.0](https://github.com/googleapis/python-genai/compare/v0.8.0...v1.0.0) (2025-02-05)


### ⚠ BREAKING CHANGES

* Remove deprecated field: `deprecated_response_payload`

### Features

* Add labels for GenerateContent requests ([3e3b82d](https://github.com/googleapis/python-genai/commit/3e3b82dcdc8d50852a9fdd452c8e0957bb4493de))
* Add Union support to response_schema ([eedf4f1](https://github.com/googleapis/python-genai/commit/eedf4f12aea9f5a0d4056d6f14a91b14db1903cf))
* Support automatic function calling in models.generate_content_stream and send_message_stream, sync and async mode ([7c9f8b5](https://github.com/googleapis/python-genai/commit/7c9f8b5833e393e5879fd267abf3a34d122a5d1d))


### Bug Fixes

* Avoid false test failure by skipping incompatible test case for python 3.13 ([7f10e55](https://github.com/googleapis/python-genai/commit/7f10e550db4767ab172f5f5b00eda484cb0141d6))
* Default to list base models (instead of tuned models) ([ef48f0d](https://github.com/googleapis/python-genai/commit/ef48f0dfcae1811ddc3160e368a5ef25a535ee25))
* Handle pydantic model type recognition gracefully for python 3.9 and 3.10 ([4a38fdf](https://github.com/googleapis/python-genai/commit/4a38fdf53fd689fdab611dbcaebc9570c7d46bd5))
* Raise error when Gemini API response_schema has 'default' or 'anyof' fields ([c50bca0](https://github.com/googleapis/python-genai/commit/c50bca00c814b39a98fc6aacba0c4c429fed0570))
* Remove redundant contents in Automatic Function Calling history ([5510595](https://github.com/googleapis/python-genai/commit/5510595eb18ad0a0af34ce63df1685b49e03ce10))
* Remove unsupported parameter from Gemini API ([f8addb5](https://github.com/googleapis/python-genai/commit/f8addb544e545100ae7342621910a2338072ddc6))


### Documentation

* Remove experimental classification from description. ([b14ac57](https://github.com/googleapis/python-genai/commit/b14ac57b07d4e7794d83f2b2123a4df80890f772))
* Remove thoughts examples and update tests ([af3b339](https://github.com/googleapis/python-genai/commit/af3b339a9d58e25cb3baa6fd3d0b1d078c620f9d))
* Update documentation on how to set api version using genai client ([6fd4425](https://github.com/googleapis/python-genai/commit/6fd442520d1b59003fd5fcd24d395b9790caec6f))
* Update instruction on function calling experience in `ANY` mode. ([451cf98](https://github.com/googleapis/python-genai/commit/451cf989e2a917884475cf66fce1d809a7495b53))


### Code Refactoring

* Remove deprecated field: `deprecated_response_payload` ([197fa46](https://github.com/googleapis/python-genai/commit/197fa46c9639799b8d71ddf92ab372140dc5b65b))

## [0.8.0](https://github.com/googleapis/python-genai/compare/v0.7.0...v0.8.0) (2025-01-30)


### ⚠ BREAKING CHANGES

* Rename files.upload argument to "file" instead of "path".

### Features

* Add enhanced_prompt to GeneratedImage class ([76c810b](https://github.com/googleapis/python-genai/commit/76c810b6bb82bde4cc4fe9754e0bbcc85e10a4c4))
* Added Operation and PredictOperation (internal module) ([309dd26](https://github.com/googleapis/python-genai/commit/309dd26cb3aa761bfae7070ffa5eab23b2a5a75c))
* Support global endpoint natively in Vertex ([f4530b0](https://github.com/googleapis/python-genai/commit/f4530b0af972d0b5e376e7463af235b8378e0694))
* Support unknown enum values ([da448b3](https://github.com/googleapis/python-genai/commit/da448b3cb2bf5d6cba6fdefa8d15365253fe0384))


### Bug Fixes

* Streaming in Vertex AI Express ([ff78b7b](https://github.com/googleapis/python-genai/commit/ff78b7b0277800e2b4b9e9958a87688383422d29))


### Documentation

* Correct generate content with uploaded file example ([8cea052](https://github.com/googleapis/python-genai/commit/8cea052ac148890a343f14b7185e394646802b41))


### Miscellaneous Chores

* Rename files.upload argument to "file" instead of "path". ([f68aa1f](https://github.com/googleapis/python-genai/commit/f68aa1f63f04629f9eb8629c5b1359f500f89a47))

## [0.7.0](https://github.com/googleapis/python-genai/compare/v0.6.0...v0.7.0) (2025-01-28)


### ⚠ BREAKING CHANGES

* Remove skip_project_and_location_in_path from async models.list
* remove "tuning.distill"
* Change asynchronous streaming output to an awaitable async iterator for client.aio.models.generate_content_stream and client.aio.chat.send_message_stream
* Remove pillow as a required dependency
* rename batches.list method signature.
* make Part, FunctionDeclaration, Image, and GenerateContentResponse classmethods argument keyword only
* Remove skip_project_and_location_in_path from HttpOption
* Renamed FunctionDeclaration class functions to reflect the fact that they work off of the `Callable` type not just functions.
* Moved the HttpOptions class into types.py, by making it autogenerated. This causes the following breaking change:
* rename generate_image() to generate_images(), rename GenerateImageConfig to GenerateImagesConfig, rename GenerateImageResponse to GenerateImagesResponse, rename GenerateImageParameters to GenerateImagesParameters

### Features

* [genai-modules][models] Add HttpOptions to all method configs for models. ([76fdde7](https://github.com/googleapis/python-genai/commit/76fdde7138b7bc3bd1e761bca753610fbb83a1af))
* Add support for enhance_prompt to model.generate_image ([d09e14e](https://github.com/googleapis/python-genai/commit/d09e14ea77de455c545c07ef0e4d0735c21521af))
* Added support for the new HttpOptions class in the per request options overrides. ([ad57025](https://github.com/googleapis/python-genai/commit/ad5702512ee78ad7bcda6233a7d1eafaaaf50e1f))
* Change asynchronous streaming output to an awaitable async iterator for client.aio.models.generate_content_stream and client.aio.chat.send_message_stream ([0c124eb](https://github.com/googleapis/python-genai/commit/0c124eba8909e77336a7c22681d57080d6f1a6ad))
* Enable enum support in the GenerateContentConfig.response_schema ([fe82e10](https://github.com/googleapis/python-genai/commit/fe82e1065095eabfe97cd197ebcea5b73efb01cd))
* Handle a wider variety of response_schemas - primitives and nested lists. ([24fffea](https://github.com/googleapis/python-genai/commit/24fffea93a6c127826a16a4183ff38a4376a4d5f))
* Images - Added Image.mime_type ([71a8f1d](https://github.com/googleapis/python-genai/commit/71a8f1da1904a34c9f8c720d2356e50db7b279b3))
* Make Part, FunctionDeclaration, Image, and GenerateContentResponse classmethods argument keyword only ([b58f4e0](https://github.com/googleapis/python-genai/commit/b58f4e03050fce29a6c47091cf25ef6f440c2e7e))
* Remove skip_project_and_location_in_path from async models.list ([d788626](https://github.com/googleapis/python-genai/commit/d788626a8de8bd8540739b673ae34530b494d83e))
* Remove skip_project_and_location_in_path from HttpOption ([a1c0435](https://github.com/googleapis/python-genai/commit/a1c043521558aca80a3bf55ff3eb96c95ec12e72))
* Support GenerateContentResponse.parsed to return Enum ([e214211](https://github.com/googleapis/python-genai/commit/e2142118ae7796c52503f327ca8d949a80be0e16))
* Validate enum value for different backend endpoint. ([97bb958](https://github.com/googleapis/python-genai/commit/97bb9580511c3517134d867500c8d155c231e04c))


### Bug Fixes

* Add required key to nested fields in function declaration schemas ([c7dba47](https://github.com/googleapis/python-genai/commit/c7dba473610547f153f13f82b8d8977a60b11308))
* Fix pydantic list support in Python 3.9 and 3.10 (fixes [#52](https://github.com/googleapis/python-genai/issues/52)) ([81150b3](https://github.com/googleapis/python-genai/commit/81150b3e0b21eded0cbdb2d0e3308b7866de619a))
* Handle nullable types in pydantic classes (fixes [#62](https://github.com/googleapis/python-genai/issues/62)) ([773e1c0](https://github.com/googleapis/python-genai/commit/773e1c0e28ff6dbfc799275c24b280c79375f9d5))
* Support parameterized generics Union type in automatic function calling parameters (fixes [#22](https://github.com/googleapis/python-genai/issues/22)) ([04475ab](https://github.com/googleapis/python-genai/commit/04475ab9d75e38f33ed07e7c6ad03bde36634105))


### Documentation

* Add examples & tests for thinking model ([59e2763](https://github.com/googleapis/python-genai/commit/59e27633de46f3521916a6d7819eae6ffc387405))
* Correct usage ([0c546de](https://github.com/googleapis/python-genai/commit/0c546deee62b5bbfbf3e05938f7b46a89861250e))
* Document experimental state of the live module. ([115ac47](https://github.com/googleapis/python-genai/commit/115ac4769088c43ef9eafe5eff588abc340b8213))
* Fix Blob type docstring. ([7f38e55](https://github.com/googleapis/python-genai/commit/7f38e55207d0c049a530e1f5eb605a251c133382))
* Remove repeated docstring for interrupted in docs ([230cfbc](https://github.com/googleapis/python-genai/commit/230cfbc73e45c0ea9a1a360890a68831a0dc3b60))
* Remove the word "class" in docstring and sync Live types docstring up-to-date ([7fa3ef3](https://github.com/googleapis/python-genai/commit/7fa3ef335e08cc752fa1eb41bf7d130ffccf7898))
* Update supported model parameter format for generate_content ([a5c3a1c](https://github.com/googleapis/python-genai/commit/a5c3a1ce6b0cffe3a91ffcb3756b3176ecf7b213))


### Code Refactoring

* Moved the HttpOptions class into types.py, by making it autogenerated. This causes the following breaking change: ([ad57025](https://github.com/googleapis/python-genai/commit/ad5702512ee78ad7bcda6233a7d1eafaaaf50e1f))
* Remove "tuning.distill" ([ca8cd5e](https://github.com/googleapis/python-genai/commit/ca8cd5e389263a261d1d9e05e47d6f108803efff))
* Remove pillow as a required dependency ([8ccdf2e](https://github.com/googleapis/python-genai/commit/8ccdf2e99246ba948b97f786596ae418f85749b0))
* Rename batches.list method signature. ([aa7c071](https://github.com/googleapis/python-genai/commit/aa7c071cb5922510f189da7875e1a3f6e1836733))
* Rename generate_image() to generate_images(), rename GenerateImageConfig to GenerateImagesConfig, rename GenerateImageResponse to GenerateImagesResponse, rename GenerateImageParameters to GenerateImagesParameters ([65d7bf5](https://github.com/googleapis/python-genai/commit/65d7bf5f519570c7af72d434a22e302fbafe0735))
* Renamed FunctionDeclaration class functions to reflect the fact that they work off of the `Callable` type not just functions. ([0e4a003](https://github.com/googleapis/python-genai/commit/0e4a0030295323177b38d052f7b7d695c07555b2))

## [0.6.0](https://github.com/googleapis/python-genai/compare/v0.5.0...v0.6.0) (2025-01-21)


### Features

* Add support for audio_timestamp to types.GenerateContentConfig (fixes [#132](https://github.com/googleapis/python-genai/issues/132)) ([116395b](https://github.com/googleapis/python-genai/commit/116395b23d2415407c01efb30cb6c1863a4a3032))
* Add support for case insensitive enum types. (fixes [#11](https://github.com/googleapis/python-genai/issues/11)) ([252f302](https://github.com/googleapis/python-genai/commit/252f302d3bb02271ba3e8953aeb4fb8fa7023fa6))
* Add support for class methods in the Tools for the GenerateContent Function ([5afa6bb](https://github.com/googleapis/python-genai/commit/5afa6bb9ac9445491bea6af28655535c78976a49))
* Add ThinkingConfig to generate content config. ([c23c42c](https://github.com/googleapis/python-genai/commit/c23c42c1bf012b36717dd21e86fdb7859b43b759))
* Implement client.files.download ([a034b77](https://github.com/googleapis/python-genai/commit/a034b77dc6c0806d791942d2a6ced4cf5973d2c3))
* Support BytesIO when uploading files ([4b490dc](https://github.com/googleapis/python-genai/commit/4b490dce9ead29fe28411b20801fc95a8617143c))
* Support lists in response_schema ([8ed933d](https://github.com/googleapis/python-genai/commit/8ed933dd4068add6983fc084df1cb434b444ba2a))
* Usability change to simplify generate content with uploaded files ([5c372ae](https://github.com/googleapis/python-genai/commit/5c372ae61914c75a5700297a8f2301f76379e926))


### Bug Fixes

* Fix count_tokens system_instruction and tools config ([056eaba](https://github.com/googleapis/python-genai/commit/056eabad0cd863d5729f423416a4961c5113c1a5))
* Fix models.list() with empty tuned models ([75409f1](https://github.com/googleapis/python-genai/commit/75409f12d9f531f126c427b3bd9a0b8d3bacabf7))
* Fixed the `bytes` type handling (the `base64.urlsafe_bencode` error) ([1bc161d](https://github.com/googleapis/python-genai/commit/1bc161d81c78afa35f21a24ee1840b5ed03f3a96))
* Project and location are required when using client in Vertex AI mode. ([d5859fa](https://github.com/googleapis/python-genai/commit/d5859fa8d89bb26b3c31ee3dab0deaf9c159e615))

### Documentation

* Add project description to README. ([384f413](https://github.com/googleapis/python-genai/commit/384f413666e8d2430a943163dd109814ee9b6137))
* Update formatting in README.md ([d33fb37](https://github.com/googleapis/python-genai/commit/d33fb37a082e04f512063d88bbe500a9acdbfb2c))
* Update models.list doc and code examples to include list base models ([f2e0c43](https://github.com/googleapis/python-genai/commit/f2e0c43417f4b6a7ca8b1b0e5bef97f68a8ff84b))
* Tool use example in docs ([87fe5b0](https://github.com/googleapis/python-genai/commit/87fe5b0cdfbf34c295398217185d857ca1413c02))
* Tool use example in README.md ([87fe5b0](https://github.com/googleapis/python-genai/commit/87fe5b0cdfbf34c295398217185d857ca1413c02))


## [0.5.0](https://github.com/googleapis/python-genai/compare/v0.4.0...v0.5.0) (2025-01-13)


### Features

* Support API keys for VertexAI mode generate_content ([0e4b0e5](https://github.com/googleapis/python-genai/commit/0e4b0e5ee0ecfef34f6576d8aab24cf0554bbd85))
* Support list models to return base models ([0f713f1](https://github.com/googleapis/python-genai/commit/0f713f177e84ab7a2071c635ec7231ee4fbf4657))
* Support parsing 'interrupted' field in Live Python SDK. ([eab2c4a](https://github.com/googleapis/python-genai/commit/eab2c4a9513d4ce58270b82e10698a945c01aaca))
* Use `ser_json_byte` `val_json_bytes` in bytes type public interface ([1176e43](https://github.com/googleapis/python-genai/commit/1176e43c2f87edf5566512b8f3c433b77684f87b))


### Bug Fixes

* Update header type ([62c45f9](https://github.com/googleapis/python-genai/commit/62c45f9ecdb0e7bc539d22a967672762fa6c50a8))


### Documentation

* Correct description of path parameter that only path-like object is supported ([336498b](https://github.com/googleapis/python-genai/commit/336498baebee2e064e2f44d9c6d96903bcfd63bf))

## [0.4.0](https://github.com/googleapis/python-genai/compare/v0.3.0...v0.4.0) (2025-01-08)


### ⚠ BREAKING CHANGES

* Make Imagen upscale_factor a required argument, make upscale config optional

### Features

* ApiClient - support timeout in HttpOptions ([b22286f](https://github.com/googleapis/python-genai/commit/b22286fa3cd48a7918ffa2acaa40e53f3c8bb5d8))
* Enable response_logprobs and logprobs for Google AI ([5586f3d](https://github.com/googleapis/python-genai/commit/5586f3d650964547c3e7cafa1165f9c7d1306529))
* Support function_calls quick accessor in GenerateContentResponse class ([81b8a23](https://github.com/googleapis/python-genai/commit/81b8a236b85081aa02fc4e38e27189bc2deb5cfb))


### Bug Fixes

* Change string type to int type ([5c15243](https://github.com/googleapis/python-genai/commit/5c1524370214128752905faefcf2690592b2dc90))
* FunctionCallCancellation ids type. ([b0e46b7](https://github.com/googleapis/python-genai/commit/b0e46b72aeef938414a68efd773bdac0b25c05d2))
* Gracefully catch error if streamed json does not meet schema validation (fixes [#14](https://github.com/googleapis/python-genai/issues/14)) ([f494432](https://github.com/googleapis/python-genai/commit/f494432900d60e64cbef69424918904ddbe255b1))
* Update RealtimeClientLiveMessage realtime content parameter field. ([4340939](https://github.com/googleapis/python-genai/commit/4340939d17ee38cad0d8d64aafcde5c3ef89f78f))


### Documentation

* Add readme example for Chats module ([830f0f5](https://github.com/googleapis/python-genai/commit/830f0f56e6663c173454a47ca97867031bd89819))
* Fix typo in code document ([f9243e8](https://github.com/googleapis/python-genai/commit/f9243e890aa42ae13b6f83dd885824b629a17cd3))
* Fix typo in CONTRIBUTING.md ([3e42644](https://github.com/googleapis/python-genai/commit/3e42644784304d45d0b0bfdc8279958109650576))


### Code Refactoring

* Make Imagen upscale_factor a required argument, make upscale config optional ([b06629f](https://github.com/googleapis/python-genai/commit/b06629f879b548a209e8517e92f5923d1f25c3a8))

## [0.3.0](https://github.com/googleapis/python-genai/compare/v0.2.2...v0.3.0) (2024-12-17)


### BREAKING CHANGES
* contents must be passed to CreateCachedContentConfig instead as a parameter to create_cached_content.

### Features

* Add support for Pydantic default value in Automatic Function Calling.
* Add support for thought.
* Add support for streaming chat.
