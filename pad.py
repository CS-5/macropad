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

  # Initialize the Pad class (includes init of MacroPad, pixels, and encoder)
  def __init__(self):
    self.macropad = self._init_macropad()
    self.pixels = self.macropad.pixels

    self._last_encoder_position = self.encoder_position
    self._last_encoder_switch = self.encoder_switch

  # Initialize the MacroPad
  @classmethod
  def _init_macropad(cls, rotation: int = 0, midi_in_channel: int = 1, midi_out_channel: int = 1) -> MacroPad:
    """Initialize the macropad.
    
    Args:
      rotation (int, optional): The rotation of the MacroPad. Defaults to 0.
      midi_in_channel (int, optional): The MIDI in channel. Defaults to 1.
      midi_out_channel (int, optional): The MIDI out channel. Defaults to 1.

    Returns:
      MacroPad: The initialized MacroPad.
    """

    macropad = MacroPad(rotation, midi_in_channel, midi_out_channel)
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

  def event_stream(self) -> Iterable[Union[EncoderButtonEvent, EncoderEvent, KeyEvent]]:
    while True:
      yield from self.check_events()

  def check_events(self) -> Iterable[Union[EncoderButtonEvent, EncoderEvent, KeyEvent]]:
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