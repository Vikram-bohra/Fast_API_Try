from fastapi import FastAPI, Request , Depends, BackgroundTasks,status
# from starlette.responses import RedirectResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import models
from sqlalchemy.orm import Session
from database import engine,SessionLocal

from pydantic import BaseModel

from models import Questions, Student
from sqlalchemy import String
from starlette.status import HTTP_302_FOUND,HTTP_303_SEE_OTHER

#Creating a fast api instance

app = FastAPI()

#setting the templates directory
templates = Jinja2Templates(directory = "templates")


models.Base.metadata.create_all(bind=engine)

class get_name(BaseModel):
	name: str

# Creating a database session
def get_db():
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()

global c
c = 1
@app.get("/")
def dashboard(request : Request,db : Session = Depends(get_db)):
	global c
	data = db.query(Questions).all()
	single = db.query(Questions).filter(models.Questions.id == c).first()
	if single == None:
		print("get /")
		c = 1
		return RedirectResponse("/first")
	return templates.TemplateResponse("dashboard.html",{'request':request, "data":data ,"i":single})


global l
l = []
@app.get("/post/{marks}")
async def score(request : Request,marks : int):
	global c
	global l
	c = c+1
	l.append(marks)
	return RedirectResponse("/")
	# return templates.TemplateResponse("dashboard.html",{'request':request,"i":marks})

global name,c1,stu_id,temp
c1 = 0


@app.post("/name")
async def data_store(student_name : get_name,db : Session = Depends(get_db)):
	global name,c1,stu_id,temp
	c1 = 1
	name = student_name.name
	temp = l.copy()
	l.clear()
	print(name,temp)
	student = Student()
	student.name = name
	student.marks = sum(temp)
	db.add(student)
	db.commit()
	stu_id = student.id
	print("\n data added")
	# return RedirectResponse(url = "/first",status_code=status.HTTP_303_SEE_OTHER)

@app.get("/first")
def name2(request: Request,db : Session = Depends(get_db)):
	
	global c1
	print("first",c1)
	if c1 == 1:
		c1 = 0
		print("/ first")
		return RedirectResponse('/end')
	
	return templates.TemplateResponse("first_page.html",{'request':request})

@app.post('/first')
def trying():
	return RedirectResponse('/first',status_code=303)

@app.get("/end")
def total(request:Request):
	if sum(temp) < 50:
		per = '''
The Guider

you are accepted everywhere
People loves you
because you are good listner,communicator and have a good sense of humor.
You have an intutive sense of the emotions of others,and often act as an emotional barometer for the people around them.
The best jobs for you
Market research analyst
public relations specialist
teacher
social worker
therapist
		'''
	if sum(temp) >= 50 and sum(temp) < 100:
		per='''
The artist
You are happy to be who you are.
You live in a colorful world inspired by connections with people and ideas.
The biggest challenge for you is planning for the future.
finding constructive ideals to base their goals on and working out goals is the hardest things to do.
The Jobs for you
Artist
Graphic Designer
Arhitect
Fashion designer
Photographer
Actor/Actress
Writer,Editor
		'''

	if sum(temp) >= 100 and sum(temp) < 150:
		per = '''
The leader
You are special,you can be whoever you like.
People in this type embody the gifts of charisma and confidence.
The Jobs for you
Judge
Lawyer
Enterpreneur
project manager
accountant
financial advisor

		'''
	if sum(temp) >= 150:
		per = '''
The Scientist
You are a genius thats super hard to find
You enjoys theoretical and abstact concepts,dislikes confusion,disorientaion and inefficiency.
You are more focused on the future than on the present.
The Jobs
Scientist
doctor
pilot
austronuat
computer programmer
		'''
	return templates.TemplateResponse("final.html",{"request":request, "marks":sum(temp),'name':name,'personality':per})