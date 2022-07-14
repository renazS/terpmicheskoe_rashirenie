import re
import tkinter as tk

coef_a = {
    "ZnO2": -60,
    "SnO2": -45,
    "Al2O3": -30,
    "Sb2O3": 75,
    "BeO": 45,
    "MgO": 60,
    "CaO": 130,
    "SrO": 160,
    "BaO": 200,
    "ZnO": 50,
    "CdO": 115,
    "CoO": 50,
    "NiO": 50,
    "CuO": 30,
    "Li2O": 270,
    "Na2O": 395,
    "K2O": 495,
    "CaF2": 180,
    "Na2SiF6": 340,
    "P2O5": 140
}

Atom_massa = {
    "N": 14,
    "Al": 27,
    "Ba": 137,
    "Br": 80,
    "H": 1,
    "Fe": 56,
    "I": 127,
    "K": 39,
    "O": 16,
    "Si": 28,
    "Mg": 37,
    "Cu": 63,
    "Na": 23,
    "Hg": 201,
    "Pb": 207,
    "S": 32,
    "Ag": 108,
    "C": 12,
    "P": 31,
    "F": 19,
    "Cl": 35.5,
    "Zn": 65,
    "Be": 9,
    "Sn": 119,
    "Ca": 40,
    "Sr": 88,
    "Cd": 112,
    "Co": 59,
    "Ni": 59,
    "Li": 7,
    "Sb": 121,
    "Ti": 48,
    "B": 11
}


def razbit_veshestvo(v):
    data = []
    elements = re.sub(r"([A-Z])", r' \1', v).split()
    for elem in elements:
        found = False
        count_elems = len(elem)
        for letter_index in range(count_elems):
            is_Num = elem[letter_index].isnumeric()
            if found == False and is_Num:
                found = True
                data.append([elem[:letter_index], float(elem[letter_index:])])
                break
        if not found:
            data.append([elem, 1])
    return data


