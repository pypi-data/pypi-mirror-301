import hashlib
from abc import ABC
from enum import Enum
from typing import Optional, Union

from practicuscore import get_logger, Log
from practicuscore.util import CryptoUtil


class K8sAuthToken:
    def __init__(self, refresh_token: str, access_token: str, username: str | None = None) -> None:
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.username = username


class K8sClusterDefinition:
    name: str = ""
    region_name: str = ""


class K8sConfig:
    def __init__(
            self,
            host_url: str,
            email: str | None = None,
            refresh_token: str | None = None,
            username: str | None = None,
            access_token: str | None = None,
    ):
        super().__init__()
        if host_url.endswith("/"):
            host_url = host_url[:-1]
        self.host_url: str = host_url
        self.email: str | None = email
        self.refresh_token: str | None = refresh_token
        self.password: str | None = None
        self.cluster_name: str | None = None
        self.region_name: str | None = None
        self._username: str | None = username
        self.access_token: str | None = access_token

    def to_dict(self) -> dict:
        conf_dict = {
            'host_url': self.host_url
        }

        if self.email:
            conf_dict['email'] = self.email

        if self.username:
            conf_dict['username'] = self.username

        if self.password is not None:
            conf_dict['password'] = self.password

        if self.refresh_token is not None:
            conf_dict['refresh_token'] = self.refresh_token

        if self.cluster_name is not None:
            conf_dict['cluster_name'] = self.cluster_name

        if self.region_name is not None:
            conf_dict['region_name'] = self.region_name

        # Note: we never save access token and serialize it since it's short lived
        # if self.access_token is not None:
        #     conf_dict['access_token'] = self.access_token

        return conf_dict

    @staticmethod
    def from_dict(dict_item: dict) -> 'K8sConfig':
        username = dict_item['username'] if 'username' in dict_item else None
        k8s_config = K8sConfig(
            host_url=dict_item['host_url'], email=dict_item['email'], refresh_token=dict_item['refresh_token'],
            username=username)
        if 'password' in dict_item:
            k8s_config.password = dict_item['password']
        if 'cluster_name' in dict_item:
            k8s_config.cluster_name = dict_item['cluster_name']
        if 'region_name' in dict_item:
            k8s_config.region_name = dict_item['region_name']
        return k8s_config

    def set_password(self, password_plain_text: str):
        self.password = CryptoUtil.encrypt(password_plain_text)

    @property
    def password_in_plain_text(self) -> str | None:
        if self.password:
            return CryptoUtil.decrypt(self.password)
        else:
            return None

    @property
    def ssl(self) -> bool:
        return self.host_url.startswith("https")

    @property
    def host_dns(self) -> str:
        return self.host_url.replace("https://", "").replace("http://", "")

    @property
    def hash_text(self) -> str:
        return f"{self.host_url}-{self.email}-{self.refresh_token}-{self.password}"

    @property
    def hash_key(self) -> str:
        m = hashlib.md5()
        m.update(bytes(self.hash_text, "utf-8"))
        return str(m.hexdigest())

    @property
    def username(self) -> str:
        try:
            if self._username:
                return self._username
            elif self.email:
                return self.email.split("@")[0]
        except Exception as e:
            print(f"ERROR: Could not get user name from email of k8s region. Err: {e}")
        return "practicus_ai"

    @property
    def key(self) -> str:
        return f"{self.username}@{self.host_dns}"


class ModelPrefix:
    logger = get_logger(Log.SDK)

    def __init__(self, key: str, prefix: str) -> None:
        super().__init__()
        self.key = key
        self.prefix = prefix

    def get_csv_header(self) -> str:
        # Updating? change __str__()
        return "key,prefix"

    def __str__(self):
        # Updating? change get_csv_header()
        return f"{self.key},{self.prefix}".replace("\n", " ").replace("\r", " ")

    def __repr__(self):
        header_items = self.get_csv_header().split(",")
        row_items = str(self).split(",")
        final_items: list[str] = []
        if len(header_items) == len(row_items):
            for i in range(len(header_items)):
                final_items.append(f"{header_items[i]}: {row_items[i]}")
            return "\n".join(final_items)
        else:
            self.logger.warning(
                "Header items do not match string items for ModelPrefix. Will return a simpler representation.")
            return str(self)


