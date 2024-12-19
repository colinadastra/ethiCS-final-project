# visualization 1

# variables to populate dropdowns
levels = {"New York City": "XN", "New York State": "NY", "United States": "NT"}

level = "NT"

level_selector1 = widgets.Dropdown(options=levels, description="Level:", value="NT")

subjects = ["Mathematics", "Reading", "Science"]

subject = "Mathematics"

subscales = {"Mathematics": "MRPCM", "Reading": "RRPCM", "Science": "SRPUV"}

subscale = "RRPCM"

years = {
    "Mathematics": [
        1990,
        1992,
        1996,
        1996,
        2000,
        2003,
        2005,
        2007,
        2009,
        2011,
        2013,
        2015,
        2017,
        2019,
        2022,
    ][::-1],
    "Reading": [
        1992,
        1994,
        1998,
        1998,
        2002,
        2003,
        2005,
        2007,
        2009,
        2011,
        2013,
        2015,
        2017,
        2019,
        2022,
    ][::-1],
    "Science": [2009, 2015, 2019][::-1],
}

year = 2019

grades = {"Mathematics": [4, 8], "Reading": [4, 8, 12], "Science": [4, 8, 12]}

grade = 8

variable = "SLUNCH3"

stattype = "MN:MN,PC:P1,PC:P2,PC:P5,PC:P7,PC:P9"

stattypes = {
    "MN:MN": "Mean",
    "PC:P1": "10th Percentile",
    "PC:P2": "25th Percentile",
    "PC:P5": "50th Percentile",
    "PC:P7": "75th Percentile",
    "PC:P9": "90th Percentile",
}

marker_colors = {
    "MN:MN": px.colors.qualitative.Prism[10],
    "PC:P1": px.colors.qualitative.Prism[7],
    "PC:P2": px.colors.qualitative.Prism[5],
    "PC:P5": px.colors.qualitative.Prism[4],
    "PC:P7": px.colors.qualitative.Prism[1],
    "PC:P9": px.colors.qualitative.Prism[0],
}

# method to build the dataframe
def build_frame1(subject="Mathematics", year=year, level=level, grade=grade):
    subscale = subscales[subject]
    response = rq.urlopen(
        f"https://www.nationsreportcard.gov/Dataservice/GetAdhocData.aspx?type=data"
        f"&subject={subject.lower()}"
        f"&grade={grade}"
        f"&subscale={subscale}"
        f"&variable={variable}"
        f"&jurisdiction={level}"
        f"&stattype={stattype}"
        f"&year={year}"
    )
    response_string = response.read().decode("utf-8")
    try:
        df1 = pd.DataFrame(json.loads(response_string)["result"])
        df1.loc[df1["value"] == 999] = 0
        return df1
    except:
        return response_string

# method to build the the figure with graph objects (plotly)
def build_figure1(df1):
    traces = []
    for stat in stattypes.keys():
        trace = go.Bar(
            x=df1.loc[df1["stattype"] == stat]["varValueLabel"],
            y=df1.loc[df1["stattype"] == stat]["value"],
            name=stattypes[stat],
            marker={"color": marker_colors[stat]},
        )
        traces.append(trace)
    return traces

# create the initial frame and build the figure
df1 = build_frame1(subject="Mathematics", year=2019, grade=8)
fw1 = go.FigureWidget(
    data=build_figure1(df1),
    layout=go.Layout(
        barmode="group",
        title=f"{grade}th Grade {subject} NAEP Scores and Federal Lunch Program Eligibility, {year}, {dict(zip(levels.values(), levels.keys()))[level]}",
    ),
)
fw1.layout.xaxis.title="Eligibility for free or reduced-price lunch"
fw1.layout.yaxis.title=f"{subject} NAEP score"

def alert_dialog(message):
    button = widgets.Button(description="OK")
    output = widgets.Output()

    def on_button_clicked(b):
        with output:
            print("Alert dismissed.")
            button.close()
            output.clear_output()

    button.on_click(on_button_clicked)
    display(widgets.VBox([widgets.HTML(f"<b>{message}</b>"), button, output]))

# method to update the figure
def update_figure(change):
    changed = False
    global subject, year, level, grade
    if (
        (subject != subject_selector.value)
        or (year != year_selector.value)
        or (grade != grade_selector.value)
        or (level != level_selector1.value)
    ):
        changed = True
    subject = subject_selector.value
    year = year_selector.value
    level = level_selector1.value
    grade = grade_selector.value
    if changed:
        try:
            df1 = build_frame1(subject, year, level, grade)
            with fw1.batch_update():
                for i, stat in enumerate(stattypes):
                    fw1.data[i].x = df1.loc[df1["stattype"] == stat]["varValueLabel"]
                    fw1.data[i].y = df1.loc[df1["stattype"] == stat]["value"]
                fw1.update_layout(
                    title=f"{grade}th Grade {subject} NAEP Scores and Federal Lunch Program Eligibility, {year}, {dict(zip(levels.values(), levels.keys()))[level]}"
                )
                fw1.layout.yaxis.title=f"{subject} NAEP score"
        except:
            alert_dialog("Data not found! Please try again!")

# create the widgets
grade_selector = widgets.Dropdown(options=grades["Mathematics"], description="Grade:", value=8)
subject_selector = widgets.Dropdown(options=subjects, description="Subject:")
year_selector = widgets.Dropdown(options=years["Mathematics"], description="Year:", value=2019)

# method to update the years dropdown
# this is called when the subject is changed
def update_years1(*args):
    year = year_selector.value
    grade = grade_selector.value
    year_selector.options = years[subject_selector.value]
    grade_selector.options = grades[subject_selector.value]
    try: # try to maintain the same grade and year if possible
        year_selector.value = year
        grade_selector.value = grade
    except: # if not, never mind
        pass

level_selector1.observe(update_figure, "value")
subject_selector.observe(update_years1, "value")
subject_selector.observe(update_figure, "value")
year_selector.observe(update_figure, "value")
grade_selector.observe(update_figure, "value")
grade_selector.observe(update_years1, "value")
container1 = widgets.VBox(
    [widgets.HBox([level_selector1, subject_selector, year_selector, grade_selector]), fw1]
)
container1