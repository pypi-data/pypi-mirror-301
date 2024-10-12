import unittest
from unittest.mock import patch, Mock
from dappier.dappier import DappierApp


class TestDappierApp(unittest.TestCase):

    @patch("requests.Session.post")
    def test_realtime_search_api(self, mock_post):
        # Mock response for the POST request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"response": {"results": "Election Day is November 5, 2024"}}
        ]
        mock_post.return_value = mock_response

        client = DappierApp(api_key="mock-api-key")
        result = client.realtime_search_api("when is election in USA")

        self.assertEqual(result.response["response"]["results"], "Election Day is November 5, 2024")

    @patch("requests.Session.post")
    def test_ai_recommendations(self, mock_post):
        # Mock response for the POST request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "author": "Test Author",
                    "image_url": "https://example.com/test.jpg",
                    "preview_content": "Test content",
                    "pubdate": "Tue, 10 Sep 2024 18:24:27 +0000",
                    "pubdate_unix": 1725992667,
                    "score": 0.75,
                    "site": "Test Site",
                    "site_domain": "testsite.com",
                    "title": "Test Title",
                    "url": "https://example.com/test",
                }
            ]
        }
        mock_post.return_value = mock_response

        client = DappierApp(api_key="mock-api-key")
        result = client.ai_recommendations(
            "latest tech news", "dm_02hr75e8ate6adr15hjrf3ikol", similarity_top_k=5, ref="techcrunch.com"
        )

        self.assertEqual(result.results["results"][0]["title"], "Test Title")

    def test_empty_query_realtime(self):
        client = DappierApp(api_key="mock-api-key")
        with self.assertRaises(ValueError):
            client.realtime_search_api("")

    def test_empty_query_ai_recommendations(self):
        client = DappierApp(api_key="mock-api-key")
        with self.assertRaises(ValueError):
            client.ai_recommendations("", "dm_02hr75e8ate6adr15hjrf3ikol")


if __name__ == "__main__":
    unittest.main()