class AppPrefix:
    logger = get_logger(Log.SDK)

    def __init__(
            self,
            key: str,
            prefix: str,
            visible_name: str = "",
            description: str = "",
            icon: str = "",
            sort_order: int | None = None,
            has_extra_conf: bool | None = False,
            has_extra_secret: bool | None = False,
    ) -> None:
        super().__init__()
        self.key = key
        self.prefix = prefix
        self.visible_name = visible_name
        self.description = description
        self.icon = icon
        self.sort_order = sort_order
        self.has_extra_conf: bool = has_extra_conf if has_extra_conf else False
        self.has_extra_secret: bool = has_extra_secret if has_extra_secret else False

    def get_csv_header(self) -> str:
        # Updating? change __str__()
        return "key,prefix,visible_name,description,icon,sort_order,has_extra_conf,has_extra_secret"

    def __str__(self):
        # Updating? change get_csv_header()
        visible_name = self.visible_name
        if visible_name:
            visible_name = visible_name.replace(",", " ")
        description = self.description
        if description:
            description = description.replace(",", " ")
        icon = self.icon
        if icon:
            icon = icon.replace(",", " ")
        sort_order = self.sort_order if self.sort_order is not None else ""
        return (f"{self.key},{self.prefix},{visible_name},{description},{icon},{sort_order},{self.has_extra_conf},{self.has_extra_secret}"
                f"").replace("\n", " ").replace("\r", " ")

    def __repr__(self):
        header_items = self.get_csv_header().split(",")
        row_items = str(self).split(",")
        final_items: list[str] = []
        if len(header_items) == len(row_items):
            for i in range(len(header_items)):
                final_items.append(f"{header_items[i]}: {row_items[i]}")
            return "\n".join(final_items)
        else:
            self.logger.warning(
                "Header items do not match string items for AppPrefix. Will return a simpler representation.")
            return str(self)


class ModelDeployment:
    logger = get_logger(Log.SDK)

    def __init__(
            self, key: str, name: str, worker_type: str = "", scaling: str = "",
            startup_script: bool = False, custom_image: str = "",
    ) -> None:
        super().__init__()
        self.key = key
        self.name = name
        self.worker_type = worker_type
        self.scaling = scaling
        self.startup_script = startup_script
        self.custom_image = custom_image

    def get_csv_header(self) -> str:
        # Updating? change __str__()
        return "key,name,worker_type,scaling,startup_script,custom_image"

    def __str__(self):
        # Updating? change get_csv_header()
        name = self.name
        if name:
            name = name.replace(",", " ")
        worker_type = self.worker_type
        if worker_type:
            worker_type = worker_type.replace(",", " ")
        scaling = self.scaling
        if scaling:
            scaling = scaling.replace(",", " ")
        custom_image = self.custom_image
        if custom_image:
            custom_image = custom_image.replace(",", " ")
        return f"{self.key},{name},{worker_type},{scaling},{self.startup_script},{custom_image}".replace("\n", " ").replace("\r", " ")

    def __repr__(self):
        header_items = self.get_csv_header().split(",")
        row_items = str(self).split(",")
        final_items: list[str] = []
        if len(header_items) == len(row_items):
            for i in range(len(header_items)):
                final_items.append(f"{header_items[i]}: {row_items[i]}")
            return "\n".join(final_items)
        else:
            self.logger.warning(
                "Header items do not match string items for ModelDeployment. Will return a simpler representation.")
            return str(self)


