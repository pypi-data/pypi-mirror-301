import io

from .infra import MinioInfra

from clandestino_interfaces import IMigrateRepository


class MinIOMigrateRepository(IMigrateRepository, MinioInfra):

    @classmethod
    def get_control_bucket(cls):
        return "clandestino"

    @classmethod
    async def create_control_table(cls) -> None:
        control_bucket = cls.get_control_bucket()
        async with cls.get_client() as client:
            await client.make_bucket(control_bucket)

    @classmethod
    async def control_table_exists(cls) -> bool:
        control_bucket = cls.get_control_bucket()
        async with cls.get_client() as client:
            exits = await client.bucket_exists(control_bucket)
            return bool(exits)

    @classmethod
    async def register_migration_execution(cls, migration_name: str) -> None:
        control_bucket = cls.get_control_bucket()
        async with cls.get_client() as client:
            await client.put_object(
                control_bucket,
                migration_name,
                io.BytesIO(b"1"),
                1,
            )

    @classmethod
    async def remove_migration_execution(cls, migration_name: str) -> None:
        control_bucket = cls.get_control_bucket()
        async with cls.get_client() as client:
            await client.remove_object(control_bucket, migration_name)

    @classmethod
    async def migration_already_executed(cls, migration_name: str) -> bool:
        control_bucket = cls.get_control_bucket()
        async with cls.get_client() as client:
            try:
                await client.stat_object(control_bucket, migration_name)
                return True
            except Exception:
                return False
