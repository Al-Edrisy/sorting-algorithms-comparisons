import pandas as pd
import gradio as gd
from Algorithms import SortingAlgorithms
import time

#Algoriths Object
alg = SortingAlgorithms()


def algorithm(file, option):

    try:
        data = pd.read_excel(file)
        image = ""
        if file == None:
            "file not uploded !", None, None
        
        # Convert DataFrame to string without including the index column
        data_entry = [n for n in data["Worst Case"]]
        best_case = [n for n in data["Best Case"]]
        avg_case = [n for n in data["Average Case"]]
        worst_case = [n for n in data["Worst Case"]]

        initial_time = time.time()
        if option == "MergeSort":
            image = "https://willrosenbaum.com/assets/img/2022f-cosc-311/merge-sort.gif"
            sorted_data = alg.merge_sort(data_entry)
        elif option == "QuickSort":
            image = "https://www.lavivienpost.net/wp-content/uploads/2022/02/quicksort-600-1.gif"
            sorted_data = alg.quick_sort(data_entry)
        elif option == "InsertionSort":
            image = "https://www.lavivienpost.net/wp-content/uploads/2022/01/insertion-600.gif"
            sorted_data = alg.insertion_sort(data_entry)
        elif option == "SelectionSort":
            image = "https://www.lavivienpost.net/wp-content/uploads/2022/01/selection-600.gif"
            sorted_data = alg.selection_sort(data_entry)
        else:
            return "Select which algorithm you want to use..", None, None
        dalta = time.time() - initial_time
        return data_entry, image, sorted_data, dalta
    except pd.errors.EmptyDataError:
        return "The uploaded file is probably empty !", None, None
    except pd.errors.ParserError:
        return "The uploaded file is not a valid Excel file", None, None
    except Exception as e:
        return f"An error occurred: {e}", None, None

UI = gd.Interface(
    fn=algorithm,
    inputs=[
        gd.File(label="Upload excel file."),
        gd.Dropdown(
            label="Select Sorting Algorithm",  # Dropdown for selecting sorting algorithm
            choices=[
                "MergeSort",
                "QuickSort",
                "SelectionSort",
                "InsertionSort"])
    ],
    outputs=[
        gd.Text("Data entry as example: "),
        gd.Image("The animations part of the algorithm."),
        gd.Text(label="The result: "),
        gd.Text(label="Running Time: ")
    ],
    theme="light"
)

UI.launch()