class AppDeploymentSetting:
    logger = get_logger(Log.SDK)

    def __init__(
            self, key: str, name: str, worker_type: str = "", scaling: str = "",
            startup_script: bool = False, custom_image: str = "",
    ) -> None:
        super().__init__()
        self.key = key
        self.name = name
        self.worker_type = worker_type
        self.scaling = scaling
        self.startup_script = startup_script
        self.custom_image = custom_image

    def get_csv_header(self) -> str:
        # Updating? change __str__()
        return "key,name,worker_type,scaling,startup_script,custom_image"

    def __str__(self):
        # Updating? change get_csv_header()
        name = self.name
        if name:
            name = name.replace(",", " ")
        worker_type = self.worker_type
        if worker_type:
            worker_type = worker_type.replace(",", " ")
        scaling = self.scaling
        if scaling:
            scaling = scaling.replace(",", " ")
        custom_image = self.custom_image
        if custom_image:
            custom_image = custom_image.replace(",", " ")
        return f"{self.key},{name},{worker_type},{scaling},{self.startup_script},{custom_image}".replace("\n", " ").replace("\r", " ")

    def __repr__(self):
        header_items = self.get_csv_header().split(",")
        row_items = str(self).split(",")
        final_items: list[str] = []
        if len(header_items) == len(row_items):
            for i in range(len(header_items)):
                final_items.append(f"{header_items[i]}: {row_items[i]}")
            return "\n".join(final_items)
        else:
            self.logger.warning(
                "Header items do not match string items for AppDeploymentSetting. Will return a simpler representation.")
            return str(self)


class AppVersionInfo:
    def __init__(self, version_tag: str, version: str | None = None):
        self.version_tag = version_tag
        self.version = version

    @staticmethod
    def create_from_version(version: str) -> 'AppVersionInfo':
        return AppVersionInfo(version_tag=f"v{version}", version=version)

    @staticmethod
    def create_latest() -> 'AppVersionInfo':
        return AppVersionInfo(version_tag="latest")

    @staticmethod
    def create_production() -> 'AppVersionInfo':
        return AppVersionInfo(version_tag="production")

    @staticmethod
    def create_staging() -> 'AppVersionInfo':
        return AppVersionInfo(version_tag="staging")


class ModelVersionInfo:
    def __init__(self, version_tag: str, version: str | None = None):
        self.version_tag = version_tag
        self.version = version

    @staticmethod
    def create_from_version(version: str) -> 'ModelVersionInfo':
        return ModelVersionInfo(version_tag=f"v{version}", version=version)

    @staticmethod
    def create_latest() -> 'ModelVersionInfo':
        return ModelVersionInfo(version_tag="latest")

    @staticmethod
    def create_production() -> 'ModelVersionInfo':
        return ModelVersionInfo(version_tag="production")

    @staticmethod
    def create_staging() -> 'ModelVersionInfo':
        return ModelVersionInfo(version_tag="staging")


class ModelMetaVersion:
    def __init__(self, version_id: int, version: str, model_deployment: ModelDeployment, stage: str | None = None) -> None:
        super().__init__()
        self.id = version_id
        self.version = version
        self.stage = stage
        self.model_deployment = model_deployment

    def to_model_version_info(self) -> ModelVersionInfo:
        return ModelVersionInfo.create_from_version(self.version)


class AppMetaVersion:
    def __init__(self, version_id: int, version: str, app_deployment_setting: AppDeploymentSetting, stage: str | None = None) -> None:
        super().__init__()
        self.id = version_id
        self.version = version
        self.stage = stage
        self.app_deployment_setting = app_deployment_setting

    def to_app_version_info(self) -> ModelVersionInfo:
        return ModelVersionInfo.create_from_version(self.version)


