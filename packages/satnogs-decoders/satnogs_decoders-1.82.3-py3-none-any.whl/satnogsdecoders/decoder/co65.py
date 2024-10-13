# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Co65(KaitaiStruct):
    """:field v3_3: v3_3
    :field v5: v5
    :field v_batt: v_batt
    :field v_batt_main_bus: v_batt_main_bus
    :field digipeater_mode: digipeater_mode
    :field dtmf_permission: dtmf_permission
    :field antenna_deployment: antenna_deployment
    :field tx_mutual_monitor: tx_mutual_monitor
    :field rx_mutual_monitor: rx_mutual_monitor
    :field usb_enable: usb_enable
    :field satellite_mode: satellite_mode
    :field temp_com_board: temp_com_board
    :field temp_batt: temp_batt
    :field i_batt: i_batt
    :field s_meter_144: s_meter_144
    :field s_meter_1200: s_meter_1200
    :field power_dj_c5_tx: power_dj_c5_tx
    :field power_cw_430_beacon: power_cw_430_beacon
    :field power_th_59_1200_uplink: power_th_59_1200_uplink
    :field power_pda: power_pda
    :field power_daq: power_daq
    :field power_apd_main: power_apd_main
    :field power_apd_3_3b: power_apd_3_3b
    :field power_apd_3_3a: power_apd_3_3a
    
    .. seealso::
       Source - https://web.archive.org/web/20210928003812/http://lss.mes.titech.ac.jp/ssp/cute1.7/cwtelemetry_e.html
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.callsign = (self._io.read_bytes(4)).decode(u"ASCII")
        if not  ((self.callsign == u"CUTE") or (self.callsign == u"cute")) :
            raise kaitaistruct.ValidationNotAnyOfError(self.callsign, self._io, u"/seq/0")
        self.v3_3_raw = self._io.read_u1()
        self.v5_raw = self._io.read_u1()
        self.v_batt_raw = self._io.read_u1()
        self.v_batt_main_bus_raw = self._io.read_u1()
        self.sat_status = self._io.read_u1()
        self.temp_com_board_raw = self._io.read_u1()
        self.temp_batt_raw = self._io.read_u1()
        self.i_batt_raw = self._io.read_u1()
        self.s_meter_144_raw = self._io.read_u1()
        self.s_meter_1200_raw = self._io.read_u1()
        self.fet_status = self._io.read_u1()

    @property
    def power_cw_430_beacon(self):
        if hasattr(self, '_m_power_cw_430_beacon'):
            return self._m_power_cw_430_beacon if hasattr(self, '_m_power_cw_430_beacon') else None

        self._m_power_cw_430_beacon = ((self.fet_status & 2) >> 1)
        return self._m_power_cw_430_beacon if hasattr(self, '_m_power_cw_430_beacon') else None

    @property
    def power_apd_3_3b(self):
        if hasattr(self, '_m_power_apd_3_3b'):
            return self._m_power_apd_3_3b if hasattr(self, '_m_power_apd_3_3b') else None

        self._m_power_apd_3_3b = ((self.fet_status & 64) >> 6)
        return self._m_power_apd_3_3b if hasattr(self, '_m_power_apd_3_3b') else None

    @property
    def v3_3(self):
        if hasattr(self, '_m_v3_3'):
            return self._m_v3_3 if hasattr(self, '_m_v3_3') else None

        self._m_v3_3 = ((self.v3_3_raw * 6.16) / 255)
        return self._m_v3_3 if hasattr(self, '_m_v3_3') else None

    @property
    def power_apd_3_3a(self):
        if hasattr(self, '_m_power_apd_3_3a'):
            return self._m_power_apd_3_3a if hasattr(self, '_m_power_apd_3_3a') else None

        self._m_power_apd_3_3a = ((self.fet_status & 128) >> 7)
        return self._m_power_apd_3_3a if hasattr(self, '_m_power_apd_3_3a') else None

    @property
    def tx_mutual_monitor(self):
        if hasattr(self, '_m_tx_mutual_monitor'):
            return self._m_tx_mutual_monitor if hasattr(self, '_m_tx_mutual_monitor') else None

        self._m_tx_mutual_monitor = ((self.sat_status & 16) >> 4)
        return self._m_tx_mutual_monitor if hasattr(self, '_m_tx_mutual_monitor') else None

    @property
    def s_meter_144(self):
        if hasattr(self, '_m_s_meter_144'):
            return self._m_s_meter_144 if hasattr(self, '_m_s_meter_144') else None

        self._m_s_meter_144 = (((202.972 * self.s_meter_144_raw) / 255) - 171.5)
        return self._m_s_meter_144 if hasattr(self, '_m_s_meter_144') else None

    @property
    def power_pda(self):
        if hasattr(self, '_m_power_pda'):
            return self._m_power_pda if hasattr(self, '_m_power_pda') else None

        self._m_power_pda = ((self.fet_status & 8) >> 3)
        return self._m_power_pda if hasattr(self, '_m_power_pda') else None

    @property
    def v_batt_main_bus(self):
        if hasattr(self, '_m_v_batt_main_bus'):
            return self._m_v_batt_main_bus if hasattr(self, '_m_v_batt_main_bus') else None

        self._m_v_batt_main_bus = ((self.v_batt_main_bus_raw * 9.24) / 255)
        return self._m_v_batt_main_bus if hasattr(self, '_m_v_batt_main_bus') else None

    @property
    def s_meter_1200(self):
        if hasattr(self, '_m_s_meter_1200'):
            return self._m_s_meter_1200 if hasattr(self, '_m_s_meter_1200') else None

        self._m_s_meter_1200 = (((54.824 * self.s_meter_1200_raw) / 255) - 151.9)
        return self._m_s_meter_1200 if hasattr(self, '_m_s_meter_1200') else None

    @property
    def power_daq(self):
        if hasattr(self, '_m_power_daq'):
            return self._m_power_daq if hasattr(self, '_m_power_daq') else None

        self._m_power_daq = ((self.fet_status & 16) >> 4)
        return self._m_power_daq if hasattr(self, '_m_power_daq') else None

    @property
    def temp_com_board(self):
        if hasattr(self, '_m_temp_com_board'):
            return self._m_temp_com_board if hasattr(self, '_m_temp_com_board') else None

        self._m_temp_com_board = ((((3.08 * self.temp_com_board_raw) / 255) - 0.424) / 0.00625)
        return self._m_temp_com_board if hasattr(self, '_m_temp_com_board') else None

    @property
    def power_apd_main(self):
        if hasattr(self, '_m_power_apd_main'):
            return self._m_power_apd_main if hasattr(self, '_m_power_apd_main') else None

        self._m_power_apd_main = ((self.fet_status & 32) >> 5)
        return self._m_power_apd_main if hasattr(self, '_m_power_apd_main') else None

    @property
    def temp_batt(self):
        if hasattr(self, '_m_temp_batt'):
            return self._m_temp_batt if hasattr(self, '_m_temp_batt') else None

        self._m_temp_batt = ((((3.08 * self.temp_batt_raw) / 255) - 0.424) / 0.00625)
        return self._m_temp_batt if hasattr(self, '_m_temp_batt') else None

    @property
    def power_th_59_1200_uplink(self):
        if hasattr(self, '_m_power_th_59_1200_uplink'):
            return self._m_power_th_59_1200_uplink if hasattr(self, '_m_power_th_59_1200_uplink') else None

        self._m_power_th_59_1200_uplink = ((self.fet_status & 4) >> 2)
        return self._m_power_th_59_1200_uplink if hasattr(self, '_m_power_th_59_1200_uplink') else None

    @property
    def rx_mutual_monitor(self):
        if hasattr(self, '_m_rx_mutual_monitor'):
            return self._m_rx_mutual_monitor if hasattr(self, '_m_rx_mutual_monitor') else None

        self._m_rx_mutual_monitor = ((self.sat_status & 32) >> 5)
        return self._m_rx_mutual_monitor if hasattr(self, '_m_rx_mutual_monitor') else None

    @property
    def antenna_deployment(self):
        if hasattr(self, '_m_antenna_deployment'):
            return self._m_antenna_deployment if hasattr(self, '_m_antenna_deployment') else None

        self._m_antenna_deployment = ((self.sat_status & 8) >> 3)
        return self._m_antenna_deployment if hasattr(self, '_m_antenna_deployment') else None

    @property
    def satellite_mode(self):
        if hasattr(self, '_m_satellite_mode'):
            return self._m_satellite_mode if hasattr(self, '_m_satellite_mode') else None

        self._m_satellite_mode = ((self.sat_status & 128) >> 7)
        return self._m_satellite_mode if hasattr(self, '_m_satellite_mode') else None

    @property
    def i_batt(self):
        if hasattr(self, '_m_i_batt'):
            return self._m_i_batt if hasattr(self, '_m_i_batt') else None

        self._m_i_batt = (((-3.08924 * self.i_batt_raw) / 255) + 1.486)
        return self._m_i_batt if hasattr(self, '_m_i_batt') else None

    @property
    def usb_enable(self):
        if hasattr(self, '_m_usb_enable'):
            return self._m_usb_enable if hasattr(self, '_m_usb_enable') else None

        self._m_usb_enable = ((self.sat_status & 64) >> 6)
        return self._m_usb_enable if hasattr(self, '_m_usb_enable') else None

    @property
    def dtmf_permission(self):
        if hasattr(self, '_m_dtmf_permission'):
            return self._m_dtmf_permission if hasattr(self, '_m_dtmf_permission') else None

        self._m_dtmf_permission = ((self.sat_status & 4) >> 2)
        return self._m_dtmf_permission if hasattr(self, '_m_dtmf_permission') else None

    @property
    def digipeater_mode(self):
        if hasattr(self, '_m_digipeater_mode'):
            return self._m_digipeater_mode if hasattr(self, '_m_digipeater_mode') else None

        self._m_digipeater_mode = (self.sat_status & 3)
        return self._m_digipeater_mode if hasattr(self, '_m_digipeater_mode') else None

    @property
    def v5(self):
        if hasattr(self, '_m_v5'):
            return self._m_v5 if hasattr(self, '_m_v5') else None

        self._m_v5 = ((self.v5_raw * 6.16) / 255)
        return self._m_v5 if hasattr(self, '_m_v5') else None

    @property
    def v_batt(self):
        if hasattr(self, '_m_v_batt'):
            return self._m_v_batt if hasattr(self, '_m_v_batt') else None

        self._m_v_batt = ((self.v_batt_raw * 6.16) / 255)
        return self._m_v_batt if hasattr(self, '_m_v_batt') else None

    @property
    def power_dj_c5_tx(self):
        if hasattr(self, '_m_power_dj_c5_tx'):
            return self._m_power_dj_c5_tx if hasattr(self, '_m_power_dj_c5_tx') else None

        self._m_power_dj_c5_tx = (self.fet_status & 1)
        return self._m_power_dj_c5_tx if hasattr(self, '_m_power_dj_c5_tx') else None


