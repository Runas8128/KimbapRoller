import typing

import os
import sys
import webbrowser

import tkinter
import tkinter.font
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk

import adofaiParser

PosType = typing.Dict[str, int]
ElementType = typing.Tuple[tkinter.Widget, PosType]
LabelType = typing.Tuple[tkinter.Label, PosType]

def Pos(x: int = 0, y: int = 0, width: int = 0, height: int = 0, anchor: str = '') -> PosType:
    pos: PosType = {}

    if x != 0: pos['x'] = x
    if y != 0: pos['y'] = y
    if width != 0: pos['width'] = width
    if height != 0: pos['height'] = height
    if anchor != '': pos['anchor'] = anchor

    return pos

def Font(family: str, size: int) -> tkinter.font.Font:
    return tkinter.font.Font(family=family, size=size)

class UI:
    def __init__(self):
        self.Elements: typing.List[ElementType] = []
        self.Labels: typing.List[LabelType] = []
        self.adofaiFileName: str = ''

        self.BuildWindow()
        self.InitValues()
        self.BuildElements()
        self.PlaceElements()

    def BuildWindow(self):
        self.window = tkinter.Tk()

        self.window.title("얼불춤용 김밥말이")
        self.window.geometry("640x480")
        self.window.resizable(False, False)

        def closeWindow(event):
            self.window.withdraw()
            sys.exit()
            
        self.window.bind('<Escape>', closeWindow)
    
    def InitValues(self):
        self.Log = tkinter.StringVar(self.window, value='', name='Log')
    
    def BuildLabel(self, text: str, font: tkinter.font.Font, pos: PosType, parent: tkinter.Widget=None, *, var: tkinter.StringVar=None):
        label = tkinter.Label(parent if parent else self.window, text=text, height=3, font=font, textvariable=var)
        self.Labels.append((label, pos))
        return label
    
    def BuildEntry(self, pos: PosType, parent: tkinter.Widget=None):
        entry = tkinter.Entry(parent if parent else self.window)
        self.Elements.append((entry, pos))
        return entry
    
    def BuildButton(self, text: str, command: typing.Callable[[], None], pos: PosType, parent: tkinter.Widget=None):
        button = tkinter.Button(parent if parent else self.window, text=text, command=command, bg='#dfdfdf')
        self.Elements.append((button, pos))
        return button
    
    def BuildFrame(self, text: str, pos: PosType, parent: tkinter.Widget=None):
        frame = tkinter.LabelFrame(parent if parent else self.window, text=text, relief=tkinter.GROOVE, bd=2)
        self.Elements.append((frame, pos))
        return frame
    
    def BuildRadioButton(self, text: str, variable: tkinter.StringVar, value: int, pos: PosType, parent: tkinter.Widget=None, *, command=None):
        radio = tkinter.Radiobutton(parent if parent else self.window, text=text, variable=variable, value=value, anchor='w', command=command)
        self.Elements.append((radio, pos))
        return radio

    def BuildProgressBar(self, pos: PosType, parent: tkinter.Widget=None):
        progress = tkinter.ttk.Progressbar(parent if parent else self.window, length=550)
        self.Elements.append((progress, pos))
        return progress

    def BuildComboBox(self, values: typing.List[str], pos: PosType, parent: tkinter.Widget=None):
        comboBox = tkinter.ttk.Combobox(parent if parent else self.window, values=values, state="readonly")
        comboBox.current(0)
        self.Elements.append((comboBox, pos))
        return comboBox

    def BuildElements(self):
        copyright = self.BuildLabel('made by Runas, ', Font("Arial", 10), Pos(380, 430))
        copyright.bind('<Button-1>', lambda e: webbrowser.open_new('https://github.com/Runas8128/KimbapRoller'))
        copyright = self.BuildLabel('CC BY License', Font("Arial", 10), Pos(480, 430))
        copyright.bind('<Button-1>', lambda e: webbrowser.open_new('https://creativecommons.org/licenses/by/4.0/deed.ko'))

        self.BuildLabel("필터 김밥말이 프로그램", Font("Arial", 20), Pos(200, -10))
        fileNameEntry = self.BuildEntry(Pos(60, 90, 400, 30))

        def onClickBrowseButton():
            adofaiFileName = tkinter.filedialog.askopenfilename(
                initialdir="/",
                title="Select file",
                filetypes=(
                    ("adofai files", "*.adofai"),
                )
            )

            fileNameEntry.delete(0, "end")
            fileNameEntry.insert(0, adofaiFileName)
            self.adofaiFileName = adofaiFileName

        self.BuildButton("Browse...", onClickBrowseButton, Pos(490, 90, 100, 30))

        self.BuildLabel("대상 타일", Font('Arial', 12), Pos(45, 130, 100, 50))
        targetFloor = self.BuildEntry(Pos(150, 145, 100, 25))
        targetFloor.insert(tkinter.END, "0")

        self.BuildLabel("필터 종류 선택", Font('Arial', 12), Pos(60, 170, 100, 50))
        filterComboBox = self.BuildComboBox(list(adofaiParser.Filters.keys()), Pos(65, 215, 175, 30))

        self.BuildLabel("각도 오프셋 설정 (소수점 사용 가능)", Font('Arial', 12), Pos(300, 130, 0, 50))
        self.BuildLabel("시작 각도", Font('Arial', 10), Pos(305, 180, 0, 20))
        startAngleOffset = self.BuildEntry(Pos(380, 180, 100, 25))
        startAngleOffset.insert(tkinter.END, "0")
        self.BuildLabel("끝 각도", Font('Arial', 10), Pos(305, 220, 0, 20))
        endAngleOffset = self.BuildEntry(Pos(380, 220, 100, 25))
        endAngleOffset.insert(tkinter.END, "180")

        self.BuildLabel("필터 강도 설정", Font('Arial', 12), Pos(60, 245, 100, 50))
        self.BuildLabel("시작 강도", Font('Arial', 10), Pos(65, 295, 0, 20))
        startIntensity = self.BuildEntry(Pos(140, 295, 100, 25))
        startIntensity.insert(tkinter.END, "0")
        self.BuildLabel("끝 강도", Font('Arial', 10), Pos(65, 335, 0, 20))
        endIntensity = self.BuildEntry(Pos(140, 335, 100, 25))
        endIntensity.insert(tkinter.END, "100")
        
        self.BuildLabel("이펙 갯수", Font('Arial', 12), Pos(280, 245, 100, 50))
        self.BuildLabel("많을수록 부드럽지만 렉이 심해집니다", Font('Arial', 10), Pos(300, 290, 0, 20))
        density = self.BuildEntry(Pos(305, 320, 150, 25))
        density.insert(tkinter.END, "180")

        self.BuildLabel("", Font('Arial', 10), Pos(50, 410), var=self.Log)
        progress = self.BuildProgressBar(Pos(50, 390, 400))

        def Run():
            fileName = fileNameEntry.get()

            if not fileName or not os.path.isfile(fileName):
                tkinter.messagebox.showerror("error", "파일을 선택해주세요!")
                return
            
            def logger(log: str):
                self.Log.set(log)
                progress.step(100 / 3)
            
            try:
                adofaiParser.run(fileName, int(targetFloor.get()), filterComboBox.get(),
                    float(startAngleOffset.get()), float(endAngleOffset.get()),
                    int(startIntensity.get()), int(endIntensity.get()),
                    int(density.get()),
                    logger)
                tkinter.messagebox.showinfo("done", "성공했습니다!")
            except adofaiParser.ParseException as Error:
                tkinter.messagebox.showerror("error", str(Error))
            except ValueError as Error:
                tkinter.messagebox.showerror("error", "정수 또는 실수를 적절히 입력해주세요!")
            except Exception as Error:
                tkinter.messagebox.showerror("fatal", f"예상치못한 오류가 발생했습니다.\n{Error}")
            finally:
                progress.stop()
                self.Log.set('')

        self.BuildButton("실행!", Run, Pos(485, 350, 100, 70))
        self.window.bind('<Return>', lambda event: Run())
    
    def PlaceElements(self):
        for Label in self.Labels:
            Label[0].place(**Label[1])

        for Element in self.Elements:
            Element[0].place(**Element[1])

    def start(self):
        self.window.mainloop()