def calc(elements):
    summa = 0
    summarnaya_molyarnaya_massa = 0

    mi = []

    for veshestvo in elements:
        """Суммарная молярная масса вещества"""
        data = razbit_veshestvo(veshestvo)
        for elem_kolvo in data:
            t = Atom_massa[elem_kolvo[0]] * elem_kolvo[1]
            summarnaya_molyarnaya_massa += t

    for veshestvo in elements:
        """Дольное соотношение"""
        mi_elem = 0
        data = razbit_veshestvo(veshestvo)
        for elem_kolvo in data:
            t = Atom_massa[elem_kolvo[0]] * elem_kolvo[1]
            mi_elem += t
        mi.append(mi_elem / summarnaya_molyarnaya_massa)

    for veshestvo_index in range(len(elements)):
        summa = 0
        # SiO2
        if elements[veshestvo_index] == "SiO2":
            if mi[veshestvo_index] < 67:
                a = 38 - 1.0 * (mi[veshestvo_index] * 100 - 67)
            else:
                a = 5
            summa += a * mi[veshestvo_index]
        # B2O3
        elif elements[veshestvo_index] == "B2O3":
            if mi[veshestvo_index] < 10:
                a = -50
            elif mi[veshestvo_index] < 25:
                a = -38
            elif mi[veshestvo_index] < 50:
                a = -25
            elif mi[veshestvo_index] < 75:
                a = -13
            else:
                a = 0

            summa += a * mi[veshestvo_index]
        elif elements[veshestvo_index] == "PbO":
            if mi[veshestvo_index] >= 1 / 3:
                a = 130
            else:
                a = 190
            summa += a * mi[veshestvo_index]
        elif elements[veshestvo_index] == "TiO2":
            try:
                index = elements.index("SiO2")
                mol_SiO2 = mi[index]
                if 80 > mol_SiO2 * 100 > 50:
                    a = 30 - 1.5 * (mol_SiO2 - 50)
            except:
                pass

            if mi[veshestvo_index] >= 1 / 3:
                a = 130
            else:
                a = 190
            summa += a * mi[veshestvo_index]
        else:
            a = coef_a[elements[veshestvo_index]]
            m = mi[veshestvo_index]
            a * mi[veshestvo_index]
            summa += a * mi[veshestvo_index]
    return summa



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.num_izmer = 1
        self.x = 50
        self.points = []
        self.result = None
        self.title("Расчет линейного коэффициента термического расширения стекла")
        self.geometry("1000x700")
        self.Left_Frame = tk.Frame(width=500, height=500, bg="white")
        self.Left_Frame.grid(row=1,column=1)
        self.Right_Frame = tk.Frame(width=500, height=500, bg="blue")
        self.Right_Frame.grid(row=1, column=2)

        self.elements = list(coef_a.keys()) + ["SiO2", "B2O3", "PbO", "TiO2"]

        self.obj_list = []
        el_index = 0
        for row in range(1, 450, 80):
            for column in range(1, 500, 140):
                self.obj_list.append(self.ElementConteiner(row, column, self.elements[el_index]))
                el_index += 1

        self.canvas = tk.Canvas(self.Right_Frame, width=500, height=500, bg="#effffe")
        self.canvas.place(x=0, y=0)
        self.canvas.create_line(0, 400, 470, 400, fill="black")
        self.canvas.create_text(480.0, 400.0, text="0", )

        self.ButtonCalc = tk.Button(self.Right_Frame, text="Рассчитать коэффициент", command=self.calc)
        self.ButtonCalc.place(x=80, y=450)

        self.ButtonClear = tk.Button(self.Right_Frame, text="Очистить график", command=self.clearChart)
        self.ButtonClear.place(x=250, y=450)

        self.Frame_info = tk.Frame(width=1000, height=200)
        self.Frame_info.grid(row=2,column=1,columnspan=2)
        self.Info = tk.Text(self.Frame_info, height=200, width=125, wrap="word")
        self.Info.place(x=0,y=0)

    def clearChart(self):
        self.x = 70
        for elem in self.points:
            self.canvas.delete(elem)
        for Container in self.obj_list:
            Container[2].delete(0,tk.END)
            Container[2].insert(0, "0")
        self.Info.delete("1.0", tk.END)
        self.num_izmer = 1

    def increase(self, entry):
        counter = int(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(counter + 1))

    def decrease(self, entry):
        counter = int(entry.get())
        if counter > 0:
            entry.delete(0, tk.END)
            entry.insert(0, str(counter - 1))

    def calc(self):
        current_elements = []
        for Container in self.obj_list:
            for i in range(int(Container[2].get())):
                current_elements.append(Container[0])
        self.result = round(calc(current_elements), 3)
        self.draw_point()
        text = f"Измерение №{self.num_izmer}. Оксиды: " + ", ".join(current_elements)+ f". Линейный коэф-нт = {self.result}/10^7"+"\n "
        self.Info.insert(tk.END, text)
        self.num_izmer += 1

    def draw_point(self):
        self.points.append(self.canvas.create_oval(self.x - 2, 500 - (self.result // 3 * 2 + 100 - 2), self.x + 2,
                                                   500 - (self.result // 3 * 2 + 100 + 2), fill="red"))
        self.points.append(
            self.canvas.create_text(self.x - 3, 500 - (self.result // 3 * 2 + 100 + 10), text=str(self.result)+ "/10^7"))
        self.x += 100

    def ElementConteiner(self, r, c, name_element):
        text = tk.StringVar()
        text.set("0")
        row = r
        column = c
        tk.Label(self.Left_Frame, text=name_element, bg="white").place(x=row + 20, y=column)
        decreaseButton = tk.Button(self.Left_Frame, text="-", width=1, height=1, command=lambda: self.decrease(entry))
        decreaseButton.place(x=row + 1, y=column + 20)
        entry = tk.Entry(textvariable=text, master=self.Left_Frame, width=5)
        entry.place(x=row + 20, y=column + 25)
        encrease = tk.Button(self.Left_Frame, text="+", width=1, height=1, command=lambda: self.increase(entry))
        encrease.place(x=row + 50, y=column + 20)
        return [name_element, decreaseButton, entry, encrease]


if __name__ == "__main__":
    app = App()
    app.mainloop()

