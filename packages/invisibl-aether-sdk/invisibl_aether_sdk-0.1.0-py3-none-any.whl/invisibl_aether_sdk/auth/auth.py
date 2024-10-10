import configparser
import os
from pathlib import Path

from dotenv import load_dotenv

from ..exceptions import (
    ImproperProfileSetupException,
    MissingSharedCredentialsFileException,
    ProfileAlreadyExistsException,
    ProfileDoesNotExistException,
)

load_dotenv(override=True)


class Auth:
    def __init__(self) -> None:
        pass

    @staticmethod
    def setup(
        user_id: str,
        api_key: str,
        profile: str = "default",
        overwrite_if_exists: bool = False,
    ) -> None:
        """Create a shared credentials if it doesn't exist, and set up a new profile.

        Args
        ----
        user_id: str
            The user ID to use for this profile.
        api_key: str
            The API key given to the user for this profile.
        profile: str (optional, default `"default"`)
            The name of profile to set up.
        overwrite_if_exists: bool (optional, default `False`)
            Whether or not to overwrite an existing profile if it had previously been
            set up.
        """

        shared_credentials_file_location = Path(
            os.environ.get(
                "AETHER_SHARED_CREDENTIALS_FILE", Path.home() / ".aether/credentials"
            )
        )
        credentials_parser = configparser.ConfigParser()

        if shared_credentials_file_location.exists():
            credentials_parser.read(shared_credentials_file_location)
            if profile in credentials_parser and not overwrite_if_exists:
                raise ProfileAlreadyExistsException(
                    f"Profile `{profile}` already exists. If you want to overwrite its "
                    "value, set `overwrite_if_exists` to `True`."
                )
        else:
            shared_credentials_file_location.parent.mkdir(parents=True)

        credentials_parser[profile] = {"user_id": user_id, "api_key": api_key}
        with open(shared_credentials_file_location, "w", encoding="utf-8") as f:
            credentials_parser.write(f)

    @staticmethod
    def get_authenticated_ids(profile: str = "default") -> dict[str, str]:
        """Retrieve the user ID and API key for a profile.

        Args
        ----
        profile: str
            The name of the profile whose credentials are to be retrieved.

        Returns
        -------
        credentials: dict
            A dictionary with the keys `"user_id"` and `"api_key"`.
        """

        user_id, api_key = None, None
        if os.environ.get("AETHER_USER_ID"):
            user_id = os.environ.get("AETHER_USER_ID")
        if os.environ.get("AETHER_API_KEY"):
            api_key = os.environ.get("AETHER_API_KEY")

        if user_id is None or api_key is None:
            shared_credentials_file_location = Path(
                os.environ.get(
                    "AETHER_SHARED_CREDENTIALS_FILE",
                    Path.home() / ".aether/credentials",
                )
            )
            if not shared_credentials_file_location.exists():
                raise MissingSharedCredentialsFileException(
                    "The shared credentials file is missing. Run `Auth.setup` first."
                )

            credentials_parser = configparser.ConfigParser()
            credentials_parser.read(shared_credentials_file_location)

            if profile not in credentials_parser:
                raise ProfileDoesNotExistException(
                    f"Profile `{profile}` doesn't exist. Run `Auth.setup` for this "
                    "profile, or select a different one."
                )

            if user_id is None:
                user_id = credentials_parser[profile].get("user_id")
            if api_key is None:
                api_key = credentials_parser[profile].get("api_key")
            if not (user_id and api_key):
                raise ImproperProfileSetupException(
                    f"One of `user_id` and `api_key` is missing for profile "
                    f"`{profile}`. Please re-run `Auth.setup` with "
                    "`overwrite_if_exists=True`."
                )

        return {"user_id": user_id, "api_key": api_key}
