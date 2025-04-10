# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


"""Tests for live.py."""
import contextlib
import json
from typing import AsyncIterator
from unittest import mock
from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch
import warnings

import pytest
from websockets import client

from ... import _api_client as api_client
from ... import _common
from ... import Client
from ... import client as gl_client
from ... import live
from ... import types


def exception_if_mldev(vertexai, exception_type: type[Exception]):
  if vertexai:
    return contextlib.nullcontext()
  else:
    return pytest.raises(exception_type)

function_declarations = [{
    'name': 'get_current_weather',
    'description': 'Get the current weather in a city',
    'parameters': {
        'type': 'OBJECT',
        'properties': {
            'location': {
                'type': 'STRING',
                'description': 'The location to get the weather for',
            },
            'unit': {
                'type': 'STRING',
                'enum': ['C', 'F'],
            },
        },
    },
}]


def get_current_weather(location: str, unit: str):
  """Get the current weather in a city."""
  return 15 if unit == 'C' else 59


def mock_api_client(vertexai=False):
  api_client = mock.MagicMock(spec=gl_client.BaseApiClient)
  if not vertexai:
    api_client.api_key = 'TEST_API_KEY'
    api_client.location = None
    api_client.project = None
  else:
    api_client.api_key = None
    api_client.location = 'us-central1'
    api_client.project = 'test_project'

  api_client._host = lambda: 'test_host'
  api_client._http_options = types.HttpOptions.model_validate(
      {'headers': {}}
  )  # Ensure headers exist
  api_client.vertexai = vertexai
  return api_client


@pytest.fixture
def mock_websocket():
  websocket = AsyncMock(spec=client.ClientConnection)
  websocket.send = AsyncMock()
  websocket.recv = AsyncMock(
      return_value='{"serverContent": {"turnComplete": true}}'
  )  # Default response
  websocket.close = AsyncMock()
  return websocket


async def get_connect_message(api_client, model, config=None):
  if config is None:
    config = {}
  mock_ws = AsyncMock()
  mock_ws.send = AsyncMock()
  mock_ws.recv = AsyncMock(return_value=b'some response')

  mock_google_auth_default = Mock(return_value=(None, None))
  mock_creds = Mock(token='test_token')
  mock_google_auth_default.return_value = (mock_creds, None)

  @contextlib.asynccontextmanager
  async def mock_connect(uri, additional_headers=None):
    yield mock_ws

  @patch('google.auth.default', new=mock_google_auth_default)
  @patch.object(live, 'connect', new=mock_connect)
  async def _test_connect():
    live_module = live.AsyncLive(api_client)
    async with live_module.connect(
        model=model,
        config=config,
    ):
      pass

    mock_ws.send.assert_called_once()
    return json.loads(mock_ws.send.call_args[0][0])

  return await _test_connect()


async def _async_iterator_to_list(async_iter):
  return [value async for value in async_iter]


def test_mldev_from_env(monkeypatch):
  api_key = 'google_api_key'
  monkeypatch.setenv('GOOGLE_API_KEY', api_key)

  client = Client()

  assert not client.aio.live._api_client.vertexai
  assert client.aio.live._api_client.api_key == api_key
  assert isinstance(client.aio.live._api_client, api_client.BaseApiClient)


def test_vertex_from_env(monkeypatch):
  project_id = 'fake_project_id'
  location = 'fake-location'
  monkeypatch.setenv('GOOGLE_GENAI_USE_VERTEXAI', 'true')
  monkeypatch.setenv('GOOGLE_CLOUD_PROJECT', project_id)
  monkeypatch.setenv('GOOGLE_CLOUD_LOCATION', location)

  client = Client()

  assert client.aio.live._api_client.vertexai
  assert client.aio.live._api_client.project == project_id
  assert isinstance(client.aio.live._api_client, api_client.BaseApiClient)


