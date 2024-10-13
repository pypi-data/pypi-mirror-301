from dataclasses import dataclass, field
from cooptools.config import JsonConfigHandler
from typing import Callable
from cooptools.typeProviders import resolve
from cooptools.typeProviders import StringProvider

@dataclass(frozen=True)
class Creds:
    user: str
    pw: str

    def as_dict(self):
        return {'user': self.user,
                'pw': self.pw}

    @classmethod
    def mock(cls):
        return Creds(
            user='MOCK_USER',
            pw='MOCK_PW'
        )

    @classmethod
    def from_json_config(cls,
                         config: JsonConfigHandler,
                         user_key: str = 'user',
                         pw_key: str = 'pw',
                         user_fallback_provider: StringProvider = None,
                         pw_fallback_provider: StringProvider = None
                         ):
        user = config.resolve(
            config=user_key,
            fallback_val_provider=user_fallback_provider
        )
        pw = config.resolve(
            config=pw_key,
            fallback_val_provider=pw_fallback_provider
        )
        return Creds(
            user=user,
            pw=pw
        )
@dataclass(frozen=True)
class CnxnInfo:
    uri: str = None
    creds: Creds = None
    mock: bool = False

    def __post_init__(self):
        if self.mock == True and self.uri is None:
            object.__setattr__(self, f'{self.uri=}'.split('=')[0].replace('self.', ''), 'MOCK_URL')

        if self.mock == True and self.creds is None:
            object.__setattr__(self, f'{self.creds=}'.split('=')[0].replace('self.', ''), Creds.mock())

        if self.mock == False and self.uri is None:
            raise ValueError(f"url cannot be None if not mocking")

        if self.mock == False and self.creds is None:
            raise ValueError(f"creds cannot be None if not mocking")

    @classmethod
    def mock(cls,
             creds: Creds = None,
             uri: str = None):
        return CnxnInfo(mock=True,
                        creds=creds if creds is not None else Creds.mock(),
                        uri=uri if uri else "MOCK_URI")


CnxnProvider = CnxnInfo | Callable[[], CnxnInfo]
def resolve_cnxn_provider(cnxn_provider: CnxnProvider) ->CnxnInfo:
    return resolve(cnxn_provider)