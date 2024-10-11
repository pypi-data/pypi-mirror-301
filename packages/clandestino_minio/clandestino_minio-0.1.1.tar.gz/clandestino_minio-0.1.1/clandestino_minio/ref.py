from clandestino_interfaces import AbstractMigration
from clandestino_minio.infra import MinioInfra


class Migration(AbstractMigration):

    infra = MinioInfra()

    async def up(self) -> None:
        """Do modifications in database"""
        pass

    async def down(self) -> None:
        """Undo modifications in database"""
        pass
