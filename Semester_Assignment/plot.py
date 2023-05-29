import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display

def extract_data_from_file(file_path):
    # Initialize empty lists to store the extracted data
    frame = []
    left_eye_area = []
    right_eye_area = []
    left_eye_closed = []
    right_eye_closed = []
    left_eye_threshold = []
    right_eye_threshold = []
    blinkCounter = []

    # Open the file
    with open(file_path, 'r') as file:
        # Read each line in the file
        for line in file:
            # Split the line into different fields
            fields = line.strip().split(', ')

            # Extract the desired fields (frame, left_eye_area, right_eye_area)
            for field in fields:
                key, value = field.split(': ')
                if key == 'frame':
                    frame.append(int(value))
                elif key == 'left_eye_area':
                    left_eye_area.append(float(value))
                elif key == 'right_eye_area':
                    right_eye_area.append(float(value))
                elif key == 'left_eye_closed':
                    left_eye_closed.append(float(value))
                elif key == 'right_eye_closed':
                    right_eye_closed.append(float(value))
                elif key == 'left_eye_threshold':
                    left_eye_threshold.append(float(value))
                elif key == 'right_eye_threshold':
                    right_eye_threshold.append(float(value))
                elif key == 'blinkCounter':
                    blinkCounter.append(float(value))

    return frame, left_eye_area, right_eye_area, left_eye_closed, right_eye_closed, left_eye_threshold, right_eye_threshold, blinkCounter

def plot_data(file_path):
    # Extract data from the file
    frame, left_eye_area, right_eye_area, left_eye_closed, right_eye_closed, left_eye_threshold, right_eye_threshold, blinkCounter = extract_data_from_file(file_path)

    # Create a Figure object
    fig = go.Figure()

    # Create checkboxes
    checkbox_left_eye_area = widgets.Checkbox(value=True, description='Left Eye Area')
    checkbox_left_eye_closed = widgets.Checkbox(value=True, description='Left Eye Closed')
    checkbox_left_eye_threshold = widgets.Checkbox(value=True, description='Left Eye Threshold')
    checkbox_right_eye_area = widgets.Checkbox(value=True, description='Right Eye Area')
    checkbox_right_eye_closed = widgets.Checkbox(value=True, description='Right Eye Closed')
    checkbox_right_eye_threshold = widgets.Checkbox(value=True, description='Right Eye Threshold')
    display(widgets.VBox([checkbox_left_eye_area, checkbox_left_eye_closed, checkbox_left_eye_threshold]))
    display(widgets.VBox([checkbox_right_eye_area, checkbox_right_eye_closed, checkbox_right_eye_threshold]))

    def update_plot():
        fig.data = []  # Clear existing traces

        if checkbox_left_eye_area.value:
            fig.add_trace(go.Scatter(x=frame, y=left_eye_area, mode='lines', name='Left Eye Area'))
        if checkbox_left_eye_closed.value:
            fig.add_trace(go.Scatter(x=frame, y=left_eye_closed, mode='lines', name='Left Eye Closed'))
        if checkbox_left_eye_threshold.value:
            fig.add_trace(go.Scatter(x=frame, y=left_eye_threshold, mode='lines', name='Left Eye Threshold'))
        if checkbox_right_eye_area.value:
            fig.add_trace(go.Scatter(x=frame, y=right_eye_area, mode='lines', name='Right Eye Area'))
        if checkbox_right_eye_closed.value:
            fig.add_trace(go.Scatter(x=frame, y=right_eye_closed, mode='lines', name='Right Eye Closed'))
        if checkbox_right_eye_threshold.value:
            fig.add_trace(go.Scatter(x=frame, y=right_eye_threshold, mode='lines', name='Right Eye Threshold'))

        # Customize the layout
        fig.update_layout(
            xaxis=dict(title='Frames', rangeslider=dict(visible=True)),
            yaxis=dict(title='Value'),
            hovermode='x',  # Enable hover interactions
        )

        # Update the plot
        fig.show()

    # Register the update function as an event handler for the checkbox value changes
    checkbox_left_eye_area.observe(lambda _: update_plot(), names='value')
    checkbox_left_eye_closed.observe(lambda _: update_plot(), names='value')
    checkbox_left_eye_threshold.observe(lambda _: update_plot(), names='value')
    checkbox_right_eye_area.observe(lambda _: update_plot(), names='value')
    checkbox_right_eye_closed.observe(lambda _: update_plot(), names='value')
    checkbox_right_eye_threshold.observe(lambda _: update_plot(), names='value')

    # Display the initial plot
    update_plot()


if __name__=="__main__":
    file_path = './logs_plot2.log'
    plot_data(file_path)