def test_websocket_base_url():
  base_url = 'https://test.com'
  api_client = gl_client.BaseApiClient(
      api_key='google_api_key',
      http_options={'base_url': base_url},
  )
  assert api_client._websocket_base_url() == 'wss://test.com'


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_send_text(
    mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  await session.send(input='test')
  mock_websocket.send.assert_called_once()
  sent_data = json.loads(mock_websocket.send.call_args[0][0])
  assert 'client_content' in sent_data


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_send_content_dict(
    mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  client_content = {
      'content': [{'parts': [{'text': 'test'}]}],
      'turn_complete': True,
  }
  await session.send(input=client_content)
  mock_websocket.send.assert_called_once()
  sent_data = json.loads(mock_websocket.send.call_args[0][0])
  assert 'client_content' in sent_data


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_send_content(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  client_content = types.LiveClientContent(
      turns=[types.Content(parts=[types.Part(text='test')])], turn_complete=True
  )
  await session.send(input=client_content)
  mock_websocket.send.assert_called_once()
  sent_data = json.loads(mock_websocket.send.call_args[0][0])
  assert 'client_content' in sent_data


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_send_bytes(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  realtime_input = {'data': b'000000', 'mime_type': 'audio/pcm'}

  await session.send(input=realtime_input)
  mock_websocket.send.assert_called_once()
  sent_data = json.loads(mock_websocket.send.call_args[0][0])
  assert 'realtime_input' in sent_data


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_send_blob(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  realtime_input = types.Blob(data=b'000000', mime_type='audio/pcm')

  await session.send(input=realtime_input)
  mock_websocket.send.assert_called_once()
  sent_data = json.loads(mock_websocket.send.call_args[0][0])
  assert 'realtime_input' in sent_data


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_send_realtime_input(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  realtime_input = types.LiveClientRealtimeInput(
      media_chunks=[types.Blob(data='MDAwMDAw', mime_type='audio/pcm')]
  )
  await session.send(input=realtime_input)
  mock_websocket.send.assert_called_once()
  sent_data = json.loads(mock_websocket.send.call_args[0][0])
  assert 'realtime_input' in sent_data


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_send_tool_response(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )

  if vertexai:
    tool_response = types.LiveClientToolResponse(
        function_responses=[
            types.FunctionResponse(
                name='get_current_weather',
                response={'temperature': 14.5, 'unit': 'C'},
            )
        ]
    )
  else:
    tool_response = types.LiveClientToolResponse(
        function_responses=[
            types.FunctionResponse(
                name='get_current_weather',
                response={'temperature': 14.5, 'unit': 'C'},
                id='some-id',
            )
        ]
    )
  await session.send(input=tool_response)
  mock_websocket.send.assert_called_once()
  sent_data = json.loads(mock_websocket.send.call_args[0][0])
  assert 'tool_response' in sent_data


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_send_input_none(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  await session.send(input=None)
  mock_websocket.send.assert_called_once()
  sent_data = json.loads(mock_websocket.send.call_args[0][0])
  assert 'client_content' in sent_data
  assert sent_data['client_content']['turn_complete']


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_send_error(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  with pytest.raises(ValueError):
    await session.send(input=[{'invalid_key': 'invalid_value'}])

  with pytest.raises(ValueError):
    await session.send(input={'invalid_key': 'invalid_value'})


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_receive( mock_websocket, vertexai):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  responses = session.receive()
  responses = await _async_iterator_to_list(responses)
  assert isinstance(responses[0], types.LiveServerMessage)


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_receive_error(
     mock_websocket, vertexai
):
  mock_websocket.recv = AsyncMock(return_value='invalid json')
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  with pytest.raises(ValueError):
    await session.receive().__anext__()


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_receive_text(
     mock_websocket, vertexai
):
  mock_websocket.recv = AsyncMock(
      side_effect=[
          '{"serverContent": {"modelTurn": {"parts":[{"text": "test"}]}}}',
          '{"serverContent": {"turnComplete": true}}',
      ]
  )
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  messages = session.receive()
  messages = await _async_iterator_to_list(messages)
  assert isinstance(messages[0], types.LiveServerMessage)
  assert messages[0].server_content.model_turn.parts[0].text == 'test'
  assert messages[1].server_content.turn_complete == True


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_receive_audio(
     mock_websocket, vertexai
):
  mock_websocket.recv = AsyncMock(
      side_effect=[
          (
              '{"serverContent": {"modelTurn": {"parts":[{"inlineData":'
              ' {"data": "MDAwMDAw", "mime_type": "audio/pcm" }}]}}}'
          ),
          '{"serverContent": {"turnComplete": true}}',
      ]
  )
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  messages = session.receive()
  messages = await _async_iterator_to_list(messages)
  assert isinstance(messages[0], types.LiveServerMessage)
  assert (
      messages[0].server_content.model_turn.parts[0].inline_data.mime_type
      == 'audio/pcm'
  )
  assert (
      messages[0].server_content.model_turn.parts[0].inline_data.data
      == b'000000'
  )

  with pytest.raises(RuntimeError):
    await _async_iterator_to_list(session.receive())


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_receive_tool_call(
     mock_websocket, vertexai
):
  mock_websocket.recv = AsyncMock(
      side_effect=[
          (
              '{"toolCall": {"functionCalls": [{"name":'
              ' "get_current_weather", "args": {"location": "San Francisco",'
              ' "unit": "C"}}]}}'
          ),
          '{"serverContent": {"turnComplete": true}}',
      ]
  )
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  messages = session.receive()
  messages = await _async_iterator_to_list(messages)
  assert isinstance(messages[0], types.LiveServerMessage)
  assert messages[0].tool_call.function_calls[0].name == 'get_current_weather'
  assert (
      messages[0].tool_call.function_calls[0].args['location']
      == 'San Francisco'
  )
  assert messages[0].tool_call.function_calls[0].args['unit'] == 'C'

  with pytest.raises(RuntimeError):
    await _async_iterator_to_list(session.receive())


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_receive_transcription(
     mock_websocket, vertexai
):
  mock_websocket.recv = AsyncMock(
      side_effect=[
          '{"serverContent": {"inputTranscription": {"text": "test_input", "finished": true}}}',
          '{"serverContent": {"outputTranscription": {"text": "test_output", "finished": false}}}',
          '{"serverContent": {"turnComplete": true}}',
      ]
  )
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  messages = session.receive()
  messages = await _async_iterator_to_list(messages)
  assert isinstance(messages[0], types.LiveServerMessage)
  assert messages[0].server_content.input_transcription.text == 'test_input'
  assert messages[0].server_content.input_transcription.finished == True

  assert isinstance(messages[1], types.LiveServerMessage)
  assert messages[1].server_content.output_transcription.text == 'test_output'
  assert messages[1].server_content.output_transcription.finished == False


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_go_away(
    mock_websocket, vertexai
):
  mock_websocket.recv = AsyncMock(
      side_effect=[
          '{"goAway": {"timeLeft": "10s"}}',
          '{"serverContent": {"turnComplete": true}}',
      ]
  )
  expected_result = types.LiveServerMessage(
      go_away=types.LiveServerGoAway(time_left='10s'),
  )
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  messages = session.receive()
  messages = await _async_iterator_to_list(messages)
  message = messages[0]

  assert isinstance(message, types.LiveServerMessage)
  assert message == expected_result


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_resumption_update(
    mock_websocket, vertexai
):
  mock_websocket.recv = AsyncMock(
      side_effect=[
          """{
                "sessionResumptionUpdate": {
                    "newHandle": "test_handle",
                    "resumable": "true",
                    "lastConsumedClientMessageIndex": "123456789"
                }
          }""",
          '{"serverContent": {"turnComplete": true}}',
      ]
  )

  expected_result = types.LiveServerMessage(
      session_resumption_update=types.LiveServerSessionResumptionUpdate(
          new_handle='test_handle',
          resumable=True,
          last_consumed_client_message_index=123456789
      ),
  )

  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  messages = session.receive()
  messages = await _async_iterator_to_list(messages)
  message = messages[0]

  assert isinstance(message, types.LiveServerMessage)
  assert message == expected_result


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_start_stream(
     mock_websocket, vertexai
):

  session = live.AsyncSession(
      mock_api_client(vertexai=vertexai), mock_websocket
  )

  async def mock_stream():
    yield b'data1'
    yield b'data2'

  async for message in session.start_stream(
      stream=mock_stream(), mime_type='audio/pcm'
  ):
    assert isinstance(message, types.LiveServerMessage)


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_async_session_close( mock_websocket, vertexai):
  session = live.AsyncSession(
      mock_api_client(vertexai=vertexai), mock_websocket
  )
  await session.close()
  mock_websocket.close.assert_called_once()


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_no_config(vertexai):
  with warnings.catch_warnings():
    # Make sure there are no warnings cause by default values.
    warnings.simplefilter('error')
    result = await get_connect_message(
        mock_api_client(vertexai=vertexai),
        model='test_model'
    )
  expected_result = {'setup': {}}
  if vertexai:
    expected_result['setup']['model'] = 'projects/test_project/locations/us-central1/publishers/google/models/test_model'
    expected_result['setup']['generationConfig'] = {}
    expected_result['setup']['generationConfig']['responseModalities'] = ["AUDIO"]
  else:
    expected_result['setup']['model'] = 'models/test_model'
  assert result == expected_result


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_speech_config(vertexai):

  expected_result = {
      'setup': {
          'model': 'models/test_model',
          'generationConfig': {
              'speechConfig': {
                  'voiceConfig': {
                      'prebuiltVoiceConfig': {'voiceName': 'en-default'}
                  },
                  'languageCode': 'en-US',
              },
              'temperature': 0.7,
              'topP': 0.8,
              'topK': 9.0,
              'maxOutputTokens': 10,
              'mediaResolution': 'MEDIA_RESOLUTION_MEDIUM',
              'seed': 13,
          },
          'systemInstruction': {
              'parts': [
                  {
                      'text': 'test instruction',
                  },
              ],
              'role': 'user',
          },
      }
  }
  if vertexai:
    expected_result['setup']['model'] = (
        'projects/test_project/locations/us-central1/'
        'publishers/google/models/test_model'
    )
    expected_result['setup']['generationConfig']['responseModalities'] = [
        'AUDIO'
    ]
  else:
    expected_result['setup']['model'] = 'models/test_model'

  # Config is a dict
  config_dict = {
      'speech_config': {
          'voice_config': {
              'prebuilt_voice_config': {'voice_name': 'en-default'}
          },
          'language_code': 'en-US',
      },
      'temperature': 0.7,
      'top_p': 0.8,
      'top_k': 9,
      'max_output_tokens': 10,
      'seed': 13,
      'system_instruction': 'test instruction',
      'media_resolution': 'MEDIA_RESOLUTION_MEDIUM'
  }
  result = await get_connect_message(
      mock_api_client(vertexai=vertexai), model='test_model', config=config_dict
  )
  assert result == expected_result
  # Config is a LiveConnectConfig
  config = types.LiveConnectConfig(
      speech_config=types.SpeechConfig(
          voice_config=types.VoiceConfig(
              prebuilt_voice_config=types.PrebuiltVoiceConfig(
                  voice_name='en-default'
              )
          ),
          language_code='en-US',
      ),
      temperature=0.7,
      top_p=0.8,
      top_k=9,
      max_output_tokens=10,
      media_resolution=types.MediaResolution.MEDIA_RESOLUTION_MEDIUM,
      seed=13,
      system_instruction='test instruction',
  )
  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )
  assert result == expected_result


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_system_instruction_as_content_type(
    vertexai,
):
  config_dict = {
      'system_instruction': {
          'parts': [{'text': 'test instruction'}],
          'role': 'user',
      },
  }
  config = types.LiveConnectConfig(**config_dict)
  expected_result = {
      'setup': {
          'model': 'test_model',
          'systemInstruction': {
              'parts': [{'text': 'test instruction'}],
              'role': 'user',
          },
      }
  }
  if vertexai:
    expected_result['setup'][
        'model'
    ] = 'projects/test_project/locations/us-central1/publishers/google/models/test_model'
    expected_result['setup']['generationConfig'] = {}
    expected_result['setup']['generationConfig']['responseModalities'] = [
        'AUDIO'
    ]
  else:
    expected_result['setup']['model'] = 'models/test_model'

  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )
  assert result == expected_result


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_config_tools_google_search(vertexai):
  config_dict = {
      'response_modalities': ['TEXT'],
      'system_instruction': 'test instruction',
      'generation_config': {'temperature': 0.7},
      'tools': [{'google_search': {}}],
  }

  config = types.LiveConnectConfig(**config_dict)
  expected_result = {
      'setup': {
          'generationConfig': {
              'temperature': 0.7,
              'responseModalities': ['TEXT'],
          },
          'systemInstruction': {
              'parts': [{'text': 'test instruction'}],
              'role': 'user',
          },
          'tools': [{'googleSearch': {}}],
      }
  }
  if vertexai:
    expected_result['setup']['model'] = 'projects/test_project/locations/us-central1/publishers/google/models/test_model'
  else:
    expected_result['setup']['model'] = 'models/test_model'

  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )

  assert result == expected_result

  # Test for vertex, config is a LiveConnectConfig
  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )

  assert result == expected_result


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_context_window_compression(
     vertexai
):
  config = types.LiveConnectConfig(
      generation_config=types.GenerationConfig(temperature=0.7),
      response_modalities=['TEXT'],
      system_instruction=types.Content(
          parts=[types.Part(text='test instruction')], role='user'
      ),
      context_window_compression=types.ContextWindowCompressionConfig(
          trigger_tokens=1000,
          sliding_window=types.SlidingWindow(target_tokens=10),
      ),
  )
  expected_result = {
      'setup': {
          'generationConfig': {
              'temperature': 0.7,
              'responseModalities': ['TEXT'],
          },
          'systemInstruction': {
              'parts': [{'text': 'test instruction'}],
              'role': 'user',
          },
           'contextWindowCompression': {
              'triggerTokens': 1000,
              'slidingWindow': {'targetTokens': 10},
          }
      }
  }
  if vertexai:
    expected_result['setup']['model'] = 'projects/test_project/locations/us-central1/publishers/google/models/test_model'
  else:
    expected_result['setup']['model'] = 'models/test_model'

  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )
  assert result == expected_result

@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_config_tools_function_declaration(
     vertexai
):
  config_dict = {
      'generation_config': {'temperature': 0.7},
      'tools': [{'function_declarations': function_declarations}],
  }
  config = types.LiveConnectConfig(**config_dict)
  expected_result = {
      'setup': {
          'model': 'test_model',
          'tools': [{
              'functionDeclarations': [{
                  'parameters': {
                      'type': 'OBJECT',
                      'properties': {
                          'location': {
                              'type': 'STRING',
                              'description': (
                                  'The location to get the weather for'
                              ),
                          },
                          'unit': {'type': 'STRING', 'enum': ['C', 'F']},
                      },
                  },
                  'name': 'get_current_weather',
                  'description': 'Get the current weather in a city',
              }],
          }],
      }
  }
  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )

  assert result['setup']['tools'][0]['functionDeclarations'][0][
      'description'
  ] == (
      expected_result['setup']['tools'][0]['functionDeclarations'][0][
          'description'
      ]
  )

  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )

  assert result['setup']['tools'][0]['functionDeclarations'][0][
      'description'
  ] == (
      expected_result['setup']['tools'][0]['functionDeclarations'][0][
          'description'
      ]
  )


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_config_tools_function_directly(
     vertexai
):
  config_dict = {
      'generation_config': {'temperature': 0.7},
      'tools': [get_current_weather],
  }
  config = types.LiveConnectConfig(**config_dict)
  expected_result = {
      'setup': {
          'model': 'test_model',
          'tools': [{
              'functionDeclarations': [{
                  'parameters': {
                      'type': 'OBJECT',
                      'properties': {
                          'location': {
                              'type': 'STRING',
                              'description': (
                                  'The location to get the weather for'
                              ),
                          },
                          'unit': {'type': 'STRING', 'enum': ['C', 'F']},
                      },
                  },
                  'name': 'get_current_weather',
                  'description': 'Get the current weather in a city.',
              }],
          }],
      }
  }
  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )

  assert result['setup']['tools'][0]['functionDeclarations'][0][
      'description'
  ] == (
      expected_result['setup']['tools'][0]['functionDeclarations'][0][
          'description'
      ]
  )

  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )

  assert result['setup']['tools'][0]['functionDeclarations'][0][
      'description'
  ] == (
      expected_result['setup']['tools'][0]['functionDeclarations'][0][
          'description'
      ]
  )


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_config_tools_code_execution(
     vertexai
):
  config_dict = {
      'tools': [{'code_execution': {}}],
  }
  config = types.LiveConnectConfig(**config_dict)
  expected_result = {
      'setup': {
          'model': 'test_model',
          'tools': [{
              'codeExecution': {},
          }],
      }
  }
  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )

  assert result['setup']['tools'][0] == expected_result['setup']['tools'][0]


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_realtime_input_config(vertexai):
  config_dict = {
      'realtime_input_config': {
          'automatic_activity_detection': {
              'disabled': True,
              'start_of_speech_sensitivity': 'START_SENSITIVITY_HIGH',
              'end_of_speech_sensitivity': 'END_SENSITIVITY_HIGH',
              'prefix_padding_ms': 20,
              'silence_duration_ms': 100,
          },
          'activity_handling': 'NO_INTERRUPTION',
          'turn_coverage': 'TURN_INCLUDES_ALL_INPUT',
      }
  }

  config = types.LiveConnectConfig(**config_dict)
  expected_result = {
      'setup': {
          'model': 'test_model',
          'realtimeInputConfig': {
              'automaticActivityDetection': {
                  'disabled': True,
                  'startOfSpeechSensitivity': 'START_SENSITIVITY_HIGH',
                  'endOfSpeechSensitivity': 'END_SENSITIVITY_HIGH',
                  'prefixPaddingMs': 20,
                  'silenceDurationMs': 100,
              },
              'activityHandling': 'NO_INTERRUPTION',
              'turnCoverage': 'TURN_INCLUDES_ALL_INPUT',
          },
      }
  }

  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )

  assert (
      result['setup']['realtimeInputConfig']
      == expected_result['setup']['realtimeInputConfig']
  )


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_input_transcription(vertexai):
  config_dict = {
      'input_audio_transcription': {},
  }
  config = types.LiveConnectConfig(**config_dict)
  expected_result = {
      'setup': {
          'model': 'test_model',
          'inputAudioTranscription': {},
      }
  }

  with exception_if_mldev(vertexai, ValueError):
    result = await get_connect_message(
        mock_api_client(vertexai=vertexai),
        model='test_model', config=config
    )
  if not vertexai:
    return

  assert (
      result['setup']['inputAudioTranscription']
      == expected_result['setup']['inputAudioTranscription']
  )


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_output_transcription(vertexai):
  config_dict = {
      'output_audio_transcription': {},
  }
  config = types.LiveConnectConfig(**config_dict)
  expected_result = {
      'setup': {
          'model': 'test_model',
          'outputAudioTranscription': {},
      }
  }

  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )

  assert (
      result['setup']['outputAudioTranscription']
      == expected_result['setup']['outputAudioTranscription']
  )

