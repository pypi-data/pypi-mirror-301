# DO NOT MODIFY -- This file is generated by type_spec
# flake8: noqa: F821
# ruff: noqa: E402 Q003
# fmt: off
# isort: skip_file
from __future__ import annotations
import typing  # noqa: F401
import datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from pkgs.strenum_compat import StrEnum
import dataclasses
from pkgs.serialization import serial_class
from pkgs.serialization import serial_union_annotation
from . import client_config_t
from . import generic_upload_t
from . import secret_retrieval_t

__all__: list[str] = [
    "AuthRetrieval",
    "AuthRetrievalBase",
    "AuthRetrievalBasic",
    "AuthRetrievalOAuth",
    "AuthRetrievalType",
    "CronJobDefinition",
    "GenericUploadDataSource",
    "GenericUploadDataSourceBase",
    "GenericUploadDataSourceS3",
    "GenericUploadDataSourceSFTP",
    "GenericUploadDataSourceType",
    "JobDefinition",
    "JobDefinitionBase",
    "JobDefinitionType",
    "JobExecutor",
    "JobExecutorBase",
    "JobExecutorGenericUpload",
    "JobExecutorScript",
    "JobExecutorType",
    "JobResult",
    "ProfileDefinition",
    "ProfileMetadata",
    "S3CloudProvider",
    "WebhookJobDefinition",
]


# DO NOT MODIFY -- This file is generated by type_spec
class JobDefinitionType(StrEnum):
    CRON = "cron"
    WEBHOOK = "webhook"


# DO NOT MODIFY -- This file is generated by type_spec
class JobExecutorType(StrEnum):
    SCRIPT = "script"
    GENERIC_UPLOAD = "generic_upload"


# DO NOT MODIFY -- This file is generated by type_spec
class AuthRetrievalType(StrEnum):
    OAUTH = "oauth"
    BASIC = "basic"


# DO NOT MODIFY -- This file is generated by type_spec
class GenericUploadDataSourceType(StrEnum):
    SFTP = "sftp"
    S3 = "s3"


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class JobExecutorBase:
    type: JobExecutorType


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    parse_require={"type"},
)
@dataclasses.dataclass(kw_only=True)
class JobExecutorScript(JobExecutorBase):
    type: typing.Literal[JobExecutorType.SCRIPT] = JobExecutorType.SCRIPT
    import_path: str


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class GenericUploadDataSourceBase:
    type: GenericUploadDataSourceType


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    parse_require={"type"},
)
@dataclasses.dataclass(kw_only=True)
class GenericUploadDataSourceSFTP(GenericUploadDataSourceBase):
    type: typing.Literal[GenericUploadDataSourceType.SFTP] = GenericUploadDataSourceType.SFTP
    host: str
    username: str
    pem_secret: secret_retrieval_t.SecretRetrieval


# DO NOT MODIFY -- This file is generated by type_spec
class S3CloudProvider(StrEnum):
    OVH = "ovh"
    AWS = "aws"


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    parse_require={"type"},
)
@dataclasses.dataclass(kw_only=True)
class GenericUploadDataSourceS3(GenericUploadDataSourceBase):
    type: typing.Literal[GenericUploadDataSourceType.S3] = GenericUploadDataSourceType.S3
    bucket_name: str
    cloud_provider: typing.Optional[S3CloudProvider] = None
    endpoint_url: typing.Optional[str] = None
    region_name: typing.Optional[str] = None
    access_key_id: typing.Optional[str] = None
    access_key_secret: typing.Optional[secret_retrieval_t.SecretRetrieval] = None


# DO NOT MODIFY -- This file is generated by type_spec
GenericUploadDataSource = typing.Annotated[
    typing.Union[GenericUploadDataSourceSFTP, GenericUploadDataSourceS3],
    serial_union_annotation(
        discriminator="type",
        discriminator_map={
            "sftp": GenericUploadDataSourceSFTP,
            "s3": GenericUploadDataSourceS3,
        },
    ),
]


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    parse_require={"type"},
)
@dataclasses.dataclass(kw_only=True)
class JobExecutorGenericUpload(JobExecutorBase):
    type: typing.Literal[JobExecutorType.GENERIC_UPLOAD] = JobExecutorType.GENERIC_UPLOAD
    data_source: GenericUploadDataSource
    upload_strategy: generic_upload_t.GenericUploadStrategy
    remote_directories: list[generic_upload_t.GenericRemoteDirectoryScope]


# DO NOT MODIFY -- This file is generated by type_spec
JobExecutor = typing.Annotated[
    typing.Union[JobExecutorScript, JobExecutorGenericUpload],
    serial_union_annotation(
        discriminator="type",
        discriminator_map={
            "script": JobExecutorScript,
            "generic_upload": JobExecutorGenericUpload,
        },
    ),
]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class JobDefinitionBase:
    id: str
    name: str
    executor: JobExecutor
    enabled: bool = True


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    parse_require={"type"},
)
@dataclasses.dataclass(kw_only=True)
class CronJobDefinition(JobDefinitionBase):
    type: typing.Literal[JobDefinitionType.CRON] = JobDefinitionType.CRON
    cron_spec: str


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    parse_require={"type"},
)
@dataclasses.dataclass(kw_only=True)
class WebhookJobDefinition(JobDefinitionBase):
    type: typing.Literal[JobDefinitionType.WEBHOOK] = JobDefinitionType.WEBHOOK
    signature_key_secret: secret_retrieval_t.SecretRetrieval


# DO NOT MODIFY -- This file is generated by type_spec
JobDefinition = typing.Annotated[
    typing.Union[CronJobDefinition, WebhookJobDefinition],
    serial_union_annotation(
        discriminator="type",
        discriminator_map={
            "cron": CronJobDefinition,
            "webhook": WebhookJobDefinition,
        },
    ),
]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class AuthRetrievalBase:
    type: AuthRetrievalType


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    parse_require={"type"},
)
@dataclasses.dataclass(kw_only=True)
class AuthRetrievalOAuth(AuthRetrievalBase):
    type: typing.Literal[AuthRetrievalType.OAUTH] = AuthRetrievalType.OAUTH
    refresh_token_secret: secret_retrieval_t.SecretRetrieval


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    parse_require={"type"},
)
@dataclasses.dataclass(kw_only=True)
class AuthRetrievalBasic(AuthRetrievalBase):
    type: typing.Literal[AuthRetrievalType.BASIC] = AuthRetrievalType.BASIC
    api_id_secret: secret_retrieval_t.SecretRetrieval
    api_key_secret: secret_retrieval_t.SecretRetrieval


# DO NOT MODIFY -- This file is generated by type_spec
AuthRetrieval = typing.Annotated[
    typing.Union[AuthRetrievalOAuth, AuthRetrievalBasic],
    serial_union_annotation(
        discriminator="type",
        discriminator_map={
            "oauth": AuthRetrievalOAuth,
            "basic": AuthRetrievalBasic,
        },
    ),
]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class ProfileDefinition:
    auth_retrieval: AuthRetrieval
    base_url: str
    jobs: list[JobDefinition]
    client_options: typing.Optional[client_config_t.ClientConfigOptions] = None


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class ProfileMetadata:
    name: str
    base_url: str
    auth_retrieval: AuthRetrieval
    client_options: typing.Optional[client_config_t.ClientConfigOptions]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class JobResult:
    success: bool
# DO NOT MODIFY -- This file is generated by type_spec
