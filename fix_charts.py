code = open('src/charts.py', 'r').read()
fixed = code.replace(
    "        legend = dict(orientation=\"h\", yanchor=\"bottom\", y=1.02,\n                      xanchor=\"right\", x=1, bgcolor=\"rgba(0,0,0,0)\"),\n",
    ""
)
open('src/charts.py', 'w').write(fixed)
print("Done! Legend line removed.")