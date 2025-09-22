import tkinter as tk
from tkinter import messagebox
import random
import pyperclip

# --- Resistor Data ---
color_codes = {"Black":0,"Brown":1,"Red":2,"Orange":3,"Yellow":4,
               "Green":5,"Blue":6,"Violet":7,"Gray":8,"White":9,"Gold":-1,"Silver":-2}
tolerance_codes = {"Brown":"±1%","Red":"±2%","Green":"±0.5%","Blue":"±0.25%","Violet":"±0.1%","Gray":"±0.05%",
                   "Gold":"±5%","Silver":"±10%"}
color_hex = {"Black":"#000000","Brown":"#5C4033","Red":"#FF0000","Orange":"#FF8C00",
             "Yellow":"#FFD700","Green":"#008000","Blue":"#0000FF","Violet":"#8B00FF",
             "Gray":"#808080","White":"#FFFFFF","Gold":"#FFD700","Silver":"#C0C0C0"}

# --- Tkinter GUI Setup ---
root = tk.Tk()
root.title("Resistor Calculator - Left Input Layout with Result")
root.geometry("1400x900")
root.config(bg="#ADD8E6")

# --- Frames Layout ---
left_frame = tk.Frame(root, bg="#ADD8E6", width=500)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

right_frame = tk.Frame(root, bg="#ADD8E6", width=900)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# --- Resistor Canvas on Right ---
canvas = tk.Canvas(right_frame, width=850, height=300, bg="#ADD8E6", highlightthickness=0)
canvas.pack(pady=10)

# --- Target Resistance Entry on Left ---
tk.Label(left_frame, text="Enter Target Resistance (Ω):", bg="#ADD8E6", font=("Helvetica",12)).pack(pady=5)
target_resistance = tk.Entry(left_frame, width=15)
target_resistance.pack(pady=5)

# --- Band Selection Dropdown ---
tk.Label(left_frame, text="Select Band Count:", bg="#ADD8E6", font=("Helvetica",12)).pack(pady=5)
band_count = tk.IntVar(value=4)
band_selector = tk.OptionMenu(left_frame, band_count, 3,4,5)
band_selector.pack(pady=5)

# --- Sparkle Animation ---
glow_bands=[]
glow_phase=0
glow_alpha=0
sparkles=[]

def init_sparkles():
    global sparkles
    sparkles=[]
    for _ in range(30):
        x=random.randint(120,550)
        y=random.randint(80,160)
        size=random.randint(2,6)
        sparkles.append([x,y,size,random.randint(1,3)])

def draw_resistor(bands):
    global glow_bands
    glow_bands=bands.copy()
    canvas.delete("all")
    canvas.create_oval(80,70,570,170,fill="#debeb3",outline="#debeb3")
    canvas.create_line(0,120,80,120,width=6,fill="silver")
    canvas.create_line(570,120,800,120,width=6,fill="silver")
    start_x=120
    for band in glow_bands:
        if band in color_hex:
            canvas.create_rectangle(start_x,80,start_x+30,160,fill=color_hex[band],outline="#FFFFFF",width=2)
        start_x+=45
    for s in sparkles:
        canvas.create_oval(s[0],s[1],s[0]+s[2],s[1]+s[2],fill="white",outline="white")

def animate_glow():
    global glow_phase,glow_alpha,sparkles
    canvas.delete("glow")
    start_x=120
    for band in glow_bands:
        if band in color_hex:
            width=1+glow_alpha*6
            canvas.create_rectangle(start_x,80,start_x+30,160,fill=color_hex[band],outline="#FFFFFF",width=width,tags="glow")
        start_x+=45
    for s in sparkles:
        s[0]+=s[3]
        if s[0]>550: s[0]=120; s[1]=random.randint(80,160)
        canvas.create_oval(s[0],s[1],s[0]+s[2],s[1]+s[2],fill="white",outline="white",tags="glow")
    glow_alpha += 0.05 if glow_phase==0 else -0.05
    glow_phase = 0 if glow_alpha<0 else 1 if glow_alpha>1 else glow_phase
    canvas.after(50,animate_glow)

# --- Current Bands ---
current_bands = ["Black","Black","Black","Black","Gold"]

# --- Result Label on Left ---
result_label = tk.Label(left_frame, text="Resistance:", font=("Helvetica",14,"bold"), bg="#ADD8E6", fg="black")
result_label.pack(pady=10, side="bottom")

def update_resistor():
    draw_resistor(current_bands)
    try:
        digits = [color_codes[b] for b in current_bands if color_codes.get(b,10)>=0]
        if band_count.get()==3:
            value=int("".join(map(str,digits[:2])))*(10**digits[2])
            tol="±20%"
        elif band_count.get()==4:
            value=int("".join(map(str,digits[:2])))*(10**digits[2])
            tol=tolerance_codes.get(current_bands[3],"±5%")
        elif band_count.get()==5:
            value=int("".join(map(str,digits[:3])))*(10**digits[3])
            tol=tolerance_codes.get(current_bands[4],"±5%")
        try:
            target_val = int(target_resistance.get())
            if value == target_val:
                result_label.config(text=f"Resistance: {value} Ω   Tolerance: {tol} ✅ Target matched!")
            else:
                result_label.config(text=f"Resistance: {value} Ω   Tolerance: {tol} ❌ Target: {target_val} Ω")
        except:
            result_label.config(text=f"Resistance: {value} Ω   Tolerance: {tol}")
    except:
        result_label.config(text="Resistance: Custom")

def select_color(band_index, color):
    current_bands[band_index] = color
    update_resistor()

def change_band_count(event=None):
    n = band_count.get()
    for i in range(5):
        if i<n:
            color_buttons[i].pack(pady=5)
        else:
            color_buttons[i].pack_forget()
    update_resistor()

# --- Color Buttons on Left ---
color_buttons=[]
for i in range(5):
    frame=tk.Frame(left_frame, bg="#ADD8E6")
    frame.pack(pady=5)
    for color in color_hex.keys():
        btn = tk.Button(frame, text=color, bg=color_hex[color],
                        fg="white" if color!="Yellow" else "black",
                        width=8, command=lambda i=i, c=color: select_color(i,c))
        btn.pack(side="left", padx=3)
    color_buttons.append(frame)

# --- Buttons ---
def show_full_info():
    info=""
    for idx, b in enumerate(current_bands[:band_count.get()]):
        info+=f"Band {idx+1}: {b}\n"
    messagebox.showinfo("Full Info", info)

full_info_btn = tk.Button(left_frame, text="Show Full Info", command=show_full_info, bg="blue", fg="white", width=20)
full_info_btn.pack(pady=10)

def show_resistance_info():
    messagebox.showinfo("Resistance Info", "Resistance is opposition to current flow (Ω)")

learn_btn = tk.Button(left_frame, text="Learn About Resistance", command=show_resistance_info, bg="purple", fg="white", width=25)
learn_btn.pack(pady=10)

# --- Initialize ---
init_sparkles()
animate_glow()
update_resistor()
change_band_count()

root.mainloop()