@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_media_resolution(vertexai):
  config_dict = {
      'media_resolution': 'MEDIA_RESOLUTION_LOW',
  }
  config = types.LiveConnectConfig(**config_dict)
  expected_result = {
      'setup': {
          'model': 'test_model',
          'generationConfig': {'mediaResolution':'MEDIA_RESOLUTION_LOW'},
      }
  }

  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model', config=config
  )

  assert (
      result['setup']['generationConfig']['mediaResolution']
      == expected_result['setup']['generationConfig']['mediaResolution']
  )


@pytest.mark.parametrize('vertexai', [True])
@pytest.mark.asyncio
async def test_bidi_setup_publishers(
     vertexai
):
  expected_result = {
      'setup': {
         'generationConfig': {
             'responseModalities': [
                 'AUDIO',
             ],
         },
         'model': 'projects/test_project/locations/us-central1/publishers/google/models/test_model',
      }
  }
  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='publishers/google/models/test_model')

  assert result == expected_result


@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_generation_config_warning(
     vertexai
):
  with pytest.warns(
      DeprecationWarning,
      match='Setting `LiveConnectConfig.generation_config` is deprecated'
  ):
    result = await get_connect_message(
        mock_api_client(vertexai=vertexai),
        model='models/test_model',
        config={'generation_config': {'temperature': 0.7}})

  assert result['setup']['generationConfig']['temperature'] == 0.7

