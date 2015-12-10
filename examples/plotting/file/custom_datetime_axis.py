from math import pi
from pdb import set_trace as bp

import pandas as pd

from bokeh.sampledata.stocks import MSFT
from bokeh.plotting import figure, show, output_file
from bokeh.models.formatters import TickFormatter, String, Int, List

class DateGapTickFormatter(TickFormatter):
  format = String("%s")
  date_labels = List(item_type=String)
  __implementation__ = """
_ = require "underscore"
SPrintf = require "sprintf"
HasProperties = require "common/has_properties"

class DateGapTickFormatter extends HasProperties
  type: 'DateGapTickFormatter'

  format: (ticks) ->
    format = @get("format")
    date_labels = @get("date_labels")
    labels = ( 
      for tick, i in ticks
      	if date_labels[tick]
        	SPrintf.sprintf(format, date_labels[tick]) 
      	else
      		SPrintf.sprintf("") 
      )
    return labels

  defaults: () ->
    return _.extend {}, super(), {
      format: '%s'
    }

module.exports =
  Model: DateGapTickFormatter
		"""

df = pd.DataFrame(MSFT)[:50]
df["date"] = pd.to_datetime(df["date"])
df = df.set_index([range(0,len(df))])
date_labels = map(lambda x: x.strftime('%b %d'), df["date"])

mids = (df.open + df.close)/2
spans = abs(df.close-df.open)

inc = df.close > df.open
dec = df.open > df.close
w = 0.5

output_file("candlestick.html", title="candlestick.py example")

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

p = figure(tools=TOOLS, plot_width=1000, toolbar_location="left")

p.xaxis[0].formatter = DateGapTickFormatter(date_labels = date_labels)

p.segment(df.index, df.high, df.index, df.low, color="black")
p.rect(df.index[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")
p.rect(df.index[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")

p.title = "MSFT Candlestick"
p.xaxis.major_label_orientation = pi/4

p.grid[0].ticker.desired_num_ticks = 6

show(p)  # open a browser
