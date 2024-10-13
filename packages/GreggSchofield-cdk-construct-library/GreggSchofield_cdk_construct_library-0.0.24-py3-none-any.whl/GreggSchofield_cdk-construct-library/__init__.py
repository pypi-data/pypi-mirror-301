r'''
# replace this
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import constructs as _constructs_77d1e7e8


class PlatformQueue(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-construct-library.PlatformQueue",
):
    '''Construct that creates an AWS SQS queue with best practices.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        dlq: typing.Optional[builtins.bool] = None,
        fifo: typing.Optional[builtins.bool] = None,
        security_standard: typing.Optional["SecurityStandard"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param dlq: Whether the queue has a dead letter queue (dlq).
        :param fifo: Whether the queue is first-in first-out (fifo).
        :param security_standard: The security standard for the queue.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee2d7fdd62d69b291ffb23d1131c1d60c75d391305be02337377100a5565642)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PlatformQueueProps(
            dlq=dlq, fifo=fifo, security_standard=security_standard
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-construct-library.PlatformQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "dlq": "dlq",
        "fifo": "fifo",
        "security_standard": "securityStandard",
    },
)
class PlatformQueueProps:
    def __init__(
        self,
        *,
        dlq: typing.Optional[builtins.bool] = None,
        fifo: typing.Optional[builtins.bool] = None,
        security_standard: typing.Optional["SecurityStandard"] = None,
    ) -> None:
        '''Properties for the PlatformQueue Construct.

        :param dlq: Whether the queue has a dead letter queue (dlq).
        :param fifo: Whether the queue is first-in first-out (fifo).
        :param security_standard: The security standard for the queue.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80be901876bdb6c594a84ef93cc32ed85dde61ffabf4f9f3dd312cc101960b2a)
            check_type(argname="argument dlq", value=dlq, expected_type=type_hints["dlq"])
            check_type(argname="argument fifo", value=fifo, expected_type=type_hints["fifo"])
            check_type(argname="argument security_standard", value=security_standard, expected_type=type_hints["security_standard"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dlq is not None:
            self._values["dlq"] = dlq
        if fifo is not None:
            self._values["fifo"] = fifo
        if security_standard is not None:
            self._values["security_standard"] = security_standard

    @builtins.property
    def dlq(self) -> typing.Optional[builtins.bool]:
        '''Whether the queue has a dead letter queue (dlq).'''
        result = self._values.get("dlq")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fifo(self) -> typing.Optional[builtins.bool]:
        '''Whether the queue is first-in first-out (fifo).'''
        result = self._values.get("fifo")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_standard(self) -> typing.Optional["SecurityStandard"]:
        '''The security standard for the queue.'''
        result = self._values.get("security_standard")
        return typing.cast(typing.Optional["SecurityStandard"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlatformQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-construct-library.SecurityStandard")
class SecurityStandard(enum.Enum):
    '''Enum for the different types of security standards.'''

    GDPR = "GDPR"
    '''General Data Protection Regulation.'''
    PCI_DSS = "PCI_DSS"
    '''Payment Card Industry Data Security Standard.'''
    SOC_2 = "SOC_2"
    '''System and Organization Controls 2.'''


__all__ = [
    "PlatformQueue",
    "PlatformQueueProps",
    "SecurityStandard",
]

publication.publish()

def _typecheckingstub__3ee2d7fdd62d69b291ffb23d1131c1d60c75d391305be02337377100a5565642(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dlq: typing.Optional[builtins.bool] = None,
    fifo: typing.Optional[builtins.bool] = None,
    security_standard: typing.Optional[SecurityStandard] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80be901876bdb6c594a84ef93cc32ed85dde61ffabf4f9f3dd312cc101960b2a(
    *,
    dlq: typing.Optional[builtins.bool] = None,
    fifo: typing.Optional[builtins.bool] = None,
    security_standard: typing.Optional[SecurityStandard] = None,
) -> None:
    """Type checking stubs"""
    pass
