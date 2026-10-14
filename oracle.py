import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def money(x): return jround(x*100)/100
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)
def comma(x):
    if isinstance(x,float) and x==int(x): x=int(x)
    return f"{x:,}"
def money2(x): return f"{money(x):.2f}"

def chart(sqft):
    if sqft<=150: return 5000
    if sqft<=250: return 6000
    if sqft<=300: return 7000
    if sqft<=350: return 8000
    if sqft<=400: return 9000
    if sqft<=450: return 10000
    if sqft<=550: return 12000
    if sqft<=700: return 14000
    return sqft*20

def size_plan(sqft,height):
    if not num(sqft): return {"error":"the room area must be a number"}
    if not num(height): return {"error":"the ceiling height must be a number"}
    if sqft<=0: return {"error":"the room area must be above zero"}
    if height<=0: return {"error":"the ceiling height must be above zero"}
    return {"btu":jround(chart(sqft)*height/8)}

def render_size(r,sqft,height):
    return ("Your "+jsnum(sqft)+" sq ft room with "+jsnum(height)+" ft ceilings wants about "+comma(r["btu"])
            +" BTU before conditions - add 10% for full sun, drop 10% for deep shade, add 4,000 for a kitchen, and 600 per person past two.")

def power_plan(btu,ceer):
    if not num(btu): return {"error":"the BTU rating must be a number"}
    if not num(ceer): return {"error":"the CEER must be a number"}
    if btu<=0: return {"error":"the BTU rating must be above zero"}
    if ceer<=0: return {"error":"the CEER must be above zero"}
    return {"watts":r1(btu/ceer)}

def render_power(r,btu,ceer):
    return ("The "+comma(btu)+" BTU unit at CEER "+jsnum(ceer)+" pulls about "+jsnum(r["watts"])
            +" watts while the compressor runs - the box prints the BTU big and the efficiency that divides it small.")

def bill_plan(watts,hours,rate):
    if not num(watts): return {"error":"the wattage must be a number"}
    if not num(hours): return {"error":"the hours must be a number"}
    if not num(rate): return {"error":"the rate must be a number"}
    if watts<=0: return {"error":"the wattage must be above zero"}
    if hours<0: return {"error":"the hours cannot be negative"}
    if hours>24: return {"error":"a day only has 24 hours"}
    if rate<=0: return {"error":"the rate must be above zero"}
    kwh=watts/1000*hours
    return {"kwh":r1(kwh),"day":money(kwh*rate),"month":money(kwh*rate*30)}

def render_bill(r,watts,hours,rate):
    return ("At "+jsnum(watts)+" watts for "+jsnum(hours)+" hours a day and $"+money2(rate)
            +" per kWh, the room uses "+jsnum(r["kwh"])+" kWh and costs about $"+money2(r["day"])+" a day, $"+money2(r["month"])
            +" over a 30-day month - the yellow sticker priced a shorter season at a cheaper kilowatt.")

cases=[]
def add(tool,args):
    if tool=="size": r=size_plan(*args); fn=render_size
    elif tool=="power": r=power_plan(*args); fn=render_power
    else: r=bill_plan(*args); fn=render_bill
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(300,8),(450,9),(320,9),(200,10),(150,8),(151,8),(250,8),(251,8),(350,8),(451,8),(550,8),(551,8),(700,8),(701,8),(1000,8)]:
    add("size",a)
for a in [(8000,11),(12000,12),(5000,12),(14000,11.5),(10000,10)]:
    add("power",a)
for a in [(727,8,0.17),(1000,6,0.22),(909,10,0.16),(1200,4,0.1),(727,0,0.17)]:
    add("bill",a)
add("size",[0,8]); add("size",[300,0]); add("size",["big",8]); add("size",[300,"tall"])
add("power",[0,11]); add("power",[8000,0]); add("power",["cold",11])
add("bill",[0,8,0.17]); add("bill",[727,-1,0.17]); add("bill",[727,25,0.17]); add("bill",[727,8,0]); add("bill",["big",8,0.17])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
