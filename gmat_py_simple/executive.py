from __future__ import annotations
from typing import Type

import gmat_py_simple.utils
from load_gmat import gmat
from gmat_py_simple import GmatCommand


class Moderator:
    def __init__(self):
        self.gmat_obj = gmat.Moderator.Instance()

    def Initialize(self):
        self.gmat_obj.Initialize()

    def GetDefaultSpacecraft(self) -> gmat.Spacecraft:
        so_config_list: list[str] = self.gmat_obj.GetListOfObjects(gmat.SPACECRAFT)
        if so_config_list:  # list length > 0
            return self.gmat_obj.GetSpacecraft(so_config_list[0])
        else:  # no spacecraft found, so create one
            return self.gmat_obj.CreateSpacecraft('Spacecraft', 'DefaultSC')

    def GetRunState(self):
        rs = self.gmat_obj.GetRunState()
        if rs == 10000:
            return 'IDLE', 10000
        elif rs == 10001:
            return 'RUNNING', 10001
        elif rs == 10002:
            return 'PAUSED', 10002
        else:
            raise Exception(f'Run state not recognised: {rs}')

    def GetDetailedRunState(self):
        drs = self.gmat_obj.GetDetailedRunState()
        if drs == 10000:
            return 'IDLE'
        elif drs == 10001:
            return 'RUNNING'
        elif drs == 10002:
            return 'PAUSED'
        # TODO: add options for optimizer state etc
        else:
            raise Exception(f'Detailed run state not recognised: {drs}')

    def GetSandbox(self):
        return self.gmat_obj.GetSandbox()

    def GetConfiguredObjectMap(self):
        return self.gmat_obj.GetConfiguredObjectMap()

    def CreateDefaultCommand(self, command_type: str = 'Propagate', name: str = ''):
        return self.gmat_obj.CreateDefaultCommand(command_type, name)

    def GetFirstCommand(self):
        return self.gmat_obj.GetFirstCommand()

    def InsertCommand(self, command_to_insert: GmatCommand, preceding_command: GmatCommand):
        return self.gmat_obj.InsertCommand(command_to_insert, preceding_command)

    def AppendCommand(self, command_to_append: Type[GmatCommand]):
        return self.gmat_obj.AppendCommand(command_to_append)

    def RunMission(self):
        return self.gmat_obj.RunMission()

    def GetListOfObjects(self, obj_type: int, exclude_defaults: bool = False, type_max: int = 0):
        return self.gmat_obj.GetListOfObjects(obj_type, exclude_defaults, type_max)

    def CreateDefaultStopCondition(self) -> gmat.StopCondition:
        """

        :return:
        """

        sc: gmat.Spacecraft = self.GetDefaultSpacecraft()
        sc_name: str = sc.GetName()
        epoch_var = f'{sc_name}.A1ModJulian'
        stop_var = f'{sc_name}.ElapsedSecs'

        mod = Moderator()
        if not mod.GetParameter(epoch_var):
            param: gmat.Parameter = mod.gmat_obj.CreateParameter('A1ModJulian', epoch_var)
            param.SetRefObjectName(gmat.SPACECRAFT, sc_name)

        if not mod.GetParameter(stop_var):
            param: gmat.Parameter = mod.gmat_obj.CreateParameter('ElapsedSecs', stop_var)
            param.SetRefObjectName(gmat.SPACECRAFT, sc_name)

        stop_cond: gmat.StopCondition = mod.gmat_obj.CreateStopCondition('StopCondition', f'StopOn{stop_var}')
        stop_cond.SetStringParameter('EpochVar', epoch_var)
        stop_cond.SetStringParameter('StopVar', stop_var)
        stop_cond.SetStringParameter('Goal', '12000.0')
        stop_cond.Help()
        gmat_py_simple.utils.CustomHelp(stop_cond)
        return stop_cond

    def GetParameter(self, param: str) -> gmat.Parameter:
        return self.gmat_obj.GetParameter(param)