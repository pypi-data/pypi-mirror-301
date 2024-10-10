# Auth Exceptions
class ImproperProfileSetupException(Exception):
    pass


class MissingSharedCredentialsFileException(Exception):
    pass


class ProfileAlreadyExistsException(Exception):
    pass


class ProfileDoesNotExistException(Exception):
    pass


# Model Registry Exceptions
class GoogleModelGardenApiException(Exception):
    pass


class ModelDeletionException(Exception):
    pass


class ModelPublishingException(Exception):
    pass


class ModelRetrievalException(Exception):
    pass


class UnsupportedModelProviderException(Exception):
    pass
