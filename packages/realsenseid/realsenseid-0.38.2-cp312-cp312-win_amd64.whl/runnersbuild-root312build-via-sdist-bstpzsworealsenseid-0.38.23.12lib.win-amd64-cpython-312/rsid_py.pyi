"""

        RealSenseID Python Bindings
        ==============================
        Library for accessing Intel RealSenseID cameras
    
"""
from __future__ import annotations
import typing
__all__ = ['AlgoFlow', 'AuthenticateStatus', 'CameraRotation', 'DeviceConfig', 'DeviceController', 'DeviceFirmwareInfo', 'DumpMode', 'EnrollStatus', 'ExtractedFaceprintsElement', 'FWUpdateException', 'FWUpdatePolicyException', 'FWUpdater', 'FaceAuthenticator', 'FacePose', 'FaceRect', 'FaceSelectionPolicy', 'Faceprints', 'FaceprintsType', 'FirmwareBinInfo', 'Image', 'ImageMetadata', 'IncompatibleHostException', 'InvalidFirmwareException', 'LogLevel', 'MatchResult', 'MatcherConfidenceLevel', 'Preview', 'PreviewConfig', 'PreviewException', 'PreviewMode', 'RSID_FACEPRINTS_VERSION', 'RSID_FEATURES_VECTOR_ALLOC_SIZE', 'RSID_NUM_OF_RECOGNITION_FEATURES', 'ReleaseInfo', 'SKUMismatchException', 'SecurityLevel', 'Status', 'UpdateChecker', 'compatible_firmware', 'discover_capture', 'discover_devices', 'faceprints_version', 'set_log_callback']
class AlgoFlow:
    """
    Members:
    
      All
    
      FaceDetectionOnly
    
      SpoofOnly
    
      RecognitionOnly
    """
    All: typing.ClassVar[AlgoFlow]  # value = <AlgoFlow.All: 0>
    FaceDetectionOnly: typing.ClassVar[AlgoFlow]  # value = <AlgoFlow.FaceDetectionOnly: 1>
    RecognitionOnly: typing.ClassVar[AlgoFlow]  # value = <AlgoFlow.RecognitionOnly: 3>
    SpoofOnly: typing.ClassVar[AlgoFlow]  # value = <AlgoFlow.SpoofOnly: 2>
    __members__: typing.ClassVar[dict[str, AlgoFlow]]  # value = {'All': <AlgoFlow.All: 0>, 'FaceDetectionOnly': <AlgoFlow.FaceDetectionOnly: 1>, 'SpoofOnly': <AlgoFlow.SpoofOnly: 2>, 'RecognitionOnly': <AlgoFlow.RecognitionOnly: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class AuthenticateStatus:
    """
    Members:
    
      Success
    
      NoFaceDetected
    
      FaceDetected
    
      LedFlowSuccess
    
      FaceIsTooFarToTheTop
    
      FaceIsTooFarToTheBottom
    
      FaceIsTooFarToTheRight
    
      FaceIsTooFarToTheLeft
    
      FaceTiltIsTooUp
    
      FaceTiltIsTooDown
    
      FaceTiltIsTooRight
    
      FaceTiltIsTooLeft
    
      CameraStarted
    
      CameraStopped
    
      MaskDetectedInHighSecurity
    
      Spoof
    
      Forbidden
    
      DeviceError
    
      Failure
    
      TooManySpoofs
    
      InvalidFeatures
    
      Ok
    
      Error
    
      SerialError
    
      SecurityError
    
      VersionMismatch
    
      CrcError
    
      LicenseError
    
      LicenseCheck
    
      Spoof_2D
    
      Spoof_3D
    
      Spoof_LR
    
      Spoof_Surface
    
      Spoof_Disparity
    
      Spoof_Plane_Disparity
    """
    CameraStarted: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.CameraStarted: 12>
    CameraStopped: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.CameraStopped: 13>
    CrcError: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.CrcError: 105>
    DeviceError: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.DeviceError: 17>
    Error: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Error: 101>
    FaceDetected: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.FaceDetected: 2>
    FaceIsTooFarToTheBottom: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.FaceIsTooFarToTheBottom: 5>
    FaceIsTooFarToTheLeft: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.FaceIsTooFarToTheLeft: 7>
    FaceIsTooFarToTheRight: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.FaceIsTooFarToTheRight: 6>
    FaceIsTooFarToTheTop: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.FaceIsTooFarToTheTop: 4>
    FaceTiltIsTooDown: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.FaceTiltIsTooDown: 9>
    FaceTiltIsTooLeft: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.FaceTiltIsTooLeft: 11>
    FaceTiltIsTooRight: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.FaceTiltIsTooRight: 10>
    FaceTiltIsTooUp: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.FaceTiltIsTooUp: 8>
    Failure: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Failure: 18>
    Forbidden: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Forbidden: 16>
    InvalidFeatures: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.InvalidFeatures: 20>
    LedFlowSuccess: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.LedFlowSuccess: 3>
    LicenseCheck: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.LicenseCheck: 107>
    LicenseError: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.LicenseError: 106>
    MaskDetectedInHighSecurity: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.MaskDetectedInHighSecurity: 14>
    NoFaceDetected: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.NoFaceDetected: 1>
    Ok: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Ok: 100>
    SecurityError: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.SecurityError: 103>
    SerialError: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.SerialError: 102>
    Spoof: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Spoof: 15>
    Spoof_2D: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Spoof_2D: 120>
    Spoof_3D: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Spoof_3D: 121>
    Spoof_Disparity: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Spoof_Disparity: 123>
    Spoof_LR: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Spoof_LR: 122>
    Spoof_Plane_Disparity: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Spoof_Plane_Disparity: 125>
    Spoof_Surface: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Spoof_Surface: 124>
    Success: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.Success: 0>
    TooManySpoofs: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.TooManySpoofs: 19>
    VersionMismatch: typing.ClassVar[AuthenticateStatus]  # value = <AuthenticateStatus.VersionMismatch: 104>
    __members__: typing.ClassVar[dict[str, AuthenticateStatus]]  # value = {'Success': <AuthenticateStatus.Success: 0>, 'NoFaceDetected': <AuthenticateStatus.NoFaceDetected: 1>, 'FaceDetected': <AuthenticateStatus.FaceDetected: 2>, 'LedFlowSuccess': <AuthenticateStatus.LedFlowSuccess: 3>, 'FaceIsTooFarToTheTop': <AuthenticateStatus.FaceIsTooFarToTheTop: 4>, 'FaceIsTooFarToTheBottom': <AuthenticateStatus.FaceIsTooFarToTheBottom: 5>, 'FaceIsTooFarToTheRight': <AuthenticateStatus.FaceIsTooFarToTheRight: 6>, 'FaceIsTooFarToTheLeft': <AuthenticateStatus.FaceIsTooFarToTheLeft: 7>, 'FaceTiltIsTooUp': <AuthenticateStatus.FaceTiltIsTooUp: 8>, 'FaceTiltIsTooDown': <AuthenticateStatus.FaceTiltIsTooDown: 9>, 'FaceTiltIsTooRight': <AuthenticateStatus.FaceTiltIsTooRight: 10>, 'FaceTiltIsTooLeft': <AuthenticateStatus.FaceTiltIsTooLeft: 11>, 'CameraStarted': <AuthenticateStatus.CameraStarted: 12>, 'CameraStopped': <AuthenticateStatus.CameraStopped: 13>, 'MaskDetectedInHighSecurity': <AuthenticateStatus.MaskDetectedInHighSecurity: 14>, 'Spoof': <AuthenticateStatus.Spoof: 15>, 'Forbidden': <AuthenticateStatus.Forbidden: 16>, 'DeviceError': <AuthenticateStatus.DeviceError: 17>, 'Failure': <AuthenticateStatus.Failure: 18>, 'TooManySpoofs': <AuthenticateStatus.TooManySpoofs: 19>, 'InvalidFeatures': <AuthenticateStatus.InvalidFeatures: 20>, 'Ok': <AuthenticateStatus.Ok: 100>, 'Error': <AuthenticateStatus.Error: 101>, 'SerialError': <AuthenticateStatus.SerialError: 102>, 'SecurityError': <AuthenticateStatus.SecurityError: 103>, 'VersionMismatch': <AuthenticateStatus.VersionMismatch: 104>, 'CrcError': <AuthenticateStatus.CrcError: 105>, 'LicenseError': <AuthenticateStatus.LicenseError: 106>, 'LicenseCheck': <AuthenticateStatus.LicenseCheck: 107>, 'Spoof_2D': <AuthenticateStatus.Spoof_2D: 120>, 'Spoof_3D': <AuthenticateStatus.Spoof_3D: 121>, 'Spoof_LR': <AuthenticateStatus.Spoof_LR: 122>, 'Spoof_Surface': <AuthenticateStatus.Spoof_Surface: 124>, 'Spoof_Disparity': <AuthenticateStatus.Spoof_Disparity: 123>, 'Spoof_Plane_Disparity': <AuthenticateStatus.Spoof_Plane_Disparity: 125>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class CameraRotation:
    """
    Members:
    
      Rotation_0_Deg
    
      Rotation_180_Deg
    
      Rotation_90_Deg
    
      Rotation_270_Deg
    """
    Rotation_0_Deg: typing.ClassVar[CameraRotation]  # value = <CameraRotation.Rotation_0_Deg: 0>
    Rotation_180_Deg: typing.ClassVar[CameraRotation]  # value = <CameraRotation.Rotation_180_Deg: 1>
    Rotation_270_Deg: typing.ClassVar[CameraRotation]  # value = <CameraRotation.Rotation_270_Deg: 3>
    Rotation_90_Deg: typing.ClassVar[CameraRotation]  # value = <CameraRotation.Rotation_90_Deg: 2>
    __members__: typing.ClassVar[dict[str, CameraRotation]]  # value = {'Rotation_0_Deg': <CameraRotation.Rotation_0_Deg: 0>, 'Rotation_180_Deg': <CameraRotation.Rotation_180_Deg: 1>, 'Rotation_90_Deg': <CameraRotation.Rotation_90_Deg: 2>, 'Rotation_270_Deg': <CameraRotation.Rotation_270_Deg: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class DeviceConfig:
    algo_flow: AlgoFlow
    camera_rotation: CameraRotation
    dump_mode: DumpMode
    face_selection_policy: FaceSelectionPolicy
    matcher_confidence_level: MatcherConfidenceLevel
    max_spoofs: int
    security_level: SecurityLevel
    def __copy__(self) -> DeviceConfig:
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class DeviceController:
    def __enter__(self) -> DeviceController:
        ...
    def __exit__(self, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: str) -> None:
        ...
    def connect(self, port: str) -> None:
        ...
    def disconnect(self) -> None:
        ...
    def fetch_log(self) -> str:
        ...
    def ping(self) -> Status:
        ...
    def query_firmware_version(self) -> str:
        ...
    def query_serial_number(self) -> str:
        ...
    def reboot(self) -> bool:
        ...
