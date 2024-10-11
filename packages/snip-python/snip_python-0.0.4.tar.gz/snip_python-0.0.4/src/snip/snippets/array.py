from .base import BaseSnip


class ArraySnip(BaseSnip[dict, dict]):
    """Array snip class.

    Allows to combine multiple snippets into an array.
    """

    type = "array"

    snippets: list[BaseSnip]

    def __init__(self, snippets: list[BaseSnip], **kwargs):
        """Create an array snip from a list of snippets.

        Parameters
        ----------
        snippets : list[BaseSnip]
            The snippets to combine into an array. Accepts any type of snippet.
        kwargs : Any
            Additional keyword arguments passed :class:`snip.snippets.base.BaseSnip.__init__`.
        """
        super().__init__(**kwargs)
        self.snippets = snippets

    def _data(self):
        return {"snips": [snip.as_json() for snip in self.snippets]}
