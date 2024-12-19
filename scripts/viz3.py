# visualization 3, funding vs poverty
# scatterplot that shows school poverty vs funding
# we already know that poverty impacts achievement, from previous graph
# now we want to show the correlation between poverty and funding
# we are going to do this using data from NCES and the Census Bureau

# data are not available at the city level
levels2 = {"New York State": "NY", "United States": "NT"}

level2 = "NY"

level_selector2 = widgets.Dropdown(options=levels2, description="Level:", value="NT")

# Source: https://nces.ed.gov/ccd/elsi/tableGenerator.aspx
povertyDF = pd.read_csv("data/DistrictFundingData.csv")
# Source: https://www.census.gov/data/datasets/2022/demo/saipe/2022-school-districts.html
censusDF = pd.read_csv("data/ussd22.csv")
censusDF["Agency ID - NCES Assigned [District] Latest available year"] = (
    censusDF["State FIPS Code"].astype(str).str.zfill(2)
    + censusDF["District ID"].astype(str).str.zfill(5)
).astype(np.int64)
# combine both FIPS ID with the distrcit ID from census data

df3 = pd.merge(censusDF, povertyDF)

# divide children in poverty by the total population
df3["Percentage in poverty"] = (
    df3[
        "Estimated number of relevant children 5 to 17 years old in poverty who are related to the householder"
    ]
    .str.replace(",", "")
    .astype(int)
    / df3["Estimated Population 5-17"].str.replace(",", "").astype(int)
    * 100
)

# clean and organize data
df3 = df3[
    df3[
        "Total Expenditures (TOTALEXP) per Pupil (V33) [District Finance] 2021-22"
    ].str.isnumeric()
]
df3["Expenditures per student"] = df3[
    "Total Expenditures (TOTALEXP) per Pupil (V33) [District Finance] 2021-22"
].astype(int)
df3.dropna(subset=["Expenditures per student", "Percentage in poverty"], inplace=True)

# create the visualization
fw3 = go.FigureWidget()
fw3.layout.title = "District Per Pupil Funding vs. Childhood Poverty"
fw3.layout.xaxis.title = "Percentage of children living in poverty [%]"
fw3.layout.yaxis.title = "Expenditures [$/student]"
scatter = go.Scatter(
    x=df3["Percentage in poverty"],
    y=df3["Expenditures per student"],
    mode="markers",
    text=df3["Agency Name"],
    name="District Data",
    marker={"color": marker_colors['PC:P7']},
)
fw3.add_trace(scatter)
X = df3["Percentage in poverty"]
X = sm.add_constant(X)
model = sm.OLS(df3["Expenditures per student"], X).fit()
X_pred = sm.add_constant(np.linspace(0, 100, 100))
yModel = model.predict(X_pred)
line = go.Scatter(
    x=np.linspace(0, 100, 100), y=yModel, mode="lines", name="Line of Best Fit",
    marker={"color": marker_colors['PC:P9']},
)
fw3.add_trace(line)

# updates the figure depending on level selection
def update_poverty(change):
    level2 = level_selector2.value
    # need to restrict data based on the area

    if level2 == "NT":
        tempdf = df3
    elif level2 == "NY":
        tempdf = df3[
            df3["State Abbr [District] Latest available year"].str.contains("NY")
        ]
    elif level2 == "XN":
        # NEW YORK CITY per pupil data not available
        tempdf = df3[df3["Agency Name [District] 2021-22"].str.contains("NEW YORK CITY")]
    with fw3.batch_update():
        fw3.data[0].y = (
            sm.OLS(tempdf["Expenditures per student"], tempdf["Percentage in poverty"])
            .fit()
            .predict(np.linspace(0, 100, 100))
        )
        fw3.data[0].x = tempdf["Percentage in poverty"]
        fw3.data[0].y = tempdf["Expenditures per student"]
        fw3.data[0].text = tempdf["Agency Name"]

level_selector2.observe(update_poverty, "value")

container3 = widgets.VBox([widgets.HBox([level_selector2]), fw3])
container3