class DeviceFirmwareInfo:
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def fw_version(self) -> str:
        ...
    @property
    def recognition_version(self) -> str:
        ...
    @property
    def serial_number(self) -> str:
        ...
class DumpMode:
    """
    Members:
    
      Disable
    
      CroppedFace
    
      FullFrame
    """
    CroppedFace: typing.ClassVar[DumpMode]  # value = <DumpMode.CroppedFace: 1>
    Disable: typing.ClassVar[DumpMode]  # value = <DumpMode.Disable: 0>
    FullFrame: typing.ClassVar[DumpMode]  # value = <DumpMode.FullFrame: 2>
    __members__: typing.ClassVar[dict[str, DumpMode]]  # value = {'Disable': <DumpMode.Disable: 0>, 'CroppedFace': <DumpMode.CroppedFace: 1>, 'FullFrame': <DumpMode.FullFrame: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class EnrollStatus:
    """
    Members:
    
      Success
    
      NoFaceDetected
    
      FaceDetected
    
      LedFlowSuccess
    
      FaceIsTooFarToTheTop
    
      FaceIsTooFarToTheBottom
    
      FaceIsTooFarToTheRight
    
      FaceIsTooFarToTheLeft
    
      FaceTiltIsTooUp
    
      FaceTiltIsTooDown
    
      FaceTiltIsTooRight
    
      FaceTiltIsTooLeft
    
      FaceIsNotFrontal
    
      CameraStarted
    
      CameraStopped
    
      MultipleFacesDetected
    
      Failure
    
      DeviceError
    
      EnrollWithMaskIsForbidden
    
      Spoof
    
      InvalidFeatures
    
      Ok
    
      Error
    
      SerialError
    
      SecurityError
    
      VersionMismatch
    
      CrcError
    
      LicenseError
    
      LicenseCheck
    
      Spoof_2D
    
      Spoof_3D
    
      Spoof_LR
    
      Spoof_Surface
    
      Spoof_Disparity
    
      Spoof_Plane_Disparity
    """
    CameraStarted: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.CameraStarted: 13>
    CameraStopped: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.CameraStopped: 14>
    CrcError: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.CrcError: 105>
    DeviceError: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.DeviceError: 17>
    EnrollWithMaskIsForbidden: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.EnrollWithMaskIsForbidden: 18>
    Error: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Error: 101>
    FaceDetected: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.FaceDetected: 2>
    FaceIsNotFrontal: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.FaceIsNotFrontal: 12>
    FaceIsTooFarToTheBottom: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.FaceIsTooFarToTheBottom: 5>
    FaceIsTooFarToTheLeft: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.FaceIsTooFarToTheLeft: 7>
    FaceIsTooFarToTheRight: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.FaceIsTooFarToTheRight: 6>
    FaceIsTooFarToTheTop: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.FaceIsTooFarToTheTop: 4>
    FaceTiltIsTooDown: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.FaceTiltIsTooDown: 9>
    FaceTiltIsTooLeft: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.FaceTiltIsTooLeft: 11>
    FaceTiltIsTooRight: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.FaceTiltIsTooRight: 10>
    FaceTiltIsTooUp: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.FaceTiltIsTooUp: 8>
    Failure: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Failure: 16>
    InvalidFeatures: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.InvalidFeatures: 20>
    LedFlowSuccess: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.LedFlowSuccess: 3>
    LicenseCheck: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.LicenseCheck: 107>
    LicenseError: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.LicenseError: 106>
    MultipleFacesDetected: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.MultipleFacesDetected: 15>
    NoFaceDetected: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.NoFaceDetected: 1>
    Ok: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Ok: 100>
    SecurityError: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.SecurityError: 103>
    SerialError: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.SerialError: 102>
    Spoof: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Spoof: 19>
    Spoof_2D: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Spoof_2D: 120>
    Spoof_3D: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Spoof_3D: 121>
    Spoof_Disparity: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Spoof_Disparity: 123>
    Spoof_LR: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Spoof_LR: 122>
    Spoof_Plane_Disparity: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Spoof_Plane_Disparity: 125>
    Spoof_Surface: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Spoof_Surface: 124>
    Success: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.Success: 0>
    VersionMismatch: typing.ClassVar[EnrollStatus]  # value = <EnrollStatus.VersionMismatch: 104>
    __members__: typing.ClassVar[dict[str, EnrollStatus]]  # value = {'Success': <EnrollStatus.Success: 0>, 'NoFaceDetected': <EnrollStatus.NoFaceDetected: 1>, 'FaceDetected': <EnrollStatus.FaceDetected: 2>, 'LedFlowSuccess': <EnrollStatus.LedFlowSuccess: 3>, 'FaceIsTooFarToTheTop': <EnrollStatus.FaceIsTooFarToTheTop: 4>, 'FaceIsTooFarToTheBottom': <EnrollStatus.FaceIsTooFarToTheBottom: 5>, 'FaceIsTooFarToTheRight': <EnrollStatus.FaceIsTooFarToTheRight: 6>, 'FaceIsTooFarToTheLeft': <EnrollStatus.FaceIsTooFarToTheLeft: 7>, 'FaceTiltIsTooUp': <EnrollStatus.FaceTiltIsTooUp: 8>, 'FaceTiltIsTooDown': <EnrollStatus.FaceTiltIsTooDown: 9>, 'FaceTiltIsTooRight': <EnrollStatus.FaceTiltIsTooRight: 10>, 'FaceTiltIsTooLeft': <EnrollStatus.FaceTiltIsTooLeft: 11>, 'FaceIsNotFrontal': <EnrollStatus.FaceIsNotFrontal: 12>, 'CameraStarted': <EnrollStatus.CameraStarted: 13>, 'CameraStopped': <EnrollStatus.CameraStopped: 14>, 'MultipleFacesDetected': <EnrollStatus.MultipleFacesDetected: 15>, 'Failure': <EnrollStatus.Failure: 16>, 'DeviceError': <EnrollStatus.DeviceError: 17>, 'EnrollWithMaskIsForbidden': <EnrollStatus.EnrollWithMaskIsForbidden: 18>, 'Spoof': <EnrollStatus.Spoof: 19>, 'InvalidFeatures': <EnrollStatus.InvalidFeatures: 20>, 'Ok': <EnrollStatus.Ok: 100>, 'Error': <EnrollStatus.Error: 101>, 'SerialError': <EnrollStatus.SerialError: 102>, 'SecurityError': <EnrollStatus.SecurityError: 103>, 'VersionMismatch': <EnrollStatus.VersionMismatch: 104>, 'CrcError': <EnrollStatus.CrcError: 105>, 'LicenseError': <EnrollStatus.LicenseError: 106>, 'LicenseCheck': <EnrollStatus.LicenseCheck: 107>, 'Spoof_2D': <EnrollStatus.Spoof_2D: 120>, 'Spoof_3D': <EnrollStatus.Spoof_3D: 121>, 'Spoof_LR': <EnrollStatus.Spoof_LR: 122>, 'Spoof_Surface': <EnrollStatus.Spoof_Surface: 124>, 'Spoof_Disparity': <EnrollStatus.Spoof_Disparity: 123>, 'Spoof_Plane_Disparity': <EnrollStatus.Spoof_Plane_Disparity: 125>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ExtractedFaceprintsElement:
    features: list[int]
    features_type: int
    flags: int
    version: int
    def __copy__(self) -> ExtractedFaceprintsElement:
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class FWUpdateException(RuntimeError):
    pass
