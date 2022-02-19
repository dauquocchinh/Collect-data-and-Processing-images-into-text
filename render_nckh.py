
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/detect',methods=['POST'])
def detect():
    title=[]
    date=[]
    congty=[]
    content=[]
    for x in request.form.values():
        if str(x)=='https://www.topcv.vn/viec-lam':
            from Full import tools_all
            tools = pickle.load(open('df.pkl','rb'))
    for i in range(0,8):
        title.append(tools['title'][i])
        date.append(tools['date'][i])
        congty.append(tools['congty'][i])
        content.append(tools['content'][i][0])
        content.append(tools['content'][i][1])
        content.append(tools['content'][i][2])
    return render_template('content.html',title_0=title[0],date_0=date[0],congty_0=congty[0],content_0=content[0]+content[1]+content[2],
                                          title_1=title[1],date_1=date[1],congty_1=congty[1],content_1=content[3]+content[4]+content[5],
                                          title_2=title[2],date_2=date[2],congty_2=congty[2],content_2=content[6]+content[7]+content[8],
                                          title_3=title[3],date_3=date[3],congty_3=congty[3],content_3=content[9]+content[10]+content[11],
                                          title_4=title[4],date_4=date[4],congty_4=congty[4],content_4=content[12]+content[13]+content[14],
                                          title_5=title[5],date_5=date[5],congty_5=congty[5],content_5=content[15]+content[16]+content[17],
                                          title_6=title[6],date_6=date[6],congty_6=congty[6],content_6=content[18]+content[19]+content[20],
                                          title_7=title[7],date_7=date[7],congty_7=congty[7],content_7=content[21]+content[22]+content[23])
if __name__ == '__main__':
    app.run(host='localhost',port=8002)
