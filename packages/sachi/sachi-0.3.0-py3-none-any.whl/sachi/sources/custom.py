import re

from sachi.sources.base import (
    MediaType,
    SachiEpisodeModel,
    SachiParentModel,
    SachiSource,
)

INPUT_RE = re.compile(r"(?P<title>.+?)(?: \((?P<year>\d+)\))?$")


class CustomMovieSource(
    SachiSource[None], media_type=MediaType.MOVIE, service="Custom"
):
    async def search(self, query: str) -> list[SachiParentModel[None]]:
        qmatch = INPUT_RE.match(query)
        if qmatch is None:
            return []
        groups = qmatch.groupdict()
        return [
            SachiParentModel(
                media_type=MediaType.MOVIE,
                ref_id=None,
                title=groups["title"],
                year=int(groups["year"]) if groups["year"] else None,
            )
        ]

    async def get_episodes(
        self, parent: SachiParentModel[None]
    ) -> list[SachiEpisodeModel[None]]:
        return [SachiEpisodeModel(ref_id=None, season=0, episode=0)]
