from getHTML import getHTML

ord = "korpulent"
webpage = f"https://naob.no/ordbok/{ord}"
html = getHTML(webpage)

with open(f"./testdata/{ord}.html", "w") as file:
    file.write(str(html))