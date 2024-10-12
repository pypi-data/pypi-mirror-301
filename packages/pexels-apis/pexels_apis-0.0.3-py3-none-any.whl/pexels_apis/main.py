import requests
from .utils import search_filter, create_request

class PexelsAPI:
    """
        The Pexels API enables programmatic access to the full Pexels content library, including photos, videos. All content is available free of charge, and you are welcome to use Pexels content for anything you'd like, as long as it is within our Guidelines [https://www.pexels.com/api/documentation/#guidelines].
    """
    PHOTO_URL = "https://api.pexels.com/v1"
    VIDEO_URL = "https://api.pexels.com/videos"
    COLLECTION_URL = "https://api.pexels.com/v1/collections"
    HEADERS = { "Authorization" : "" }

    def __init__(self, apikey):
        """
            Set the default, like API KEY
        """
        self.apikey = apikey
        self.HEADERS["Authorization"] = apikey

    """
        The Photo resource is a JSON formatted version of a Pexels photo. The Photo API endpoints respond with the photo data formatted in this shape.
        Response
    """

    def search_photos(self, params):
        """
            Search photos
            GET https://api.pexels.com/v1/search
            This endpoint enables you to search Pexels for any topic that you would like. For example your query could be something broad like Nature, Tigers, People. Or it could be something specific like Group of people working.

            Parameters
            query string | required
            The search query. Ocean, Tigers, Pears, etc.

            orientation string | optional
            Desired photo orientation. The current supported orientations are: landscape, portrait or square.

            size string | optional
            Minimum photo size. The current supported sizes are: large(24MP), medium(12MP) or small(4MP).

            color string | optional
            Desired photo color. Supported colors: red, orange, yellow, green, turquoise, blue, violet, pink, brown, black, gray, white or any hexidecimal color code (eg. #ffffff).

            locale string | optional
            The locale of the search you are performing. The current supported locales are: 'en-US' 'pt-BR' 'es-ES' 'ca-ES' 'de-DE' 'it-IT' 'fr-FR' 'sv-SE' 'id-ID' 'pl-PL' 'ja-JP' 'zh-TW' 'zh-CN' 'ko-KR' 'th-TH' 'nl-NL' 'hu-HU' 'vi-VN' 'cs-CZ' 'da-DK' 'fi-FI' 'uk-UA' 'el-GR' 'ro-RO' 'nb-NO' 'sk-SK' 'tr-TR' 'ru-RU'.

            page integer | optional
            The page number you are requesting. Default: 1

            per_page integer | optional
            The number of results you are requesting per page. Default: 15 Max: 80

            Response
            photos array of Photo
            An array of Photo objects.

            page integer
            The current page number.

            per_page integer
            The number of results returned with each page.

            total_results integer
            The total number of results for the request.

            prev_page string | optional
            URL for the previous page of results, if applicable.

            next_page string | optional
            URL for the next page of results, if applicable.
        """
        if not isinstance(params, dict):
            return {"status": "error", "error": "invalid type, only dict {} is accepted"}
        query = params.get('query')
        if not query:
            return {"status": "error", "error": "query params cannot be empty"}
            
        filtered_params = search_filter(params)
        filtered_params["query"] = query
        response = create_request(self.PHOTO_URL+"/search", headers=self.HEADERS, params=filtered_params)
        return response

    def get_curated_photos(self, params):
        """
            Curated Photos
            GET https://api.pexels.com/v1/curated
            This endpoint enables you to receive real-time photos curated by the Pexels team.

            We add at least one new photo per hour to our curated list so that you always get a changing selection of trending photos.

            Parameters
            page integer | optional
            The page number you are requesting. Default: 1

            per_page integer | optional
            The number of results you are requesting per page. Default: 15 Max: 80

            Response
            photos array of Photo
            An array of Photo objects.

            page integer
            The current page number.

            per_page integer
            The number of results returned with each page.

            total_results integer
            The total number of results for the request.

            prev_page string | optional
            URL for the previous page of results, if applicable.

            next_page string | optional
            URL for the next page of results, if applicable.
        """
        if not isinstance(params, dict):
            return {"status": "error", "error": "invalid type, only dict {} is accepted"}
        filtered_params = search_filter(params)
        response = create_request(self.PHOTO_URL+"/curated", headers=self.HEADERS, params=filtered_params)
        return response

    def get_photo(self, id):
        """
            Get a Photo
            GET https://api.pexels.com/v1/photos/:id
            Retrieve a specific Photo from its id.

            Parameters
            id integer | required
            The id of the photo you are requesting.

            Response
            Returns a Photo object
        """
        if type(id)!=int:
            return {"status": "error", "error": "photo id must be an int. e.g 2014422"}
        response = create_request(self.PHOTO_URL+"/photos/"+str(id), headers=self.HEADERS)
        return response

    """
    The Video Resource
    The Video resource is a JSON formatted version of a Pexels video. The Video API endpoints respond with the video data formatted in this shape.
    """

    def search_videos(self, params):
        """
            Search for Videos
            GET https://api.pexels.com/videos/search
            This endpoint enables you to search Pexels for any topic that you would like. For example your query could be something broad like Nature, Tigers, People. Or it could be something specific like Group of people working.

            Parameters
            query string | required
            The search query. Ocean, Tigers, Pears, etc.

            orientation string | optional
            Desired video orientation. The current supported orientations are: landscape, portrait or square.

            size string | optional
            Minimum video size. The current supported sizes are: large(4K), medium(Full HD) or small(HD).

            locale string | optional
            The locale of the search you are performing. The current supported locales are: 'en-US' 'pt-BR' 'es-ES' 'ca-ES' 'de-DE' 'it-IT' 'fr-FR' 'sv-SE' 'id-ID' 'pl-PL' 'ja-JP' 'zh-TW' 'zh-CN' 'ko-KR' 'th-TH' 'nl-NL' 'hu-HU' 'vi-VN' 'cs-CZ' 'da-DK' 'fi-FI' 'uk-UA' 'el-GR' 'ro-RO' 'nb-NO' 'sk-SK' 'tr-TR' 'ru-RU'.

            page integer | optional
            The page number you are requesting. Default: 1

            per_page integer | optional
            The number of results you are requesting per page. Default: 15 Max: 80

            Response
            videos array of Video
            An array of Video objects.

            url string
            The Pexels URL for the current search query.

            page integer
            The current page number.

            per_page integer
            The number of results returned with each page.

            total_results integer
            The total number of results for the request.

            prev_page string | optional
            URL for the previous page of results, if applicable.

            next_page string | optional
            URL for the next page of results, if applicable.
        """
        if not isinstance(params, dict):
            return {"status": "error", "error": "invalid type, only dict {} is accepted"}
        query = params.get('query')
        if not query:
            return {"status": "error", "error": "query params cannot be empty"}
            
        filtered_params = search_filter(params)
        filtered_params["query"] = query
        response = create_request(self.VIDEO_URL+"/search", headers=self.HEADERS, params=filtered_params)
        return response


    def get_popular_videos(self, params):
        """
            Popular Videos
            GET https://api.pexels.com/videos/popular
            This endpoint enables you to receive the current popular Pexels videos.

            Parameters
            min_width integer | optional
            The minimum width in pixels of the returned videos.

            min_height integer | optional
            The minimum height in pixels of the returned videos.

            min_duration integer | optional
            The minimum duration in seconds of the returned videos.

            max_duration integer | optional
            The maximum duration in seconds of the returned videos.

            page integer | optional
            The page number you are requesting. Default: 1

            per_page integer | optional
            The number of results you are requesting per page. Default: 15 Max: 80

            Response
            videos array of Video
            An array of Video objects.

            url string
            The Pexels URL for the current page.

            page integer
            The current page number.

            per_page integer
            The number of results returned with each page.

            total_results integer
            The total number of results for the request.

            prev_page string | optional
            URL for the previous page of results, if applicable.

            next_page string | optional
            URL for the next page of results, if applicable.
        """
        if not isinstance(params, dict):
            return {"status": "error", "error": "invalid type, only dict {} is accepted"}
        filtered_params = search_filter(params)
        response = create_request(self.VIDEO_URL+"/popular", headers=self.HEADERS, params=filtered_params)
        return response
    
    def get_video(self, id):
        """
            Get a Video
            GET https://api.pexels.com/videos/videos/:id
            Retrieve a specific Video from its id.

            Parameters
            id integer | required
            The id of the video you are requesting.

            Response
            Returns a Video object
        """
        if not isinstance(id, int):
            return {"status": "error", "error": "video id must be an int. e.g 2014422"}
        response = create_request(self.VIDEO_URL+"/videos/"+str(id), headers=self.HEADERS)
        return response

    """
    Collections
    Pexels Collections are a way to group specific photos and videos into one unified gallery. This can be useful if, for example, you want to expose a specific subset of Pexels content to your users. You can access all your collections and the media within them via the Pexels API.

    Note: Collections cannot be created or modified using the Pexels API. Rather, you can manage your collections on the Pexels website, iOS or Android app. API only gives you access to featured collections and your own collections.
    """

    def get_featured_collections(self, params):
        """
            Featured Collections
            GET https://api.pexels.com/v1/collections/featured
            This endpoint returns all featured collections on Pexels.

            Parameters
            page integer | optional
            The page number you are requesting. Default: 1

            per_page integer | optional
            The number of results you are requesting per page. Default: 15 Max: 80

            Response
            collections array of Collection
            An array of Collection objects.

            page integer
            The current page number.

            per_page integer
            The number of results returned with each page.

            total_results integer
            The total number of results for the request.

            prev_page string | optional
            URL for the previous page of results, if applicable.

            next_page string | optional
            URL for the next page of results, if applicable.
        """
        if not isinstance(params, dict):
            return {"status": "error", "error": "invalid type, only dict {} is accepted"}
        filtered_params = search_filter(params)
        response = create_request(self.COLLECTION_URL+"/featured", headers=self.HEADERS, params=filtered_params)
        return response

    def get_my_collections(self, params):
        """
            My Collections
            GET https://api.pexels.com/v1/collections
            This endpoint returns all of your collections.

            Parameters
            page integer | optional
            The page number you are requesting. Default: 1

            per_page integer | optional
            The number of results you are requesting per page. Default: 15 Max: 80

            Response
            collections array of Collection
            An array of Collection objects.

            page integer
            The current page number.

            per_page integer
            The number of results returned with each page.

            total_results integer
            The total number of results for the request.

            prev_page string | optional
            URL for the previous page of results, if applicable.

            next_page string | optional
            URL for the next page of results, if applicable.
        """
        if not isinstance(params, dict):
            return {"status": "error", "error": "invalid type, only dict {} is accepted"}
        filtered_params = search_filter(params)
        response = create_request(self.COLLECTION_URL, headers=self.HEADERS, params=filtered_params)
        return response

    def get_collection_media(self, params):
        """
            Collection Media
            GET https://api.pexels.com/v1/collections/:id
            This endpoint returns all the media (photos and videos) within a single collection. You can filter to only receive photos or videos using the type parameter.

            Parameters
            type string | optional
            The type of media you are requesting. If not given or if given with an invalid value, all media will be returned. Supported values are photos and videos.

            sort string | optional
            The order of items in the media collection. Supported values are: asc, desc. Default: asc

            page integer | optional
            The page number you are requesting. Default: 1

            per_page integer | optional
            The number of results you are requesting per page. Default: 15 Max: 80

            Response
            id string
            The id of the collection you are requesting.

            media array of Photo or Video objects.
            An array of media objects. Each object has an extra type attribute to indicate the type of object.

            page integer
            The current page number.

            per_page integer
            The number of results returned with each page.

            total_results integer
            The total number of results for the request.

            prev_page string | optional
            URL for the previous page of results, if applicable.

            next_page string | optional
            URL for the next page of results, if applicable.
        """
        if not isinstance(params, dict):
            return {"status": "error", "error": "invalid type, only dict {} is accepted"}
        filtered_params = search_filter(params)
        response = create_request(self.COLLECTION_URL+"/featured", headers=self.HEADERS, params=filtered_params)
        return response