class ModelMeta:
    logger = get_logger(Log.SDK)

    def __init__(
            self, model_id: int, name: str, model_prefix: ModelPrefix, model_versions: list[ModelMetaVersion]) -> None:
        super().__init__()
        self.model_id = model_id
        self.name = name
        self.model_prefix = model_prefix
        self.model_versions = model_versions

    @property
    def production_version(self) -> Optional[ModelMetaVersion]:
        for model_meta_version in self.model_versions:
            if model_meta_version.stage and model_meta_version.stage.lower().startswith("prod"):
                return model_meta_version
        return None

    @property
    def staging_version(self) -> Optional[ModelMetaVersion]:
        for model_meta_version in self.model_versions:
            if model_meta_version.stage and model_meta_version.stage.lower() == "staging":
                return model_meta_version
        return None

    def get_csv_header(self) -> str:
        # Updating? change __str__()
        return "model_id,name,prefix,versions"

    def __str__(self):
        # Updating? change get_csv_header()
        model_versions_summary = ""
        for i in range(len(self.model_versions)):
            model_version = self.model_versions[i]
            if model_version.stage is not None:
                stage = f" ({model_version.stage})"
            else:
                stage = ""
            model_versions_summary += f"{model_version.version}{stage}"
            if i + 1 < len(self.model_versions):
                model_versions_summary += " / "

        return f"{self.model_id},{self.name},{self.model_prefix.prefix},{model_versions_summary.strip()}".replace("\n", " ").replace("\r", " ")

    def __repr__(self):
        header_items = self.get_csv_header().split(",")
        row_items = str(self).split(",")
        final_items: list[str] = []
        if len(header_items) == len(row_items):
            for i in range(len(header_items)):
                final_items.append(f"{header_items[i]}: {row_items[i]}")
            return "\n".join(final_items)
        else:
            self.logger.warning(
                "Header items do not match string items for ModelMeta. Will return a simpler representation.")
            return str(self)


class AppMeta:
    logger = get_logger(Log.SDK)

    def __init__(
            self,
            app_id: int,
            name: str,
            app_prefix: AppPrefix,
            app_versions: list[AppMetaVersion],
            visible_name: str = "",
            description: str = "",
            owner_email: str = "",
            icon: str = "",
            sort_order: int | None = None,
            has_extra_conf: bool | None = False,
            has_extra_secret: bool | None = False,
    ) -> None:
        super().__init__()
        self.app_id = app_id
        self.name = name
        self.app_prefix = app_prefix
        self.app_versions = app_versions
        self.visible_name = visible_name
        self.description = description
        self.owner_email = owner_email
        self.icon = icon
        self.sort_order = sort_order
        self.has_extra_conf: bool = has_extra_conf if has_extra_conf else False
        self.has_extra_secret: bool = has_extra_secret if has_extra_secret else False

    @property
    def production_version(self) -> Optional[AppMetaVersion]:
        for app_meta_version in self.app_versions:
            if app_meta_version.stage and app_meta_version.stage.lower().startswith("prod"):
                return app_meta_version
        return None

    @property
    def staging_version(self) -> Optional[AppMetaVersion]:
        for app_meta_version in self.app_versions:
            if app_meta_version.stage and app_meta_version.stage.lower() == "staging":
                return app_meta_version
        return None

    def get_csv_header(self) -> str:
        # Updating? change __str__()
        return "app_id,name,prefix,versions,visible_name,description,owner_email,icon,sort_order,has_extra_conf,has_extra_secret"

    def __str__(self):
        # Updating? change get_csv_header()
        app_versions_summary = ""
        for i in range(len(self.app_versions)):
            app_version = self.app_versions[i]
            if app_version.stage is not None:
                stage = f" ({app_version.stage})"
            else:
                stage = ""
            app_versions_summary += f"{app_version.version}{stage}"
            if i + 1 < len(self.app_versions):
                app_versions_summary += " / "
        visible_name = self.visible_name
        if visible_name:
            visible_name = visible_name.replace(",", " ")
        description = self.description if self.description else ""
        if description:
            description = description.replace(",", " ")
        icon = self.icon
        if icon:
            icon = icon.replace(",", " ")
        sort_order = self.sort_order if self.sort_order is not None else ""

        return (f"{self.app_id},{self.name},{self.app_prefix.prefix},{app_versions_summary.strip()},{visible_name},"
                f"{description},{self.owner_email},{icon},{sort_order},{self.has_extra_conf},{self.has_extra_secret}"
                f"").replace("\n", " ").replace("\r", " ")

    def __repr__(self):
        header_items = self.get_csv_header().split(",")
        row_items = str(self).split(",")
        final_items: list[str] = []
        if len(header_items) == len(row_items):
            for i in range(len(header_items)):
                final_items.append(f"{header_items[i]}: {row_items[i]}")
            return "\n".join(final_items)
        else:
            self.logger.warning(
                "Header items do not match string items for AppMeta. Will return a simpler representation.")
            return str(self)


