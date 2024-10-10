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
"""Module for performing media tagging.

Media tagging sends API requests to tagging engine (i.e. Google Vision API)
and returns tagging results that can be easily written.
"""

# pylint: disable=C0330, g-bad-import-order, g-multiple-import
import itertools
import logging
import os
from collections.abc import Sequence
from concurrent import futures

from media_tagging import media, repository
from media_tagging.taggers import api, base, llm

TAGGERS = {
  'vision-api': api.GoogleVisionAPITagger,
  'video-api': api.GoogleVideoIntelligenceAPITagger,
  'gemini-image': llm.GeminiImageTagger,
  'gemini-structured-image': llm.GeminiImageTagger,
  'gemini-description-image': llm.GeminiImageTagger,
  'gemini-video': llm.GeminiVideoTagger,
  'gemini-structured-video': llm.GeminiVideoTagger,
  'gemini-description-video': llm.GeminiVideoTagger,
  'gemini-youtube-video': llm.GeminiYouTubeVideoTagger,
  'gemini-structured-youtube-video': llm.GeminiYouTubeVideoTagger,
  'gemini-description-youtube-video': llm.GeminiYouTubeVideoTagger,
}

_LLM_TAGGERS_TYPES = {
  'gemini-image': llm.LLMTaggerTypeEnum.UNSTRUCTURED,
  'gemini-structured-image': llm.LLMTaggerTypeEnum.STRUCTURED,
  'gemini-description-image': llm.LLMTaggerTypeEnum.DESCRIPTION,
  'gemini-video': llm.LLMTaggerTypeEnum.UNSTRUCTURED,
  'gemini-structured-video': llm.LLMTaggerTypeEnum.STRUCTURED,
  'gemini-description-video': llm.LLMTaggerTypeEnum.DESCRIPTION,
  'gemini-youtube-video': llm.LLMTaggerTypeEnum.UNSTRUCTURED,
  'gemini-structured-youtube-video': llm.LLMTaggerTypeEnum.STRUCTURED,
  'gemini-description-youtube-video': llm.LLMTaggerTypeEnum.DESCRIPTION,
}


def create_tagger(
  tagger_type: str, tagger_parameters: dict[str, str] | None = None
) -> base.BaseTagger:
  """Factory for creating taggers based on provided type.

  Args:
    tagger_type: Type of tagger.
    tagger_parameters: Various parameters to instantiate tagger.

  Returns:
    Concrete tagger class.
  """
  if not tagger_parameters:
    tagger_parameters = {}
  if tagger := TAGGERS.get(tagger_type):
    if issubclass(tagger, llm.LLMTagger):
      return tagger(
        tagger_type=_LLM_TAGGERS_TYPES.get(tagger_type), **tagger_parameters
      )
    return tagger(**tagger_parameters)
  raise ValueError(
    f'Incorrect tagger "{tagger_type}" is provided, '
    f'valid options: {list(TAGGERS.keys())}'
  )


def tag_media_sequentially(
  media_paths: Sequence[str | os.PathLike],
  tagger_type: base.BaseTagger,
  tagging_parameters: dict[str, str] | None = None,
  persist_repository: repository.BaseTaggingResultsRepository | None = None,
) -> list[base.TaggingResult]:
  """Runs media tagging algorithm.

  Args:
    media_paths: Local or remote path to media file.
    tagger_type: Initialized tagger.
    tagging_parameters: Optional keywords arguments to be sent for tagging.
    persist_repository: Repository to store tagging results.

  Returns:
    Results of tagging for all media.
  """
  if not tagging_parameters:
    tagging_parameters = {}
  results = []
  for path in media_paths:
    medium = media.Medium(path, media.MediaTypeEnum.YOUTUBE_LINK)
    if persist_repository and (
      tagging_results := persist_repository.get([medium.name])
    ):
      logging.info('Getting media from repository: %s', path)
      results.extend(tagging_results)
      continue
    logging.info('Processing media: %s', path)
    tagging_results = tagger_type.tag(
      medium,
      tagging_options=base.TaggingOptions(**tagging_parameters),
    )
    if persist_repository:
      persist_repository.add([tagging_results])
    results.append(tagging_results)
  return results


def tag_media(
  media_paths: Sequence[str | os.PathLike],
  tagger_type: base.BaseTagger,
  tagging_parameters: dict[str, str] | None = None,
  parallel_threshold: int = 1,
  persist_repository: repository.BaseTaggingResultsRepository | None = None,
) -> list[base.TaggingResult]:
  """Runs media tagging algorithm.

  Args:
    media_paths: Local or remote path to media file.
    tagger_type: Initialized tagger.
    tagging_parameters: Optional keywords arguments to be sent for tagging.
    parallel_threshold: Number of threads.
    persist_repository: Repository to store tagging results.

  Returns:
    Results of tagging for all media.
  """
  untagged_media = media_paths
  tagged_media = []
  if persist_repository and (
    tagged_media := persist_repository.get(media_paths)
  ):
    tagged_media_names = {media.identifier for media in tagged_media}
    untagged_media = {
      media_path
      for media_path in media_paths
      if media.convert_path_to_media_name(media_path) not in tagged_media_names
    }

  if not parallel_threshold:
    return (
      tag_media_sequentially(
        untagged_media, tagger_type, tagging_parameters, persist_repository
      )
      + tagged_media
    )
  with futures.ThreadPoolExecutor(max_workers=parallel_threshold) as executor:
    future_to_media_path = {
      executor.submit(
        tag_media_sequentially,
        [media_path],
        tagger_type,
        tagging_parameters,
        persist_repository,
      ): media_path
      for media_path in media_paths
    }
    untagged_media = itertools.chain.from_iterable(
      [future.result() for future in futures.as_completed(future_to_media_path)]
    )
    return list(untagged_media) + tagged_media
