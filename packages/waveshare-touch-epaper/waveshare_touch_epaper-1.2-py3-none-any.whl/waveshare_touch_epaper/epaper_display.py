import math
import time
from abc import ABCMeta, abstractmethod
import logging


import spidev
import gpiozero
from PIL import Image


epaper_models = dict()


class MetaEpaper(ABCMeta):

    """meta class  for epaper displays to store class
    and their model in a dict"""

    def __init__(cls, name, bases, dict):
        """store the class and in a dict upon creation"""
        ABCMeta.__init__(cls, name, bases, dict)
        epaper_models[name] = cls


class BaseEpaper(object, metaclass=ABCMeta):

    """Base class for epaper, define interface with abstract methid. """

    WIDTH: int = NotImplemented
    """width of screen in number of pixels"""

    HEIGHT: int = NotImplemented
    """height of screen in number of pixels"""

    @abstractmethod
    def open(self):
        """power off, initial configuration and clear screen

        """
        pass

    @abstractmethod
    def __enter__(self):
        """use open method for context manager
        :returns: self

        """
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """exit the context manager. enter sleep mode and close all ports

        :exc_type: None if exited without exception
        :exc_value: None if exited without exception
        :traceback: None if exited without exception

        """
        pass

    @abstractmethod
    def close(self):
        """deep sleep, power off device and close all ports

        """
        pass

    @abstractmethod
    def display(self, img: Image.Image, full_refresh: bool):
        """send img to epaper RAM and do a full or partial refresh
        (partial update will be called if full refresh)

        :img: that will be displayed
        :full_refresh: if True, apply a full refresh, otherise a partial one
        :raise EpaperException: when too many consecutive partial refresh

        """
        pass

    @abstractmethod
    def clear(self):
        """clear the e-paper to white

        """
        pass

    # @abstractmethod
    # def sleep(self):
        # """enter deep sleep mode

        # """
        # pass


class EPD2in13Mock(BaseEpaper, metaclass=MetaEpaper):
    """mock interface for epaper display, 2.13 inch. no need of gpio,
    the image are displayed on the screen with pillow module"""

    WIDTH = 122
    HEIGHT = 250

    def clear(self):
        logging.info('clear image')
        img = Image.new('1', (self.WIDTH, self.HEIGHT), 255)
        img.show()

    def open(self):
        logging.info('mock open epd')

    def close(self):
        logging.info('mock close epd')

    def sleep(self):
        logging.info('mock: enter sleep mode')

    def display(self, img: Image.Image, full_refresh=True):
        img.show()

    def __enter__(self):
        self.open()
        self.clear()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sleep()
        self.close()


class EpaperException(Exception):
    pass