@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_session_resumption(vertexai):
  config_dict = {
      'session_resumption': {'handle': 'test_handle'},
  }
  config = types.LiveConnectConfig(**config_dict)

  result = await get_connect_message(
      mock_api_client(vertexai=vertexai),
      model='test_model',
      config=config
  )
  expected_result = {
      'setup': {
          'sessionResumption': {
              'handle': 'test_handle',
          },
      }
  }
  if vertexai:
    expected_result['setup']['generationConfig'] = {
        'responseModalities': [
            'AUDIO',
        ],
    }
    expected_result['setup']['model'] = 'projects/test_project/locations/us-central1/publishers/google/models/test_model'
  else:
    expected_result['setup']['model'] = 'models/test_model'
  assert result == expected_result

@pytest.mark.parametrize('vertexai', [True, False])
@pytest.mark.asyncio
async def test_bidi_setup_to_api_with_transparent_session_resumption(vertexai):
  config_dict = {
      'session_resumption': {'handle': 'test_handle', 'transparent': True},
  }
  config = types.LiveConnectConfig(**config_dict)

  with exception_if_mldev(vertexai, ValueError):
    result = await get_connect_message(
        mock_api_client(vertexai=vertexai),
        model='test_model',
        config=config
    )

  expected_result = {
      'setup': {
          'sessionResumption': {
              'handle': 'test_handle',
              'transparent': True,
          },
      }
  }
  if vertexai:
    expected_result['setup']['generationConfig'] = {
        'responseModalities': [
            'AUDIO',
        ],
    }
    expected_result['setup']['model'] = 'projects/test_project/locations/us-central1/publishers/google/models/test_model'
  else:
    return

  assert result == expected_result


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_str( mock_websocket, vertexai):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  result = session._parse_client_message('test')
  assert 'client_content' in result
  assert result == {
      'client_content': {
          'turn_complete': False,
          'turns': [{'role': 'user', 'parts': [{'text': 'test'}]}],
      }
  }
  # _parse_client_message returns a TypedDict, so we should be able to
  # construct a LiveClientMessage from it
  assert types.LiveClientMessage(**result)


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_blob( mock_websocket, vertexai):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  result = session._parse_client_message(
      types.Blob(data=bytes([0, 0, 0]), mime_type='text/plain')
  )
  assert 'realtime_input' in result
  assert result == {
      'realtime_input': {
          'media_chunks': [{'mime_type': 'text/plain', 'data': 'AAAA'}],
      }
  }


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_blob_dict(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )

  blob = types.Blob(data=bytes([0, 0, 0]), mime_type='text/plain')
  blob_dict = blob.model_dump()
  result = session._parse_client_message(blob_dict)
  assert 'realtime_input' in result
  assert result == {
      'realtime_input': {
          'media_chunks': [{'mime_type': 'text/plain', 'data': 'AAAA'}],
      }
  }


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_client_content(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  result = session._parse_client_message(
      types.LiveClientContent(
          turn_complete=False,
          turns=[types.Content(parts=[types.Part(text='test')], role='user')],
      )
  )
  assert 'client_content' in result
  assert result == {
      'client_content': {
          'turn_complete': False,
          'turns': [{'role': 'user', 'parts': [{'text': 'test'}]}],
      }
  }


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_client_content_blob(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  client_content = types.LiveClientContent(
      turn_complete=False,
      turns=[
          types.Content(
              parts=[
                  types.Part(
                      inline_data=types.Blob(
                          data=bytes([0, 0, 0]), mime_type='text/plain'
                      )
                  )
              ],
              role='user',
          )
      ],
  )
  result = session._parse_client_message(client_content)
  assert 'client_content' in result
  assert (
      type(
          result['client_content']['turns'][0]['parts'][0]['inline_data'][
              'data'
          ]
      )
      == str
  )
  assert result == {
      'client_content': {
          'turn_complete': False,
          'turns': [{
              'role': 'user',
              'parts': [
                  {'inline_data': {'mime_type': 'text/plain', 'data': 'AAAA'}}
              ],
          }],
      }
  }


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_client_content_dict(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  client_content = types.LiveClientContent(
      turn_complete=False,
      turns=[
          types.Content(
              parts=[
                  types.Part(
                      inline_data=types.Blob(
                          data=bytes([0, 0, 0]), mime_type='text/plain'
                      )
                  )
              ],
              role='user',
          )
      ],
  )
  result = session._parse_client_message(
      client_content.model_dump(mode='json', exclude_none=True)
  )
  assert 'client_content' in result
  assert (
      type(
          result['client_content']['turns'][0]['parts'][0]['inline_data'][
              'data'
          ]
      )
      == str
  )
  assert result == {
      'client_content': {
          'turn_complete': False,
          'turns': [{
              'role': 'user',
              'parts': [
                  {'inline_data': {'mime_type': 'text/plain', 'data': 'AAAA'}}
              ],
          }],
      }
  }


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_realtime_input(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  input = types.LiveClientRealtimeInput(
      media_chunks=[types.Blob(data=bytes([0, 0, 0]), mime_type='text/plain')]
  )
  result = session._parse_client_message(input)
  assert 'realtime_input' in result
  assert result == {
      'realtime_input': {
          'media_chunks': [{'mime_type': 'text/plain', 'data': 'AAAA'}],
      }
  }


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_realtime_input_dict(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  input = types.LiveClientRealtimeInput(
      media_chunks=[types.Blob(data=bytes([0, 0, 0]), mime_type='text/plain')]
  )
  result = session._parse_client_message(
      input.model_dump(mode='json', exclude_none=True)
  )
  assert 'realtime_input' in result
  assert result == {
      'realtime_input': {
          'media_chunks': [{'mime_type': 'text/plain', 'data': 'AAAA'}],
      }
  }


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_tool_response(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  input = types.LiveClientToolResponse(
      function_responses=[
          types.FunctionResponse(
              id='test_id',
              name='test_name',
              response={'result': 'test_response'},
          )
      ]
  )
  result = session._parse_client_message(input)
  assert 'tool_response' in result
  assert result == {
      'tool_response': {
          'function_responses': [
              {
                  'id': 'test_id',
                  'name': 'test_name',
                  'response': {
                      'result': 'test_response',
                  },
              },
          ],
      }
  }


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_function_response(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  input = types.FunctionResponse(
    id='test_id',
    name='test_name',
    response={'result': 'test_response'},
  )
  result = session._parse_client_message(input)
  assert 'tool_response' in result
  assert result == {
      'tool_response': {
          'function_responses': [
              {
                  'id': 'test_id',
                  'name': 'test_name',
                  'response': {
                      'result': 'test_response',
                  },
              },
          ],
      }
  }


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_tool_response_dict_with_only_response(
     mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  input = {
    'id': 'test_id',
    'name': 'test_name',
    'response': {
        'result': 'test_response',
    }
  }
  result = session._parse_client_message(input)
  assert 'tool_response' in result
  assert result == {
      'tool_response': {
          'function_responses': [
              {
                  'id': 'test_id',
                  'name': 'test_name',
                  'response': {
                      'result': 'test_response',
                  },
              },
          ],
      }
  }


@pytest.mark.parametrize('vertexai', [True, False])
def test_parse_client_message_realtime_tool_response(
    mock_websocket, vertexai
):
  session = live.AsyncSession(
      api_client=mock_api_client(vertexai=vertexai), websocket=mock_websocket
  )
  input = types.LiveClientToolResponse(
      function_responses=[
          types.FunctionResponse(
              id='test_id',
              name='test_name',
              response={'result': 'test_response'},
          )
      ]
  )

  result = session._parse_client_message(
      input.model_dump(mode='json', exclude_none=True)
  )
  assert 'tool_response' in result
  assert result == {
      'tool_response': {
          'function_responses': [
              {
                  'id': 'test_id',
                  'name': 'test_name',
                  'response': {
                      'result': 'test_response',
                  },
              },
          ],
      }
  }
