from app import app
import re
from flask import Flask,flash, session, render_template, request, redirect, url_for
#from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from fpdf import FPDF
row1 = []  
app = Flask(__name__)        
@app.route('/')
def student():
	loc = ("DummyData.xlsx")
	df = pd.read_excel(loc, sheet_name='Sheet1',skiprows=1)
	regno = df['Registration Number'].unique()
	studname = df['Full Name'].unique()
	# to see all the columns
	print(list(df.columns))
	#print(regno,studname)
	# using dictionary comprehension
	# to convert lists to dictionary
	res = {regno[i]: studname[i] for i in range(len(regno))}
	#print(res)
	return render_template('student.html',result=res)
    
@app.route('/result',methods=['GET', 'POST', 'PUT'])
def view_result():
	print("request ::",str(request.form.get('reportcrd')))	
	selected = str(request.form.get('reportcrd')) #selected registration no
	loc = ("DummyData.xlsx")
	df = pd.read_excel(loc, sheet_name='Sheet1',skiprows=1)	
	df.columns = ["Candidate No","Round","First Name","Last Name","Full Name","Registration Number","Grade","Name of School","Gender","Date of Birth","City of Residence","Date and time of test","Country of Residence","Question No.","What you marked","Correct Answer","Outcome (Correct/Incorrect/Not Attempted)","Score if correct","Your score","Final result"]
	print(df['Registration Number'][0])
	fullname = df['Full Name'][0]
	grade = df['Grade'][0]
	school = df['Name of School'][0]
	Gender = df['Gender'][0]
	Dob  = df['Date of Birth'][0]
	final_result = 	df['Final result'][0]
	#stud_img = url_for('static', filename='images/stud-images/'+fullname+'.png')

	#stud_img = re.sub("^/|/$", "", stud_img)
	#img_url = request.url_root + stud_img
	#print(request.url_root)
	#print(stud_img)
	#print(img_url)
	#print("hello here",df[df['Registration Number'] == int(selected)].values)
	getda = df[df['Registration Number'] == int(selected)].values #values gives you the values of your data row as a list!
	#making dataset to store value and display in pdf
	data = [['Ques_no','Marked_ans','Correct_ans','Outcome','Score','Your_score']]
	print(data[0][0])
	#data.append([1,2,3,4,5,6])
	 
	
	for row in getda:
		ques_no = row[13]
		marked_ans = row[14]
		correct_ans = row[15]
		outcome = row[16]
		original_score = row[17]
		your_score = row[18]
		data.append([ques_no,marked_ans,correct_ans,outcome,original_score,your_score]) #adding values in dataset
		#print(ques_no,marked_ans,correct_ans)
	print(data)	
	
	# save FPDF() class into a 
	# variable pdf
	# Create instance of FPDF class
	# Letter size paper, use inches as unit of measure
	pdf=FPDF(format='letter', unit='in')
	  
	# Add new page. Without this you cannot create the document.
	pdf.add_page()
	  
	# set style and size of font 
	# that you want in the pdf
	pdf.set_font("Arial",'',10.0)
	# Effective page width, or just epw
	epw = pdf.w - 2*pdf.l_margin

 
	# Set column width to 1/4 of effective page width to distribute content 
	# evenly across table and page
	col_width = epw/6
	half_size = epw/2
	print("epw:: ",epw,"col_width::",col_width)
	# Document title centered, 'B'old, 14 pt
	pdf.set_font('Times','B',14.0) 
	# create a cell
	pdf.cell(epw, 0.0, 'Marksheet', ln = 1,align='C')
	#pdf.image(img_url, x = None, y = None, w = 0, h = 0, type = 'PNG', link = '')
	pdf.set_font('Times','',10.0)
	pdf.cell(half_size,1.0, txt="Name = "+str(fullname), align='L')
	pdf.cell(half_size,1.0, txt="Regno = "+str(selected), align='R')
	#pdf.set_font('Times','',10.0) 
	pdf.ln(0.5)
	pdf.cell(half_size,0.5, txt="Grade = "+str(grade), align='L')
	pdf.cell(half_size,0.5, txt="School = "+str(school), align='R')

	pdf.ln(0.5)
	pdf.cell(half_size,0.0, txt="Gender = "+str(Gender), align='L')
	pdf.cell(half_size,0.0, txt="Dob = "+str(Dob), align='R')
 
	
	pdf.set_font('Times','',10.0) 
	pdf.ln(0.5)
 
	# Text height is the same as current font size
	th = pdf.font_size

	for row in data:
		for datum in row:
			# Enter data in colums
			# Notice the use of the function str to coerce any input to the 
			# string type. This is needed
			# since pyFPDF expects a string, not a number.
			pdf.cell(col_width, th, str(datum), border=1)
		pdf.ln(th)
	# Line break equivalent to 4 lines
	pdf.ln(4*th)	
	pdf.cell(epw,0.0, txt="Comment = "+str(final_result), align='L')
	  
	# save the pdf with name .pdf
	pdf.output("GFG.pdf")  
	
	return redirect(url_for('.student'))


       
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)

#https://pyfpdfbook.wordpress.com/2015/03/22/table-using-only-cell-borders/  
#http://www.fpdf.org/en/doc/cell.htm
#https://roytuts.com/how-to-create-a-pdf-file-using-python/
#
#  
   