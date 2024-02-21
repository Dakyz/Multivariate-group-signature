using PyCall
pushfirst!(pyimport("sys")."path", "")


window = pyimport("window")
app = window.Window()
app.mainloop()

