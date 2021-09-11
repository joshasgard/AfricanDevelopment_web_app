from numpy import longlong
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def clean_data(dataset,indicators_to_plot, keepcolumns = ['country_name_attr','1990', '2000','2010']):
  
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
    pop_2020 = [43851044, 32866272, 102334404, 114963588, 31072940, 53771296, 36910560, 206139589, 59308690, 59734218]
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
        mode = 'lines',
        name = country
        )
      )

    layout_one = dict(title = 'Change in total Population of the top 10 <br> economies 1990-2020',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=30),
                yaxis = dict(title = 'Population'),
                )

# bar chart plot of the 2010 GDP in US Dollars - "NY.GDP.MKTP.KD"   
    graph_two = []

    df = clean_data('data/adi_data.csv', ['NY.GDP.MKTP.KD'])
    value_vars = ['1990', '2000', '2010']
    df_melt = df.melt(id_vars = 'country_name_attr', value_vars=value_vars)
    df_melt.columns = ['country', 'year', 'GDP']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year
    df_melt.sort_values('GDP', ascending=False, inplace =True)
    df_melt = df_melt[df_melt['year'] == 2010]


    graph_two.append(
      go.Bar(
      x = df_melt.country.tolist(),
      y = df_melt.GDP.tolist(),
      )
    )

    layout_two = dict(title = 'Top 10 GDP as at 2010 (US$)',
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'GDP in US$'),
                )


# third chart plots GDP per person in the top 10 countries from 1990-2010
    graph_three = []

    df = clean_data('data/adi_data.csv', ['NY.GDP.PCAP.KD'])
    value_vars = ['1990', '2000', '2010']
    df_melt = df.melt(id_vars = 'country_name_attr', value_vars=value_vars)
    df_melt.columns = ['country', 'year', 'GDP_Per_Capita']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year
    df_melt.sort_values('GDP_Per_Capita', ascending=False, inplace =True)
    countrylist = df_melt.country.unique().tolist()

    for country in countrylist:
      x_val = df_melt[df_melt['country'] == country].year.tolist()
      y_val = df_melt[df_melt['country'] == country].GDP_Per_Capita.tolist()

      graph_three.append(
        go.Scatter(
        x = x_val,
        y = y_val,
        mode = 'lines', 
        name = country
        )
      )

    layout_three = dict(title = 'Change in GDP Per Capita <br> 1990-2010',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=20),
                yaxis = dict(title = 'GDP Per Capita (US$)'),
                )
    
# fourth chart shows life expectancy vs GDP per capita in each of these countries - "SP.DYN.LE00.IN"

    graph_four = []
    
# clean data and select country
    df = clean_data('data/adi_data.csv', ['SP.DYN.LE00.IN'])
    value_vars = ['1990', '2010']
    df_melt = df.melt(id_vars = 'country_name_attr', value_vars=value_vars)
    df_melt.columns = ['country', 'year', 'Life_Exptncy']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year
    df_melt.sort_values('Life_Exptncy', ascending=False, inplace =True)
    countrylist = df_melt.country.unique().tolist()

# plot a line chart for each country in countrylist above
    for country in countrylist:
      x_val = df_melt[df_melt['country'] == country].year.tolist()
      y_val = df_melt[df_melt['country'] == country].Life_Exptncy.tolist()

      graph_four.append(
        go.Scatter(
        x = x_val,
        y = y_val,
        mode = 'lines', 
        name = country
        )
      )

    layout_four = dict(title = 'Life Expectancy at birth 1990-2010',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=20),
                yaxis = dict(title = 'Life Expectancy in years'),
                )
    
# fifth chart is a bubble plot showing gdp per capita vs life expectancy: Indicator Code - NY.GDP.PCAP.KD and SP.DYN.LE00.IN
    
# clean data the usual way
    df = clean_data('data/adi_data.csv', indicators_to_plot=['NY.GDP.PCAP.KD','SP.DYN.LE00.IN','SP.POP.TOTL'], keepcolumns = ['country_name_attr', 
    'indicator_code','1990', '2000','2010'])
    value_vars = ['1990', '2000', '2010']
    id_vars = ['country_name_attr','indicator_code']
    df_melt = df.melt(id_vars = id_vars, value_vars=value_vars)
    df_melt.columns =  ['country','indicator_code', 'year', 'metric']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year

# pivot the data for our two indicators to appear as columns and reset the index
    df_melt = df_melt.pivot(index =[ 'country', 'year'],columns = 'indicator_code', values= 'metric' ).reset_index()
    df_melt = df_melt.dropna()
    df_melt.columns = ['country', 'year', 'GDPperCapita_USD', 'LifeExpectancy_years', 'Population']
    
# create a figure object using plotly.express
    fig = px.scatter(df_melt, x = 'GDPperCapita_USD', y = 'LifeExpectancy_years',animation_frame = 'year', 
                    animation_group = 'country', size = 'Population', color = 'country', hover_name = 'country', 
                    log_x= True, size_max= 100, range_x= [50, 10000], range_y= [25,90], title = 'Life Expectancy vs GDP Per Capita for top 10 countries')

# extract data and layout from embedded px dictionary     
    graph_five = fig.to_dict()['data']
    layout_five = fig.to_dict()['layout']

# append all charts to the figures list
    
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))

    return figures