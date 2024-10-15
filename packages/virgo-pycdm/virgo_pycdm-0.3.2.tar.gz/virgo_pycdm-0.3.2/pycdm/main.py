import signal

from .cfg import Cfg
from .utils import check_valid_board_identifier
from .data_mgr import DataManager
from .cmd_mgr import CmdManager


class CdmCmd:
    def __init__(self, cmd):
        self._cmd = cmd

    def get_info(self):
        return self._cmd.cdm_get_info()

    def get_sm_state(self):
        return self._cmd.cdm_get_state()

    def get_config(self):
        return self._cmd.get_cdm_config()

    def download_file(self, year, month, day, hour, fname, dpath):
        return self._cmd.download_file(year, month, day, hour, fname, dpath)

    def power_on(self, s=""):
        return self._cmd.power_on_ps(s)

    def power_off(self, s=""):
        return self._cmd.power_off_ps(s)

    def get_warnings(self):
        return self._cmd.get_warnings()


class BcgCmd:
    def __init__(self, cmd):
        self._cmd = cmd

    def get_running_partition(self):
        return self._cmd.get_running_partition()

    def get_info(self):
        return self._cmd.get_info()

    def get_voltage(self):
        return self._cmd.get_voltage()

    def get_adc_map(self):
        return self._cmd.get_adc_map()

    def get_config(self):
        return self._cmd.get_configuration()

    def get_state(self):
        return self._cmd.get_state()

    def dump_log(self, idns: list[str]):
        """
        :param idns: List of valid identifiers. Can be any of {R,L} or {R,L}{0,1,2}
        """
        for i in idns:
            check_valid_board_identifier(i)

        return self._cmd.dump_log(idns)

    def hard_reset(self):
        return self._cmd.hard_reset()


class EbisCmd:
    def __init__(self, cmd):
        self._cmd = cmd

    # XXX: Maybe this function should be moved to CDM class as it's the CDM who is connecting to the EBI
    # the EBI is not connecting anywhere
    def connect(self):
        self._cmd.connect()
        return self.version()

    def disconnect(self):
        return self._cmd.disconnect()

    def echo(self, ebi):
        return self._cmd.ebi_echo(ebi)

    def version(self):
        return self._cmd.baffle_get_version()

    def flash_ota(self, file):
        return self._cmd.flash_ebi_ota(file)

    def boot_ota(self):
        return self._cmd.boot_ebi_ota()

    def mark_ota_as_ok(self):
        return self._cmd.mark_ebi_ota_as_ok()


class BsdasCmd:
    def __init__(self, cmd):
        self._cmd = cmd

    def echo(self, ebi: str, bsda: int):
        return self._cmd.bsda_echo(ebi, bsda)

    def boot_ota(self):
        return self._cmd.boot_ota()

    def crash_system(self, idn: str):
        """
        :param idn: A board identifier, it must be one of {R,L}{0,1,2}
        """
        return self._cmd.crash_system(idn)

    def get_coredump(self, idn: str, out_path):
        """
        :param idn: A board identifier, it must be one of {R,L}{0,1,2}
        :param out_path: File where coredump will be saved
        """
        return self._cmd.get_coredump(idn, out_path)

    def prepare_ota(self):
        return self._cmd.prepare_ota()

    def flash_ota(self, file):
        return self._cmd.flash_ota(file)

    def mark_ota_as_ok(self):
        return self._cmd.mark_ota_as_ok()


class PyCDM:
    """
    This class exports only the bare minimum commands needed for the normal operation of the system.
    All other commands are exported by the different classes contained by this one.
    """
    def __init__(self, cdm_addr = ""):
        self._cfg = Cfg()
        if cdm_addr == "":
            cdm_addr = self._cfg.get_cdm_addr()
        self._cmd = CmdManager(cdm_addr)
        self._data = DataManager(cdm_addr)
        signal.signal(signal.SIGINT, self._handler)

        # Commands targeted to CDM
        self.cdm = CdmCmd(self._cmd)

        # Commands targeted to one or more BCG(s)
        self.bcg = BcgCmd(self._cmd)

        # Commands targeted at one or more EBI(s)
        self.ebi = EbisCmd(self._cmd)

        # Commands targeted at one or more BSDA(s)
        self.bsda = BsdasCmd(self._cmd)

    def _handler(self, signum, frame):
        self.close()

    def close(self):
        self._data.close()

    def check_comm(self):
        return self._cmd.check_comm()

    def configure(self, baffle_settings, right_baffle_settings=None):
        return self._cmd.configure(baffle_settings, right_baffle_settings)

    def start_acq(self):
        return self._cmd.start_acq()

    def stop_acq(self):
        return self._cmd.stop_acq()

    def read_pt100(self, ebi: str, bsda: int):
        uv = self._cmd.read_pt100(ebi, bsda)["ans"]
        uva = uv[0]
        uvb = uv[1]

        r1 = 500
        vcc = 3.37
        vdiff = abs(uva-uvb)/1000.0/1000.0

        rpt100 = (r1 * vdiff + 100 * vcc) / (vcc - vdiff)
        return uv, r1, (rpt100 - 100.0) / 0.39083

    def reg_msg(self, s):
        return self._data.register(s)