class FWUpdatePolicyException(RuntimeError):
    pass
class FWUpdater:
    def __enter__(self) -> FWUpdater:
        ...
    def __exit__(self, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, file_path: str, port: str) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def get_device_firmware_info(self) -> DeviceFirmwareInfo:
        """
                     Retrieve device firmware info.
                     Returns
                     ----------
                     DeviceFirmwareInfo
                         Class containing version information for the running/current device firmware.
                     Raises
                     ------
                     RuntimeError
                         if reading device info is not possible.
        """
    def get_firmware_bin_info(self) -> FirmwareBinInfo:
        """
                     Retrieve firmware file info.
                     Returns
                     ----------
                     FirmwareBinInfo
                         Class containing version information for firmware file contents.
                     Raises
                     ------
                     InvalidFirmwareException
                         if the firmware file is invalid or corrupt.
        """
    def is_host_compatible(self) -> tuple[bool, str]:
        """
                     Verify if firmware file is compatible with current host SDK version.
                     Returns
                     ----------
                     tuple[bool, str]
                         (is_compatible: bool, message: str) - if is_compatible == False, message will
                         indicate error messages or explanation.
        """
    def is_policy_compatible(self) -> tuple[bool, str]:
        """
                     Verify if firmware file is compatible with the update policy. In some situations, you
                     may need to perform an intermediate update to an older firmware that the latest before
                     you can apply the latest update.
                     Returns
                     ----------
                     tuple[bool, str]
                         (is_compatible: bool, message: str) - if is_compatible == False, message will
                         indicate error messages or explanation.
        """
    def is_sku_compatible(self) -> tuple[bool, str]:
        """
                     Verify if firmware file is compatible with connected device.
                     Returns
                     ----------
                     tuple[bool, str]
                         (is_compatible: bool, message: str) - if is_compatible == False, message will
                         indicate error messages or explanation.
        """
    def update(self, force_version: bool = False, force_full: bool = False, progress_callback: typing.Callable[[float], None] = None) -> Status:
        """
                     Update the device to the firmware file provided.
                     Parameters
                     ----------
                     force_version: bool
                         If the host and new versions are a mismatch, you will need to specify this flag
                         in order to forcefully perform the update.
                         defaults to False
                     force_full: bool
                         Force update of all modules even if they already exist in the current device firmware.
                     progress_callback: function(progress: float)
                         Callback function to receive updates of the update
                         progress. The progress is a float value between 0 and 1
        
                     Examples
                     --------
                         def progress_callback(progress: float):
                             logger.info(f"progress: {progress}")
                         updater.update(progress_callback=progress_callback)
        
                     Returns
                     ----------
                     Status
                         Status for starting the update. Status.OK means that the update started and you should start
                         receiving callbacks on the progress_callback method.
        
                     Raises
                     ------
                     InvalidFirmwareException
                         Firmware file is corrupt or invalid
                     SKUMismatchException
                         Firmware file is incompatible with this device
                     IncompatibleHostException
                         Firmware update needs to be forced as the host is incompatible
                     FWUpdatePolicyException
                         Review exception message for policy requirements
                     FWUpdateException
                         Generic firmware update exception
                     RuntimeError
                         Generic firmware exception
        """
