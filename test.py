class File:
    def __init__(self, file_name, parent_path=""):
        self.file_name = file_name
        # setting path
        self.path = f"{parent_path}/{self.file_name}" if parent_path else self.file_name
        self.content_list = []

    def show_content(self):
        #shows the files contents
        if self.content_list:
            print("\n".join(self.content_list))
        else:
            print("No content in file")

    def append_content(self, content_list_to_add):
        # add lines to content
        for line in content_list_to_add:
            self.content_list.append(line)

    def edit_line(self, number, content):

        if 1 <= number <= len(self.content_list):
            self.content_list[number - 1] = content
            print('editing done')
        else:
            print("invalid command for line edit")

    def delete_line(self, number):
        if 1 <= number <= len(self.content_list):
            del self.content_list[number - 1]
            print('deleting done')
        else:
            print("Invalid command for deleting line")

    def set_content(self, content_list_to_add):
        # replace content
        self.content_list = content_list_to_add

    def copy(self):
        # create a  copy of the file
        new_file = File(self.file_name, "")
        new_file.content_list = self.content_list.copy()
        return new_file

class Folder:
    def __init__(self, folder_name, parent_path=""):
        self.folder_name = folder_name
        self.path = f"{parent_path}/{folder_name}" if parent_path else folder_name
        self.files_dict = {}
        self.folders_dict = {}

    def add_file(self, file):
        if file.file_name not in self.files_dict:
            self.files_dict[file.file_name] = file
            file.path = f"{self.path}/{file.file_name}"
        else:
            print(f"File {file.file_name} already exists in {self.path}")

    def add_folder(self, folder):

        if folder.folder_name not in self.folders_dict:
            self.folders_dict[folder.folder_name] = folder
            folder.path = f"{self.path}/{folder.folder_name}"
        else:
            print(f"Folder {folder.folder_name} already exists in {self.path}")

    def show_content(self):

        if not self.files_dict and not  self.folders_dict:
            print(f"No content in folder {self.path}")
            return
        if self.folders_dict:
          for folder_name in self.folders_dict:
              print(f"{folder_name} folder")
        if self.files_dict:
          for file_name in self.files_dict:
              print(file_name)

    def show_file_content(self, file_name):

        file_name = file_name
        if file_name in self.files_dict:
            self.files_dict[file_name].show_content()
        else:
            print(f"File {file_name} not found in {self.path}")

    def delete_file(self, file_name):

        file_name = file_name
        if file_name in self.files_dict:
            del self.files_dict[file_name]
            print(f"File {file_name} deleted from {self.path}")
        else:
            print(f"File {file_name} not found in {self.path}")

    def delete_folder(self, folder_name):
        #delets subfolder
        if folder_name in self.folders_dict:
            del self.folders_dict[folder_name]
            print(f"Folder {folder_name} deleted from {self.path}")
        else:
            print(f"Folder {folder_name} not found in {self.path}")

    def get_file(self, file_name):
        # get file by name
        file_name = file_name
        return self.files_dict.get(file_name)

    def get_folder(self, folder_name):
        # get subfolder by name
        return self.folders_dict.get(folder_name)

    def copy(self):
        # create a deep of the folder
        new_folder = Folder(self.folder_name, "")
        for file_name, file in self.files_dict.items():
            new_folder.add_file(file.copy())
        for folder_name, folder in self.folders_dict.items():
            new_folder.add_folder(folder.copy())
        return new_folder

