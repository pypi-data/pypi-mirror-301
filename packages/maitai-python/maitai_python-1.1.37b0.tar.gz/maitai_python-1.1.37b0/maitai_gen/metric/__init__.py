# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: metric.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from typing import Optional

import betterproto


@dataclass(eq=False, repr=False)
class RequestTimingMetric(betterproto.Message):
    time_request_start: float = betterproto.float_field(1)
    time_pre_request: float = betterproto.float_field(2)
    time_first_chunk: Optional[float] = betterproto.float_field(
        3, optional=True, group="_time_first_chunk"
    )
    time_request_end: float = betterproto.float_field(4)
    request_id: str = betterproto.string_field(5)