class FaceAuthenticator:
    MAX_USERID_LENGTH: typing.ClassVar[int] = 31
    @staticmethod
    def get_license_key() -> str:
        ...
    @staticmethod
    def set_license_key(arg0: str) -> None:
        ...
    def __enter__(self) -> FaceAuthenticator:
        ...
    def __exit__(self, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: str) -> None:
        ...
    def authenticate(self, on_result: typing.Callable[[AuthenticateStatus, str], None] = None, on_hint: typing.Callable[[AuthenticateStatus], None] = None, on_faces: typing.Callable[[list[FaceRect], int], None] = None) -> None:
        ...
    def authenticate_loop(self, on_result: typing.Callable[[AuthenticateStatus, str], None] = None, on_hint: typing.Callable[[AuthenticateStatus], None] = None, on_faces: typing.Callable[[list[FaceRect], int], None] = None) -> None:
        ...
    def cancel(self) -> None:
        ...
    def connect(self, arg0: str) -> None:
        ...
    def disable_license_check_handler(self) -> None:
        ...
    def disconnect(self) -> None:
        ...
    def enable_license_check_handler(self) -> None:
        ...
    def enroll(self, on_result: typing.Callable[[EnrollStatus], None] = None, on_progress: typing.Callable[[FacePose], None] = None, on_hint: typing.Callable[[EnrollStatus], None] = None, on_faces: typing.Callable[[list[FaceRect], int], None] = None, user_id: str) -> None:
        ...
    def enroll_image(self, user_id: str, buffer: list[int], width: int, height: int) -> EnrollStatus:
        """
        Enroll with image. Buffer should be bgr24
        """
    def extract_faceprints_for_auth(self, on_result: typing.Callable[[AuthenticateStatus, ExtractedFaceprintsElement], None] = None, on_hint: typing.Callable[[AuthenticateStatus], None] = None, on_faces: typing.Callable[[list[FaceRect], int], None] = None) -> None:
        ...
    def extract_faceprints_for_enroll(self, on_result: typing.Callable[[EnrollStatus, ExtractedFaceprintsElement], None] = None, on_progress: typing.Callable[[FacePose], None] = None, on_hint: typing.Callable[[EnrollStatus], None] = None, on_faces: typing.Callable[[list[FaceRect], int], None] = None) -> None:
        ...
    def extract_image_faceprints_for_enroll(self, buffer: list[int], width: int, height: int) -> ExtractedFaceprintsElement:
        """
        Enroll with image. Buffer should be bgr24
        """
    def match_faceprints(self, new_faceprints: ExtractedFaceprintsElement, existing_faceprints: Faceprints, updated_faceprints: Faceprints, confidence_level: MatcherConfidenceLevel = ...) -> MatchResult:
        ...
    def provide_license(self) -> None:
        ...
    def query_device_config(self) -> DeviceConfig:
        ...
    def query_number_of_users(self) -> int:
        ...
    def query_user_ids(self) -> list[str]:
        ...
    def remove_all_users(self) -> None:
        ...
    def remove_user(self, user_id: str) -> None:
        ...
    def set_device_config(self, arg0: DeviceConfig) -> None:
        ...
    def standby(self) -> None:
        ...
    def unlock(self) -> None:
        ...
