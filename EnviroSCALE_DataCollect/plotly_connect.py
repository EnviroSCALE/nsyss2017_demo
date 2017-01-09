import plotly
#plotly.__version__
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
# (*) Import module keep track and format current time
import datetime
import time

stream_id = {}
stream_obj = {}
trace = {}
s = {}

#plotly.tools.set_credentials_file(username='enviro_scale', api_key='xxjrfn3fqa')
stream_ids = tls.get_credentials_file()['stream_ids']
print stream_ids

def map_sensor_id_to_title(x):
    return {
        1 : "CH4 Concentration (ppm)",
        2 : "LPG Concentration (ppm)",
        3 : "CO2 Concentration (ppm) ",
        4 : "Dust Concentration (micrograms/m3)",
        5 : "Temperature (degree C)",
        6 : "Humidity (%)",
    }.get(x, "none")    # "none" is default if x not found


# Get stream id from stream id list
for i in range(0,3):
    stream_id[i] = stream_ids[i]

    # Make instance of stream id object
    stream_obj[i] = go.Stream(
        token=stream_id[i],  # link stream id to 'token' key
        maxpoints=80      # keep a max of 80 pts on screen
    )

    # Initialize trace of streaming plot by embedding the unique stream_id
    trace[i] = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_obj[i]         # (!) embed stream id, 1 per trace
    )

    data = go.Data([trace[i]])

    # Add title to layout object
    layout = go.Layout(title=map_sensor_id_to_title(i+1))

    # Make a figure object
    fig = go.Figure(data=data, layout=layout)

    # Send fig to Plotly, initialize streaming plot, open new tab
    py.iplot(fig, filename=map_sensor_id_to_title(i+1))

    # We will provide the stream link object the same token that's associated with the trace we wish to stream to
    s[i] = py.Stream(stream_id[i])



def draw_to_plotly(sensor_bundle):
    """
    :param sensor_bundle:
    sensor_bundle[0] -> time
    sensor_bundle[1] -> ch4
    sensor_bundle[2] -> lpg
    sensor_bundle[3] -> co2
    sensor_bundle[4] -> dust
    sensor_bundle[5] -> temp
    sensor_bundle[6] -> humidity

    :return: Just draw to our plotly site
    """

    global s
    # We then open a connection

    for i in range(0, 3):
        s[i].open()
    time.sleep(5)

    for i in range(0, 3):
        # Delay start of stream by 5 sec (time to switch tabs)


        # Current time on x-axis, random numbers on y-axis
        x = datetime.datetime.fromtimestamp(sensor_bundle[0]).strftime('%Y-%m-%d %H:%M:%S')
        datetime.datetime.fromtimestamp(1466257792).strftime('%Y-%m-%d %H:%M:%S')


        y = sensor_bundle[i+1]

        # Send data to your plot
        s[i].write(dict(x=x, y=y))

        #     Write numbers to stream to append current data on plot,
        #     write lists to overwrite existing data on plot

        #time.sleep(1)  # plot a point every second

        # Close the stream when done plotting
        s[i].close()


