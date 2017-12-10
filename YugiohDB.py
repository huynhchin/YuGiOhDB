import mysql.connector
import config

#the user creates his own deck
def createDeck():
    name = input("Enter name for deck: ")

#Main Menu
def main():
    try:
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        db = 'chuynh_DB'
        # create a connection
        con = mysql.connector.connect(user=usr, password=pwd, host=hst, database=db)
        exitProgram = False
        while exitProgram == False:
            print("")
            print("1. Look at existing")
            print("2. Add country")
            print("3. Find countries based on gdp and inflation")
            print("4. Update country's gdp and inflation")
            print("5. Exit")
            command = input("Enter your choice (1-5): ")
            print("")
            if command == 1:
            elif command == 2:
            elif command == 3:
            elif command == 4:
            elif command == 5:
                exitProgram = True
                con.close()
            else:
                print("Not a valid selection, please pick from the choices above.")
    except mysql.connector.Error as err:
        print(err)

if __name__ == '__main__':
    main()