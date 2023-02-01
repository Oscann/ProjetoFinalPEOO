import tkinter as tk
from user_management import getData, saveData, User, ToDoItem
import datetime

LIST_BOX_WIDTH = 50
FORMATTED_VIEW_TEXT = "Prazo: %s\n%s"


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Login")
        self.resizable(False, False)

        self.user_data = getData()

        self.protocol("WM_DELETE_WINDOW", self.handleClose)

        Login(self)

        self.mainloop()

    def handleClose(self):
        saveData(self.user_data)
        self.destroy()


class WindowContent(tk.Frame):
    def __init__(self, master: App):
        tk.Frame.__init__(self, master)
        self.loadContent()
        self.grid()

    def loadContent(self):
        pass

    def redirect(self, Content):
        self.destroy()
        Content(self.master)


class Main(WindowContent):
    def loadContent(self):
        self.toDoList = self.master.user.getToDoList()

        mainFrame = tk.Frame(self)
        mainFrame.grid(row=0, column=0)

        self.listBox = tk.Listbox(
            mainFrame, width=LIST_BOX_WIDTH, height=10, font=("Arial", "10"))
        self.listBox.bind("<<ListboxSelect>>", self.onSelect)
        self.listBox.grid(row=0, column=0)

        self.fillListBox()

        viewFrame = tk.Frame(mainFrame)
        viewFrame.grid(row=0, column=1)

        self.todoText = tk.Label(
            viewFrame, width=LIST_BOX_WIDTH, wraplength=200)
        self.todoText.grid()

        inputsFrame = tk.Frame(self)
        inputsFrame.grid(row=1, column=0, padx=10, pady=10)

        tk.Label(inputsFrame, text="Tarefa").grid(
            column=0, row=0, pady=(0, 10))
        self.addToDoText = tk.Entry(inputsFrame)
        self.addToDoText.grid(column=0, row=1, padx=10)

        tk.Label(inputsFrame, text="Dia").grid(
            column=1, row=0, pady=(0, 10))
        self.day = tk.Entry(inputsFrame, width=8)
        self.day.grid(column=1, row=1, padx=10)

        tk.Label(inputsFrame, text="Mês").grid(
            column=2, row=0, pady=(0, 10))
        self.month = tk.Entry(inputsFrame, width=8)
        self.month.grid(column=2, row=1, padx=10)

        tk.Label(inputsFrame, text="Ano").grid(
            column=3, row=0, pady=(0, 10))
        self.year = tk.Entry(inputsFrame, width=8)
        self.year.grid(column=3, row=1, padx=10)

        actionsFrame = tk.Frame(self)
        actionsFrame.grid(row=2, column=0, padx=20, pady=10)
        self.addToDoButton = tk.Button(
            actionsFrame,
            text="Adicionar Tarefa",
            command=self.addToDo
        )
        self.addToDoButton.grid(column=0, row=0, padx=10, pady=10)

        self.editToDoButton = tk.Button(
            actionsFrame, text="Editar Tarefa", command=self.createEditScreen)
        self.editToDoButton.grid(row=0, column=1, padx=10)

        self.doneButton = tk.Button(
            actionsFrame, text="Marcar como concluído", command=self.deleteToDo)
        self.doneButton.grid(row=1, column=0, padx=10, pady=10)

        self.exitButton = tk.Button(
            actionsFrame, text="Sair", command=self.exit)
        self.exitButton.grid(row=1, column=1, padx=10)

        self.message = tk.Label(self)
        self.message.grid(row=3, column=0)

    def updateToDoList(self):
        def sortDeadline(item):
            if (item.deadline == None):
                return item.text
            return str(item.deadline)

        self.toDoList.sort(key=sortDeadline)
        self.listBox.delete(0, self.listBox.size() - 1)
        self.fillListBox()

    def fillListBox(self):
        print(self.toDoList)
        for i in range(len(self.toDoList)):
            if self.toDoList[i].deadline != None:
                text = self.toDoList[i].text + \
                                      " - " + self.toDoList[i].deadline.__str__()
            else:
                text = self.toDoList[i].text
            self.listBox.insert(i, text)

    def addToDo(self):
        addToDoText = self.addToDoText.get()
        try:
            day = self.day.get().strip()
            month = self.month.get().strip()
            year = self.year.get().strip()

            if day == "" or month == "" or year == "":
                deadline = None
            else:
                deadline = datetime.datetime(
                    year=int(year), month=int(month), day=int(day))
        except:
            self.message["text"] = "Algum dos valores é inválido, passe apenas n"

        self.toDoList.append(ToDoItem(addToDoText, deadline=deadline))
        self.updateToDoList()

    def deleteToDo(self):
        todo = self.listBox.curselection()[0]
        self.toDoList.pop(todo)
        self.updateToDoList()

    def editToDo(self, index: int):
        editToDoText = self.editTaskText.get()
        try:
            day = self.editDayEntry.get().strip()
            month = self.editMonthEntry.get().strip()
            year = self.editYearEntry.get().strip()

            if day == "" or month == "" or year == "":
                deadline = None
            else:
                deadline = datetime.datetime(
                    year=int(year), month=int(month), day=int(day))
        except:
            self.editMessage["text"] = "Algum dos valores é inválido, passe apenas n"

        self.toDoList[index].text = editToDoText
        self.toDoList[index].deadline = deadline
        self.updateToDoList()

    def exit(self):
        self.redirect(Login)

    def onSelect(self, e):
        print(e)
        if len(self.listBox.curselection()) == 0:
            return
        todo = self.listBox.curselection()[0]
        text, deadline = self.toDoList[todo].text, self.toDoList[todo].deadline

        self.todoText["text"] = FORMATTED_VIEW_TEXT % (deadline, text)

    def createEditScreen(self):
        if len(self.listBox.curselection()) == 0:
            return

        todoIndex = self.listBox.curselection()[0]
        todo = self.toDoList[todoIndex]

        editScreen = tk.Toplevel(self.master)

        inputsFrame = tk.Frame(editScreen)
        inputsFrame.grid(row=0, column=0)

        tk.Label(inputsFrame, text="Tarefa").grid(
            column=0, row=0, pady=(0, 10))
        self.editTaskText = tk.Entry(inputsFrame)
        self.editTaskText.insert(0, todo.text)
        self.editTaskText.grid(column=0, row=1, padx=10)

        if todo.deadline != None:
            day = todo.deadline.day
            month = todo.deadline.month
            year = todo.deadline.year

        else:
            day, month, year = "", "", ""

        tk.Label(inputsFrame, text="Dia").grid(
            column=0, row=2, pady=(0, 10))
        self.editDayEntry = tk.Entry(inputsFrame, width=8)
        self.editDayEntry.insert(0, day)
        self.editDayEntry.grid(column=0, row=3, padx=10)

        tk.Label(inputsFrame, text="Mês").grid(
            column=1, row=2, pady=(0, 10))
        self.editMonthEntry = tk.Entry(inputsFrame, width=8)
        self.editMonthEntry.insert(0, month)
        self.editMonthEntry.grid(column=1, row=3, padx=10)

        tk.Label(inputsFrame, text="Ano").grid(
            column=2, row=2, pady=(0, 10))
        self.editYearEntry = tk.Entry(inputsFrame, width=8)
        self.editYearEntry.insert(0, year)
        self.editYearEntry.grid(column=2, row=3, padx=10)

        def edit():
            self.editToDo(todoIndex)
            editScreen.destroy()

        tk.Button(editScreen, text="Editar", command=edit).grid(
            row=1, column=0, padx=10, pady=10)

        self.editMessage = tk.Label(editScreen)
        self.editMessage.grid(row=2, column=0)

        editScreen.grid()


