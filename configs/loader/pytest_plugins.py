from pathlib import Path
from configs.loader.fixtures import FixtureLoader


ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def get_pytest_plugins(service_name: str | list[str]) -> list[str]:
    fixtures = FixtureLoader().get_fixtures(service_name)

    module_paths = []
    for p in fixtures:
        path = Path(p).with_suffix("")
        rel = path.relative_to(ROOT_DIR)
        module_paths.append(".".join(rel.parts))
    return module_paths
