import pandas as pd
import gradio as gd
import plotly.graph_objs as go
from Algorithms import SortingAlgorithms
import time

# Instantiate the SortingAlgorithms class
alg = SortingAlgorithms()

def algorithm(file, algorithm_option, case_option, bar_width, original_color, sorted_color):
    try:
        # Check if file is uploaded
        if file is None:
            return "File not uploaded!", None, None, None, None
        
        # Read data from the Excel file
        data = pd.read_excel(file)

        # Extract data from the DataFrame columns into lists
        best_case = data["Best Case"].tolist()
        avg_case = data["Average Case"].tolist()
        worst_case = data["Worst Case"].tolist()

        # Select the data based on the case option
        if case_option == "Best Case":
            data_entry = best_case
        elif case_option == "Average Case":
            data_entry = avg_case
        elif case_option == "Worst Case":
            data_entry = worst_case
        else:
            return "Select a valid case option.", None, None, None, None

        # Record the start time of the sorting process
        initial_time = time.time()
        image = ""

        # Select and apply the chosen sorting algorithm
        if algorithm_option == "MergeSort":
            image = "https://willrosenbaum.com/assets/img/2022f-cosc-311/merge-sort.gif"
            sorted_data = alg.merge_sort(data_entry)
        elif algorithm_option == "QuickSort":
            image = "https://www.lavivienpost.net/wp-content/uploads/2022/02/quicksort-600-1.gif"
            sorted_data = alg.quick_sort(data_entry)
        elif algorithm_option == "InsertionSort":
            image = "https://www.lavivienpost.net/wp-content/uploads/2022/01/insertion-600.gif"
            sorted_data = alg.insertion_sort(data_entry)
        elif algorithm_option == "SelectionSort":
            image = "https://www.lavivienpost.net/wp-content/uploads/2022/01/selection-600.gif"
            sorted_data = alg.selection_sort(data_entry)
        elif algorithm_option == "BubbleSort":
            image = "https://www.lavivienpost.net/wp-content/uploads/2022/01/bubble-640.gif"
            sorted_data = alg.bubble_sort(data_entry)
        elif algorithm_option == "HeapSort":
            image = "https://www.lavivienpost.net/wp-content/uploads/2022/02/heapsort.jpg"
            sorted_data = alg.heap_sort(data_entry)
        else:
            return "Select which algorithm you want to use.", None, None, None, None

        # Calculate the elapsed time for sorting
        delta = time.time() - initial_time

        # Create a Plotly chart to visualize performance with adjusted bar width and colors
        fig = go.Figure(data=[
            go.Bar(name='Original Data', x=list(range(len(data_entry))), y=data_entry, marker_color=original_color, width=bar_width),
            go.Bar(name='Sorted Data', x=list(range(len(sorted_data))), y=sorted_data, marker_color=sorted_color, width=bar_width)
        ])
        fig.update_layout(
            title='Algorithm Performance',
            xaxis_title='Index',
            yaxis_title='Value',
            barmode='group'
        )

        # Return the original data, sorting animation image, sorted data, elapsed time, and performance chart
        return data_entry, fig, sorted_data, delta, image
    
    except pd.errors.EmptyDataError:
        return "The uploaded file is probably empty!", None, None, None, None
    except pd.errors.ParserError:
        return "The uploaded file is not a valid Excel file", None, None, None, None
    except Exception as e:
        return f"An error occurred: {e}", None, None, None, None

# Define the color options for the bars
color_options = ("#97E7E1", "#FF9800", "#912BBC", "#FDAF7B", "#007F73", "#5356FF", "#F7418F", "#87A922")

# Define the Gradio interface
UI = gd.Interface(
    fn=algorithm,
    inputs=[
        gd.File(label="Upload Excel file."),
        gd.Dropdown(
            label="Select Sorting Algorithm",  # Dropdown for selecting sorting algorithm
            choices=[
                "MergeSort",
                "QuickSort",
                "SelectionSort",
                "InsertionSort",
                "BubbleSort",
                "HeapSort"]
        ),
        gd.Dropdown(
            label="Select Case Type",  # Dropdown for selecting case type
            choices=[
                "Best Case",
                "Average Case",
                "Worst Case"]
        ),
        gd.Slider(
            label="Bar Width",  # Slider for adjusting bar width
            minimum=0.1,
            maximum=1.0,
            step=0.1,
            value=0.4  # Default value for bar width
        ),
        gd.Dropdown(
            label="Select Color for Original Data",  # Dropdown for selecting original data bar color
            choices=color_options,
            value=color_options[0]  # Default color
        ),
        gd.Dropdown(
            label="Select Color for Sorted Data",  # Dropdown for selecting sorted data bar color
            choices=color_options,
            value=color_options[1]  # Default color
        )
    ],
    outputs=[
        gd.Textbox(label="Data entry as example: "),
        gd.Plot(label="Performance Chart"),
        gd.Textbox(label="Sorted Data: "),
        gd.Textbox(label="Running Time: "),
        gd.Image(label="Algorithm Animation")
    ],
    theme="light"
)

# Launch the Gradio interface
UI.launch()
