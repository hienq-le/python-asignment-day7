# Day 7
import os, csv, flask, pandas
database_file_name = 'day7.csv'
input_file_name = 'day7_input.json'
app = flask.Flask(__name__)
header = ["Product ID", "Product Name", "Price"]
# Declare a global-value class
class global2:
	id2 = str
# Check if Error 404 exists
@app.errorhandler(404) 
def invalid_route(e): 
    return flask.jsonify({'errorCode' : 404, 'message' : 'Error: Route not found'})
# Create home page
@app.route('/', methods=['GET', 'POST'])
def index():
	try:
		file1 = open(database_file_name, 'r')
	except FileNotFoundError:
		file1 = open(database_file_name, 'w')
		file2 = csv.writer(file1)
		file2.writerow(header)
	return flask.render_template('index.html')
# Show database
@app.route("/table", methods=['GET', 'POST'])
def diplay_database_as_table():
	data_to_table = pandas.read_csv(database_file_name)
	return flask.render_template("table.html", tables=[data_to_table.to_html()], titles=[''])
# Overwrite the database from json, remove duplicates on product ID
@app.route("/overwrite", methods=['GET', 'POST'])
def overwrite():
	if os.path.exists(input_file_name) == False:
		print('File ' + input_file_name + ' NOT found!')
		return flask.render_template('overwrite_fail.html')
	else:
		file3 = pandas.read_json(input_file_name, orient='records')
		if file3.empty == True:
			print('Fail to overwrite Products!')
			return flask.render_template('overwrite_fail.html')
		if file3.shape[0] >= 2:
			for i5 in range(1, file3.shape[0]):
				if file3.iloc[i5]['Product ID'] == file3.iloc[i5-1]['Product ID']:
					file3.drop(file3.iloc[i5].index, axis=0, inplace=True)
					file3.reset_index(drop=True, inplace=True)
					continue		
		file3.to_csv(database_file_name, index = False)
		print('Overwrite the database successfully!')
		return flask.render_template('overwrite_success.html')
# Add products in json to database
@app.route("/add-products", methods=['GET', 'POST'])
def add_products():
	if os.path.exists(input_file_name) == False:
		print('Fail to add Products')
		return flask.render_template('add_products_fail.html')
	else:
		file6 = pandas.read_json(input_file_name, orient='records')
		file6.to_csv('temp.csv', index = False)
		file10 = pandas.read_csv(database_file_name)
		file12 = pandas.read_csv('temp.csv')
		if file12.empty == True:
			os.remove('temp.csv')
			print('Fail to add Products')
			return flask.render_template('add_products_fail.html')
		else:
			try:
				for i5 in range(file10.shape[0]):
					abcxyz2 = file10.iloc[i5]['Product ID']
					file12.drop(file12[file12['Product ID'] == abcxyz2].index, axis=0, inplace=True)
					file12.reset_index(drop=True, inplace=True)
					continue
				if file12.empty == True:
					os.remove('temp.csv')
					print('Fail to add Products')
					return flask.render_template('add_products_fail.html')
				else:
					file12.to_csv(database_file_name, mode='a+', header=None, index=False)
					os.remove('temp.csv')
					print('Add products successfully')
					return flask.render_template('add_products_success.html')
			except Exception:
				os.remove('temp.csv')
				print('Fail to add Products')
				return flask.render_template('add_products_fail.html')
# Update products from json to database
@app.route("/update-products", methods=['GET', 'POST'])
def update_products():
	if os.path.exists(input_file_name) == False:
		print('Fail to update Products')
		return flask.render_template('update_products_fail.html')
	else:
		file6 = pandas.read_json(input_file_name, orient='records')
		file6.to_csv('temp.csv', index=False)
		file10 = pandas.read_csv(database_file_name)
		file12 = pandas.read_csv('temp.csv')
		if file12.empty == True:
			os.remove('temp.csv')
			print('Fail to update Products')
			return flask.render_template('update_products_fail.html')
		else:
			try:
				for i5 in range(file10.shape[0]):
					for j5 in range(file12.shape[0]):
						abcxyz2 = file12.iloc[j5]['Product ID']
						if file10.iloc[i5]['Product ID'] == abcxyz2:
							file10.iloc[i5] = file12.iloc[j5]
							continue
					continue
				if file12.empty == True:
					os.remove('temp.csv')
					print('Fail to update Products')
					return flask.render_template('update_products_fail.html')
				else:
					file12.to_csv(database_file_name, index=False)
					os.remove('temp.csv')
					print('Update products successfully')
					return flask.render_template('update_products_success.html')
			except Exception:
				os.remove('temp.csv')
				print('Fail to update Products')
				return flask.render_template('update_products_fail.html')
# Check for file day7_input.json to delete
@app.route("/delete", methods=['GET', 'POST'])		
def delete_file_check():
	if os.path.exists(input_file_name) == False:
		print('Fail to delete Products because file '+input_file_name+': NOT found!')
		return flask.render_template('delete_products_fail1.html')
	else:
		return flask.render_template('delete_products_success1.html')
# Show delete confirmation
@app.route("/delete/delete-confirmation", methods=['GET', 'POST'])		
def delete_confirmation():
	return flask.render_template('delete_confirmation.html')
@app.route("/delete/delete-result", methods=['GET', 'POST'])
# Delete by product ID
def delete_by_id():
	file19 = pandas.read_csv(database_file_name)
	file60 = pandas.read_json(input_file_name, orient='records')
	file60.to_csv('temp.csv', index=False)
	file61 = pandas.read_csv('temp.csv')
	if file19.empty == True or file61.empty == True:
		os.remove('temp.csv')
		print('Fail to delete products!')
		return flask.render_template('delete_products_fail2.html')
	else:
		try:
			for i60 in range(file61.shape[0]):
				abcxyz3 = file61.iloc[i60]['Product ID']
				file19.drop(file19[file19['Product ID'] == abcxyz3].index, axis=0, inplace=True)
				file19.reset_index(drop=True, inplace=True)
				continue
		except Exception:
			os.remove('temp.csv')
			print('Fail to delete products!')
			return flask.render_template('delete_products_fail2.html')
		os.remove('temp.csv')
		file19.to_csv(database_file_name, index=False)
		print('Delete products successfully!')
		return flask.render_template('delete_products_success2.html')
if __name__ == '__main__':
	app.run(debug = True, port = 5000)