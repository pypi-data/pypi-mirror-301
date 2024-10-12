from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class GrantType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GRANT_TYPE_UNSPECIFIED: _ClassVar[GrantType]
    GRANT_TYPE_AUTHORIZATION_CODE: _ClassVar[GrantType]
    GRANT_TYPE_REFRESH_TOKEN: _ClassVar[GrantType]

class RoleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROLE_TYPE_UNSPECIFIED: _ClassVar[RoleType]
    ROLE_TYPE_ADMIN: _ClassVar[RoleType]
    ROLE_TYPE_USER: _ClassVar[RoleType]

class ResponseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESPONSE_TYPE_UNSPECIFIED: _ClassVar[ResponseType]
    RESPONSE_TYPE_SUCCESS: _ClassVar[ResponseType]
    RESPONSE_TYPE_FAIL: _ClassVar[ResponseType]

class LoginType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOGIN_TYPE_UNSPECIFIED: _ClassVar[LoginType]
    LOGIN_TYPE_NATIVE: _ClassVar[LoginType]
    LOGIN_TYPE_KAKAO: _ClassVar[LoginType]
    LOGIN_TYPE_NAVER: _ClassVar[LoginType]

class TokenType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TOKEN_TYPE_UNSPECIFIED: _ClassVar[TokenType]
    TOKEN_TYPE_BEARER: _ClassVar[TokenType]
GRANT_TYPE_UNSPECIFIED: GrantType
GRANT_TYPE_AUTHORIZATION_CODE: GrantType
GRANT_TYPE_REFRESH_TOKEN: GrantType
ROLE_TYPE_UNSPECIFIED: RoleType
ROLE_TYPE_ADMIN: RoleType
ROLE_TYPE_USER: RoleType
RESPONSE_TYPE_UNSPECIFIED: ResponseType
RESPONSE_TYPE_SUCCESS: ResponseType
RESPONSE_TYPE_FAIL: ResponseType
LOGIN_TYPE_UNSPECIFIED: LoginType
LOGIN_TYPE_NATIVE: LoginType
LOGIN_TYPE_KAKAO: LoginType
LOGIN_TYPE_NAVER: LoginType
TOKEN_TYPE_UNSPECIFIED: TokenType
TOKEN_TYPE_BEARER: TokenType
