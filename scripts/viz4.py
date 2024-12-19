# visualization 4 (part 3)
# Use the same level and subject selector, make a new variable selector

subjects = ["Mathematics", "Reading", "Science"]

subject = "Mathematics"

subscales2 = {"Mathematics": "MWPCM", "Reading": "RRPCM", "Science": "SRPUV"}

subscale2 = subscales2[subject]

variables = {
    "Percent of teachers absent on average day": "C036501",
    "School type is independent charter": "C0863J1",
    "Talk about studies at home": "B017451",
    "Use laptop or desktop computer during class": "B034701",
    "Use tablet during class": "B034801",
    "Days absent from school in the last month": "B018101",
}

factor = "C036501"

def build_frame4(
    subject=subject,
    factor=factor,
    year=year,
    level=level
):
    subscale2 = subscales2[subject]
    url = (
        f"https://www.nationsreportcard.gov/Dataservice/GetAdhocData.aspx?type=data"
        + f"&subject={subject.lower()}"
        + f"&grade=12"
        + f"&subscale={subscale2}"
        + f"&variable={factor}"
        + f"&jurisdiction={level}"
        + f"&stattype={stattype}"
        + f"&year={year}"
    )
    # print(url)
    response = rq.urlopen(url)
    response_string = response.read().decode("utf-8")
    try:
        df = pd.DataFrame(json.loads(response_string)["result"])
        return df
    except:
        return response_string

def build_figure4(df):
    traces = []
    if isinstance(df, str):
        print(df)
        alert_dialog("Couldn't retrieve that, sorry!")
    else: 
        for stat in stattypes.keys():
            trace = go.Bar(
                x=df.loc[df["stattype"] == stat]["varValueLabel"],
                y=df.loc[df["stattype"] == stat]["value"],
                name=stattypes[stat],
                marker={"color": marker_colors[stat]},
            )
            traces.append(trace)
        return traces

df4 = build_frame4()
variable_plain = dict(zip(variables.values(), variables.keys()))[factor].title()
fw4 = go.FigureWidget(
    data=build_figure4(df4),
    layout=go.Layout(
        barmode="group",
        title=f"12th Grade {subject} NAEP Scores and {variable_plain}, {year}, {dict(zip(levels.values(), levels.keys()))[level]}",
    ),
)
fw4.layout.xaxis.title = variable_plain

def update_figure4(change):
    subject = subject_selector.value
    factor = variable_selector.value
    level = level_selector1.value
    grade = grade_selector.value
    # what happens when the API complains?
    df = build_frame4(subject, factor, year, level)
    if isinstance(df, str):
        alert_dialog("Couldn't retrieve that, sorry!")
    else: 
        with fw4.batch_update():
            for i, stat in enumerate(stattypes):
                fw4.data[i].x = df.loc[df["stattype"] == stat]["varValueLabel"]
                fw4.data[i].y = df.loc[df["stattype"] == stat]["value"]
            factor_plain = dict(zip(variables.values(), variables.keys()))[factor]
            fw4.update_layout(
                title=f"{grade}th Grade {subject} NAEP Scores and {factor_plain.title()}, {year}, {dict(zip(levels.values(), levels.keys()))[level]}",
            )
            fw4.layout.xaxis.title = factor_plain

variable_selector = widgets.Dropdown(options=variables, description="Variable:")

level_selector1.observe(update_figure4, "value")
subject_selector.observe(update_figure4, "value")
variable_selector.observe(update_figure4, "value")

container4 = widgets.VBox(
    [widgets.HBox([level_selector1, subject_selector, year_selector, variable_selector]), fw4]
)
container4