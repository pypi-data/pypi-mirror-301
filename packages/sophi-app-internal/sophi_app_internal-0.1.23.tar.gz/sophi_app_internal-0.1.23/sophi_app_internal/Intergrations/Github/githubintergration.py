import os
import time
import logging
import requests
import jwt
from github import Github, Auth
from sophi_app_internal.Security.base_64_private_key import base_64_private_key

GITHUB_APP_SLUG = os.getenv('GITHUB_APP_SLUG')
GITHUB_APP_ID = os.getenv('GITHUB_APP_ID')
PRIVATE_KEY = os.getenv('GITHUB_PRIVATE_KEY')

class GithubIntergration:

    def __init__(self, token, expiration_time, installation_id):
        self.app_id = GITHUB_APP_ID
        self.private_key = base_64_private_key.base64_to_private_key_pem_string(PRIVATE_KEY)
        self.installation_id = installation_id
        self.access_token = token
        self.token_expiration = time.mktime(time.strptime(expiration_time, "%Y-%m-%dT%H:%M:%SZ"))
        self.auth = Auth.Token(token)
        self.github = Github(auth=self.auth)

    def create_jwt(self):
        payload = {
            'iat': int(time.time()),  # Issued at time
            'exp': int(time.time()) + (10 * 60),  # Expiration time (max 10 minutes)
            'iss': self.app_id  # GitHub App ID
        }

        token = jwt.encode(payload, self.private_key, algorithm='RS256')
        return token

    def refresh_access_token(self):
        """
        Refreshes the installation access token.
        """
        logging.info("Refreshing access token...")

        jwt_token = self.create_jwt()

        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github+json'
        }
        url = f'https://api.github.com/app/installations/{self.installation_id}/access_tokens'

        response = requests.post(url, headers=headers)

        if response.status_code == 201:
            token_data = response.json()
            self.access_token = token_data['token']

            expires_at_str = token_data['expires_at']
            self.token_expiration = time.mktime(time.strptime(expires_at_str, "%Y-%m-%dT%H:%M:%SZ"))

            # To-Do: Save the new token and expiration time to the database

            self.github = Github(self.access_token)
            logging.info(f"Access token refreshed. Expires at: {expires_at_str}")
        else:
            logging.error(f"Failed to refresh access token: {response.status_code} - {response.text}")

    def check_token(func):
        """
        Decorator to check if the token is expired.
        """
        def wrapper(self, *args, **kwargs):
            if time.time() > self.token_expiration:
                self.refresh_access_token()
            return func(self, *args, **kwargs)

        return wrapper

    @check_token
    def get_all_download_raw_urls(self, repo, path=''):
        """
        Fetches all the raw download URLs for files in a repository.

        Parameters:
        - repo: The repository object.

        Returns:
        - A list of raw download URLs if successful.
        - None if the request fails.
        """

        raw_urls = []
        repo = self.github.get_repo(repo)
        contents = repo.get_contents(path)

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                raw_urls.append(file_content.download_url)

        self.close()
        return raw_urls

    @check_token
    def get_selected_repositories(self):
        """
        Fetches the list of repositories that the user selected during the GitHub App installation.

        Parameters:
        - access_token: The installation access token (string).

        Returns:
        - A list of repository information (full_name, private status) if successful.
        - None if the request fails.
        """
        # Set up the headers with the access token
        headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github+json'
        }

        # Make the request to GitHub to get the repositories the app can access
        response = requests.get('https://api.github.com/installation/repositories', headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            repositories = data.get('repositories', [])
            repo_list = [repo['full_name'] for repo in repositories]
            return repo_list
        else:
            logging.error(f"Failed to fetch repositories: {response.status_code} - {response.text}")
            return None

    @check_token
    def should_throttle(self):
        """
        Checks if the rate limit is approaching and prints a warning if so.

        Returns:
        - True if the rate limit is approaching, along with the reset time.
        - False otherwise, along with None.
        """

        rate_limit = self.github.get_rate_limit()

        if rate_limit.core.remaining < 100:
            reset_time = rate_limit.core.reset.timestamp() - time.time()
            logging.warning(f"Warning: Approaching rate limit. {rate_limit.core.remaining} calls remaining.")
            logging.warning(f"Rate limit will reset in {reset_time:.2f} seconds.")
            return True, rate_limit.core.reset.timestamp()

        return False, None

    def get_file_name(self, url):
        """
        Extracts the file name from a URL.
        Args:
            url: The URL of the file fetched from the GitHub API.

        Returns:
            The file name.
        """
        return url.split("/")[-1]

    def download_file(self, download_url):
        """
        Downloads a file from a URL.

        Args:
            download_url: The URL of the file to download.

        Returns:
            The content of the file.
        """

        response = requests.get(download_url)
        response.raise_for_status()
        return response.content

    def close(self):
        """
        Closes the GitHub client.
        """
        self.github.close()