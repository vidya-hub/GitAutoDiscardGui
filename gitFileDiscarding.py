

import subprocess
import tkinter as tk
import customtkinter

# change the file extensions according to our needs

fileExtensionException = ["dart","png","svg","yaml"]



class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)



    def add_item(self, item):
        check_var = tk.IntVar(value=item["status"])
        checkbox = customtkinter.CTkCheckBox(self, text=item["fileName"],onvalue=1, offvalue=0,variable=check_var)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]



class App(customtkinter.CTk):
    gitFileList =[]
    def getFileItem(self,fileName):
        if fileName.split(".")[-1] in fileExtensionException:
            return {"fileName":fileName,"status":0}
        else:
            return {"fileName":fileName,"status":1}
    def getListOfFilesInStagingArea(self):
        subOutPut = subprocess.run(["git", "diff", "--name-only"], stdout=subprocess.PIPE)
        listOfUncommittedFiles = subOutPut.stdout.decode("utf-8").split("\n")
        unCommittedList = listOfUncommittedFiles[0:len(listOfUncommittedFiles)-1]
        [self.gitFileList.append(self.getFileItem(fileName)) for fileName in unCommittedList]
    def __init__(self):
        self.getListOfFilesInStagingArea()
        print(self.gitFileList)
        super().__init__()

        self.title("Git file remove exmample")
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.generateResultsButton = customtkinter.CTkButton(self,
                                         text="Submit",command=self.subMitCallBackEvent)
        self.generateResultsButton.grid(row=1, column=0, padx=15, pady=15, sticky="ns")

        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=200, command=self.checkbox_frame_event,
                                                                 item_list= self.gitFileList)
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

    def subMitCallBackEvent(self):
        selectedItems= self.scrollable_checkbox_frame.get_checked_items()
        gitCommands = ["git", "checkout", "--"]
        gitCommands.extend(selectedItems)
        print(gitCommands)
        subprocess.run(gitCommands)
        self.quit()


    def checkbox_frame_event(self):
        print("Clicking")
        

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()


