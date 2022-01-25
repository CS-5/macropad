import board
import busio

from adafruit_macropad import MacroPad
from collections import namedtuple

try:
    from typing import Iterable, Union
except ImportError:
    pass

# Event indicating the Encoder Button was pressed or released.
EncoderButtonEvent = namedtuple("EncoderButtonEvent", ("pressed",))

# Event indicating the Encoder was rotated.
EncoderEvent = namedtuple("EncoderEvent", ("position", "previous_position"))

# Event indicating a key was pressed or released.
KeyEvent = namedtuple("KeyEvent", ("number", "pressed"))

class Pad:

  def __init__(self):
      self.macropad = self._init_macropad()
      self.pixels = self.macropad.pixels

      self._last_encoder_position = self.encoder_position
      self._last_encoder_switch = self.encoder_switch


  @classmethod
  def _init_macropad(cls) -> MacroPad:
      """Initialize the macropad component."""

      macropad = MacroPad()
      macropad.display.auto_refresh = False
      macropad.pixels.auto_write = False

      return macropad

  @property
  def encoder_position(self) -> int:
      """Return the position of the encoder."""

      return self.macropad.encoder

  @property
  def encoder_switch(self) -> bool:
      """Return the state of the encoder switch."""

      self.macropad.encoder_switch_debounced.update()
      return self.macropad.encoder_switch_debounced.pressed

  def event_stream(
      self,
  ) -> Iterable[Union[EncoderButtonEvent, EncoderEvent, KeyEvent]]:
      while True:
          yield from self.check_events()

  def check_events(
      self,
  ) -> Iterable[Union[EncoderButtonEvent, EncoderEvent, KeyEvent]]:
      """Check for changes in state and return a tuple of events.

      Also execute any timers that are scheduled to run.

      Returns:
          Tuple[Union[EncoderButtonEvent, EncoderEvent, KeyEvent], ...]:
              A tuple of Events.
      """
      
      position = self.encoder_position
      if position != self._last_encoder_position:
          last_encoder_position = self._last_encoder_position
          self._last_encoder_position = position
          yield EncoderEvent(position=position, previous_position=last_encoder_position)

      encoder_switch = self.encoder_switch
      if encoder_switch != self._last_encoder_switch:
          yield EncoderButtonEvent(pressed=encoder_switch)

      key_event = self.macropad.keys.events.get()
      if key_event:
          yield KeyEvent(number=key_event.key_number, pressed=key_event.pressed)

      yield from self.execute_ready_timers()

class HostConnection:

  def __init__(self, baud_rate: int = 115200):
    self.baud_rate = baud_rate
    self.uart = self._init_uart(baud_rate=baud_rate)
  
  @classmethod
  def _init_uart(cls, baud_rate: int) -> busio.UART:
    return busio.UART(board.TX, board.RX, baudrate=baud_rate)

  def read(self):
    return self.uart.read()
  
  def write(self, data: bytes):
    self.uart.write(data)
