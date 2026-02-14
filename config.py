from dynaconf import Dynaconf
import os

settings = Dynaconf(
    settings_files=[os.path.join(os.path.dirname(__file__), "settings.toml")],
    environments=True,   # important to use [dev]
    env_switcher="ENV_FOR_DYNACONF",
    load_dotenv=True,
    envvar_prefix="HRMS"
)
