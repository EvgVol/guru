from pathlib import Path
from typing import List


class FixtureLoader:
    def __init__(self, base_dir: str = "fixtures"):
        self.base_dir = (
            Path(__file__).resolve().parent.parent.parent / base_dir
        )

    def get_fixtures(self, service_name: str | list[str] | None) -> List[str]:
        """
        Загружает фикстуры для указанного сервиса.
        """
        fixtures = []

        common_path = self.base_dir / "common"
        if common_path.exists():
            for file in common_path.glob("*.py"):
                if file.name != "__init__.py":
                    fixtures.append(file)

        if service_name:
            if isinstance(service_name, str):
                service_name = [service_name]
            for svc in service_name:
                svc_path = self.base_dir / svc
                if svc_path.exists():
                    for file in svc_path.glob("*.py"):
                        if file.name != "__init__.py":
                            fixtures.append(file)

        return fixtures
