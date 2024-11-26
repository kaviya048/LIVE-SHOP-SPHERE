from datetime import date

from flask import Flask, render_template, request, session, flash, send_file

import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/FarmerLogin')
def FarmerLogin():
    return render_template('FarmerLogin.html')


@app.route('/CustomerLogin')
def CustomerLogin():
    return render_template('CustomerLogin.html')


@app.route('/NewCustomer')
def NewCustomer():
    return render_template('NewCustomer.html')


@app.route("/ANewProduct")
def ANewProduct():
    return render_template('ANewProduct.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/AFarmerInfo")
def AFarmerInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmertb  ")
    data = cur.fetchall()
    return render_template('AFarmerInfo.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/FNewProduct")
def FNewProduct():
    return render_template('FNewProduct.html')


@app.route("/FSales")
def FSales():
    uname = session['fname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where fname='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()
    return render_template('FSales.html', data1=data1)


@app.route("/fnewproduct", methods=['GET', 'POST'])
def fnewproduct():
    if request.method == 'POST':
        pname = request.form['pname']
        ptype = request.form['ptype']
        price = request.form['price']
        qty = request.form['qty']
        info = request.form['info']
        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)
        uname = 'admin'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO   uprotb VALUES ('','" + pname + "','" + ptype + "','" + price + "','" + qty + "','" + info + "','" + savename + "','" + uname + "')")
        conn.commit()
        conn.close()

    flash('New Product Register successfully')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM uprotb where fname='" + uname + "'")
    data = cur.fetchall()
    return render_template('FNewProduct.html', data=data)


@app.route("/Update")
def Update():
    uid = request.args.get('id')
    session['uid'] = uid
    return render_template('Update.html')


@app.route("/fnewupdate", methods=['GET', 'POST'])
def fnewupdate():
    if request.method == 'POST':
        price = request.form['price']
        qty = request.form['qty']
        uname = 'admin'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cursor = conn.cursor()
        cursor.execute(
            "update  uprotb set price='" + price + "',Qty='" + qty + "'  where  id ='" + session['uid'] + "'")
        conn.commit()
        conn.close()
        flash(' Product Update  Register successfully')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM uprotb where fname='" + uname + "'")
        data = cur.fetchall()
        return render_template('FNewProduct.html', data=data)


@app.route("/FPRemove")
def FPRemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from uprotb where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('Product  info Remove Successfully!')
    return FNewProduct()


@app.route("/newcust", methods=['GET', 'POST'])
def newcust():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')

    return render_template('NewCustomer.html')


@app.route("/clogin", methods=['GET', 'POST'])
def clogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['cname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('CustomerLogin.html')
        else:

            session['cadd'] = data[4]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('CustomerHome.html', data=data)


@app.route("/CustomerHome")
def CustomerHome():
    uname = session['cname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM  regtb where username='" + uname + "'  ")
    data = cur.fetchall()

    return render_template('CustomerHome.html', data=data)


@app.route("/CSearch")
def CSearch():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM uprotb ")
    data = cur.fetchall()
    return render_template('CSearch.html', data=data)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ptype = request.form['ptype']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM uprotb where  ProductType ='" + ptype + "'")
        data = cur.fetchall()

        return render_template('CSearch.html', data=data)


@app.route("/Add")
def Add():
    id = request.args.get('id')
    session['pid'] = id
    fname = request.args.get('name')

    import cv2
    from ultralytics import YOLO

    # Load the YOLOv8 model
    model = YOLO('runs/detect/fruit/weights/best.pt')
    # Open the video file
    # video_path = "path/to/your/video/file.mp4"
    cap = cv2.VideoCapture(0)
    dd1 = 0
    dd2 = 0

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        dd2 += 1
        print(dd2)

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame, conf=0.7)
            for result in results:
                if result.boxes:
                    box = result.boxes[0]
                    class_id = int(box.cls)
                    object_name = model.names[class_id]
                    print(object_name)

                    if object_name == fname:
                        dd1 += 1

            if dd1 == 50:
                print('yes')
                cv2.waitKey(1)
                cap.release()
                cv2.destroyAllWindows()
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM uprotb  where id='" + id + "' ")
                data = cur.fetchall()

                return render_template('AddCart.html', data=data)
            if dd2 == 1000:
                print('no')

                cv2.waitKey(1)
                cap.release()
                cv2.destroyAllWindows()

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM uprotb ")
                data = cur.fetchall()
                flash('Product Not Found..!')
                return render_template('CSearch.html', data=data)



            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    # Release the video capture object and close the display window





@app.route("/addcart", methods=['GET', 'POST'])
def addcart():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        pid = session['pid']
        uname = session['cname']
        qty = request.form['qty']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM uprotb  where  id='" + pid + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[1]
            Producttype = data[2]
            price = data[3]
            cQty = data[4]

            Image = data[6]
            fname = data[7]

        else:
            return 'No Record Found!'

        tprice = float(price) * float(qty)

        clqty = float(cQty) - float(qty)

        if clqty < 0:

            flash('Low  Product ')

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM uprotb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('AddCart.html', data=data)

        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
            cursor = conn.cursor()
            cursor.execute(
                "update  uprotb set Qty='" + str(clqty) + "' where  id='" + pid + "' ")
            conn.commit()
            conn.close()
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO carttb VALUES ('','" + uname + "','" + ProductName + "','" + Producttype + "','" + str(
                    price) + "','" + str(qty) + "','" + str(tprice) + "','" +
                Image + "','" + date + "','0','','" + fname + "','" + session['cadd'] + "')")
            conn.commit()
            conn.close()

            flash('Add To Cart  Successfully')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM uprotb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('AddCart.html', data=data)


@app.route("/Cart")
def Cart():
    uname = session['cname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]
    else:
        return 'No Record Found!'

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)


@app.route("/RemoveCart")
def RemoveCart():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from carttb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product Remove Successfully!')

    uname = session['cname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)


@app.route("/payment", methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        uname = session['cname']
        cname = request.form['cname']
        Cardno = request.form['cno']
        Cvno = request.form['cvno']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
        data1 = cursor.fetchone()
        if data1:
            tqty = data1[0]
            tprice = data1[1]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  *   FROM  carttb where UserName='" + uname + "' and Status='0' ")
        data22 = cursor.fetchall()
        for x in data22:
            ffname = x[11]
            print(ffname)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) As count  FROM booktb ")
        data = cursor.fetchone()
        if data:
            bookno = data[0]
            print(bookno)

            if bookno == 'Null' or bookno == 0:
                bookno = 1
            else:
                bookno += 1

        else:
            return 'Incorrect username / password !'

        if bookno == 'Null' or bookno == 0:
            bookno = 1
        else:
            bookno += 1

        bookno = 'BOOKID' + str(bookno)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cursor = conn.cursor()
        cursor.execute(
            "update   carttb set status='1',Bookid='" + bookno + "' where UserName='" + uname + "' and Status='0' ")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO booktb VALUES ('','" + uname + "','" + bookno + "','" + str(tqty) + "','" + str(
                tprice) + "','" + cname + "','" + Cardno + "','" + Cvno + "','" + date + "')")
        conn.commit()
        conn.close()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
        data1 = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
        data2 = cur.fetchall()

    return render_template('CBookInfo.html', data1=data1, data2=data2)


def sendmail(Mailid, message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


@app.route("/CBookInfo")
def CBookInfo():
    uname = session['cname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
    data2 = cur.fetchall()

    return render_template('CBookInfo.html', data1=data1, data2=data2)


@app.route("/ASalesInfo")
def ASalesInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where   Status='1' ")
    data1 = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2liveshopdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb ")
    data2 = cur.fetchall()
    return render_template('ASalesInfo.html', data1=data1, data2=data2)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
