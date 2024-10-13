# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Grbbeta(KaitaiStruct):
    """:field uptime_total: id1.id2.uptime_total
    :field radio_boot_count: id1.id2.radio_boot_count
    :field radio_mcu_act_temperature: id1.id2.radio_mcu_act_temperature
    :field rf_power_amplifier_act_temperature: id1.id2.rf_power_amplifier_act_temperature
    :field cw_beacon: id1.id2.cw_beacon
    :field digi_dest_callsign: id1.id2.id3.ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field digi_src_callsign: id1.id2.id3.ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field digi_src_ssid: id1.id2.id3.ax25_frame.ax25_header.src_ssid_raw.ssid
    :field digi_dest_ssid: id1.id2.id3.ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field rpt_instance___callsign: id1.id2.id3.ax25_frame.ax25_header.repeater.rpt_instance.___.rpt_callsign_raw.callsign_ror.callsign
    :field rpt_instance___ssid: id1.id2.id3.ax25_frame.ax25_header.repeater.rpt_instance.___.rpt_ssid_raw.ssid
    :field rpt_instance___hbit: id1.id2.id3.ax25_frame.ax25_header.repeater.rpt_instance.___.rpt_ssid_raw.hbit
    :field digi_ctl: id1.id2.id3.ax25_frame.ax25_header.ctl
    :field digi_pid: id1.id2.id3.ax25_frame.ax25_header.pid
    :field digi_message: id1.id2.id3.ax25_frame.digi_message
    :field uhf_uptime_since_reset: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_uptime_since_reset
    :field uhf_uptime_total: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_uptime_total
    :field uhf_radio_boot_count: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_radio_boot_count
    :field uhf_rf_segment_reset_count: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_rf_segment_reset_count
    :field uhf_radio_mcu_act_temperature: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_radio_mcu_act_temperature
    :field uhf_rf_chip_act_temperature: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_rf_chip_act_temperature
    :field uhf_rf_power_amplifier_act_temperature: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_rf_power_amplifier_act_temperature
    :field uhf_digipeater_forwarded_message_count: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_digipeater_forwarded_message_count
    :field uhf_last_digipeater_user_sender_s_callsign: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_last_digipeater_user_sender_s_callsign
    :field uhf_rx_data_packets: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_rx_data_packets
    :field uhf_tx_data_packets: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_tx_data_packets
    :field uhf_actual_rssi: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_actual_rssi
    :field uhf_value_of_rssi_when_carrier_detected: id1.id2.id3.id4.ax25_frame.ax25_payload.uhf_value_of_rssi_when_carrier_detected
    :field vhf_uptime_since_reset: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_uptime_since_reset
    :field vhf_uptime_total: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_uptime_total
    :field vhf_radio_boot_count: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_radio_boot_count
    :field vhf_rf_segment_reset_count: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_rf_segment_reset_count
    :field vhf_radio_mcu_act_temperature: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_radio_mcu_act_temperature
    :field vhf_rf_chip_act_temperature: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_rf_chip_act_temperature
    :field vhf_rf_power_amplifier_act_temperature: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_rf_power_amplifier_act_temperature
    :field vhf_digipeater_forwarded_message_count: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_digipeater_forwarded_message_count
    :field vhf_last_digipeater_user_sender_s_callsign: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_last_digipeater_user_sender_s_callsign
    :field vhf_rx_data_packets: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_rx_data_packets
    :field vhf_tx_data_packets: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_tx_data_packets
    :field vhf_actual_rssi: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_actual_rssi
    :field vhf_value_of_rssi_when_carrier_detected: id1.id2.id3.id4.ax25_frame.ax25_payload.vhf_value_of_rssi_when_carrier_detected
    :field message: id1.id2.id3.id4.id5.ax25_frame.message
    
    .. seealso::
       Source - https://grbbeta.tuke.sk/index.php/en/home/
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.id1 = Grbbeta.Type1(self._io, self, self._root)

    class NotCwMessage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self.message_type2
            if _on == 2424464526:
                self.id3 = Grbbeta.Digi(self._io, self, self._root)
            else:
                self.id3 = Grbbeta.NotDigi(self._io, self, self._root)

        @property
        def message_type2(self):
            if hasattr(self, '_m_message_type2'):
                return self._m_message_type2 if hasattr(self, '_m_message_type2') else None

            _pos = self._io.pos()
            self._io.seek(14)
            self._m_message_type2 = self._io.read_u4be()
            self._io.seek(_pos)
            return self._m_message_type2 if hasattr(self, '_m_message_type2') else None


    class Type1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self.message_type1
            if _on == 7234224009119950706:
                self.id2 = Grbbeta.CwMessage(self._io, self, self._root)
            else:
                self.id2 = Grbbeta.NotCwMessage(self._io, self, self._root)

        @property
        def message_type1(self):
            if hasattr(self, '_m_message_type1'):
                return self._m_message_type1 if hasattr(self, '_m_message_type1') else None

            _pos = self._io.pos()
            self._io.seek(0)
            self._m_message_type1 = self._io.read_u8be()
            self._io.seek(_pos)
            return self._m_message_type1 if hasattr(self, '_m_message_type1') else None


    class BeaconVhf(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_frame = Grbbeta.BeaconVhf.Ax25Frame(self._io, self, self._root)

        class Ax25Frame(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.ax25_header = Grbbeta.BeaconVhf.Ax25Header(self._io, self, self._root)
                self.ax25_payload = Grbbeta.BeaconVhf.Ax25Payload(self._io, self, self._root)


        class Ax25Payload(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.vhf_beacon_identification = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_uptime_since_reset_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_uptime_total_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_radio_boot_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_rf_segment_reset_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_radio_mcu_act_temperature_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_rf_chip_act_temperature_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_rf_power_amplifier_act_temperature_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_digipeater_forwarded_message_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_last_digipeater_user_sender_s_callsign = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_rx_data_packets_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_tx_data_packets_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_actual_rssi_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.vhf_value_of_rssi_when_carrier_detected_raw = (self._io.read_bytes_term(0, False, True, True)).decode(u"utf8")

            @property
            def vhf_uptime_since_reset(self):
                if hasattr(self, '_m_vhf_uptime_since_reset'):
                    return self._m_vhf_uptime_since_reset if hasattr(self, '_m_vhf_uptime_since_reset') else None

                self._m_vhf_uptime_since_reset = int(self.vhf_uptime_since_reset_raw)
                return self._m_vhf_uptime_since_reset if hasattr(self, '_m_vhf_uptime_since_reset') else None

            @property
            def vhf_digipeater_forwarded_message_count(self):
                if hasattr(self, '_m_vhf_digipeater_forwarded_message_count'):
                    return self._m_vhf_digipeater_forwarded_message_count if hasattr(self, '_m_vhf_digipeater_forwarded_message_count') else None

                self._m_vhf_digipeater_forwarded_message_count = int(self.vhf_digipeater_forwarded_message_count_raw)
                return self._m_vhf_digipeater_forwarded_message_count if hasattr(self, '_m_vhf_digipeater_forwarded_message_count') else None

            @property
            def vhf_radio_boot_count(self):
                if hasattr(self, '_m_vhf_radio_boot_count'):
                    return self._m_vhf_radio_boot_count if hasattr(self, '_m_vhf_radio_boot_count') else None

                self._m_vhf_radio_boot_count = int(self.vhf_radio_boot_count_raw)
                return self._m_vhf_radio_boot_count if hasattr(self, '_m_vhf_radio_boot_count') else None

            @property
            def vhf_value_of_rssi_when_carrier_detected(self):
                if hasattr(self, '_m_vhf_value_of_rssi_when_carrier_detected'):
                    return self._m_vhf_value_of_rssi_when_carrier_detected if hasattr(self, '_m_vhf_value_of_rssi_when_carrier_detected') else None

                self._m_vhf_value_of_rssi_when_carrier_detected = int(self.vhf_value_of_rssi_when_carrier_detected_raw)
                return self._m_vhf_value_of_rssi_when_carrier_detected if hasattr(self, '_m_vhf_value_of_rssi_when_carrier_detected') else None

            @property
            def vhf_tx_data_packets(self):
                if hasattr(self, '_m_vhf_tx_data_packets'):
                    return self._m_vhf_tx_data_packets if hasattr(self, '_m_vhf_tx_data_packets') else None

                self._m_vhf_tx_data_packets = int(self.vhf_tx_data_packets_raw)
                return self._m_vhf_tx_data_packets if hasattr(self, '_m_vhf_tx_data_packets') else None

            @property
            def vhf_radio_mcu_act_temperature(self):
                if hasattr(self, '_m_vhf_radio_mcu_act_temperature'):
                    return self._m_vhf_radio_mcu_act_temperature if hasattr(self, '_m_vhf_radio_mcu_act_temperature') else None

                self._m_vhf_radio_mcu_act_temperature = int(self.vhf_radio_mcu_act_temperature_raw)
                return self._m_vhf_radio_mcu_act_temperature if hasattr(self, '_m_vhf_radio_mcu_act_temperature') else None

            @property
            def vhf_rf_chip_act_temperature(self):
                if hasattr(self, '_m_vhf_rf_chip_act_temperature'):
                    return self._m_vhf_rf_chip_act_temperature if hasattr(self, '_m_vhf_rf_chip_act_temperature') else None

                self._m_vhf_rf_chip_act_temperature = int(self.vhf_rf_chip_act_temperature_raw)
                return self._m_vhf_rf_chip_act_temperature if hasattr(self, '_m_vhf_rf_chip_act_temperature') else None

            @property
            def vhf_rf_power_amplifier_act_temperature(self):
                if hasattr(self, '_m_vhf_rf_power_amplifier_act_temperature'):
                    return self._m_vhf_rf_power_amplifier_act_temperature if hasattr(self, '_m_vhf_rf_power_amplifier_act_temperature') else None

                self._m_vhf_rf_power_amplifier_act_temperature = int(self.vhf_rf_power_amplifier_act_temperature_raw)
                return self._m_vhf_rf_power_amplifier_act_temperature if hasattr(self, '_m_vhf_rf_power_amplifier_act_temperature') else None

            @property
            def vhf_rx_data_packets(self):
                if hasattr(self, '_m_vhf_rx_data_packets'):
                    return self._m_vhf_rx_data_packets if hasattr(self, '_m_vhf_rx_data_packets') else None

                self._m_vhf_rx_data_packets = int(self.vhf_rx_data_packets_raw)
                return self._m_vhf_rx_data_packets if hasattr(self, '_m_vhf_rx_data_packets') else None

            @property
            def vhf_actual_rssi(self):
                if hasattr(self, '_m_vhf_actual_rssi'):
                    return self._m_vhf_actual_rssi if hasattr(self, '_m_vhf_actual_rssi') else None

                self._m_vhf_actual_rssi = int(self.vhf_actual_rssi_raw)
                return self._m_vhf_actual_rssi if hasattr(self, '_m_vhf_actual_rssi') else None

            @property
            def vhf_rf_segment_reset_count(self):
                if hasattr(self, '_m_vhf_rf_segment_reset_count'):
                    return self._m_vhf_rf_segment_reset_count if hasattr(self, '_m_vhf_rf_segment_reset_count') else None

                self._m_vhf_rf_segment_reset_count = int(self.vhf_rf_segment_reset_count_raw)
                return self._m_vhf_rf_segment_reset_count if hasattr(self, '_m_vhf_rf_segment_reset_count') else None

            @property
            def vhf_uptime_total(self):
                if hasattr(self, '_m_vhf_uptime_total'):
                    return self._m_vhf_uptime_total if hasattr(self, '_m_vhf_uptime_total') else None

                self._m_vhf_uptime_total = int(self.vhf_uptime_total_raw)
                return self._m_vhf_uptime_total if hasattr(self, '_m_vhf_uptime_total') else None


        class Ax25Header(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.dest_callsign_raw = Grbbeta.BeaconVhf.CallsignRaw(self._io, self, self._root)
                self.dest_ssid_raw = Grbbeta.BeaconVhf.SsidMask(self._io, self, self._root)
                self.src_callsign_raw = Grbbeta.BeaconVhf.CallsignRaw(self._io, self, self._root)
                self.src_ssid_raw = Grbbeta.BeaconVhf.SsidMask(self._io, self, self._root)
                self.ctl = self._io.read_u1()
                self.pid = self._io.read_u1()


        class Callsign(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


        class SsidMask(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.ssid_mask = self._io.read_u1()

            @property
            def ssid(self):
                if hasattr(self, '_m_ssid'):
                    return self._m_ssid if hasattr(self, '_m_ssid') else None

                self._m_ssid = ((self.ssid_mask & 15) >> 1)
                return self._m_ssid if hasattr(self, '_m_ssid') else None


        class CallsignRaw(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self._raw__raw_callsign_ror = self._io.read_bytes(6)
                self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
                _io__raw_callsign_ror = KaitaiStream(BytesIO(self._raw_callsign_ror))
                self.callsign_ror = Grbbeta.BeaconVhf.Callsign(_io__raw_callsign_ror, self, self._root)



    class CwMessage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.de_ha2grb = (self._io.read_bytes(13)).decode(u"ASCII")
            if not  ((self.de_ha2grb == u"de ha2grb = u") or (self.de_ha2grb == u"DE HA2GRB = U")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.de_ha2grb, self._io, u"/types/cw_message/seq/0")
            self.uptime_total_raw = (self._io.read_bytes_term(114, False, True, True)).decode(u"UTF-8")
            self.radio_boot_count_raw = (self._io.read_bytes_term(116, False, True, True)).decode(u"UTF-8")
            self.radio_mcu_act_temperature_raw = (self._io.read_bytes_term(112, False, True, True)).decode(u"UTF-8")
            self.rf_power_amplifier_act_temperature_raw = (self._io.read_bytes_term(32, False, True, True)).decode(u"UTF-8")

        @property
        def uptime_total(self):
            if hasattr(self, '_m_uptime_total'):
                return self._m_uptime_total if hasattr(self, '_m_uptime_total') else None

            self._m_uptime_total = (int(self.uptime_total_raw) * 60)
            return self._m_uptime_total if hasattr(self, '_m_uptime_total') else None

        @property
        def radio_boot_count(self):
            if hasattr(self, '_m_radio_boot_count'):
                return self._m_radio_boot_count if hasattr(self, '_m_radio_boot_count') else None

            self._m_radio_boot_count = int(self.radio_boot_count_raw)
            return self._m_radio_boot_count if hasattr(self, '_m_radio_boot_count') else None

        @property
        def cw_beacon(self):
            if hasattr(self, '_m_cw_beacon'):
                return self._m_cw_beacon if hasattr(self, '_m_cw_beacon') else None

            self._m_cw_beacon = u"de ha2grb = u" + self.uptime_total_raw + u"r" + self.radio_boot_count_raw + u"t" + self.radio_mcu_act_temperature_raw + u"p" + self.rf_power_amplifier_act_temperature_raw + u" ar"
            return self._m_cw_beacon if hasattr(self, '_m_cw_beacon') else None

        @property
        def rf_power_amplifier_act_temperature(self):
            if hasattr(self, '_m_rf_power_amplifier_act_temperature'):
                return self._m_rf_power_amplifier_act_temperature if hasattr(self, '_m_rf_power_amplifier_act_temperature') else None

            self._m_rf_power_amplifier_act_temperature = int(self.rf_power_amplifier_act_temperature_raw)
            return self._m_rf_power_amplifier_act_temperature if hasattr(self, '_m_rf_power_amplifier_act_temperature') else None

        @property
        def radio_mcu_act_temperature(self):
            if hasattr(self, '_m_radio_mcu_act_temperature'):
                return self._m_radio_mcu_act_temperature if hasattr(self, '_m_radio_mcu_act_temperature') else None

            self._m_radio_mcu_act_temperature = int(self.radio_mcu_act_temperature_raw)
            return self._m_radio_mcu_act_temperature if hasattr(self, '_m_radio_mcu_act_temperature') else None


    class BeaconUhf(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_frame = Grbbeta.BeaconUhf.Ax25Frame(self._io, self, self._root)

        class Ax25Frame(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.ax25_header = Grbbeta.BeaconUhf.Ax25Header(self._io, self, self._root)
                self.ax25_payload = Grbbeta.BeaconUhf.Ax25Payload(self._io, self, self._root)


        class Ax25Payload(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.uhf_beacon_identification = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_uptime_since_reset_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_uptime_total_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_radio_boot_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_rf_segment_reset_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_radio_mcu_act_temperature_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_rf_chip_act_temperature_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_rf_power_amplifier_act_temperature_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_digipeater_forwarded_message_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_last_digipeater_user_sender_s_callsign = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_rx_data_packets_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_tx_data_packets_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_actual_rssi_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
                self.uhf_value_of_rssi_when_carrier_detected_raw = (self._io.read_bytes_term(0, False, True, True)).decode(u"utf8")

            @property
            def uhf_radio_mcu_act_temperature(self):
                if hasattr(self, '_m_uhf_radio_mcu_act_temperature'):
                    return self._m_uhf_radio_mcu_act_temperature if hasattr(self, '_m_uhf_radio_mcu_act_temperature') else None

                self._m_uhf_radio_mcu_act_temperature = int(self.uhf_radio_mcu_act_temperature_raw)
                return self._m_uhf_radio_mcu_act_temperature if hasattr(self, '_m_uhf_radio_mcu_act_temperature') else None

            @property
            def uhf_uptime_total(self):
                if hasattr(self, '_m_uhf_uptime_total'):
                    return self._m_uhf_uptime_total if hasattr(self, '_m_uhf_uptime_total') else None

                self._m_uhf_uptime_total = int(self.uhf_uptime_total_raw)
                return self._m_uhf_uptime_total if hasattr(self, '_m_uhf_uptime_total') else None

            @property
            def uhf_tx_data_packets(self):
                if hasattr(self, '_m_uhf_tx_data_packets'):
                    return self._m_uhf_tx_data_packets if hasattr(self, '_m_uhf_tx_data_packets') else None

                self._m_uhf_tx_data_packets = int(self.uhf_tx_data_packets_raw)
                return self._m_uhf_tx_data_packets if hasattr(self, '_m_uhf_tx_data_packets') else None

            @property
            def uhf_value_of_rssi_when_carrier_detected(self):
                if hasattr(self, '_m_uhf_value_of_rssi_when_carrier_detected'):
                    return self._m_uhf_value_of_rssi_when_carrier_detected if hasattr(self, '_m_uhf_value_of_rssi_when_carrier_detected') else None

                self._m_uhf_value_of_rssi_when_carrier_detected = int(self.uhf_value_of_rssi_when_carrier_detected_raw)
                return self._m_uhf_value_of_rssi_when_carrier_detected if hasattr(self, '_m_uhf_value_of_rssi_when_carrier_detected') else None

            @property
            def uhf_actual_rssi(self):
                if hasattr(self, '_m_uhf_actual_rssi'):
                    return self._m_uhf_actual_rssi if hasattr(self, '_m_uhf_actual_rssi') else None

                self._m_uhf_actual_rssi = int(self.uhf_actual_rssi_raw)
                return self._m_uhf_actual_rssi if hasattr(self, '_m_uhf_actual_rssi') else None

            @property
            def uhf_rf_segment_reset_count(self):
                if hasattr(self, '_m_uhf_rf_segment_reset_count'):
                    return self._m_uhf_rf_segment_reset_count if hasattr(self, '_m_uhf_rf_segment_reset_count') else None

                self._m_uhf_rf_segment_reset_count = int(self.uhf_rf_segment_reset_count_raw)
                return self._m_uhf_rf_segment_reset_count if hasattr(self, '_m_uhf_rf_segment_reset_count') else None

            @property
            def uhf_rf_chip_act_temperature(self):
                if hasattr(self, '_m_uhf_rf_chip_act_temperature'):
                    return self._m_uhf_rf_chip_act_temperature if hasattr(self, '_m_uhf_rf_chip_act_temperature') else None

                self._m_uhf_rf_chip_act_temperature = int(self.uhf_rf_chip_act_temperature_raw)
                return self._m_uhf_rf_chip_act_temperature if hasattr(self, '_m_uhf_rf_chip_act_temperature') else None

            @property
            def uhf_rx_data_packets(self):
                if hasattr(self, '_m_uhf_rx_data_packets'):
                    return self._m_uhf_rx_data_packets if hasattr(self, '_m_uhf_rx_data_packets') else None

                self._m_uhf_rx_data_packets = int(self.uhf_rx_data_packets_raw)
                return self._m_uhf_rx_data_packets if hasattr(self, '_m_uhf_rx_data_packets') else None

            @property
            def uhf_uptime_since_reset(self):
                if hasattr(self, '_m_uhf_uptime_since_reset'):
                    return self._m_uhf_uptime_since_reset if hasattr(self, '_m_uhf_uptime_since_reset') else None

                self._m_uhf_uptime_since_reset = int(self.uhf_uptime_since_reset_raw)
                return self._m_uhf_uptime_since_reset if hasattr(self, '_m_uhf_uptime_since_reset') else None

            @property
            def uhf_digipeater_forwarded_message_count(self):
                if hasattr(self, '_m_uhf_digipeater_forwarded_message_count'):
                    return self._m_uhf_digipeater_forwarded_message_count if hasattr(self, '_m_uhf_digipeater_forwarded_message_count') else None

                self._m_uhf_digipeater_forwarded_message_count = int(self.uhf_digipeater_forwarded_message_count_raw)
                return self._m_uhf_digipeater_forwarded_message_count if hasattr(self, '_m_uhf_digipeater_forwarded_message_count') else None

            @property
            def uhf_rf_power_amplifier_act_temperature(self):
                if hasattr(self, '_m_uhf_rf_power_amplifier_act_temperature'):
                    return self._m_uhf_rf_power_amplifier_act_temperature if hasattr(self, '_m_uhf_rf_power_amplifier_act_temperature') else None

                self._m_uhf_rf_power_amplifier_act_temperature = int(self.uhf_rf_power_amplifier_act_temperature_raw)
                return self._m_uhf_rf_power_amplifier_act_temperature if hasattr(self, '_m_uhf_rf_power_amplifier_act_temperature') else None

            @property
            def uhf_radio_boot_count(self):
                if hasattr(self, '_m_uhf_radio_boot_count'):
                    return self._m_uhf_radio_boot_count if hasattr(self, '_m_uhf_radio_boot_count') else None

                self._m_uhf_radio_boot_count = int(self.uhf_radio_boot_count_raw)
                return self._m_uhf_radio_boot_count if hasattr(self, '_m_uhf_radio_boot_count') else None


        class Ax25Header(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.dest_callsign_raw = Grbbeta.BeaconUhf.CallsignRaw(self._io, self, self._root)
                self.dest_ssid_raw = Grbbeta.BeaconUhf.SsidMask(self._io, self, self._root)
                self.src_callsign_raw = Grbbeta.BeaconUhf.CallsignRaw(self._io, self, self._root)
                self.src_ssid_raw = Grbbeta.BeaconUhf.SsidMask(self._io, self, self._root)
                self.ctl = self._io.read_u1()
                self.pid = self._io.read_u1()


        class Callsign(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


        class SsidMask(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.ssid_mask = self._io.read_u1()

            @property
            def ssid(self):
                if hasattr(self, '_m_ssid'):
                    return self._m_ssid if hasattr(self, '_m_ssid') else None

                self._m_ssid = ((self.ssid_mask & 15) >> 1)
                return self._m_ssid if hasattr(self, '_m_ssid') else None


        class CallsignRaw(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self._raw__raw_callsign_ror = self._io.read_bytes(6)
                self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
                _io__raw_callsign_ror = KaitaiStream(BytesIO(self._raw_callsign_ror))
                self.callsign_ror = Grbbeta.BeaconUhf.Callsign(_io__raw_callsign_ror, self, self._root)



    class NotBeacon(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self.message_type4
            if _on == 2220950512:
                self.id5 = Grbbeta.Msg(self._io, self, self._root)

        @property
        def message_type4(self):
            if hasattr(self, '_m_message_type4'):
                return self._m_message_type4 if hasattr(self, '_m_message_type4') else None

            _pos = self._io.pos()
            self._io.seek(12)
            self._m_message_type4 = self._io.read_u4be()
            self._io.seek(_pos)
            return self._m_message_type4 if hasattr(self, '_m_message_type4') else None


    class Msg(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_frame = Grbbeta.Msg.Ax25Frame(self._io, self, self._root)

        class Ax25Frame(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.ax25_header = Grbbeta.Msg.Ax25Header(self._io, self, self._root)
                self.message = (self._io.read_bytes_full()).decode(u"utf-8")


        class Ax25Header(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.dest_callsign_raw = Grbbeta.Msg.CallsignRaw(self._io, self, self._root)
                self.dest_ssid_raw = Grbbeta.Msg.SsidMask(self._io, self, self._root)
                self.src_callsign_raw = Grbbeta.Msg.CallsignRaw(self._io, self, self._root)
                self.src_ssid_raw = Grbbeta.Msg.SsidMask(self._io, self, self._root)
                self.ctl = self._io.read_u1()
                self.pid = self._io.read_u1()


        class Callsign(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


        class SsidMask(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.ssid_mask = self._io.read_u1()

            @property
            def ssid(self):
                if hasattr(self, '_m_ssid'):
                    return self._m_ssid if hasattr(self, '_m_ssid') else None

                self._m_ssid = ((self.ssid_mask & 15) >> 1)
                return self._m_ssid if hasattr(self, '_m_ssid') else None

            @property
            def hbit(self):
                if hasattr(self, '_m_hbit'):
                    return self._m_hbit if hasattr(self, '_m_hbit') else None

                self._m_hbit = ((self.ssid_mask & 128) >> 7)
                return self._m_hbit if hasattr(self, '_m_hbit') else None


        class CallsignRaw(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self._raw__raw_callsign_ror = self._io.read_bytes(6)
                self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
                _io__raw_callsign_ror = KaitaiStream(BytesIO(self._raw_callsign_ror))
                self.callsign_ror = Grbbeta.Msg.Callsign(_io__raw_callsign_ror, self, self._root)



    class Digi(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_frame = Grbbeta.Digi.Ax25Frame(self._io, self, self._root)

        class Ax25Frame(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.ax25_header = Grbbeta.Digi.Ax25Header(self._io, self, self._root)
                self.digi_message = (self._io.read_bytes_full()).decode(u"utf-8")


        class Ax25Header(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.dest_callsign_raw = Grbbeta.Digi.CallsignRaw(self._io, self, self._root)
                self.dest_ssid_raw = Grbbeta.Digi.SsidMask(self._io, self, self._root)
                self.src_callsign_raw = Grbbeta.Digi.CallsignRaw(self._io, self, self._root)
                self.src_ssid_raw = Grbbeta.Digi.SsidMask(self._io, self, self._root)
                if (self.src_ssid_raw.ssid_mask & 1) == 0:
                    self.repeater = Grbbeta.Digi.Repeater(self._io, self, self._root)

                self.ctl = self._io.read_u1()
                self.pid = self._io.read_u1()


        class Callsign(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


        class SsidMask(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.ssid_mask = self._io.read_u1()

            @property
            def ssid(self):
                if hasattr(self, '_m_ssid'):
                    return self._m_ssid if hasattr(self, '_m_ssid') else None

                self._m_ssid = ((self.ssid_mask & 15) >> 1)
                return self._m_ssid if hasattr(self, '_m_ssid') else None

            @property
            def hbit(self):
                if hasattr(self, '_m_hbit'):
                    return self._m_hbit if hasattr(self, '_m_hbit') else None

                self._m_hbit = ((self.ssid_mask & 128) >> 7)
                return self._m_hbit if hasattr(self, '_m_hbit') else None


        class Repeaters(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.rpt_callsign_raw = Grbbeta.Digi.CallsignRaw(self._io, self, self._root)
                self.rpt_ssid_raw = Grbbeta.Digi.SsidMask(self._io, self, self._root)


        class Repeater(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.rpt_instance = []
                i = 0
                while True:
                    _ = Grbbeta.Digi.Repeaters(self._io, self, self._root)
                    self.rpt_instance.append(_)
                    if (_.rpt_ssid_raw.ssid_mask & 1) == 1:
                        break
                    i += 1


        class CallsignRaw(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self._raw__raw_callsign_ror = self._io.read_bytes(6)
                self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
                _io__raw_callsign_ror = KaitaiStream(BytesIO(self._raw_callsign_ror))
                self.callsign_ror = Grbbeta.Digi.Callsign(_io__raw_callsign_ror, self, self._root)



    class NotDigi(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self.message_type3
            if _on == 21804:
                self.id4 = Grbbeta.BeaconUhf(self._io, self, self._root)
            elif _on == 22060:
                self.id4 = Grbbeta.BeaconVhf(self._io, self, self._root)
            else:
                self.id4 = Grbbeta.NotBeacon(self._io, self, self._root)

        @property
        def message_type3(self):
            if hasattr(self, '_m_message_type3'):
                return self._m_message_type3 if hasattr(self, '_m_message_type3') else None

            _pos = self._io.pos()
            self._io.seek(16)
            self._m_message_type3 = self._io.read_u2be()
            self._io.seek(_pos)
            return self._m_message_type3 if hasattr(self, '_m_message_type3') else None