class Login(WindowContent):
    def loadContent(self):
        tk.Label(self, text="LOGIN", font=("Arial", "16", "bold")).grid(
            row=0, column=0, pady=10)

        inputs = tk.Frame(self)
        inputs.grid(row=1, column=0, padx=10, pady=10)

        tk.Label(inputs, text="Usuário", anchor="w").grid(row=0, column=0)
        self.username = tk.Entry(inputs)
        self.username.grid(row=1, column=0, pady=(0, 10))
        tk.Label(inputs, text="Senha", anchor="w").grid(row=2, column=0)
        self.password = tk.Entry(inputs, show="*")
        self.password.grid(row=3, column=0)

        buttons = tk.Frame(self)
        buttons.grid(row=2, column=0)
        self.loginButton = tk.Button(buttons, text="Login", command=self.login)
        self.loginButton.grid(row=0, column=0, pady=10, padx=[0, 5])

        self.signupButton = tk.Button(
            buttons, text="Cadastrar", command=self.signup)
        self.signupButton.grid(row=0, column=1, pady=10, padx=[5, 0])

        self.message = tk.Label(self, wraplength=100)
        self.message.grid(padx=10, pady=10)

    def login(self):
        username = self.username.get()
        password = self.password.get()

        data = self.master.user_data

        if username == "" or password == "":
            self.message["text"] = "Está faltando dados obrigatórios"
            return

        if username not in data.keys():
            self.message["text"] = "Usuário inexistente"
            return

        if data[username].getPassword() != password:
            self.message["text"] = "Senha incorreta"
            return

        self.master.user = data[username]
        self.redirect(Main)

    def signup(self):
        self.redirect(SignUp)


class SignUp(WindowContent):
    def loadContent(self):
        tk.Label(self, text="CADASTRO", font=("Arial", "16", "bold")).grid(
            row=0, column=0, pady=10)

        inputs = tk.Frame(self)
        inputs.grid(row=1, column=0, padx=10, pady=10)

        tk.Label(inputs, text="Usuário", anchor="w").grid(row=0, column=0)
        self.username = tk.Entry(inputs)
        self.username.grid(row=1, column=0, pady=(0, 10))
        tk.Label(inputs, text="Senha", anchor="w").grid(row=2, column=0)
        self.password = tk.Entry(inputs, show="*")
        self.password.grid(row=3, column=0)

        buttons = tk.Frame(self)
        buttons.grid(row=2, column=0)
        self.signupButton = tk.Button(
            buttons, text="Cadastrar", command=self.signup)
        self.signupButton.grid(row=0, column=0, pady=[0, 5])

        self.exitButton = tk.Button(
            buttons, text="Sair", command=self.exit)
        self.exitButton.grid(row=1, column=0, pady=[5, 0])

        self.message = tk.Label(self, wraplength=100)
        self.message.grid(padx=10, pady=10)

    def exit(self):
        self.redirect(Login)

    def signup(self):
        username = self.username.get()
        password = self.password.get()

        data = self.master.user_data

        if username == "" or password == "":
            self.message["text"] = "Está faltando dados obrigatórios"
            return

        if username in data.keys():
            self.message["text"] = "Usuário já existe"
            return

        if len(password) < 8:
            self.message["text"] = "Senha precisa ter ao menos 8 caracteres"
            return

        data[username] = User(username, password)

        self.master.user = data[username]
        self.redirect(Main)
