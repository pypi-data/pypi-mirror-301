import pytest
from unittest.mock import patch, MagicMock
from pexels_apis import PexelsAPI

test_api_key = 'iasjjas'

@pytest.fixture
def pexels_api():
    return PexelsAPI(test_api_key)

def test_init(pexels_api):
    assert pexels_api.apikey == test_api_key
    assert pexels_api.HEADERS["Authorization"] == test_api_key

def test_search_photos(pexels_api):    
    result = pexels_api.search_photos({"query": "nature"})    
    assert result.get("status") == "success"


def test_get_curated_photos(pexels_api):
    result = pexels_api.get_curated_photos({"page": 1, "per_page": 5})
    assert result.get("status") == "success"



def test_get_photo(pexels_api):
    result = pexels_api.get_photo(13032608)
    assert result.get("status") == "success"



def test_search_videos(pexels_api):
    result = pexels_api.search_videos({"query": "nature"})
    assert result.get("status") == "success"


def test_get_popular_videos(pexels_api):
    result = pexels_api.get_popular_videos({"page": 1, "per_page": 15})
    assert result.get("status") == "success"


def test_get_video(pexels_api):
    result = pexels_api.get_video(27877597)
    assert result.get("status") == "success"


def test_get_featured_collections(pexels_api):
    result = pexels_api.get_featured_collections({"page": 1, "per_page": 15})
    assert result.get("status") == "success"
    


def test_get_my_collections(pexels_api):
    result = pexels_api.get_my_collections({"page": 1, "per_page": 15})
    assert result.get("status") == "success"



def test_get_collection_media(pexels_api):
    result = pexels_api.get_collection_media({"type": "photos", "page": 1, "per_page": 15})
    assert result.get("status") == "success"