import json
from typing import Any

import cdmpy

from .comm import ZmqSyncConn
from .structs import EbiSettings
from .utils import *

"""
for the list of implemented commands see cmd.cpp:CmdExecutor::execute
"""
class CmdManager:
    def __init__(self, addr):
        self._cdm_cmd = ZmqSyncConn(addr)

    def ebi_echo(self, ebi):
        return self._process_cmd(cdmpy.ebi_echo, {"ebi": ebi})

    def bsda_echo(self, ebi, bsda):
        return self._process_cmd(cdmpy.bsda_echo, {"ebi": ebi, "bsda": bsda})

    def baffle_get_version(self):
        return self._process_cmd(cdmpy.get_version)

    def cdm_get_info(self):
        return self._process_cmd(cdmpy.cdm_version)

    def cdm_get_state(self):
        return cdmpy.SM_STATE(self._process_cmd(cdmpy.get_cdm_state)["state"])

    def connect(self):
        return self._process_cmd(cdmpy.connect)

    def disconnect(self):
        return self._process_cmd(cdmpy.disconnect)

    def configure(self, baffle_settings, right_baffle_settings=None):
        if right_baffle_settings:
            d = {"left": baffle_settings.to_json(), "right": right_baffle_settings.to_json()}
            return self._process_cmd(cdmpy.configure, d)
        else:
            d = {"left": baffle_settings.to_json(), "right": baffle_settings.to_json()}
            return self._process_cmd(cdmpy.configure, d)

    def get_configuration(self):
        s = self._process_cmd(cdmpy.get_config)
        left = EbiSettings().from_json(s["left"])
        right = EbiSettings().from_json(s["right"])
        return left, right

    def start_acq(self):
        return self._process_cmd(cdmpy.start)

    def stop_acq(self):
        return self._process_cmd(cdmpy.stop)

    def check_comm(self):
        return self._process_cmd(cdmpy.check)

    def get_state(self):
        return self._process_cmd(cdmpy.get_state)

    def download_file(self, year, month, day, hour, fname, dpath):
        d = {"year": year, "month": month, "day": day, "hour": hour, "file_name": fname}
        ans = self._process_cmd(cdmpy.download_file, d)
        decode_to_file(ans["file_content"], dpath)
        del ans["file_content"]
        return ans

    def get_cdm_config(self):
        return self._process_cmd(cdmpy.get_cdm_config)

    def hard_reset(self, reset_bsda=False):
        return self._process_cmd(cdmpy.hard_reset, {"reset_bsdas": reset_bsda})

    def crash_system(self, idn: str):
        """
        :param idn: A board identifier, it must be one of {R,L}{0,1,2}
        """
        check_valid_board_identifier(idn)
        return self._process_cmd(cdmpy.crash, {"board_identifier": idn})

    def get_coredump(self, idn: str, out_path):
        """
        :param idn: A board identifier, it must be one of {R,L}{0,1,2}
        :param out_path: File where coredump will be saved
        """
        idn = check_valid_board_identifier(idn)
        # check that a BSDA is select and not only one of the ERBIs
        if len(idn) != 2:
            raise Exception("Invalid board identifier")

        ans = self._process_cmd(cdmpy.get_coredump, {"board_identifier": idn})
        decode_to_file(ans["coredump"], out_path)
        del ans["coredump"]
        return ans

    def dump_log(self, idns):
        for i in idns:
            check_valid_board_identifier(i)

        args = {"board_identifiers": idns}
        ans = self._process_cmd(cdmpy.dump_log, args)

        for k, v in ans.items():
            ans[k] = v.splitlines()

        return ans

    def prepare_ota(self):
        return self._process_cmd(cdmpy.prepare_bsda_ota)

    def flash_ota(self, fname):
        return self._flash(fname, cdmpy.flash_bsda_ota)

    def boot_ota(self):
        return self._process_cmd(cdmpy.boot_bsda_ota)

    def mark_ota_as_ok(self):
        return self._process_cmd(cdmpy.mark_bsda_ota_ok)

    def flash_ebi_ota(self, fname):
        return self._flash(fname, cdmpy.flash_ebi_ota)

    def boot_ebi_ota(self):
        return self._process_cmd(cdmpy.boot_ebi_ota)

    def mark_ebi_ota_as_ok(self):
        return self._process_cmd(cdmpy.mark_ebi_ota_ok)

    def get_running_partitions(self):
        return self._process_cmd(cdmpy.get_partition)

    def get_info(self):
        return self._process_cmd(cdmpy.get_info)

    def get_voltage(self):
        return self._process_cmd(cdmpy.get_voltage)

    def get_adc_map(self):
        return self._process_cmd(cdmpy.get_adc_map)

    def read_pt100(self, ebi: str, bsda: int):
        return self._process_cmd(cdmpy.read_pt100, {"ebi": ebi, "bsda": bsda})

    def power_on_ps(self, s):
        if s != "I_KNOW_WHAT_I_AM_DOING":
            raise Exception("Not allowed to use this method")

        return self._process_cmd(cdmpy.power_on, {"is_engineer": True})

    def power_off_ps(self, s):
        if s != "I_KNOW_WHAT_I_AM_DOING":
            raise Exception("Not allowed to use this method")

        return self._process_cmd(cdmpy.power_off, {"is_engineer": True})

    def get_warnings(self):
        return self._process_cmd(cdmpy.get_warnings)

    def _flash(self, fname, cmd):
        fw, h = encode_from_file(fname)
        args = {"hash": h, "firmware_data": fw.decode()}
        return self._process_cmd(cmd, args)

    def _process_cmd(self, cmd: str, args: dict[str, Any] = {}):
        msg = json.dumps({"cmd": cmd, "args": args})
        self._cdm_cmd.send(msg)

        ans = json.loads(self._cdm_cmd.recv())
        if ans is None:
            return {}

        err = ans.pop("error", None)
        if err is not None:
            raise Exception(err)

        return ans