class ExternalServiceType(str, Enum):
    AIRFLOW = "AIRFLOW"
    MLFLOW = "MLFLOW"
    JUPYTER_LAB = "JUPYTER_LAB"
    SPARKUI = "SPARKUI"
    STREAMLIT = "STREAMLIT"
    VSCODE = "VSCODE"
    GRAFANA = "GRAFANA"
    SUPERSET = "SUPERSET"
    TRINO = "TRINO"

    @classmethod
    def from_value(cls, value: Union[str, Enum]) -> 'ExternalServiceType':
        str_val = str(value.value if hasattr(value, "value") else value).upper()
        for i, enum_val in enumerate(cls):
            # noinspection PyUnresolvedReferences
            if str(enum_val.value).upper() == str_val:
                return cls(enum_val)

        raise ValueError(f'{value} is not a valid {cls}')


# Pages that use hardware acceleration can fail on Chrome + K8s workspace
# Sample test site: https://webglsamples.org/blob/blob.html
# https://bugs.chromium.org/p/chromium/issues/detail?id=1506249#c2
KNOWN_COMPLEX_WEB_SERVICES = [ExternalServiceType.JUPYTER_LAB]


class ExternalService(ABC):
    def __init__(
            self, key: str, name: str, service_type: ExternalServiceType, url: str | None = None,
            oauth_key: str | None = None, db_key: str | None = None, obj_key: str | None = None,
            git_key: str | None = None, configuration: dict | None = None,
    ) -> None:
        self.key: str = key
        self.name: str = name
        self.service_type: ExternalServiceType = service_type
        self.url: str | None = url
        self.oauth_key: str | None = oauth_key
        self.db_key: str | None = db_key
        self.obj_key: str | None = obj_key
        self.git_key: str | None = git_key
        self.configuration: dict = configuration if configuration is not None else {}


class WorkflowService(ExternalService):
    MY_SVC_TYPE = ExternalServiceType.AIRFLOW

    def __init__(
            self, key: str, name: str, url: str | None = None,
            oauth_key: str | None = None, db_key: str | None = None, obj_key: str | None = None,
            git_key: str | None = None, configuration: dict | None = None,
    ) -> None:
        super().__init__(
            key=key, name=name, service_type=self.MY_SVC_TYPE, url=url, oauth_key=oauth_key,
            db_key=db_key, obj_key=obj_key, git_key=git_key, configuration=configuration)

        assert self.url, f"url must be defined for {type(self)}. key: {key}, name: {name}"
        assert self.git_key, f"git_key must be defined for {type(self)}. key: {key}, name: {name}"


class ExperimentService(ExternalService):
    MY_SVC_TYPE = ExternalServiceType.MLFLOW

    def __init__(
            self, key: str, name: str, url: str | None = None,
            oauth_key: str | None = None, db_key: str | None = None, obj_key: str | None = None,
            git_key: str | None = None, configuration: dict | None = None,
    ) -> None:
        super().__init__(
            key=key, name=name, service_type=self.MY_SVC_TYPE, url=url, oauth_key=oauth_key,
            db_key=db_key, obj_key=obj_key, git_key=git_key, configuration=configuration)

        assert self.url, f"url must be defined for {type(self)}. key: {key}, name: {name}"


class ObservabilityService(ExternalService):
    MY_SVC_TYPE = ExternalServiceType.GRAFANA

    def __init__(
            self, key: str, name: str, url: str | None = None,
            oauth_key: str | None = None, db_key: str | None = None, obj_key: str | None = None,
            git_key: str | None = None, configuration: dict | None = None,
    ) -> None:
        super().__init__(
            key=key, name=name, service_type=self.MY_SVC_TYPE, url=url, oauth_key=oauth_key,
            db_key=db_key, obj_key=obj_key, git_key=git_key, configuration=configuration)

        assert self.url, f"url must be defined for {type(self)}. key: {key}, name: {name}"
