import LLPlay
import LLStorage
import LLFiller

#DB initialisation
sqlite = LLStorage.SQLite()
LLPlay.run_play(sqlite)
#LLFiller.run_filler(sqlite)