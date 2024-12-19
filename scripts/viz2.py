# visualization 2, funding by state over time

df2 = pd.read_csv("data/FundingData.csv")
# different traces for each state
fw2 = go.FigureWidget()
fw2.layout.title = "State Per Pupil Funding over Time"
fw2.layout.xaxis.title = "Year"
fw2.layout.yaxis.title = "Funding [$/student]"
x = np.array(range(2021, 1986, -1))
colors = list(marker_colors.values())
for i, state in enumerate(df2["State Name"].unique()):
    # x is the year, y is the funding. individual bars are the state
    # y should access the single row of funding for the state
    fw2.add_scatter(
        x=x,
        y=df2.loc[df2["State Name"] == state].to_numpy()[0][1:],
        name=state,
        marker={"color": colors[i % len(colors)]},
    )
container2 = fw2