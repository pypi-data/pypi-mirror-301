
"""This module is not intended to be called explicitly"""

from typing import Any

def get_pyinstaller_hook_dirs() -> Any:
  """Function required by PyInstaller. Returns paths to module 
  PyInstaller hooks. Not intended to be called explicitly."""
  raise NotImplementedError()


class Color:
  """This class wraps ARGB color model."""

  a : int
  """ The alpha component of the color """

  r : int
  """ The red component of the color """

  g : int
  """ The green component of the color """

  b : int
  """ The blue component of the color """


  alice_blue : Color
  antique_white : Color
  aqua : Color
  aquamarine : Color
  azure : Color
  beige : Color
  bisque : Color
  black : Color
  blanched_almond : Color
  blue : Color
  blue_violet : Color
  brown : Color
  burly_wood : Color
  cadet_blue : Color
  chartreuse : Color
  chocolate : Color
  coral : Color
  cornflower_blue : Color
  cornsilk : Color
  crimson : Color
  cyan : Color
  dark_blue : Color
  dark_cyan : Color
  dark_goldenrod : Color
  dark_gray : Color
  dark_green : Color
  dark_khaki : Color
  dark_magenta : Color
  dark_olive_green : Color
  dark_orange : Color
  dark_orchid : Color
  dark_red : Color
  dark_salmon : Color
  dark_sea_green : Color
  dark_slate_blue : Color
  dark_slate_gray : Color
  dark_turquoise : Color
  dark_violet : Color
  deep_pink : Color
  deep_sky_blue : Color
  dim_gray : Color
  dodger_blue : Color
  empty : Color
  firebrick : Color
  floral_white : Color
  forest_green : Color
  fuchsia : Color
  gainsboro : Color
  get_brightness : Color
  get_hue : Color
  get_saturation : Color
  get_type : Color
  ghost_white : Color
  gold : Color
  goldenrod : Color
  gray : Color
  green : Color
  green_yellow : Color
  honeydew : Color
  hot_pink : Color
  indian_red : Color
  indigo : Color
  ivory : Color
  khaki : Color
  lavender : Color
  lavender_blush : Color
  lawn_green : Color
  lemon_chiffon : Color
  light_blue : Color
  light_coral : Color
  light_cyan : Color
  light_goldenrod_yellow : Color
  light_gray : Color
  light_green : Color
  light_pink : Color
  light_salmon : Color
  light_sea_green : Color
  light_sky_blue : Color
  light_slate_gray : Color
  light_steel_blue : Color
  light_yellow : Color
  lime : Color
  lime_green : Color
  linen : Color
  magenta : Color
  maroon : Color
  medium_aquamarine : Color
  medium_blue : Color
  medium_orchid : Color
  medium_purple : Color
  medium_sea_green : Color
  medium_slate_blue : Color
  medium_spring_green : Color
  medium_turquoise : Color
  medium_violet_red : Color
  midnight_blue : Color
  mint_cream : Color
  misty_rose : Color
  moccasin : Color
  navajo_white : Color
  navy : Color
  old_lace : Color
  olive : Color
  olive_drab : Color
  orange : Color
  orange_red : Color
  orchid : Color
  pale_goldenrod : Color
  pale_green : Color
  pale_turquoise : Color
  pale_violet_red : Color
  papaya_whip : Color
  peach_puff : Color
  peru : Color
  pink : Color
  plum : Color
  powder_blue : Color
  purple : Color
  red : Color
  rosy_brown : Color
  royal_blue : Color
  saddle_brown : Color
  salmon : Color
  sandy_brown : Color
  sea_green : Color
  sea_shell : Color
  sienna : Color
  silver : Color
  sky_blue : Color
  slate_blue : Color
  slate_gray : Color
  snow : Color
  spring_green : Color
  steel_blue : Color
  tan : Color
  teal : Color
  thistle : Color
  tomato : Color
  transparent : Color
  turquoise : Color
  violet : Color
  wheat : Color
  white : Color
  white_smoke : Color
  yellow : Color
  yellow_green : Color


  @classmethod
  def from_argb(argb : int) -> Color: ...
  """
  Convert ARGB value into Color instance
  """

  @classmethod
  def from_name(name : str) -> Color: ...
  """
  Gets a color instance from name
  """

  def to_argb(self) -> int: ...
  """
	Convert the color to an int
  """

