import board
import busio

try:
  from typing import Iterable
except ImportError:
  pass

class Comm:

  def __init__(self, baud_rate: int = 115200):
    """Initialize the host_comm class.
    
    Args: 
      baud_rate (int, optional): The baud rate of the UART. Defaults to 115200.
    """
    self.baud_rate = baud_rate
    self.uart = self._init_uart(baud_rate=baud_rate)
  
  @classmethod
  def _init_uart(cls, baud_rate: int) -> busio.UART:
    """Initialize the serial connection.
    
    Args:
      baud_rate (int): The baud rate of the connection.
    """
    return busio.UART(board.TX, board.RX, baudrate=baud_rate)

  def read_stream(self, size: int = 32) -> Iterable[str]:
    while True:
      yield self.read(size)

  def read(self, size: int = 32) -> bytes:
    """Read data from the serial connection.
    
    Args:
      size (int, optional): The number of bytes to read. Defaults to 32.
    """

    return self.uart.read(size)
  
  def write(self, data: bytes):
    """Write data to the serial connection.
    
    Args:
      data (bytes): The data to write.
    """

    self.uart.write(data)
