import os

from contextlib import asynccontextmanager
from urllib.parse import urlparse

from decouple import AutoConfig
from miniopy_async import Minio

config = AutoConfig(search_path=os.getcwd())


class MinioInfra:
    __client: Minio | None = None

    @classmethod
    def __get_client(cls) -> Minio:
        if cls.__client is None:
            _bucket_url = urlparse(config("CLANDESTINO_BUCKET_CONNECTION_STRING"))
            _access_key: str | None = config(
                "CLANDESTINO_BUCKET_ACCESS_KEY", default=None
            )
            _secret_key: str | None = config(
                "CLANDESTINO_BUCKET_SECRET_KEY", default=None
            )
            cls.__client = Minio(
                _bucket_url.netloc,
                _access_key,
                _secret_key,
                secure=(_bucket_url.scheme == "https"),
            )
        return cls.__client

    @classmethod
    async def __close_client(cls) -> None:
        if cls.__client is not None:
            cls.__client = None

    @classmethod
    @asynccontextmanager
    async def get_client(cls) -> Minio:
        async_client = None
        try:
            async_client = cls.__get_client()
            yield async_client
        except Exception as e:
            print(f"{cls.__class__}::get_client")
            raise e
        finally:
            if async_client:
                await cls.__close_client()
