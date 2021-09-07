import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def clean_data(dataset,indicators_to_plot, keepcolumns = ['country_name_attr', '1990', '2000','2010']):
  
  """Cleans raw dataset for the visualization

  Imports the world bank dataset
  Cleans the dataset by structuring it for the respective feature plot using Arg
  Reorients the columns into a year, country and value
  Returns analysis-ready data for the top 10 economies in Africa

  Args: 
      dataset (str):              name of the csv raw dataset from worldbank
      indicators_to_plot (list):  economic indicator(s) to be visualised
      keepcolumns:                data columns required for the plot
  
  Returns:
      df_melt(dataframe): plot-ready data
  
  """
  # read in the data
  df = pd.read_csv(dataset)

  # declare and select the top 10 African Economies from the dataset
  top10countries = ['Nigeria', 'Egypt, Arab Rep.', 'South Africa', 'Algeria', 'Morocco', 'Kenya', 'Ethiopia', 'Ghana', 'Tanzania', 'Angola']
  df = df[df['country_name_attr'].isin(top10countries)]

  # select development indicators to plot and other columns to keep
  df_indicator = df[df['indicator_code'].isin (indicators_to_plot)]
  df_indicator = df_indicator[keepcolumns]

  return df_indicator
  

def return_figures():
    """Creates plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots total population from 1990 to 2020 
    # as a line chart
    graph_one = []

    # Clean the data and use the WorldBank Indicator standard for total population- "'SP.POP.TOTL'"
    df = clean_data('data/adi_data.csv',['SP.POP.TOTL'])

    # Add 2020 Population data from worldometer for recency
    pop_2020 = ['43851044', '32866272', '102334404', '114963588', '31072940', '53771296', '36910560', '206139589', '59308690', '59734218']
    df.loc[ : , '2020'] = pop_2020

    # Unpivot data into 3 columns using melt
    value_vars = ['1990', '2000', '2010', '2020']
    df_melt = df.melt(id_vars = 'country_name_attr', value_vars=value_vars)
    df_melt.columns = ['country', 'year', 'population']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year    # year column to datetime
    df_melt.sort_values('population', ascending=False, inplace =True)
    countrylist = df_melt.country.unique().tolist()

    for country in countrylist:
      x_val = df_melt[df_melt['country'] == country].year.tolist()
      y_val = df_melt[df_melt['country'] == country].population.tolist()

    graph_one.append(
      go.Scatter(
      x = x_val,
      y = y_val,
      mode = 'lines'
      )
    )

    layout_one = dict(title = 'Chart One',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []

    graph_two.append(
      go.Bar(
      x = ['a', 'b', 'c', 'd', 'e'],
      y = [12, 9, 7, 5, 1],
      )
    )

    layout_two = dict(title = 'Chart Two',
                xaxis = dict(title = 'x-axis label',),
                yaxis = dict(title = 'y-axis label'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    graph_three.append(
      go.Scatter(
      x = [5, 4, 3, 2, 1, 0],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines'
      )
    )

    layout_three = dict(title = 'Chart Three',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label')
                       )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    
    graph_four.append(
      go.Scatter(
      x = [20, 40, 60, 80],
      y = [10, 20, 30, 40],
      mode = 'markers'
      )
    )

    layout_four = dict(title = 'Chart Four',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures