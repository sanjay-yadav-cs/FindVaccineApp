from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import requests
import os

root=Tk()
icon= PhotoImage(file = 'images/vacineicon.png')
root.geometry("690x600")
root.title("Find Vaccine App")
root.iconphoto(False, icon)
root.config(bg="#d5fdfa")
style=ttk.Style()
fr1=Frame(bg="#8ab5d4",width=340,height=600,bd=5,relief=SUNKEN)
fr1.grid(row=0,column=0)
fr2=Frame(bg="orange",width=345,height=600,padx=0,pady=0,bd=5,relief=SUNKEN)
fr2.grid(row=0,column=1)
root.resizable(0,0)


covishield=BooleanVar()
covaxin=BooleanVar()
sputnik=BooleanVar()
age=StringVar()
dose=StringVar()
fees_type=StringVar()




#***********************-------state name in list-------**********************#

states=[]
distic=[]

stateapi="https://cdn-api.co-vin.in/api/v2/admin/location/states"     #      
data=requests.get(stateapi).json()                                    #     chombokbox me state ke name set karne ke liye 
for i in data["states"]:                                              #   $$ appending state name in list so it display in combobox kyo ki chombobox me value lis se set
    states.append(i["state_name"])                                    #      hote hai
                                                                             


#***********************************----LABEL OF GET DISTRICT------*************************

white1=PhotoImage(file="images\white.png") #x diffrence 27 y diffrence 41
white1=white1.subsample(3,4)
ll=Label(fr1,image=white1,font=('Courier',13),bg="#8ab5d4",compound=BOTTOM)#x diff =19 y diff= 16
# ll.place(x=20,y=130)
cbstate=ttk.Combobox(root,values=states,width=17,justify="center",state="r")
cbstate.set("Select State")

l5=Label(fr1,image=white1,font=('Courier',13),bg="#8ab5d4",compound=BOTTOM)
cbdist=ttk.Combobox(root,values=distic,width=17,justify="center",state="r")
cbdist.set("Select District")

l3=Label(fr1,image=white1,text="Pincode",font=('Courier',13),bg="#8ab5d4",compound=BOTTOM,height=60)
pincodeentry=Entry(fr1,width=13,bd=False,font=("serif",13))




#************************************************************************************************************

def dist():
    # getstate()
    global searchbydist
    global searchbypin
    ll.place(x=20,y=130)
    cbstate.place(x=39,y=146)
    l5.place(x=20,y=180)
    cbdist.place(x=39,y=196)
    l3.place_forget()               # label l3 ko hide karene ke liye { widget.mager_forget() }
    pincodeentry.place_forget()
    searchbydist=True
    searchbypin=False
    cbstate.focus()
dist()

def pincode():
    global searchbydist
    global searchbypin
    l3.place(x=20,y=132)
    pincodeentry.place(x=39,y=165,height=22)
    ll.pack_forget()
    cbstate.place_forget()
    l5.place_forget()
    cbdist.place_forget()
    searchbypin=True
    searchbydist=False
    pincodeentry.focus()





#****************---------Finding State Id------*********************#

def getstate(event):
    global state_id
    try:
        if searchbydist:                                                            
            cbdist.set("Select Distric")            #checkbox ka first value set kiye
            state_name=cbstate.get()                                   ######
            for i in data["states"]:                                          #
                if i["state_name"]==state_name:                               #  #agar search by district true hai to use distric name ka use kare 
                    distic.clear()                                            #    #data ko itrate kare usme compare karke state id find karnge
                    state_id=str(i["state_id"])                         ######
                    districapi="https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+state_id
                    data1=requests.get(districapi).json()
                    for j in data1["districts"]:
                        distic.append(j["district_name"])           #appending district name in list so it display in  combobox
                    break
            cbdist.config(values=distic)
    except Exception as e:
        print(e)
cbdist.bind('<Button-1>',getstate)         # binding event when click on slect distric combobox to then call function 
                                                #   getstaete jisse use state id milega aur wo use hoga api me




#*************----Featching information for check boxes check by user

def check_condition():
    global vaccine_var1
    global vaccine_var2
    global vaccine_var3
    global fee_type1
    global fee_type2
    global minage
    
    if covishield.get()&covaxin.get()&sputnik.get():
        vaccine_var1="COVISHIELD"
        vaccine_var2="COVAXIN"
        vaccine_var3="SPUTNIC"
    elif covishield.get()&covaxin.get():
        vaccine_var1="COVISHIELD"
        vaccine_var2="COVAXIN"
        vaccine_var3="COVAXIN"
    elif covishield.get():                  #checkbox ke var $covishied ka value fetch karke check karega ki true hai ki nahi (get boolean value dega kyoki usbar
        vaccine_var1="COVISHIELD"                                                                                                    #         boolean declare ha)
        vaccine_var2="COVISHIELD"
        vaccine_var3="COVISHIELD"
    elif covaxin.get():
        vaccine_var1="COVAXIN"
        vaccine_var2="COVAXIN"
        vaccine_var3="COVAXIN"
    elif sputnik.get():
        vaccine_var1="SPUTNIC"
        vaccine_var2="SPUTNIC"
        vaccine_var3="SPUTNIC"

    if fees_type.get()=="both":
        fee_type1="Free"
        fee_type2="Paid"                         #fee_type=bool(i["fee_type"]=="Paid")
    if fees_type.get()=="free":
         fee_type1="Free"
         fee_type2="Free"
    if fees_type.get()=="paid":
         fee_type1="Paid"
         fee_type2="Paid"

    if age.get()=="15-all":
        minage=15
        # maxage=44
    if age.get()=="18-44":
        minage=18
        # maxage=44
    if age.get()=="45+":
        minage=45

    '''if dose_1.get():
        dose_var1=
        dose_var2=
    if dose_2.get():'''
    



#***************---------MAIN FUNCTIN FOR FINDING SLOTS--------*******************************

def main():
    global pin
    global date
    global dist
    try:
        text_box.config(state="normal")
        text_box.delete("1.0","end")
        if searchbydist:
            finddisticid_api="https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+str(state_id)           #api for get

            data1=requests.get(finddisticid_api).json()    #####
            distt_name=cbdist.get()                               #
            for j in data1["districts"]:                           #         FINDGING DISTRIC ID using state id from above api
                if j["district_name"]==distt_name:                  #
                    dist=j["district_id"]                           #
                    break                                      #####
        else:
            pin=pincodeentry.get()
            if pin=="":
                messagebox.showerror('Find Vaccine App','Please Enter Pincode')
                pincodeentry.focus()
    except Exception as d:
        messagebox.showerror('Find Vaccine App','Please Chosee State And District')
        cbstate.focus()
    date=dateEntry.get()                     #Feching date form entry box
    if date=="":
        messagebox.showerror('Find Vaccine App','Please Enter Date')  #if date in entered showing error msg
        dateEntry.focus()
    else:
        findAvailability()
        if os.stat(r"vaccinedetail.txt").st_size == 0:
           text_box.insert(END,"Slots Not Avilable")
        else:
            s=open(r"vaccinedetail.txt","r")
            slotdata=s.read()
            text_box.insert(END,slotdata)               #INSERTING SLOT_DATA/ message data into texbox
            text_box.config(state="disabled")           #texbox state disable kiya inset ke bad taki koi texbox edit na kar sake   (i["fee_type"]=="t")==True)


#***************************----------MAIN FUNCTION---------********************************************

def findAvailability():
    try:
        fh=open(r"vaccinedetail.txt","r+")
        fh.truncate()           # after every call ersae data from file jisse usme purana data nahi rahega
        fh.close()
        if searchbydist:
            url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}'.format(dist,date)  # districid and date api
        if searchbypin:
            url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+pin+"&date="+date  # pincode and date api
        data=requests.get(url).json()
        for i in data['sessions']:
            check_condition()       # check contion selected from chrckbox and radiobutton
            if((i["available_capacity"]>0)&(i["min_age_limit"]==minage)&((i["fee_type"]==fee_type1)|(i["fee_type"]==fee_type2))&(((i["vaccine"]==vaccine_var1)|(i["vaccine"]==vaccine_var2)|(i["vaccine"]==vaccine_var3)))):


                message='Vaccine: {} \nArea: {} \nPincode: {} \n\nAge Group: {} \nCenter Name: {} \nDate: {} \nDose1 Slot: {} \nDose2 Slot: {} \n\nCost: {} \n'.format(i["vaccine"],i["block_name"],i["pincode"],i["min_age_limit"],i["name"],date,i["available_capacity_dose1"],i["available_capacity_dose2"],i["fee_type"])
                message=message+'\n\n*******************************\n\n'
                # text_box.insert(END,message+"\n\n\n")
                fh=open(r"vaccinedetail.txt","a")
                msa=fh.write(message)
                fh.close()
    except:
        messagebox.showerror('Find Vaccine App','Please Select Parameters')
        
#*************************---------HEADINGS-------**********************************

head=Label(fr1,text="Find Vaccine Availability Tracker",font=("FANTASY",15,"bold"),bg="#BF2200",bd=5,relief=RAISED)
head.place(x=10,y=8)

l=Label(fr1,text="Search By District or Pincode",font=('Arial',12,'bold'),bg="#f2ff00",padx=0,bd=2,relief=RAISED)
l.place(x=10,y=50)

#***************-------DISTRIC BUTTON-----*******************************************8

red=PhotoImage(file=r"images\red.png")
red=red.subsample(4,4)
l1=Label(fr1,image=red,font=('Courier',100,'bold'),fg="red",bg="#8ab5d4",padx=0)
l1.place(x=35,y=80)
lred=Button(fr1,text="DISTRICT",font=('Arial',10),fg="black",bg="#ff5722",bd=False,padx=4,pady=5,command=dist,cursor="hand2")
lred.place(x=58,y=90)

#**************----------PINCODE BUTTON---------*****************************************command=lambda: hide_button(cal)

green=PhotoImage(file=r"images\green.png")
green=green.subsample(4,4)
l2=Label(fr1,image=green,font=('Courier',100,'bold'),fg="red",bg="#8ab5d4")
l2.place(x=180,y=80)
lgreen=Button(fr1,text="PINCODE",font=('Arial',10),fg="black",bg="#009688",bd=False,padx=4,pady=5,command=pincode,cursor="hand2")
lgreen.place(x=200,y=89)




#*******************----------SELECT DATE-----------*********************************

white=PhotoImage(file=r"images\white.png") #x diffrence 27 y diffrence 41
white=white.subsample(3,4)
ldate=Label(fr1,image=white,text="Select Date",font=('Courier',13),bg="#8ab5d4",compound=BOTTOM,height=60)
ldate.place(x=180,y=132)

dateEntry=Entry(fr1,width=13,bd=False,font=("serif",13))
dateEntry.place(x=198,y=165,height=22)


#******************************SELECT VACCINE***************************


violet=PhotoImage(file=r"images\violet.png")
violet=violet.subsample(4,4)
l4=Label(fr1,image=violet,text="Select Vaccine",font=('Courier',14,"bold"),bg="#8ab5d4",compound=BOTTOM)
l4.place(x=10,y=220)
cb_vaccine=Checkbutton(fr1,text="Covishield",bg="#b84aff",font=("fantasy",11),variable=covishield, onvalue=1, offvalue=0,activebackground="#b84aff",cursor="hand2")
cb_vaccine.place(x=30,y=255)
cb_vaccine=Checkbutton(fr1,text="Covaxin",bg="#b84aff",font=("fantasy",11),variable=covaxin, onvalue=1, offvalue=0,activebackground="#b84aff",cursor="hand2")
cb_vaccine.place(x=130,y=255)
cb_vaccine=Checkbutton(fr1,text="Sputnik V",bg="#b84aff",font=("fantasy",11),variable=sputnik, onvalue=1, offvalue=0,activebackground="#b84aff",cursor="hand2")
cb_vaccine.place(x=220,y=255)


#****************************SELECT AGE***********************************


