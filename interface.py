import tkinter as tk
from user_management import getData, saveData, User, ToDoItem

LIST_BOX_WIDTH = 50


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
        self.listBox.grid(row=0, column=0)

        self.fillListBox()

        viewFrame = tk.Frame(mainFrame)
        viewFrame.grid(row=0, column=1)

        self.todoText = tk.Label(
            viewFrame, width=LIST_BOX_WIDTH, wraplength=LIST_BOX_WIDTH)
        self.todoText.grid()

        actionsFrame = tk.Frame(self)
        actionsFrame.grid(row=1, column=0, padx=20, pady=10)
        self.addToDoText = tk.Entry(actionsFrame)
        self.addToDoText.grid(column=0, row=0)
        self.addToDoButton = tk.Button(
            actionsFrame,
            text="Adicionar Tarefa",
            command=self.addToDo
        )
        self.addToDoButton.grid(column=1, row=0)

        self.deleteToDoButton = tk.Button(
            actionsFrame, text="Excluir Tarefa", command=self.deleteToDo)

    def updateToDoList(self):

        def sortDeadline(item):
            if (item.deadline == None):
                return item.text
            return item.deadline
        self.toDoList.sort(key=sortDeadline)
        self.listBox.delete(0, self.listBox.size() - 1)
        self.fillListBox()

    def fillListBox(self):
        print(self.toDoList)
        for i in range(len(self.toDoList)):
            if self.toDoList[i].deadline != None:
                text = breakTextLines(self.toDoList[i].text +
                                      " - " + self.toDoList[i].deadline.__str__())
            else:
                text = breakTextLines(self.toDoList[i].text)
            self.listBox.insert(i, text)

    def addToDo(self):
        addToDoText = self.addToDoText.get()
        self.toDoList.append(ToDoItem(addToDoText))
        self.updateToDoList()

    def deleteToDo(self):
        todo = self.listBox.curselection()
        self.toDoList.pop(todo)
        self.updateToDoList()


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


def breakTextLines(text: str):
    splittedText = text.split()

    newText = []
    tempText = ""

    for substring in splittedText:
        if len(tempText + " " + substring) >= LIST_BOX_WIDTH:
            newText.append(tempText + "\n")
            tempText = substring
        else:
            tempText += " " + substring
    newText.append(tempText)

    return "".join(newText)
