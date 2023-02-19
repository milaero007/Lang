import LLPlay
import LLStorage
import LLFiller
from tkinter import messagebox

#DB initialisation
sqlite = LLStorage.SQLite()
see_more = messagebox.askyesno(title='What to do',  message='Would you like to run test?', detail='Click NO to start filling')
if not see_more:
    LLFiller.run_filler(sqlite)
    exit(0)
else:
    LLPlay.run_play(sqlite)
    exit(0)
    