class FacePose:
    """
    Members:
    
      Center
    
      Up
    
      Down
    
      Left
    
      Right
    """
    Center: typing.ClassVar[FacePose]  # value = <FacePose.Center: 0>
    Down: typing.ClassVar[FacePose]  # value = <FacePose.Down: 2>
    Left: typing.ClassVar[FacePose]  # value = <FacePose.Left: 3>
    Right: typing.ClassVar[FacePose]  # value = <FacePose.Right: 4>
    Up: typing.ClassVar[FacePose]  # value = <FacePose.Up: 1>
    __members__: typing.ClassVar[dict[str, FacePose]]  # value = {'Center': <FacePose.Center: 0>, 'Up': <FacePose.Up: 1>, 'Down': <FacePose.Down: 2>, 'Left': <FacePose.Left: 3>, 'Right': <FacePose.Right: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class FaceRect:
    h: int
    w: int
    x: int
    y: int
    def __copy__(self) -> FaceRect:
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class FaceSelectionPolicy:
    """
    Members:
    
      Single
    
      All
    """
    All: typing.ClassVar[FaceSelectionPolicy]  # value = <FaceSelectionPolicy.All: 1>
    Single: typing.ClassVar[FaceSelectionPolicy]  # value = <FaceSelectionPolicy.Single: 0>
    __members__: typing.ClassVar[dict[str, FaceSelectionPolicy]]  # value = {'Single': <FaceSelectionPolicy.Single: 0>, 'All': <FaceSelectionPolicy.All: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Faceprints:
    adaptive_descriptor_nomask: list[int]
    adaptive_descriptor_withmask: list[int]
    enroll_descriptor: list[int]
    features_type: int
    flags: int
    reserved: list[int]
    version: int
    def __copy__(self) -> Faceprints:
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class FaceprintsType:
    """
    Members:
    
      W10
    
      RGB
    """
    RGB: typing.ClassVar[FaceprintsType]  # value = <FaceprintsType.RGB: 1>
    W10: typing.ClassVar[FaceprintsType]  # value = <FaceprintsType.W10: 0>
    __members__: typing.ClassVar[dict[str, FaceprintsType]]  # value = {'W10': <FaceprintsType.W10: 0>, 'RGB': <FaceprintsType.RGB: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class FirmwareBinInfo:
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def fw_version(self) -> str:
        ...
    @property
    def module_names(self) -> list[str]:
        ...
    @property
    def recognition_version(self) -> str:
        ...