class FileSystem:
    def __init__(self):
        # initialize with root folder
        self.root = Folder("root")
        self.current_folder = self.root
        self.previous_folders = []  # Stack for cd ..

        self.map_dict = {self.root.path: {"subfolders": {}, "files": {}}}#values of files are contents_list

    def _navigate_to_folder(self, path):
        # navigate to folder by absolute or relative path
        components = path.split('/')
        current = self.root if path.startswith('root') else self.current_folder
        for i, component in enumerate(components):
            if component == 'root':
                continue
            next_folder = current.get_folder(component)
            if not next_folder:
                print(f"Path not found: {'/'.join(components[:i+1])}")
                return None
            self.previous_folders.append(current)
            current = next_folder
        return current

    def _get_folder_map(self, folder_path):
        # get or initialize map dictionary entry for a folder
        if folder_path not in self.map_dict:
            self.map_dict[folder_path] = {"subfolders": {}, "files": {}}
        return self.map_dict[folder_path]

    def mkdir(self, path):
        # Create folder at path
        components = path.split('/')
        if not components:
            print("no path was entered!")
            return
        parent_folder = self._navigate_to_folder('/'.join(components[:-1])) if len(components) > 1 else self.current_folder
        if not parent_folder:
            return
        folder_name = components[-1]
        if parent_folder.get_folder(folder_name):
            print(f"Folder {path} already exists")
            return
        folder = Folder(folder_name, parent_folder.path)
        parent_folder.add_folder(folder)
        # Update map dictionary
        parent_map = self._get_folder_map(parent_folder.path)
        parent_map["subfolders"][folder_name] = {"subfolders": {}, "files": {}}
        self.map_dict[folder.path] = {"subfolders": {}, "files": {}}
        print(f"Folder {folder_name} created")

    def touch(self, path):
        # create file at path
        components = path.split('/')
        if not components:
            print("no file path was entered!")
            return
        parent_folder = self._navigate_to_folder('/'.join(components[:-1])) if len(components) > 1 else self.current_folder
        if not parent_folder:
            return
        file_name = components[-1]
        if parent_folder.get_file(file_name):
            print(f"File {path} already exists")
            return
        file = File(file_name, parent_folder.path)
        parent_folder.add_file(file)
        # update map dictionary
        parent_map = self._get_folder_map(parent_folder.path)
        parent_map["files"][file.file_name] = file.content_list
        print(f"File '{file_name}' created in {parent_folder.path}")

    def rm(self, path):
        # remove file or folder at path
        components = path.split('/')
        if not components:
            print("you didnt give me the file or fplder path")
            return
        parent_folder = self._navigate_to_folder('/'.join(components[:-1])) if len(components) > 1 else self.current_folder
        if not parent_folder:
            return
        name = components[-1]#we still dont know if its a folder or a file

        if  name in parent_folder.files_dict:
            file_name=name
            parent_folder.delete_file(file_name)
            # Update map dictionary
            parent_map = self._get_folder_map(parent_folder.path)
            del parent_map["files"][file_name]
        elif name in parent_folder.folders_dict:
            parent_folder.delete_folder(name)
            # Update map dictionary
            parent_map = self._get_folder_map(parent_folder.path)
            del parent_map["subfolders"][name]
            del self.map_dict[f"{parent_folder.path}/{name}"]
        else:
            print(f"{name} not found in {parent_folder.path}")

    def cd(self, path):
        # change directory
        if path == '..':
            if self.previous_folders:
                self.current_folder = self.previous_folders.pop()
                print(f"Changed to {self.current_folder.path}")
            else:
                print("No parent folder you are at root !")
            return
        folder = self._navigate_to_folder(path)
        if folder:
            self.current_folder = folder
            print(f"Changed to {folder.path}")
        else:
            print(f"Folder {path} not found")

    def ls(self):
        #  contents of current folder
        self.current_folder.show_content()

    def nwfiletxt(self, path):
        # set file content
        components = path.split('/')
        if not components:
            print("no file psth eas given for adding text")
            return
        parent_folder = self._navigate_to_folder('/'.join(components[:-1])) if len(components) > 1 else self.current_folder
        if not parent_folder:
            return
        file_name = components[-1]
        file = parent_folder.get_file(file_name)
        if not file:
            print(f"File {file_name} not found in {parent_folder.path}")
            return
        print("Enter the lines (end means done)")
        content = []
        while True:
            line = input()
            if line == "end":
                break
            content.append(line)
        file.set_content(content)
        # Update map dictionary
        parent_map = self._get_folder_map(parent_folder.path)
        parent_map["files"][file.file_name] = file.content_list
        print(f"Content updated for {file.path}")

    def appendtxt(self, path):
        # append content to file
        components = path.split('/')
        if not components:
            print("no file path was given for appending file ")
            return
        parent_folder = self._navigate_to_folder('/'.join(components[:-1])) if len(components) > 1 else self.current_folder
        if not parent_folder:
            return
        file_name = components[-1]
        file = parent_folder.get_file(file_name)
        if not file:
            print(f"File {file_name} not found in {parent_folder.path}")
            return
        print("Enter the lines (end means done)")
        content = []
        while True:
            line = input()
            if line == "end":
                break
            content.append(line)
        file.append_content(content)
        # Update map dictionary
        parent_map = self._get_folder_map(parent_folder.path)
        parent_map["files"][file.file_name] = file.content_list
        print(f"Content appended to {file.path}")

    def editline(self, path, line_number, text):
        # edit specific line
        components = path.split('/')
        if not components:
            print("no given file path for line editing")
            return
        parent_folder = self._navigate_to_folder('/'.join(components[:-1])) if len(components) > 1 else self.current_folder
        if not parent_folder:
            return
        file_name = components[-1]
        file = parent_folder.get_file(file_name)
        if file:
            file.edit_line(line_number, text)
            # update map dictionary
            parent_map = self._get_folder_map(parent_folder.path)
            parent_map["files"][file.file_name] = file.content_list
        else:
            print(f"File {file_name} not found in {parent_folder.path}")

    def deline(self, path, line_number):
        # delete specific line
        components = path.split('/')
        if not components:
            print("no given path for deleting file !")
            return
        parent_folder = self._navigate_to_folder('/'.join(components[:-1])) if len(components) > 1 else self.current_folder
        if not parent_folder:
            return
        file_name = components[-1]
        file = parent_folder.get_file(file_name)
        if file:
            file.delete_line(line_number)
            # Update map dictionary
            parent_map = self._get_folder_map(parent_folder.path)
            parent_map["files"][file.file_name] = file.content_list
        else:
            print(f"File {file_name} not found in {parent_folder.path}")

    def cat(self, path):
        # show file content
        components = path.strip('/').split('/')
        if not components:
            print("no file path for showing content ")
            return
        parent_folder = self._navigate_to_folder('/'.join(components[:-1])) if len(components) > 1 else self.current_folder
        if not parent_folder:
            return
        file_name = components[-1]
        parent_folder.show_file_content(file_name)

    def mv(self, source_path, dest_path):
        # move file or folder
        source_components = source_path.split('/')
        dest_components = dest_path.split('/')
        if not source_components or not dest_components:
            print("pathes are not given ")
            return
        source_parent = self._navigate_to_folder('/'.join(source_components[:-1])) if len(
            source_components) > 1 else self.current_folder
        dest_parent = self._navigate_to_folder('/'.join(dest_components[:-1])) if len(
            dest_components) > 1 else self.current_folder
        if not (source_parent and dest_parent):
            return
        source_name = source_components[-1]
        dest_name = dest_components[-1]

        # move file
        if source_name in source_parent.files_dict:
            file = source_parent.get_file(source_name)  # Use get_file
            if dest_parent.get_file(dest_name):
                print(f"File {dest_name} already exists in {dest_parent.path}")
                return
            source_parent.delete_file(source_name)
            file.file_name = dest_name  # Set new file name
            file.path = f"{dest_parent.path}/{file.file_name}"
            dest_parent.add_file(file)
            # Update map dictionary
            source_map = self._get_folder_map(source_parent.path)
            dest_map = self._get_folder_map(dest_parent.path)
            del source_map["files"][source_name]
            dest_map["files"][file.file_name] = file.content_list
            print(f"Moved {source_path} to {dest_path}")
        # move folder
        elif source_name in source_parent.folders_dict:
            folder = source_parent.folders_dict[source_name]
            if dest_parent.get_folder(dest_name):
                print(f"Folder {dest_name} already exists in {dest_parent.path}")
                return
            source_parent.delete_folder(source_name)
            folder.folder_name = dest_name  # set new folder name
            folder.path = f"{dest_parent.path}/{folder.folder_name}"
            dest_parent.add_folder(folder)
            # Update map dictionary
            source_map = self._get_folder_map(source_parent.path)
            dest_map = self._get_folder_map(dest_parent.path)
            del source_map["subfolders"][source_name]
            dest_map["subfolders"][folder.folder_name] = self.map_dict.pop(f"{source_parent.path}/{source_name}")
            self.map_dict[f"{dest_parent.path}/{folder.folder_name}"] = dest_map["subfolders"][folder.folder_name]
            print(f"Moved {source_path} to {dest_path}")
        else:
            print(f"{source_name} not found in {source_parent.path}")

    def cp(self, source_path, dest_path):
        # copy file or folder
        source_components = source_path.strip('/').split('/')
        dest_components = dest_path.strip('/').split('/')
        if not (source_components and dest_components):
            print("Invalid path")
            return
        source_parent = self._navigate_to_folder('/'.join(source_components[:-1])) if len(source_components) > 1 else self.current_folder
        dest_parent = self._navigate_to_folder('/'.join(dest_components[:-1])) if len(dest_components) > 1 else self.current_folder
        if not (source_parent and dest_parent):
            return
        source_name = source_components[-1]
        dest_name = dest_components[-1]
        source_file_name = source_name if source_name.endswith('.txt') else source_name + '.txt'
        # copy file
        if source_file_name in source_parent.files_dict:
            file = source_parent.files_dict[source_file_name].copy()
            if dest_parent.get_file(dest_name):
                print(f"File {dest_name} already exists in {dest_parent.path}")
                return
            file.file_name = dest_name if dest_name.endswith('.txt') else dest_name + '.txt'
            file.path = f"{dest_parent.path}/{file.file_name}"
            dest_parent.add_file(file)
            # Update map dictionary
            dest_map = self._get_folder_map(dest_parent.path)
            dest_map["files"][file.file_name] = file.content_list
            print(f"Copied {source_path} to {dest_path}")
        # copy folder
        elif source_name in source_parent.folders_dict:
            folder = source_parent.folders_dict[source_name].copy()
            if dest_parent.get_folder(dest_name):
                print(f"Folder {dest_name} already exists in {dest_parent.path}")
                return
            folder.folder_name = dest_name
            folder.path = f"{dest_parent.path}/{dest_name}"
            dest_parent.add_folder(folder)
            # Update map dictionary
            dest_map = self._get_folder_map(dest_parent.path)
            dest_map["subfolders"][dest_name] = {"subfolders": {}, "files": {}}
            self.map_dict[folder.path] = dest_map["subfolders"][dest_name]
            # Copy map dictionary entries
            source_map = self._get_folder_map(f"{source_parent.path}/{source_name}")
            dest_map["subfolders"][dest_name]["subfolders"] = source_map["subfolders"].copy()
            dest_map["subfolders"][dest_name]["files"] = source_map["files"].copy()
            print(f"Copied {source_path} to {dest_path}")
        else:
            print(f"{source_name} not found in {source_parent.path}")

    def rename(self, path, new_name):
        # rename file or folder
        components = path.split('/')
        if not components:
            print("Invalid path") #chnage it
            return
        parent_folder = self._navigate_to_folder('/'.join(components[:-1])) if len(components) > 1 else self.current_folder
        if not parent_folder:
            return
        name = components[-1]
        file_name = name
        new_file_name = new_name
        # rename file
        if file_name in parent_folder.files_dict:
            file = parent_folder.files_dict.pop(file_name)
            file.file_name = new_file_name
            file.path = f"{parent_folder.path}/{new_file_name}"
            parent_folder.files_dict[new_file_name] = file
            # update map dictionary
            parent_map = self._get_folder_map(parent_folder.path)
            content = parent_map["files"].pop(file_name)
            parent_map["files"][new_file_name] = content
            print(f"Renamed {path} to {new_name}")
        # rename folder
        elif name in parent_folder.folders_dict:
            folder = parent_folder.folders_dict.pop(name)
            old_path = folder.path
            folder.folder_name = new_name
            folder.path = f"{parent_folder.path}/{new_name}"
            parent_folder.folders_dict[new_name] = folder
            # Update map dictionary
            parent_map = self._get_folder_map(parent_folder.path)
            content = parent_map["subfolders"].pop(name)
            parent_map["subfolders"][new_name] = content
            self.map_dict[f"{parent_folder.path}/{new_name}"] = self.map_dict.pop(old_path)
            print(f"Renamed {path} to {new_name}")
        else:
            print(f"{name} not found in {parent_folder.path}")
