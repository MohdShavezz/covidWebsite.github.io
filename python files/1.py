from flask import Flask, redirect, url_for, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Data=pd.read_csv("covid_19_dataset.csv")

app = Flask(__name__)


# ....Script start................


Data.drop(["Province/State","Lat","Long",'WHO Region'],axis=1,inplace=True)

Data.rename(columns={"Country/Region":"Country"},inplace=True)

Top=Data[Data["Date"]==Data["Date"].max()]

Top.reset_index(inplace=True)
World=Top.groupby("Country")["Confirmed","Deaths","Recovered","Active"].sum()

World.reset_index(inplace=True)

Data.drop(["Country","Date"],axis=1,inplace=True)

from sklearn import linear_model
r=linear_model.LinearRegression()
active_=r.fit(Data[['Confirmed','Deaths','Recovered']],Data.Active)
confirmed_=r.fit(Data[['Deaths','Recovered','Active']],Data.Confirmed)
deaths_=r.fit(Data[['Confirmed','Recovered','Active']],Data.Deaths)
recovered_=r.fit(Data[['Confirmed','Deaths','Active']],Data.Recovered)


active_ = str(active_.predict([[72822,2728,288229]]))
confirmed_ = str(confirmed_.predict([[666,8127,7031]]))
deaths_ = str(deaths_.predict([[15824,8127,7011]]))
recovered_ = str(recovered_.predict([[15824,66,7031]]))

print(active_,confirmed_,deaths_,recovered_)
a=np.array([active_,confirmed_,deaths_,recovered_])
# ....script end...
@app.route("/")
def home():
    return a

@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()