class Image:
    def __init__(self) -> None:
        ...
    def get_buffer(self) -> memoryview:
        ...
    @property
    def height(self) -> int:
        ...
    @property
    def metadata(self) -> ImageMetadata:
        ...
    @property
    def number(self) -> int:
        ...
    @property
    def size(self) -> int:
        ...
    @property
    def stride(self) -> int:
        ...
    @property
    def width(self) -> int:
        ...
class ImageMetadata:
    def __init__(self) -> None:
        ...
    @property
    def exposure(self) -> int:
        ...
    @property
    def gain(self) -> int:
        ...
    @property
    def is_snapshot(self) -> bool:
        ...
    @property
    def led(self) -> bool:
        ...
    @property
    def sensor_id(self) -> int:
        ...
    @property
    def status(self) -> int:
        ...
    @property
    def timestamp(self) -> int:
        ...
class IncompatibleHostException(RuntimeError):
    pass
class InvalidFirmwareException(RuntimeError):
    pass
class LogLevel:
    """
    Members:
    
      Trace
    
      Debug
    
      Info
    
      Warning
    
      Error
    
      Critical
    
      Off
    """
    Critical: typing.ClassVar[LogLevel]  # value = <LogLevel.Critical: 5>
    Debug: typing.ClassVar[LogLevel]  # value = <LogLevel.Debug: 1>
    Error: typing.ClassVar[LogLevel]  # value = <LogLevel.Error: 4>
    Info: typing.ClassVar[LogLevel]  # value = <LogLevel.Info: 2>
    Off: typing.ClassVar[LogLevel]  # value = <LogLevel.Off: 6>
    Trace: typing.ClassVar[LogLevel]  # value = <LogLevel.Trace: 0>
    Warning: typing.ClassVar[LogLevel]  # value = <LogLevel.Warning: 3>
    __members__: typing.ClassVar[dict[str, LogLevel]]  # value = {'Trace': <LogLevel.Trace: 0>, 'Debug': <LogLevel.Debug: 1>, 'Info': <LogLevel.Info: 2>, 'Warning': <LogLevel.Warning: 3>, 'Error': <LogLevel.Error: 4>, 'Critical': <LogLevel.Critical: 5>, 'Off': <LogLevel.Off: 6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class MatchResult:
    score: int
    should_update: bool
    success: bool
    def __copy__(self) -> MatchResult:
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class MatcherConfidenceLevel:
    """
    Members:
    
      High
    
      Medium
    
      Low
    """
    High: typing.ClassVar[MatcherConfidenceLevel]  # value = <MatcherConfidenceLevel.High: 0>
    Low: typing.ClassVar[MatcherConfidenceLevel]  # value = <MatcherConfidenceLevel.Low: 2>
    Medium: typing.ClassVar[MatcherConfidenceLevel]  # value = <MatcherConfidenceLevel.Medium: 1>
    __members__: typing.ClassVar[dict[str, MatcherConfidenceLevel]]  # value = {'High': <MatcherConfidenceLevel.High: 0>, 'Medium': <MatcherConfidenceLevel.Medium: 1>, 'Low': <MatcherConfidenceLevel.Low: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Preview:
    def __init__(self, arg0: PreviewConfig) -> None:
        ...
    def start(self, preview_callback: typing.Callable[[Image], None], snapshot_callback: typing.Callable[[Image], None]) -> None:
        ...
    def stop(self) -> None:
        ...
