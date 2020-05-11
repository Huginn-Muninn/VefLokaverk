from flask import Flask, render_template, request
import pyrebase

app = Flask(__name__)

# tengin við firebase realtime database á firebase.google.com ( db hjá danielsimongalvez@gmail.com )
config = {
    # hér kemur tengingin þín við Firebase gagnagrunninn ( realtime database )
	"apiKey": "AIzaSyCDK-GKRwgN8Y5XMnNkhfXpQFhYThDR4gU",
    "authDomain": "lokaverk-aeca6.firebaseapp.com",
    "databaseURL": "https://lokaverk-aeca6.firebaseio.com",
    "projectId": "lokaverk-aeca6",
    "storageBucket": "lokaverk-aeca6.appspot.com",
    "messagingSenderId": "393097867521",
    "appId": "1:393097867521:web:e3cb7f6fed2a74f119eb00",
    "measurementId": "G-PK65QNEXEV"


}

fb = pyrebase.initialize_app(config)
db = fb.database()

# Test route til að setja gögn í db
@app.route('/')
def index():
	return render_template("index.html")


@app.route('/info', methods=['GET', 'POST'])
def info():
	check = False
	y = 0
	if request.method == 'POST':
		notendanafn = request.form['notendanafn']
		lykilord = request.form['lykilord']
		u = db.child("notandi").get().val()
		lst = list(u.items())
		for x in range(len(lst)):
			if lst[y][1]["notendanafn"] == notendanafn:
				y += 1
				print(lst[y][1]["notendanafn"])
				check = False
				break
			elif lst[y][1]["notendanafn"] != notendanafn:
				print(lst[y][1]["notendanafn"])
				check = True
				y+=1
		if check == True:
			db.child("notandi").push({"notendanafn":notendanafn, "lykilorð":lykilord})
			return render_template("sida.html")
		else:
			return "Þetta notendanafn er nú þegar í notkun,<a href='/'>vinsamlegast reyndu aftur</a>"
	else:
		return "<h1>Má ekki</h1>"
		
@app.route('/info2', methods=['GET', 'POST'])
def info2():
	check = False
	y = 0
	if request.method == 'POST':
		notendanafn = request.form['notendanafn']
		lykilord = request.form['lykilord']
		u = db.child("notandi").get().val()
		lst = list(u.items())
		for x in range(len(lst)):
			if lst[y][1]["notendanafn"] == notendanafn:
				if lst[y][1]["lykilorð"] == lykilord:
					y += 1
					check = True
					break
			elif lst[y][1]["notendanafn"] != notendanafn:
				check = False
				y+=1
		if check == True:
			return render_template("sida.html")
		else:
			return "Þetta notendanafn er ekki til,<a href='/'>vinsamlegast reyndu aftur</a>"
	else:
		return "<h1>Má ekki</h1>"



@app.route('/signupp')
def signupp():
	return render_template("signupp.html")

@app.route('/delete')
def delete():
	return render_template("delete.html")

@app.route('/nytt')
def nytt():
	return render_template("nytt.html")

@app.route('/update')
def update():
	return render_template("update.html")

@app.route('/eyda', methods=['GET', 'POST'])
def eyda():
	y = 0
	if request.method == 'POST':
		numer = request.form['numer']
		u = db.child("bill").get().val()
		lst2 = list(u.items())
		for x in range(len(lst2)):
			print(lst2[y][1]["Númer"])
			print(numer)
			if int(lst2[y][1]["Númer"]) == int(numer):
				db.child("bill").child(lst2[y][0]).remove()
				break
			else:
				y += 1
		return render_template("sida.html")
	else:
		return render_template("sida.html")
		
		

@app.route('/updgrate', methods=['GET', 'POST'])
def updgrate():
		y = -1
		if request.method == 'POST':
			fyrirtaeki = request.form['fyrirtaeki']
			gerd = request.form['gerd']
			numer2 = request.form['numer2']
			numer = request.form['numer']
			argerd = request.form['argerd']
			u = db.child("bill").get().val()
			lst2 = list(u.items())
			for x in range(len(lst2)):
				if int(lst2[y][1]["Númer"]) == int(numer2):
					print(1)
					db.child("bill").child(lst2[y][0]).update({"Fyrirtæki":fyrirtaeki, "Gerð":gerd, "Númer":int(numer), "Árgerð":int(argerd)})
					break
				else:
					y += 1
					print(lst2[y][1]["Númer"])
					print(numer2)
			return render_template("sida.html")
		else:
			return render_template("sida.html")

@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		fyrirtaeki = request.form['fyrirtaeki']
		gerd = request.form['gerd']
		numer = request.form['numer']
		argerd = request.form['argerd']
		db.child("bill").push({"Fyrirtæki":fyrirtaeki, "Gerð":gerd, "Númer":int(numer), "Árgerð":int(argerd)}) 
		return render_template("sida.html")
	else:
		return render_template("sida.html")

# Test route til að sækja öll gögn úr db




@app.route('/lesa')
def lesa():
	u = db.child("notandi").get().val()
	lst = list(u.items())
	print(lst)
	print(lst[0][1]["notendanafn"])
	print(len(lst))
	return "Lesum úr grunni"

if __name__ == "__main__":
	app.run(debug=True)

# skrifum nýjan í grunn hnútur sem heitir notandi 
# db.child("notandi").push({"notendanafn":"dsg", "lykilorð":1234}) 

# # förum í grunn og sækjum allar raðir ( öll gögn )
# u = db.child("notandi").get().val()
# lst = list(u.items())
