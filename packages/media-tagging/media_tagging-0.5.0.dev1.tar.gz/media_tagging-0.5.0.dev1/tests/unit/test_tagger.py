# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from media_tagging import repository, tagger
from media_tagging.taggers import api, base, llm


@pytest.mark.parametrize(
  ('tagger_type', 'tagger_class'),
  [
    ('vision-api', api.GoogleVisionAPITagger),
    ('video-api', api.GoogleVideoIntelligenceAPITagger),
  ],
)
def test_create_tagger_returns_correct_api_tagger(tagger_type, tagger_class):
  created_tagger = tagger.create_tagger(
    tagger_type, {'project': 'test-project'}
  )
  assert isinstance(created_tagger, tagger_class)
  assert created_tagger._project == 'test-project'


@pytest.mark.parametrize(
  ('tagger_type', 'llm_tagger_type'),
  [
    ('gemini-image', 'UNSTRUCTURED'),
    ('gemini-structured-image', 'STRUCTURED'),
    ('gemini-description-image', 'DESCRIPTION'),
  ],
)
def test_create_tagger_returns_correct_llm_image_tagger(
  tagger_type, llm_tagger_type
):
  created_tagger = tagger.create_tagger(tagger_type)
  assert isinstance(created_tagger, llm.GeminiImageTagger)
  assert (
    created_tagger.llm_tagger_type == llm.LLMTaggerTypeEnum[llm_tagger_type]
  )


@pytest.mark.parametrize(
  ('tagger_type', 'llm_tagger_type'),
  [
    ('gemini-video', 'UNSTRUCTURED'),
    ('gemini-structured-video', 'STRUCTURED'),
    ('gemini-description-video', 'DESCRIPTION'),
  ],
)
def test_create_tagger_returns_correct_llm_video_tagger(
  tagger_type, llm_tagger_type
):
  created_tagger = tagger.create_tagger(tagger_type)
  assert isinstance(created_tagger, llm.GeminiVideoTagger)
  assert (
    created_tagger.llm_tagger_type == llm.LLMTaggerTypeEnum[llm_tagger_type]
  )


def test_create_tagger_raises_erorr_on_incorrect_tagger():
  with pytest.raises(
    ValueError, match='Incorrect tagger "unknown-tagger" is provided*'
  ):
    tagger.create_tagger('unknown-tagger')


def test_tag_media_saves_tagging_results_to_repository(mocker):
  expected_result = base.TaggingResult(
    identifier='test',
    type='image',
    content=base.Description(text='Test description.'),
  )
  mocker.patch(
    'media_tagging.taggers.api.GoogleVisionAPITagger.tag',
    return_value=expected_result,
  )
  persist_repository = repository.InMemoryTaggingResultsRepository()
  tagging_result = tagger.tag_media(
    media_paths=['test'],
    tagger_type=api.GoogleVisionAPITagger(),
    persist_repository=persist_repository,
  )

  assert tagging_result == [expected_result]
  assert persist_repository.list() == [expected_result]