class PreviewConfig:
    camera_number: int
    portrait_mode: bool
    preview_mode: PreviewMode
    rotate_raw: bool
    def __init__(self) -> None:
        ...
class PreviewException(RuntimeError):
    pass
class PreviewMode:
    """
    Members:
    
      MJPEG_1080P
    
      MJPEG_720P
    
      RAW10_1080P
    """
    MJPEG_1080P: typing.ClassVar[PreviewMode]  # value = <PreviewMode.MJPEG_1080P: 0>
    MJPEG_720P: typing.ClassVar[PreviewMode]  # value = <PreviewMode.MJPEG_720P: 1>
    RAW10_1080P: typing.ClassVar[PreviewMode]  # value = <PreviewMode.RAW10_1080P: 2>
    __members__: typing.ClassVar[dict[str, PreviewMode]]  # value = {'MJPEG_1080P': <PreviewMode.MJPEG_1080P: 0>, 'MJPEG_720P': <PreviewMode.MJPEG_720P: 1>, 'RAW10_1080P': <PreviewMode.RAW10_1080P: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ReleaseInfo:
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def fw_version(self) -> int:
        ...
    @property
    def fw_version_str(self) -> str:
        ...
    @property
    def release_notes_url(self) -> str:
        ...
    @property
    def release_url(self) -> str:
        ...
    @property
    def sw_version(self) -> int:
        ...
    @property
    def sw_version_str(self) -> str:
        ...
