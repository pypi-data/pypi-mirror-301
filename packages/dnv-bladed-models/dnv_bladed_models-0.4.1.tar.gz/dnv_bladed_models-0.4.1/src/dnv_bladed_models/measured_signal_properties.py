# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401
from enum import Enum, IntEnum

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Type, Union, Callable  # noqa: F401
from pathlib import Path
from typing import TypeVar
Model = TypeVar('Model', bound='BaseModel')
StrBytes = Union[str, bytes]

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, root_validator, Extra,PrivateAttr  # noqa: F401
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from pydantic.utils import ROOT_KEY
from json import encoder

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.signal_properties_acceleration import SignalPropertiesAcceleration

from dnv_bladed_models.signal_properties_angle import SignalPropertiesAngle

from dnv_bladed_models.signal_properties_angular_acceleration import SignalPropertiesAngularAcceleration

from dnv_bladed_models.signal_properties_angular_velocity import SignalPropertiesAngularVelocity

from dnv_bladed_models.signal_properties_force import SignalPropertiesForce

from dnv_bladed_models.signal_properties_length import SignalPropertiesLength

from dnv_bladed_models.signal_properties_moment import SignalPropertiesMoment

from dnv_bladed_models.signal_properties_power import SignalPropertiesPower

from dnv_bladed_models.signal_properties_velocity import SignalPropertiesVelocity



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class MeasuredSignalProperties(BladedModel):
    r"""
    The noise and transducer properties for those signals representing values coming from a physical sensor.
    
    Not supported yet.
    
    Attributes:
    ----------
    RandomNumberSeed : int, default=0, Not supported yet
        A seed for the random number generator to ensure that subsequent runs have identical noise signatures.

    TurnOffNoise : bool, default=False, Not supported yet
        This allows the noise to be turned off globally.  Note: this turns off noise, but keeps discretisation, sampling time, faults and transducer behaviour.

    ShaftPowerSignals : SignalPropertiesPower, Not supported yet

    RotorSpeedSignals : SignalPropertiesAngularVelocity, Not supported yet

    ElectricalPowerOutputSignals : SignalPropertiesPower, Not supported yet

    GeneratorSpeedSignals : SignalPropertiesAngularVelocity, Not supported yet

    GeneratorTorqueSignals : SignalPropertiesMoment, Not supported yet

    YawBearingAngularPositionSignals : SignalPropertiesAngle, Not supported yet

    YawBearingAngularVelocitySignals : SignalPropertiesAngularVelocity, Not supported yet

    YawBearingAngularAccelerationSignals : SignalPropertiesAngularAcceleration, Not supported yet

    YawMotorRateSignals : SignalPropertiesAngularVelocity, Not supported yet

    YawErrorSignals : SignalPropertiesAngle, Not supported yet

    NacelleAngleFromNorthSignals : SignalPropertiesAngle, Not supported yet

    TowerTopForeAftAccelerationSignals : SignalPropertiesAcceleration, Not supported yet

    TowerTopSideSideAccelerationSignals : SignalPropertiesAcceleration, Not supported yet

    ShaftTorqueSignals : SignalPropertiesMoment, Not supported yet

    YawBearingMySignals : SignalPropertiesMoment, Not supported yet

    YawBearingMzSignals : SignalPropertiesMoment, Not supported yet

    NacelleRollAngleSignals : SignalPropertiesAngle, Not supported yet

    NacelleNoddingAngleSignals : SignalPropertiesAngle, Not supported yet

    NacelleRollAccelerationSignals : SignalPropertiesAngularAcceleration, Not supported yet

    NacelleNoddingAccelerationSignals : SignalPropertiesAngularAcceleration, Not supported yet

    NacelleYawAccelerationSignals : SignalPropertiesAngularAcceleration, Not supported yet

    RotorAzimuthAngleSignals : SignalPropertiesAngle, Not supported yet

    NominalHubFlowSpeedSignals : SignalPropertiesVelocity, Not supported yet

    RotatingHubMySignals : SignalPropertiesMoment, Not supported yet

    RotatingHubMzSignals : SignalPropertiesMoment, Not supported yet

    FixedHubMySignals : SignalPropertiesMoment, Not supported yet

    FixedHubMzSignals : SignalPropertiesMoment, Not supported yet

    FixedHubFxSignals : SignalPropertiesForce, Not supported yet

    FixedHubFySignals : SignalPropertiesForce, Not supported yet

    FixedHubFzSignals : SignalPropertiesForce, Not supported yet

    PitchAngleSignals : SignalPropertiesAngle, Not supported yet

    PitchRateSignals : SignalPropertiesAngularVelocity, Not supported yet

    PitchActuatorTorqueSignals : SignalPropertiesMoment, Not supported yet

    PitchBearingFrictionSignals : SignalPropertiesMoment, Not supported yet

    PitchBearingStictionSignals : SignalPropertiesMoment, Not supported yet

    BladeOutOfPlaneBendingMomentSignals : SignalPropertiesMoment, Not supported yet

    BladeInPlaneBendingMomentSignals : SignalPropertiesMoment, Not supported yet

    PitchBearingMxSignals : SignalPropertiesMoment, Not supported yet

    PitchBearingMySignals : SignalPropertiesMoment, Not supported yet

    PitchBearingMzSignals : SignalPropertiesMoment, Not supported yet

    PitchBearingRadialForceSignals : SignalPropertiesForce, Not supported yet

    PitchBearingAxialForceSignals : SignalPropertiesForce, Not supported yet

    PitchBearingFxSignals : SignalPropertiesForce, Not supported yet

    PitchBearingFySignals : SignalPropertiesForce, Not supported yet

    BladeStationWindSpeedSignals : SignalPropertiesVelocity, Not supported yet

    BladeStationAngleOfAttackSignals : SignalPropertiesAngle, Not supported yet

    AileronAngleSignals : SignalPropertiesAngle, Not supported yet

    AileronRateSignals : SignalPropertiesAngularVelocity, Not supported yet

    BladeStationPositionXSignals : SignalPropertiesLength, Not supported yet

    BladeStationPositionYSignals : SignalPropertiesLength, Not supported yet

    BladeStationPositionZSignals : SignalPropertiesLength, Not supported yet

    BladeStationPositionXRotationSignals : SignalPropertiesAngle, Not supported yet

    BladeStationPositionYRotationSignals : SignalPropertiesAngle, Not supported yet

    BladeStationPositionZRotationSignals : SignalPropertiesAngle, Not supported yet

    LidarBeamFocalPointVelocitySignals : SignalPropertiesVelocity, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Turbine/BladedControl/MeasuredSignalProperties/MeasuredSignalProperties.json')
    
    RandomNumberSeed: Optional[int] = Field(alias="RandomNumberSeed", default=0) # Not supported yet
    TurnOffNoise: Optional[bool] = Field(alias="TurnOffNoise", default=False) # Not supported yet
    ShaftPowerSignals: Optional[SignalPropertiesPower] = Field(alias="ShaftPowerSignals", default=None) # Not supported yet
    RotorSpeedSignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="RotorSpeedSignals", default=None) # Not supported yet
    ElectricalPowerOutputSignals: Optional[SignalPropertiesPower] = Field(alias="ElectricalPowerOutputSignals", default=None) # Not supported yet
    GeneratorSpeedSignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="GeneratorSpeedSignals", default=None) # Not supported yet
    GeneratorTorqueSignals: Optional[SignalPropertiesMoment] = Field(alias="GeneratorTorqueSignals", default=None) # Not supported yet
    YawBearingAngularPositionSignals: Optional[SignalPropertiesAngle] = Field(alias="YawBearingAngularPositionSignals", default=None) # Not supported yet
    YawBearingAngularVelocitySignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="YawBearingAngularVelocitySignals", default=None) # Not supported yet
    YawBearingAngularAccelerationSignals: Optional[SignalPropertiesAngularAcceleration] = Field(alias="YawBearingAngularAccelerationSignals", default=None) # Not supported yet
    YawMotorRateSignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="YawMotorRateSignals", default=None) # Not supported yet
    YawErrorSignals: Optional[SignalPropertiesAngle] = Field(alias="YawErrorSignals", default=None) # Not supported yet
    NacelleAngleFromNorthSignals: Optional[SignalPropertiesAngle] = Field(alias="NacelleAngleFromNorthSignals", default=None) # Not supported yet
    TowerTopForeAftAccelerationSignals: Optional[SignalPropertiesAcceleration] = Field(alias="TowerTopForeAftAccelerationSignals", default=None) # Not supported yet
    TowerTopSideSideAccelerationSignals: Optional[SignalPropertiesAcceleration] = Field(alias="TowerTopSideSideAccelerationSignals", default=None) # Not supported yet
    ShaftTorqueSignals: Optional[SignalPropertiesMoment] = Field(alias="ShaftTorqueSignals", default=None) # Not supported yet
    YawBearingMySignals: Optional[SignalPropertiesMoment] = Field(alias="YawBearingMySignals", default=None) # Not supported yet
    YawBearingMzSignals: Optional[SignalPropertiesMoment] = Field(alias="YawBearingMzSignals", default=None) # Not supported yet
    NacelleRollAngleSignals: Optional[SignalPropertiesAngle] = Field(alias="NacelleRollAngleSignals", default=None) # Not supported yet
    NacelleNoddingAngleSignals: Optional[SignalPropertiesAngle] = Field(alias="NacelleNoddingAngleSignals", default=None) # Not supported yet
    NacelleRollAccelerationSignals: Optional[SignalPropertiesAngularAcceleration] = Field(alias="NacelleRollAccelerationSignals", default=None) # Not supported yet
    NacelleNoddingAccelerationSignals: Optional[SignalPropertiesAngularAcceleration] = Field(alias="NacelleNoddingAccelerationSignals", default=None) # Not supported yet
    NacelleYawAccelerationSignals: Optional[SignalPropertiesAngularAcceleration] = Field(alias="NacelleYawAccelerationSignals", default=None) # Not supported yet
    RotorAzimuthAngleSignals: Optional[SignalPropertiesAngle] = Field(alias="RotorAzimuthAngleSignals", default=None) # Not supported yet
    NominalHubFlowSpeedSignals: Optional[SignalPropertiesVelocity] = Field(alias="NominalHubFlowSpeedSignals", default=None) # Not supported yet
    RotatingHubMySignals: Optional[SignalPropertiesMoment] = Field(alias="RotatingHubMySignals", default=None) # Not supported yet
    RotatingHubMzSignals: Optional[SignalPropertiesMoment] = Field(alias="RotatingHubMzSignals", default=None) # Not supported yet
    FixedHubMySignals: Optional[SignalPropertiesMoment] = Field(alias="FixedHubMySignals", default=None) # Not supported yet
    FixedHubMzSignals: Optional[SignalPropertiesMoment] = Field(alias="FixedHubMzSignals", default=None) # Not supported yet
    FixedHubFxSignals: Optional[SignalPropertiesForce] = Field(alias="FixedHubFxSignals", default=None) # Not supported yet
    FixedHubFySignals: Optional[SignalPropertiesForce] = Field(alias="FixedHubFySignals", default=None) # Not supported yet
    FixedHubFzSignals: Optional[SignalPropertiesForce] = Field(alias="FixedHubFzSignals", default=None) # Not supported yet
    PitchAngleSignals: Optional[SignalPropertiesAngle] = Field(alias="PitchAngleSignals", default=None) # Not supported yet
    PitchRateSignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="PitchRateSignals", default=None) # Not supported yet
    PitchActuatorTorqueSignals: Optional[SignalPropertiesMoment] = Field(alias="PitchActuatorTorqueSignals", default=None) # Not supported yet
    PitchBearingFrictionSignals: Optional[SignalPropertiesMoment] = Field(alias="PitchBearingFrictionSignals", default=None) # Not supported yet
    PitchBearingStictionSignals: Optional[SignalPropertiesMoment] = Field(alias="PitchBearingStictionSignals", default=None) # Not supported yet
    BladeOutOfPlaneBendingMomentSignals: Optional[SignalPropertiesMoment] = Field(alias="BladeOutOfPlaneBendingMomentSignals", default=None) # Not supported yet
    BladeInPlaneBendingMomentSignals: Optional[SignalPropertiesMoment] = Field(alias="BladeInPlaneBendingMomentSignals", default=None) # Not supported yet
    PitchBearingMxSignals: Optional[SignalPropertiesMoment] = Field(alias="PitchBearingMxSignals", default=None) # Not supported yet
    PitchBearingMySignals: Optional[SignalPropertiesMoment] = Field(alias="PitchBearingMySignals", default=None) # Not supported yet
    PitchBearingMzSignals: Optional[SignalPropertiesMoment] = Field(alias="PitchBearingMzSignals", default=None) # Not supported yet
    PitchBearingRadialForceSignals: Optional[SignalPropertiesForce] = Field(alias="PitchBearingRadialForceSignals", default=None) # Not supported yet
    PitchBearingAxialForceSignals: Optional[SignalPropertiesForce] = Field(alias="PitchBearingAxialForceSignals", default=None) # Not supported yet
    PitchBearingFxSignals: Optional[SignalPropertiesForce] = Field(alias="PitchBearingFxSignals", default=None) # Not supported yet
    PitchBearingFySignals: Optional[SignalPropertiesForce] = Field(alias="PitchBearingFySignals", default=None) # Not supported yet
    BladeStationWindSpeedSignals: Optional[SignalPropertiesVelocity] = Field(alias="BladeStationWindSpeedSignals", default=None) # Not supported yet
    BladeStationAngleOfAttackSignals: Optional[SignalPropertiesAngle] = Field(alias="BladeStationAngleOfAttackSignals", default=None) # Not supported yet
    AileronAngleSignals: Optional[SignalPropertiesAngle] = Field(alias="AileronAngleSignals", default=None) # Not supported yet
    AileronRateSignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="AileronRateSignals", default=None) # Not supported yet
    BladeStationPositionXSignals: Optional[SignalPropertiesLength] = Field(alias="BladeStationPositionXSignals", default=None) # Not supported yet
    BladeStationPositionYSignals: Optional[SignalPropertiesLength] = Field(alias="BladeStationPositionYSignals", default=None) # Not supported yet
    BladeStationPositionZSignals: Optional[SignalPropertiesLength] = Field(alias="BladeStationPositionZSignals", default=None) # Not supported yet
    BladeStationPositionXRotationSignals: Optional[SignalPropertiesAngle] = Field(alias="BladeStationPositionXRotationSignals", default=None) # Not supported yet
    BladeStationPositionYRotationSignals: Optional[SignalPropertiesAngle] = Field(alias="BladeStationPositionYRotationSignals", default=None) # Not supported yet
    BladeStationPositionZRotationSignals: Optional[SignalPropertiesAngle] = Field(alias="BladeStationPositionZRotationSignals", default=None) # Not supported yet
    LidarBeamFocalPointVelocitySignals: Optional[SignalPropertiesVelocity] = Field(alias="LidarBeamFocalPointVelocitySignals", default=None) # Not supported yet

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass



    def to_json(self, indent: Optional[int] = 2, **json_kwargs: Any) -> str:
        r"""
        Generates a JSON string representation of the model.

        Parameters
        ----------
        indent : int
            The whitespace indentation to use for formatting, as per json.dumps().

        Examples
        --------
        >>> model.to_json()
        Renders the full JSON representation of the model object.
        """

        json_kwargs['by_alias'] = True
        json_kwargs['exclude_unset'] = False
        json_kwargs['exclude_none'] = True
        if self.Schema is None:
            self.Schema = SchemaHelper.construct_schema_url(self._relative_schema_path)
        
        return super().json(indent=indent, **json_kwargs)


    @classmethod
    def from_file(cls: Type['Model'], path: Union[str, Path]) -> 'Model':
        r"""
        Loads a model from a given file path.

        Parameters
        ----------
        path : string
            The file path to the model.

        Returns
        -------
        MeasuredSignalProperties
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = MeasuredSignalProperties.from_file('/path/to/file')
        """
        
        return super().parse_file(path=path)


    @classmethod
    def from_json(cls: Type['Model'], b: StrBytes) -> 'Model':
        r"""
        Creates a model object from a JSON string.

        Parameters
        ----------
        b: StrBytes
            The JSON string describing the model.

        Returns
        -------
        MeasuredSignalProperties
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = MeasuredSignalProperties.from_json('{ ... }')
        """

        return super().parse_raw(
            b=b,
            content_type='application/json')
        

    @classmethod
    def from_dict(cls: Type['Model'], obj: Any) -> 'Model':
        r"""
        Creates a model object from a dict.
        
        Parameters
        ----------
        obj : Any
            The dictionary object describing the model.

        Returns
        -------
        MeasuredSignalProperties
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.
        """
        
        return super().parse_obj(obj=obj)


    def to_file(self, path: Union[str, Path]):
        r"""
        Writes the model as a JSON document to a file with UTF8 encoding.

        Parameters
        ----------                
        path : string
            The file path to which the model will be written.

        Examples
        --------
        >>> model.to_file('/path/to/file')
        """

        with open(file=path, mode='w', encoding="utf8") as output_file:
            output_file.write(self.to_json())


MeasuredSignalProperties.update_forward_refs()
