import mysql.connector
import config

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
            print("1. List countries")
            print("2. Add country")
            print("3. Find countries based on gdp and inflation")
            print("4. Update country's gdp and inflation")
            print("5. Exit")
            command = input("Enter your choice (1-5): ")
            print("")
            if command == 1:
                listCountries()
            elif command == 2:
                addCountry()
            elif command == 3:
                findCountries()
            elif command == 4:
                updateCountry()
            elif command == 5:
                exitProgram = True
                con.close()
            else:
                print("Not a valid selection, please pick from the choices above.")
    except mysql.connector.Error as err:
        print(err)

if __name__ == '__main__':
    main()