class SKUMismatchException(RuntimeError):
    pass
class SecurityLevel:
    """
    Members:
    
      High
    
      Medium
    
      Low
    """
    High: typing.ClassVar[SecurityLevel]  # value = <SecurityLevel.High: 0>
    Low: typing.ClassVar[SecurityLevel]  # value = <SecurityLevel.Low: 2>
    Medium: typing.ClassVar[SecurityLevel]  # value = <SecurityLevel.Medium: 1>
    __members__: typing.ClassVar[dict[str, SecurityLevel]]  # value = {'High': <SecurityLevel.High: 0>, 'Medium': <SecurityLevel.Medium: 1>, 'Low': <SecurityLevel.Low: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Status:
    """
    Members:
    
      Ok
    
      Error
    
      SerialError
    
      SecurityError
    
      VersionMismatch
    
      CrcError
    
      LicenseError
    
      LicenseCheck
    
      TooManySpoofs
    """
    CrcError: typing.ClassVar[Status]  # value = <Status.CrcError: 105>
    Error: typing.ClassVar[Status]  # value = <Status.Error: 101>
    LicenseCheck: typing.ClassVar[Status]  # value = <Status.LicenseCheck: 107>
    LicenseError: typing.ClassVar[Status]  # value = <Status.LicenseError: 106>
    Ok: typing.ClassVar[Status]  # value = <Status.Ok: 100>
    SecurityError: typing.ClassVar[Status]  # value = <Status.SecurityError: 103>
    SerialError: typing.ClassVar[Status]  # value = <Status.SerialError: 102>
    TooManySpoofs: typing.ClassVar[Status]  # value = <Status.TooManySpoofs: 108>
    VersionMismatch: typing.ClassVar[Status]  # value = <Status.VersionMismatch: 104>
    __members__: typing.ClassVar[dict[str, Status]]  # value = {'Ok': <Status.Ok: 100>, 'Error': <Status.Error: 101>, 'SerialError': <Status.SerialError: 102>, 'SecurityError': <Status.SecurityError: 103>, 'VersionMismatch': <Status.VersionMismatch: 104>, 'CrcError': <Status.CrcError: 105>, 'LicenseError': <Status.LicenseError: 106>, 'LicenseCheck': <Status.LicenseCheck: 107>, 'TooManySpoofs': <Status.TooManySpoofs: 108>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class UpdateChecker:
    @staticmethod
    def get_local_release_info(port: str) -> ReleaseInfo:
        """
                    Get device & host release info.
                    Parameters
                    ----------
                    port: str
                        serial port for the device
                    Returns
                    ----------
                    ReleaseInfo
                        local_release_info
        """
    @staticmethod
    def get_remote_release_info() -> ReleaseInfo:
        """
                    Get remote/update release info.,
                    Returns
                    ----------
                    ReleaseInfo
                        remote_release_info
        """
    @staticmethod
    def is_update_available(port: str) -> tuple[bool, ReleaseInfo, ReleaseInfo]:
        """
                    Check if update is available.
                    Parameters
                    ----------
                    port: str
                        serial port for the device
                    Returns
                    ----------
                    tuple[bool, ReleaseInfo, ReleaseInfo]
                        (is_update_available: bool, local_release_info: ReleaseInfo, remote_release_info: ReleaseInfo)
                        Where the bool represents update available if True.
                        First ReleaseInfo is the local device/host and second ReleaseInfo is the remote/server latest version
        """
    def __init__(self) -> None:
        ...
def discover_capture() -> list[int]:
    ...
def discover_devices() -> list[str]:
    ...
def set_log_callback(callback: typing.Callable[[LogLevel, str], None], log_level: LogLevel, do_formatting: bool = True) -> None:
    ...
RSID_FACEPRINTS_VERSION: int = 9
RSID_FEATURES_VECTOR_ALLOC_SIZE: int = 515
RSID_NUM_OF_RECOGNITION_FEATURES: int = 512
__cleanup_logger: typing.Any  # value = <capsule object>
__version__: str = '0.38.2'
compatible_firmware: str = '6.0'
faceprints_version: int = 9
