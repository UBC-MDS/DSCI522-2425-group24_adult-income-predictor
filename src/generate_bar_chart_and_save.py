import altair as alt
from src.create_dir_and_file_if_not_exist import create_dir_and_file_if_not_exist

def generate_bar_chart_and_save(
    adult_data_frame, 
    y_axis_label, 
    y_axis_name,
    plot_dir, 
    plot_name):
    """
    Generate bar char and save it to the directory.

    Parameters:
    ----------
    adult_income_dataframe : pandas.DataFrame
        The DataFrame containing adult income dataframe with the columns: 
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'.
    y_axis_label : str
        label of the y axis.
    y_axis_name: str
        name of the y axis in the dataframe.
    plot_dir : str
        directory to where your plot will be saved.
    plot_name: str
        name of your plot. 
    """

    plot = alt.Chart(adult_data_frame, title=f"Income for different {y_axis_label}").mark_bar(opacity=0.75).encode(
        alt.Y(y_axis_name).title(y_axis_label),
        alt.X('count()').stack(False),
        alt.Color('income')
    ).properties(
        height=200,
        width=300
    )

    dir = create_dir_and_file_if_not_exist(plot_dir, plot_name)
    plot.save(dir, scale_factor=2.0)