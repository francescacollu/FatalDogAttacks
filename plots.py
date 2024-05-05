from analysis import *
import plotly.express as px
import chart_studio.plotly as py
from credential_file import *
import chart_studio.tools as tls

def set_layout(fig_input):
    fig_input.update_layout(template="plotly_white", font_color="black", 
                            title = dict(font=dict(size=20, color = "black", family = "sans-serif")),
                            title_xanchor = 'auto')
    fig_input.update_layout(plot_bgcolor="white", xaxis=dict(linecolor="black"), yaxis=dict(linecolor="black"))
    fig_input.update_xaxes(ticks="outside")
    fig_input.update_yaxes(ticks="outside")


def plot_histogram_age(df):
    data = create_age_category(df)
    data = data[['FatalityId', 'Date', 'VictimName', 'VictimAge', 'VictimGender', 'Location', 'Country-Region', 'AgeGroup']]
    data = data.drop_duplicates(subset=['FatalityId', 'Date', 'VictimName', 'VictimAge', 'VictimGender', 'Location', 'Country-Region', 'AgeGroup'])
    fig = px.histogram(data, x='VictimAge', color_discrete_sequence=['#228b22'], title="<b>Victims Age Distribution</b>", histnorm='percent')
    fig.update_traces(xbins=dict(start=0, end=data['VictimAge'].max(), size=2))
    fig.update_traces(textfont_size=18, marker=dict(line=dict(color='#000000', width=2)))
    fig.update_traces(hovertemplate='<b>Victim Age:</b> %{x}<br><b>Percentage:</b> %{y:.2f}%<extra></extra>')
    set_layout(fig)
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    fig.write_html('results/age_distribution.html')

def plot_victims_age(df):
    data = create_age_category(df)
    data = get_most_frequent_victim_age(data)
    fig = px.bar(data, x='Count', y='AgeGroup', orientation='h', color_discrete_sequence=['#228b22'])
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    set_layout(fig)
    fig.write_html('results/age_victims.html')

def plot_victims_gender(df):
    data = get_most_frequent_victim_gender(df)
    data = data.replace('na', 'Unknown')
    fig = px.pie(data, values='Count', names='VictimGender', hole=.65, color='VictimGender', color_discrete_map={'Male':'#32A77E', 'Female':'#21596A', 'Unknown':'#B7E065'})
    fig.update_traces(textfont_size=18, marker=dict(line=dict(color='#000000', width=2)))
    fig.write_html('results/gender_victims.html')

def plot_most_dangerous_breeds(df):
    data = get_most_dangerous_breed(df)
    data = data[data['Count']>6]
    fig = px.bar(data, x='Count', y='DogBreedsList', orientation='h', color='DogBreedsList', color_discrete_sequence=['#654321'], title="<b>Most Dangerous Dog Breeds</b>")
    #fig = px.pie(data, values='Count', names='DogBreedsList', hole=0.65, color='DogBreedsList', color_discrete_sequence=px.colors.sequential.turbid, title="<b>Most Dangerous Dog Breeds</b>")
    fig.update_traces(textfont_size=18, marker=dict(line=dict(color='#000000', width=2)))
    set_layout(fig)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    fig.write_html('results/most_dangerous_breeds.html')

def plot_most_dangerous_types(df):
    data = map_dog_type(df)
    data = get_most_dangerous_types(data)
    data = data[data['Count']>1]
    data['Percentage'] = data.Count/sum(data.Count)
    fig = px.bar(data, x='Count', y='DogType', orientation='h', color='DogType', color_discrete_sequence=['#654321'], title="<b>Most Dangerous Dog Types</b>", text=data['Percentage'].apply(lambda x: '{0:1.2f}%'.format(x*100)))
    fig.update_traces(hovertemplate='<b>DogType:</b> %{y}<br><b>Count:</b> %{x}<extra></extra>')
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    set_layout(fig)
    fig.update_layout(showlegend=False)#, font=dict(size=14))
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    fig.write_html('results/most_dangerous_types.html')
    py.plot(fig, filename='most_dangerous_types', auto_open = False)

