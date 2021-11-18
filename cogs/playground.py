import pyfiglet

for i in pyfiglet.FigletFont.getFonts():
    print(pyfiglet.Figlet(font=i).renderText('Test'), f"\n {i}")
