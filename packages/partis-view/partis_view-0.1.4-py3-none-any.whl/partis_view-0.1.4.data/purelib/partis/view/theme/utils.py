
import os
import os.path as osp
from copy import copy
import re
from collections.abc import (
  Mapping,
  Sequence )
from colorsys import (
  rgb_to_hls,
  hls_to_rgb,
  rgb_to_yiq,
  yiq_to_rgb )

from jinja2 import Environment, PackageLoader

cre_fore = re.compile(rf"#ff0000", re.I)
cre_edge = re.compile(rf"#00ff00", re.I)
cre_back = re.compile(rf"#0000ff", re.I)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def hex_to_rgb(color, norm = False):
  r,g,b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)

  if norm:
    r,g,b = r / 255, g / 255, b / 255

  return r,g,b

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def rgb_to_hex(color, norm = False):

  if norm:
    color = map(lambda x: x*255, color )

  r,g,b = map(lambda x: max(0, min(255, int(round(x)))), color )

  return f"#{r:02X}{g:02X}{b:02X}"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def hex_to_hls(color):
  return rgb_to_hls(*hex_to_rgb(color, True))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def hls_to_hex(color):
  return rgb_to_hex(hls_to_rgb(*color), True)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def hex_to_yiq(color):
  return rgb_to_yiq(*hex_to_rgb(color, True))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def yiq_to_hex(color):
  return rgb_to_hex(yiq_to_rgb(*color), True)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def alpha(color, alpha):
  r,g,b = hex_to_rgb(color)
  return f"rgba({r}, {g}, {b}, {alpha:.0%})"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _lighten(h, l, s , factor):
  l = min(1.0, l + (1-l)*factor)
  return h,l,s

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def lighten(color, factor):
  return hls_to_hex(_lighten(*hex_to_hls(color), factor))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _darken(h, l, s, factor):
  l = max(0.0, l*(1-factor))
  return h,l,s

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def darken(color, factor):
  return hls_to_hex(_darken(*hex_to_hls(color), factor))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _desaturate(h, l, s, factor):
  s = max(0.0, s*(1-factor))
  return h,l,s

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def desaturate(color, factor):
  return hls_to_hex(_desaturate(*hex_to_hls(color), factor))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def cinterp(c1, c2, factor):
  color = yiq_to_hex([
    ((1-factor)*a + factor*b)
    for a,b in zip(hex_to_yiq(c1), hex_to_yiq(c2))])

  return color

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def svgcolor(file, fore, edge, back, idir, odir):
  path = osp.join(idir, file)
  rpath, name = osp.split(file)
  name = name.rsplit('.',1)[0]

  _name = '_'.join([name, fore[1:], edge[1:], back[1:] ]) + '.svg'
  _file = osp.join(rpath, _name)
  _path = osp.join(odir, _file)
  _dir = osp.dirname(_path)

  if not osp.exists(_dir):
    os.makedirs(_dir)

  if osp.exists(_path):
    return _path

  with open(path, 'r') as fp:
    svg = fp.read()

  svg = cre_fore.sub(fore, svg)
  svg = cre_edge.sub(edge, svg)
  svg = cre_back.sub(back, svg)

  with open(_path, 'w') as fp:
    fp.write(svg)

  return _path

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
FILTERS = {
  'alpha': alpha,
  'lighten': lighten,
  'darken': darken,
  'desaturate': desaturate,
  'cinterp': cinterp,
  'ex': lambda x: f'{x}ex',
  'em': lambda x: f'{x}em',
  'pt': lambda x: f'{x}pt' }


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def qss_process(
  stylesheet_str,
  variables,
  px_per_pt,
  idir,
  odir ):
  """
  Parameters
  ----------
  stylesheet_str : str
    Stylesheet to replace urls
  """

  px_per_em = px_per_pt * variables.text.narrative.size
  px_per_ex = 0.5 * px_per_em

  px_per_unit = {
    'pt' : px_per_pt,
    'em' : px_per_em,
    'ex' : px_per_ex }

  var_pattern = r"\$(?P<func>\w+)\((?P<args>[\w\.\,\s]+)\)"
  url_pattern = r"url\(\s*(?P<path>[^\)]+)\s*\)"
  px_pattern = r"(?P<start>[\:\s])(?P<length>\d+(\.\d+)?)(?P<unit>em|ex|pt)"
  # length_pattern = re.compile(r"(?P<length>(\d+)?(\.\d+)?)\s*(?P<unit>[a-zA-Z]+)?")

  #...........................................................................
  def _svgcolor(file, fore = None, edge = None, back = None):

    if isinstance(fore, Mapping):
      ctx = fore
      fore = ctx['fore']
      edge = ctx['edge']
      back = ctx['back']

    else:
      fore = fore or variables.color.static.fore_alt
      edge = edge or variables.color.static.edge_alt
      back = back or variables.color.static.back_alt

    path = svgcolor(file, fore, edge, back, idir, odir)

    return f"url({path})"

  filters = copy(FILTERS)
  filters['svg'] = _svgcolor

  env = Environment()
  env.globals.update(variables)
  env.filters.update(filters)

  stylesheet_str = env.from_string(stylesheet_str).render()

  #...........................................................................
  def _replace_rcc(match):
      _path = match.group("path")

      r_path = f":/{_path}"

      return f"url({r_path})"

  #...........................................................................
  def _replace_file(match):
      r_path = match.group("path")

      if not osp.isabs(r_path):
        r_path = osp.join(idir, r_path)

      r_path = r_path.replace("\\", "/")

      return f"url({r_path})"

  #...........................................................................
  def _replace_px(match):
    unit = match.group("unit")
    length = float(match.group("length"))
    start = match.group("start")

    _px_per_unit = px_per_unit[unit]

    if length == 0.0:
      return f"{start}0px"

    _length = max(
      # NOTE: ensure non-zero length is at least one pixel
      1,
      round( length * _px_per_unit ) )

    return f"{start}{_length}px"

  stylesheet_str = re.sub(
    url_pattern,
    _replace_file,
    stylesheet_str )

  stylesheet_str = re.sub(
    px_pattern,
    _replace_px,
    stylesheet_str )

  return stylesheet_str