def plot_victim_info(df):
    data = create_age_category(df)
    data = data[['FatalityId', 'Date', 'VictimName', 'VictimAge', 'VictimGender', 'Location', 'Country-Region', 'AgeGroup']]
    data = data.drop_duplicates(subset=['FatalityId', 'Date', 'VictimName', 'VictimAge', 'VictimGender', 'Location', 'Country-Region', 'AgeGroup'])
    data = get_most_frequent_victim_age(data)
    fig = px.bar(data, x='Count', y='AgeGroup', orientation='h', color='VictimGender', color_discrete_map={'Male':'#32A77E', 'Female':'#21596A', 'Unknown':'#B7E065'}, title="<b>Distribution of Victims by Age and Gender</b>", labels={'VictimGender':'Gender'})
    fig.update_traces(textfont_size=18, marker=dict(line=dict(color='#000000', width=2)))
    set_layout(fig)
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.write_html('results/victim_info.html')
    py.plot(fig, filename='victim_info', auto_open = False)

def plot_dog_classification_based_on_circumstance(df):
    dog_classification = pd.read_csv("dog_classification_vs_circumstances.csv")
    data = pd.merge(df.drop_duplicates(subset=['FatalityId','']), dog_classification, on="FatalityId")
    clsf = data.groupby(by='DogClassification').size().reset_index(name='Count').sort_values(by='Count', ascending=False)
    clsf['Percentage'] = clsf.Count/sum(clsf.Count)
    fig = px.pie(clsf, values='Count', names='DogClassification', hole=0.70, color='DogClassification', color_discrete_sequence=px.colors.qualitative.Antique)
    fig.update_traces(textfont_size=15, marker=dict(line=dict(color='#000000', width=2)), textinfo = 'percent+label', textposition='outside')
    fig.update_layout(showlegend=False)
    fig.update_layout(annotations=[dict(text='<b>Was the Dog Part <br>of the Family?</b>', x=0.5, y=0.5, font_size=20, showarrow=False)])
    set_layout(fig)
    fig.write_html('results/dog_classification_based_on_circumstances.html')
    py.plot(fig, filename='dog_classification_based_on_circumstances', auto_open = False)

def plot_time_evolution(df):
    all_years = pd.Series(range(df['Year'].min(), df['Year'].max() + 1), name='Year')
    df.drop_duplicates(subset=['FatalityId', 'Date', 'VictimName', 'VictimAge', 'VictimGender', 'Location', 'Country-Region'], inplace=True)
    data = df.groupby(by='Year').size().reindex(all_years).fillna(0).reset_index(name='Count')
    fig = px.line(data, x='Year', y='Count', markers=True, title="<b>Evolution of Dog Fatalities Over the Past 25 Years</b>", color_discrete_sequence=['#654321'])
    fig.update_xaxes(tickmode='linear')  # Ensures all years are shown on the x-axis
    set_layout(fig)
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    fig.update_traces(textfont_size=18, marker=dict(line=dict(color='#000000', width=2)))
    fig.write_html('results/fatalities_over_the_years.html')
    py.plot(fig, filename='fatalities_over_the_years', auto_open = False)

def plot_histogram_dog_numbers(df):
    data = df[['FatalityId','DogBreedsList','DogsNumber']]
    data.drop_duplicates(inplace=True)
    data = data.groupby(by='FatalityId').sum().reset_index().rename(columns={'DogsNumber':'Sum'}).sort_values(by='Sum', ascending=False)
    fig = px.histogram(data, x='Sum', color_discrete_sequence=['#228b22'], title="<b>Solo or Pack Attack?</b>", histnorm='percent')
    fig.update_traces(xbins=dict(start=0, end=data['Sum'].max(), size=1))
    fig.update_traces(textfont_size=18, marker=dict(line=dict(color='#000000', width=2)))
    fig.update_traces(hovertemplate='<b>Sum:</b> %{x}<br><b>Percentage:</b> %{y:.2f}%<extra></extra>')
    set_layout(fig)
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    fig.write_html('results/dog_numbers_distribution.html')

###
#plot_dog_classification_based_on_circumstance(df)
#plot_victim_info(df)
#plot_histogram_age(df)
#plot_most_dangerous_breeds(df)
plot_most_dangerous_types(df)
#plot_time_evolution(df)
#plot_victims_gender(df)
#plot_histogram_dog_numbers(df)