pink=PhotoImage(file=r"images\pink.png")
pink=pink.subsample(4,4)
l4=Label(fr1,image=pink,text="Select Age",font=('Courier',14,"bold"),bg="#8ab5d4",compound=BOTTOM)
l4.place(x=10,y=300)
rb_age=Radiobutton(fr1,text=" 15+",bg="#ff0058",font=("fantasy",11),variable=age, value="15-all",activebackground="#b84aff",cursor="hand2")
rb_age.place(x=40,y=335)
rb_age=Radiobutton(fr1,text="18-44",bg="#ff0058",font=("fantasy",11),variable=age, value="18-44",activebackground="#b84aff",cursor="hand2")
rb_age.place(x=130,y=335)
rb_age=Radiobutton(fr1,text="  45+",bg="#ff0058",font=("fantasy",11),variable=age,value="45+",activebackground="#b84aff",cursor="hand2")
rb_age.place(x=220,y=335)


#*********************************DOSE*******************************


greenlong=PhotoImage(file=r"images\greenlong.png")
greenlong=greenlong.subsample(4,4)
l4=Label(fr1,image=greenlong,text="Dose",font=('Courier',14,"bold"),bg="#8ab5d4",compound=BOTTOM)  # y diffrence is 35
l4.place(x=10,y=375)
rb_dose=Radiobutton(fr1,text="ALL",bg="green",font=("fantasy",11),variable=dose,value="all_dose",activebackground="#b84aff",cursor="hand2")
rb_dose.place(x=40,y=410)
rb_dose=Radiobutton(fr1,text="Dose 1",bg="green",font=("fantasy",11),variable=dose,value="dose_1",activebackground="#b84aff",cursor="hand2")
rb_dose.place(x=130,y=410)
rb_dose=Radiobutton(fr1,text="Dose 2",bg="green",font=("fantasy",11),variable=dose,value="dose_2",activebackground="#b84aff",cursor="hand2")
rb_dose.place(x=220,y=410)



#****************************-----FEE TYPE-----*********************************


orangelong=PhotoImage(file=r"images\orangelong.png")
orangelong=orangelong.subsample(4,4)
l4=Label(fr1,image=orangelong,text="Fee Type",font=('Courier',14,"bold"),bg="#8ab5d4",compound=BOTTOM)  # y diffrence is 35
l4.place(x=10,y=450)
rb_fees=Radiobutton(fr1,text=" All",bg="orange",font=("fantasy",11),variable=fees_type,activebackground="#b84aff",value="both",cursor="hand2")
rb_fees.place(x=40,y=485)
rb_fees=Radiobutton(fr1,text="Free",bg="orange",font=("fantasy",11),variable=fees_type,activebackground="#b84aff",value="free",cursor="hand2")
rb_fees.place(x=130,y=485)
rb_fees=Radiobutton(fr1,text="Paid",bg="orange",font=("fantasy",11),variable=fees_type,activebackground="#b84aff",value="paid",cursor="hand2")
rb_fees.place(x=220,y=485)


#*************************------FIND BUTTON------************************


findb=PhotoImage(file=r"images\find.png")
findb=findb.subsample(4,4)
l_find_bn=Label(fr1,image=findb,font=('Courier',14),bg="#8ab5d4",compound=BOTTOM)
l_find_bn.place(x=100,y=540)


findbtn=Button(fr1,text="Find",font=("fantasy",10,"bold"),padx=35,bg="#34eb4f",command=main,cursor="hand2",bd=False)
findbtn.place(x=120,y=549)


#************------TEXT BOX SHOWING RESULT -------****************************

text_box = Text(fr2,bg="#F5DEB3",height=28,width=35,font=("Garamond",15,"bold"),wrap="word")
text_box.place(x=1,y=0)

sbr=Scrollbar(fr2)                              # Making Scroll Bar
sbr.place(x=321,y=0,height=600)                 #
                                                #     
sbr.config(command=text_box.yview)              # connecting scrollbar textbox ke 'yview' arttribute ko horizontal scroll view ke liye
text_box.config(yscrollcommand=sbr.set)         #


root.mainloop()