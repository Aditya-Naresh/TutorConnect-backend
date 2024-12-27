from storages.backends.azure_storage import AzureStorage
import os
import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


class CustomAzureStaticStorage(AzureStorage):
    account_name = "tutorconnectstorage"
    account_key = env("AZURE_KEY")
    azure_container = os.getenv("AZURE_STATIC_CONTAINER", "static")
    expiration_secs = None


class CustomAzureMediaStorage(AzureStorage):
    account_name = "tutorconnectstorage"
    account_key = env("AZURE_KEY")
    azure_container = os.getenv("AZURE_MEDIA_CONTAINER", "media")
    expiration_secs = None
