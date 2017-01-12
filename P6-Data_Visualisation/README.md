## Data Visualisation: Survival Rates and Passenger Distribution in Titanic Disaster
by Yue Pan

### Summary
This data visualisation illustrates survival rates and passenger distribution across Sex and Pclass in the Titanic Disaster. It shows how passengers distributed across the three classes and how gender and class influenced the survival rate.

### Design
#### Exploratory Data Analysis with R
After I downloaded the dataset, I conducted exploratory data analysis using Rstudio. I was interested in especially two factors of the passenger, which are Sex and Pclass. I decided to find the distribution of survived passengers across Sex and Pclass.
I found that most passengers(including female and male) were from the 3rd Pclass, but passengers from the 1st Pclass had the largest survival number. Moreover, more female passengers survived no matter which class they were from. 

#### Data Visualisation (d3.js)
Originally, I decided to create a bar chart showing the comparison of survival rates across Pclass and Sex, because compared to the absolute number of survived passengers, survival rate as a proportion of survived to total, is more accurate to show the patterns of survived passengers.
To give more information on the passenger distribution, I added another group of bar charts to show the total number of passengers and the number of passengers who survived.
As survival number is part of the total number, I decided to used overlapped bar charts.

#### Post-feedback Design
After collecting the feedbacks, I made the following changes:
- After the feedback on the initial version, I added another group of overlapped bar charts to show the distribution of passengers, with total and survival number of passengers. 
- After the feedback on the second version, I added animation to show the bar charts only one at a time, so that the audience can focus on one point at a time. 
- The feedbacks on the final version helped me make some modifications on the format of the buttons, as well as adding remarks for hovering. 

### Feedbacks
I interviewed 3 persons and asked for their feedbacks on the data visualisation after prompting them with the background information and a small set of questions. Here are the highlights of their feedbacks:

#### Interview #1
> The bar chart for survival rate is really clear and simple, I can see that female passengers have a absolutely higher survival rates no matter which class they are from. Also, the higher the class, the higher the survival rate. 

> However, as an audience, I would expect more information other than this survival bar chart.

> I like the bar charts of the passenger distribution, as they give the total number, and then survival number inside of the total number, becasue it is part of the total number. However, I think the colour of the bars can be more consistent. For example, it would be nicer if the bars for the survival number are green. 

#### Interview #2
> One thing that I didn't notice was that we can hover on the bars, it will be more clear to give a note so that audience know that they can hover on the bars to see the exact value and category of that bar.

> I like the current colour, which is not too sharp. However, two same legends for female and male can be redundant, better to remove one of them.

> Show three bar charts all together can be too overwhelming. Better to use tabs or show the charts in sequences. 

#### Interview #3
> The final version looks very tidy and let audience to focus on one chart at a time, which is really good. 

> The style of buttons can be more consistent with the charts, and the current clicked button should to be highlighted. 

> I think overall, it looks clean and clear.

### Resources
- [D3 API Reference](https://github.com/d3/d3/blob/master/API.md)
- [Titanic Disaster Analysis](http://bl.ocks.org/ajaydas/raw/79fdc410599e2cae037af679c921cbb6/)
- [Titanic Disaster Introduction](https://www.kaggle.com/c/titanic)
- [Stack Overflow](http://stackoverflow.com/questions/13573771/adding-a-chart-legend-in-d3)
