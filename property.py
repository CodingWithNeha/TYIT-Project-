from flask import (Blueprint, 
                render_template, 
                redirect, 
                url_for,
                session)
# from authenticate import Registration, Upload
import sqlite3
import json

dynamic_view = Blueprint("property", __name__, static_folder="static", template_folder="templates")


## Task :- Reduce the redundancy from view and property function
@dynamic_view.route('/<string:fetch_view>',methods=['POST','GET'])
def view(fetch_view: str):
    if not session:
        return redirect(url_for("user.login"))

    if fetch_view == "view1":
        return render_template('view1.html')
    elif fetch_view == "view2":
        return render_template('view2.html')
    elif fetch_view == "view3":
        return render_template('view3.html')
    elif fetch_view == "view4":
        return render_template('view4.html')
    elif fetch_view == "view5":
        return render_template('view5.html')
    else:
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        results = cur.execute('SELECT * FROM property where view = ?', (fetch_view,))
        for record in results:
            # records.append(record)
            view = record[10]
            if fetch_view == view:
                proprietor_id = record[1]
                file = open(f'static/upload/{proprietor_id}/{proprietor_id}.json')
                data = json.load(file)
                property = data['property']
                property = property[0]
                uploaded_property = property['uploaded_property']
                image_info = []
                for images in uploaded_property['uploaded_images']:
                    name = images['image']
                    file = open(f'static/upload/{proprietor_id}/{name}')
                    del images['image']
                    images['src'] = file.read()
                    image_info.append(images)
                return render_template('dynamic_view.html', property_records=image_info)

        return redirect(url_for("property.property")) ## as property is the function of property.py 

@dynamic_view.route('/property',methods=['POST','GET'])
def property():
    if session:
        records = []
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        results = cur.execute('SELECT * FROM property')
        for record in results:
            records.append(record)
        return render_template('property.html', property_records=records)
    return redirect(url_for("user.login"))

@dynamic_view.route('/UploadProperty',methods=['POST','GET'])
def UploadProperty():
    if session:
        return render_template('UploadProperty.html')
    return redirect(url_for('user.login'))