from modules.entities import Entities
from modules.gui import MainApplication

def main():
    main_entities = Entities()
    root = MainApplication(main_entities)
    root.mainloop()

main()