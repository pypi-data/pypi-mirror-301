# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cirq_google/api/v2/calibration.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import metrics_pb2 as cirq__google_dot_api_dot_v2_dot_metrics__pb2
from . import program_pb2 as cirq__google_dot_api_dot_v2_dot_program__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$cirq_google/api/v2/calibration.proto\x12\x12\x63irq.google.api.v2\x1a cirq_google/api/v2/metrics.proto\x1a cirq_google/api/v2/program.proto\"J\n\x12\x46ocusedCalibration\x12\x34\n\x06layers\x18\x01 \x03(\x0b\x32$.cirq.google.api.v2.CalibrationLayer\"\xdc\x01\n\x10\x43\x61librationLayer\x12\x18\n\x10\x63\x61libration_type\x18\x01 \x01(\t\x12*\n\x05layer\x18\x02 \x01(\x0b\x32\x1b.cirq.google.api.v2.Program\x12<\n\x04\x61rgs\x18\x03 \x03(\x0b\x32..cirq.google.api.v2.CalibrationLayer.ArgsEntry\x1a\x44\n\tArgsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.cirq.google.api.v2.Arg:\x02\x38\x01\"W\n\x18\x46ocusedCalibrationResult\x12;\n\x07results\x18\x01 \x03(\x0b\x32*.cirq.google.api.v2.CalibrationLayerResult\"\xc4\x01\n\x16\x43\x61librationLayerResult\x12\x36\n\x04\x63ode\x18\x01 \x01(\x0e\x32(.cirq.google.api.v2.CalibrationLayerCode\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12\r\n\x05token\x18\x03 \x01(\t\x12\x34\n\x07metrics\x18\x04 \x01(\x0b\x32#.cirq.google.api.v2.MetricsSnapshot\x12\x16\n\x0evalid_until_ms\x18\x05 \x01(\x04*\xa7\x01\n\x14\x43\x61librationLayerCode\x12\"\n\x1e\x43\x41LIBRATION_RESULT_UNSPECIFIED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\x0f\n\x0b\x45RROR_OTHER\x10\x02\x12\x1c\n\x18\x45RROR_INVALID_PARAMETERS\x10\x03\x12\x11\n\rERROR_TIMEOUT\x10\x04\x12\x1c\n\x18\x45RROR_CALIBRATION_FAILED\x10\x05\x42:\n\x1d\x63om.google.cirq.google.api.v2B\x17\x46ocusedCalibrationProtoP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cirq_google.api.v2.calibration_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\035com.google.cirq.google.api.v2B\027FocusedCalibrationProtoP\001'
  _CALIBRATIONLAYER_ARGSENTRY._options = None
  _CALIBRATIONLAYER_ARGSENTRY._serialized_options = b'8\001'
  _globals['_CALIBRATIONLAYERCODE']._serialized_start=716
  _globals['_CALIBRATIONLAYERCODE']._serialized_end=883
  _globals['_FOCUSEDCALIBRATION']._serialized_start=128
  _globals['_FOCUSEDCALIBRATION']._serialized_end=202
  _globals['_CALIBRATIONLAYER']._serialized_start=205
  _globals['_CALIBRATIONLAYER']._serialized_end=425
  _globals['_CALIBRATIONLAYER_ARGSENTRY']._serialized_start=357
  _globals['_CALIBRATIONLAYER_ARGSENTRY']._serialized_end=425
  _globals['_FOCUSEDCALIBRATIONRESULT']._serialized_start=427
  _globals['_FOCUSEDCALIBRATIONRESULT']._serialized_end=514
  _globals['_CALIBRATIONLAYERRESULT']._serialized_start=517
  _globals['_CALIBRATIONLAYERRESULT']._serialized_end=713
# @@protoc_insertion_point(module_scope)