class EPD2in13(BaseEpaper, metaclass=MetaEpaper):

    WIDTH = 122
    HEIGHT = 250
    _MAX_PARTIAL_REFRESH = 50

    _RST_PIN = 17
    _DC_PIN = 25
    _CS_PIN = 8
    _BUSY_PIN = 24

    _ADRESS = 0x14

    _SPI_MAXSPEED = 10000000
    _SPI_MODE = 0b00

    _COMMAND = dict(
            reset=0x12,
            driver_output_control=0x01,
            data_entry_mode_setting=0x11,
            set_ram_x=0x44,
            set_ram_y=0x45,
            border_waveform_control=0x3c,
            temperature_sensor_control=0x18,
            deep_sleep_mode=0x10,
            display_update_control=0x21,
            set_ram_x_adress_counter=0x4e,
            set_ram_y_adress_counter=0x4f,
            write_ram_bw=0x24,
            write_ram_red=0x26,
            booster_soft_start_control=0x0c,
            display_update_control_2=0x22,
            master_activation=0x20,
            )

    def __init__(self):
        """initialise epd

        """
        self._remaining_partial_refresh = None
        self._gpio_rst = gpiozero.LED(self._RST_PIN)
        self._gpio_dc = gpiozero.LED(self._DC_PIN)
        self._gpio_busy = gpiozero.Button(
                self._BUSY_PIN,
                pull_up=False)
        self._spi = spidev.SpiDev(0, 0)

    def __enter__(self):
        self.open()
        return self

    def open(self):
        self._power_on()
        self._set_initial_configuration()
        self.clear()

    def close(self):
        self._power_off()
        self._close_all_port()

    def clear(self, color=0b1, coordinates=None):
        """
        clear the full screen
        :color: 1 for white, 0 for black
        :coords: if None, full screen is cleared
        if tuple (x_start, x_end, y_start, y_end) partial refresh in window

        """
        full_refresh = False if coordinates else True
        byte_img = self._get_mono_img_bytearray(
                color,
                coordinates,
                )
        self._process_display(byte_img, coordinates=coordinates, full_refresh=full_refresh)

    def _get_mono_img_bytearray(self, color, coord):
        if coord is None:
            x_start = 0
            x_end = self.WIDTH - 1
            y_start = 0
            y_end = self.HEIGHT - 1
        else:
            x_start, x_end, y_start, y_end = coord
        byte_color = 0xff * color
        pixel_byte = byte_color.to_bytes(1, 'big')

        window_width = math.ceil((x_end - x_start + 1) / 8)
        window_height = (y_end - y_start + 1)
        N = window_height * window_width

        img_bytes = pixel_byte * N
        img_byte_array = bytearray(img_bytes)
        return img_byte_array

    def _get_byte_img(self, img):
        img = img.convert('1').rotate(180, expand=True)
        byte_img = bytearray(img.tobytes())
        return byte_img

    def display(self, img: Image.Image, full_refresh=True):
        byte_img = self._get_byte_img(img)
        if full_refresh:
            coordinates = None
        else:
            img.crop((0, 0, 60, 249))
            # TODO: compute smaller window size for img
            x_start = 0
            y_start = 0
            x_end = self.WIDTH - 1
            y_end = self.HEIGHT - 1
            coordinates = (x_start, x_end, y_start, y_end)
        self._process_display(byte_img, coordinates=coordinates, full_refresh=full_refresh)

    def _process_display(self, byte_img: bytearray, coordinates, full_refresh: bool):
        if full_refresh:
            # set init config (hard reset?)
            self._send_initialization_code()
            self._load_waveform_lut()
            self._write_image_and_drive_display_panel(byte_img)
            self._remaining_partial_refresh = self._MAX_PARTIAL_REFRESH
        else:
            if self._remaining_partial_refresh == 0:
                msg = 'too many partial refresh. need a full refresh'
                raise EpaperException(msg)
            self._fast_hw_reset()
            self._send_initialization_code(coordinates)
            x_start = coordinates[0]
            y_start = coordinates[2]
            self._write_image_and_drive_display_panel(
                    byte_img,
                    x_start,
                    y_start,
                    display_mode=2,
                    )
            self._remaining_partial_refresh -= 1

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _power_on(self):
        logging.info('power on')
        logging.debug('power cannot be switched because rpi 3.3v connected')
        time.sleep(0.01)

    def _set_initial_configuration(self):
        logging.info('set initial configuration')
        self._spi.max_speed_hz = self._SPI_MAXSPEED
        self._spi.mode = self._SPI_MODE
        self._hw_reset()
        self._send_command('reset')
        time.sleep(0.01)

    def _send_initialization_code(self, coords=None):
        logging.info('send initialization code')
        self._set_gate_driver_output()
        self._set_display_RAM_size(coords)
        if coords is None:
            vcom = False
        else:
            vcom = True
        self._set_panel_border(vcom)
        self._set_display_source_mode()

    def _load_waveform_lut(self):
        logging.info('load waveform LUT')
        self._sense_temperature()
        self._wait_busy_low()

    def _write_image_and_drive_display_panel(
            self,
            img: bytearray,
            x_start=0,
            y_start=0,
            display_mode=1,
            ):
        logging.info('write image and drive display pannel')
        self._write_img_data_in_ram(x_start, y_start, img)
        self._set_softstart_setting()
        self._drive_display_pannel(display_mode)
        self._wait_busy_low()

    def _power_off(self):
        logging.info('power off')
        self._deep_sleep()
        logging.debug('power cannot be switched because rpi 3.3v connected')
        self._gpio_rst.off()
        self._gpio_dc.off()

    def _close_all_port(self):
        self._spi.close()
        self._gpio_rst.close()
        self._gpio_dc.close()
        self._gpio_busy.close()

    def _hw_reset(self):
        self._gpio_rst.on()
        time.sleep(0.02)
        self._gpio_rst.off()
        time.sleep(0.002)
        self._gpio_rst.on()
        time.sleep(0.02)

    def _fast_hw_reset(self):
        self._gpio_rst.off()
        time.sleep(0.001)
        self._gpio_rst.on()

    def _set_gate_driver_output(self):
        self._send_command('driver_output_control')
        self._send_data(0xf9)
        self._send_data(0x00)
        self._send_data(0x00)

    def _set_display_RAM_size(self, coords):
        """set windows size to be refreshed.

        :coords: if None, full screen is refresh
        if tuple (x_start, x_end, y_start, y_end) coord of window

        """
        if coords is None:
            x_start = 0
            x_end = self.WIDTH - 1
            y_start = 0
            y_end = self.HEIGHT - 1
        else:
            x_start, x_end, y_start, y_end = coords
        self._send_command('data_entry_mode_setting')
        self._send_data(0b011)
        self._send_command('set_ram_x')
        self._send_data(x_start >> 3)  # adress div by 8 as bytes has 8 bits
        self._send_data(x_end >> 3)
        self._send_command('set_ram_y')
        data = y_start
        low_byte, hi_byte = self._split_low_hi_bytes(data)
        self._send_data(low_byte)
        self._send_data(hi_byte)
        data = y_end
        low_byte, hi_byte = self._split_low_hi_bytes(data)
        self._send_data(low_byte)
        self._send_data(hi_byte)

    def _set_panel_border(self, vcom=False):
        self._send_command('border_waveform_control')
        if vcom:
            vbd_opt = 0b10 << 6
        else:
            vbd_opt = 0b00 << 6
        vbd_level = 0b00 << 4
        if vcom:
            gs_control = 0b0 << 2
            gs_setting = 0b00
        else:
            gs_control = 0b1 << 2  # follow LUT
            gs_setting = 0b01  # LUT1
        data = gs_control + gs_setting + vbd_level + vbd_opt
        self._send_data(data)

    def _set_display_source_mode(self):
        self._send_command('display_update_control')
        self._send_data(0x0)
        source_output_mode = 0b1 << 7
        self._send_data(source_output_mode)

    def _sense_temperature(self):
        self._send_command('temperature_sensor_control')
        self._send_data(0x80)

    def _write_img_data_in_ram(self, x_start, y_start, img: bytearray):

        self._send_command('set_ram_x_adress_counter')
        self._send_data(x_start >> 3)

        self._send_command('set_ram_y_adress_counter')
        low_byte, hi_byte = self._split_low_hi_bytes(y_start)
        self._send_data(low_byte)
        self._send_data(hi_byte)

        self._send_command('write_ram_bw')
        self._send_data_array(img)

    def _set_softstart_setting(self):
        # keep default settings so do nothing
        pass
        # self._send_command('booser_soft_start_control')
        # self._send_data(0x8b)
        # self._send_data(0x9c)
        # self._send_data(0x96)
        # self._send_data(0x0f)

    def _drive_display_pannel(self, display_mode):
        self._send_command('display_update_control_2')
        if display_mode == 1:
            data = 0xf7
        else:
            data = 0xff
        self._send_data(data)
        self._send_command('master_activation')

    def _wait_busy_low(self):
        self._gpio_busy.wait_for_active(timeout=0.1)  # in case busy not yet high
        self._gpio_busy.wait_for_inactive()

    def _deep_sleep(self):
        self._send_command('deep_sleep_mode')
        # TODO: check deep sleep mode 1 or 2
        self._send_data(0x11)

    @staticmethod
    def _split_low_hi_bytes(large_byte):
        low_byte = large_byte & 0xff
        hi_byte = large_byte >> 8
        return low_byte, hi_byte

    def _send_command(self, cmd_key: str):
        command = self._COMMAND.get(cmd_key)
        self._gpio_dc.off()
        self._spi.writebytes([command])

    def _send_data(self, data):
        self._gpio_dc.on()
        self._spi.writebytes([data])

    def _send_data_array(self, data_array):
        self._gpio_dc.on()
        self._spi.writebytes(data_array)

    def _partial_update(self):
        logging.info('partial update mock')
