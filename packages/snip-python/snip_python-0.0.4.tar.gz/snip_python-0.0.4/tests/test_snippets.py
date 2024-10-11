# Mock data for testing
import pytest

from snip.snippets.array import ArraySnip
from snip.snippets.base import BaseSnip
from snip.snippets.image import ImageSnip
from snip.snippets.text import TextSnip


# Mock data for testing
class MockData:
    pass


class MockView:
    pass


class MockSnipMinimal(BaseSnip[MockData, None]):
    def __init__(self, book_id: int, type: str):
        self.type = type
        super().__init__(book_id)

    def _data(self) -> MockData:
        return MockData()

    def _get_schema(self):
        return None


class MockSnipFull(BaseSnip[MockData, MockView]):
    def __init__(self, book_id: int, type: str):
        self.type = type
        super().__init__(book_id)

    def _data(self) -> MockData:
        return MockData()

    def _view(self) -> MockView:
        return MockView()

    def _get_schema(self):
        return {"type": "object"}


class TestBaseSnip:
    @pytest.fixture
    def snip(self):
        return MockSnipMinimal(book_id=1, type="test_type")

    def test_init(self, snip):
        assert snip.book_id == 1
        assert snip.type == "test_type"

        # raise on empty type
        with pytest.raises(ValueError):
            MockSnipMinimal(book_id=1, type="")

    def test_data(self, snip):
        assert isinstance(snip._data(), MockData)

    def test_view(self, snip):
        assert snip._view() is None

    def test_schema(self, snip):
        assert snip.schema == None

    def test_as_json(self, snip):
        json_data = snip.as_json()
        assert json_data["book_id"] == 1
        assert json_data["type"] == "test_type"
        assert isinstance(json_data["data"], MockData)
        assert json_data.get("view") is None


class TestBaseFullSnip:
    @pytest.fixture
    def snip(self):
        return MockSnipFull(book_id=1, type="test_type")

    def test_init(self, snip):
        assert snip.book_id == 1
        assert snip.type == "test_type"

        # raise on empty type
        with pytest.raises(ValueError):
            MockSnipFull(book_id=1, type="")

    def test_data(self, snip):
        assert isinstance(snip._data(), MockData)

    def test_view(self, snip):
        assert isinstance(snip._view(), MockView)

    def test_schema(self, snip):
        assert snip.schema == {"type": "object"}

    def test_as_json(self, snip):
        json_data = snip.as_json()
        assert json_data["book_id"] == 1
        assert json_data["type"] == "test_type"
        assert isinstance(json_data["data"], MockData)
        assert isinstance(json_data["view"], MockView)


class TestImageSnip:
    def test_from_pil(self):
        from PIL import Image

        img = Image.new("RGB", (100, 100))

        snip = ImageSnip.from_pil(img, book_id=1)

        assert snip.book_id == 1
        assert snip.image == img

    def test_from_array(self):
        import numpy as np

        array = np.random.rand(100, 100, 3)
        snip = ImageSnip.from_array(array, mode="RGB", book_id=1)
        assert snip.book_id == 1

    def test_from_matplotlib(self):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4])
        snip = ImageSnip.from_matplotlib(fig, book_id=1)
        assert snip.book_id == 1
        plt.close(fig)

    def test_as_json(self):
        from PIL import Image

        img = Image.new("RGB", (100, 100))

        snip = ImageSnip(book_id=1, image=img)
        ImageSnip._get_schema = lambda x: None  # type: ignore

        json_data = snip.as_json(validate=False)
        assert json_data["book_id"] == 1
        assert json_data["type"] == "image"
        assert isinstance(json_data["data"], dict)
        assert json_data.get("view") is None
        assert json_data["data"]["blob"] is not None
        assert json_data["data"]["blob"]["mime"] == "image/png"
        assert json_data["data"]["blob"]["data"] is not None

    def test_width_height_scale(self):
        from PIL import Image

        img = Image.new("RGB", (100, 200))
        snip = ImageSnip(book_id=1, image=img)
        assert snip.size[0] == 100

        # Check bigg image
        img = Image.new("RGB", (2000, 2000))

        snip = ImageSnip(book_id=1, image=img)
        assert snip.size[0] == 1400
        assert snip.size[1] == 1400

        # Test set width height
        snip.set_width(200)
        assert snip.size[0] == 200
        assert snip.size[1] == 200

        snip.set_height(300)
        assert snip.size[0] == 300
        assert snip.size[1] == 300

        snip.set_width(200, keep_ratio=False)
        assert snip.size[0] == 200
        assert snip.size[1] == 300

        snip.set_height(400, keep_ratio=False)
        assert snip.size[0] == 200
        assert snip.size[1] == 400

        # Scale
        snip.scale(0.5)
        assert snip.size[0] == 100
        assert snip.size[1] == 200


from PIL import Image


class TestArraySnip:
    text = TextSnip(text="Hello World", book_id=1)
    image = ImageSnip.from_pil(Image.new("RGB", (100, 100)), book_id=1)

    def test_create(self):
        array = ArraySnip(book_id=1, snippets=[self.text, self.image])

        assert array.book_id == 1
        assert array.snippets == [self.text, self.image]

    def test_as_json(self):
        array = ArraySnip(book_id=1, snippets=[self.text, self.image])
        json_data = array.as_json(validate=False)

        assert json_data["book_id"] == 1
        assert json_data["type"] == "array"
        assert isinstance(json_data["data"], dict)
        assert json_data["data"]["snips"] == [self.text.as_json(), self.image.as_json()]
        assert json_data.get("view") == None
