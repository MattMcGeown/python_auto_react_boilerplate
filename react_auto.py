import os
import requests

packageLoc = ''
packageName = ''
components = []

class colors:
  INPUT = '\033[92m'
  WHITE = '\033[37m'  
  INFO = '\033[96m'  

def getData():
  global packageLoc
  global packageName
  global components

  # Get user input for package setup location
  packageLoc = input(f"\n{colors.INPUT}Enter Setup Root Location: {colors.WHITE}")
  # Get user input for package name
  packageName = input(f"{colors.INPUT}Enter Package Name: {colors.WHITE}")
  # Get user input for package component(s)
  componentsInput = input(f"{colors.INPUT}Enter Component(s) ( Separate with spaces ):\n {colors.WHITE}")
  # Split componentsInput and add to components array
  components = componentsInput.split()

  os.chdir(packageLoc)

  print(f"\n{colors.INFO}Navigating to {packageLoc}...\n")

  # Create React App
  os.system('npx create-react-app '+packageName)

  print('\nClearing public and src directories...\n')

  srcDir = packageLoc+'\\'+packageName+'\src'
  pubDir = packageLoc+'\\'+packageName+'\public'
  # Delete all files in public and src directories
  for file in os.scandir(srcDir):
      os.remove(file.path)
  for file in os.scandir(pubDir):
      os.remove(file.path)

  print("\nBoilerplate removed")
  
  # Get default files from GitHub
  html = requests.get("https://raw.githubusercontent.com/SiiR-GH/python_auto_react_boilerplate/main/index.html")
  css = requests.get("https://raw.githubusercontent.com/SiiR-GH/python_auto_react_boilerplate/main/index.css")
  js = requests.get("https://raw.githubusercontent.com/SiiR-GH/python_auto_react_boilerplate/main/index.js")
  
  os.chdir(pubDir)
  # Populate index.html with text from GitHub file
  with open('index.html', 'w') as f:
    f.write(html.text)

  os.chdir(srcDir)
  # Populate index.css and index.js with text from GitHub file
  with open('index.css', 'w') as f:
    f.write(css.text)
  with open('index.js', 'w') as f:
    f.write(js.text)

  # If components are passed on init, create folder, sub folders, css and js files with functional components
  # Once complete, generate App.js complete with imports and functional component returning all passed components
  if components:
    createComponents(srcDir)

  os.chdir(packageLoc+"\\"+packageName)
  # Launch VSCode
  os.system("code .")
  # Start React App
  os.system("npm start")

# This is a mess and needs a fix
def createComponents(src):
  os.mkdir('components')
  for i in components:
    compJS = ("const "+i.capitalize()+" = () => {"
    "\n\treturn ("
    "\n\t\t<div>"+i.capitalize()+"</div>"
    "\n\t);"
    "\n};"
    "\n\nexport default "+i.capitalize()+";")

    appJS = ("import "+i.capitalize()+" from \"./components/"+i+"/"+i.capitalize()+"\";\n")

    os.chdir(src+'\components')
    os.mkdir(i)

    os.chdir(src+'\components'+'\\'+i)
    with open(i.capitalize()+'.jsx', 'w') as f:
      f.write(compJS)
    with open(i+'.css', 'w') as f:
      f.write('')

    os.chdir(src)
    with open('App.js', 'a') as f:
      f.write(appJS)

  appInsert = ("\nconst App = () => {"
    "\n\treturn ("
    "\n\t\t<>"
    "\n\t\t</>"
    "\n\t);"
    "\n};"
    "\n\nexport default App;")
  with open("App.js", 'a') as f:
    f.write("\nconst App = () => {"
    "\n\treturn ("
    "\n\t\t<>\n")

  for i in components:
    with open("App.js", "a") as f:
      f.write("\t\t\t<"+i.capitalize()+" />\n")

  with open("App.js", "a") as f:
    f.write("\t\t</>"
    "\n\t);"
    "\n};"
    "\n\nexport default App;")

while packageLoc == '':
  getData()