def run_filesystem():

    fs = FileSystem()
    print("""
Unix Filesystem Simulator
------------------------
Enter commands to manage files and folders.
Available Commands:
  mkdir <path> - Create a folder
  touch <path> - Create a .txt file
  rm <path> - Remove a file or folder
  cd <path> - Change directory
  ls - List files and folders
  nwfiletxt <path> - Set file content, end with 'end'
  appendtxt <path> - Append to file, end with 'end'
  editline <path> <line> <text> - Edit line in file
  deline <path> <line> - Delete line from file
  cat <path> - Display file content
  mv <source_path> <dest_path> - Move file/folder
  cp <source_path> <dest_path> - Copy file/folder
  rename <path> <new_name> - Rename file/folder
  exit - Exit the simulator
  you should enter path using / like this root/docs/new_folder
------------------------
    """)

    while True:

            user_input = input("$ ").strip()
            if not user_input:
                print(' enter a input ')
                continue
            if user_input.lower() == "exit":
                print("Exiting bye !")
                break


            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:]

            # handle commands
            if command == "mkdir":
                if not len(args)==1 :
                    print("enter the path of directory  !")
                else:
                    path = parts[1]

                    if path.startswith("root") and path[4:] == "":
                        print("Folder root already exists")
                    else:
                        fs.mkdir(path)

            elif command == "touch":
                if not len(args)==1:
                    print("enter the path of directory  ! ")
                else:
                    path = parts[1]
                    if path.startswith("root") and path[4:] == "":
                        print("root can not be a file_name")
                    else:
                        fs.touch(path)

            elif command == "rm":
                if not len(args)==1:
                    print("enter the path where you wanna remove the folder!")
                else:
                    path=parts[1]
                    if  path.startswith("root") and path[4:] == "":
                        print("Cannot remove root folder")
                    else:
                        fs.rm(path)

            elif command == "cd":
                if not len(args)==1:
                    print("you didnt enter the directory you are willing to go !")
                else:
                    path=parts[1]
                    fs.cd(path)

            elif command == "ls":
                if len(args) != 0:
                    print("just give me ls ")
                else:
                    fs.ls()

            elif command == "nwfiletxt":
                if not len(args)==1:
                    print("you didnt give me the path of where you wanna set file content!")
                else:
                    path = parts[1]
                    if path.startswith("root") and path[4:] == "":
                        print("root is invalid ")
                    else:
                        fs.nwfiletxt(path)

            elif command == "appendtxt":
                if not len(args)==1:
                    print("you didnt give me the path of where you wanna append to file content!")
                else:
                    path=parts[1]
                    if path.startswith("root") and path[4:] == "":
                        print("root is invalid!!")
                    else:
                        fs.appendtxt(path)

            elif command == "editline":
                if not len(args)==3:
                    print("you should give me path and line number and text!")
                else:
                    path,line_number,text = parts[1],int(parts[2]),parts[3]
                    if path.startswith("root") and path[4:] == "":
                        print('root is invalid')
                    else:
                        fs.editline(path, line_number, text)

            elif command == "deline":
                if not len(args)==2:
                    print("you should give me path and line number")
                else:
                    path, line = parts[1],int(parts[2])
                    if path.startswith("root") and path[4:] == "":
                        print("Invalid file name: root")
                    else:
                        fs.deline(path, int(line))

            elif command == "cat":
                if not len(args)==1:
                    print("at least give me the path!")
                else:
                    path = parts[1]
                    if path.startswith("root") and path[4:] == "":
                        print("Invalid file name: root")
                    else:
                        fs.cat(path)

            elif command == "mv":
                if  not len(args)==2:
                    print("you didnt give me the source and destination path")
                else:
                    source_path = parts[1]
                    dest_path = parts[2]
                    if (source_path.startswith("root") and source_path[4:] == "") and (dest_path.startswith("root") and dest_path[4:] == ""):
                        print("Invalid path: root")
                    else:
                        fs.mv(source_path, dest_path)

            elif command == "cp":
                if  not len(args)==2:
                    print("you didnt give me the source and destination path")
                else:
                    source_path = parts[1]
                    dest_path = parts[2]
                    if (source_path.startswith("root") and source_path[4:] == "") and (dest_path.startswith("root") and dest_path[4:] == ""):
                        print("Invalid path: root")
                    else:
                        fs.cp(source_path, dest_path)

            elif command == "rename":
                if not len(args)==2:
                    print("you didnt give me the source and destination path")
                else:
                    path = parts[1]
                    new_name = parts[2]
                    if path.startswith("root") and path[4:] == "":
                        print("Invalid path: root")
                    else:
                        fs.rename(path, new_name)

            else:
                print(f"Unknown command: {command}. Did you mean 'ls' or another command?")



if __name__ == "__main__":
    run_filesystem()