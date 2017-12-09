#Chin Huynh

import mysql.connector
import config

#If a user selects 1 from the main menu, the program display the names and codes of
#all of the countries. Each country should be displayed on a single line as “name (code)”, e.g.,
#United States (US).
def listCountries():
    try:
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        db = 'chuynh_DB'
        # create a connection
        con = mysql.connector.connect(user=usr, password=pwd, host=hst, database=db)
        # create a result set
        rs = con.cursor()
        query = 'SELECT country_name, code FROM Country'
        # execute the query
        rs.execute(query)
        # print the results
        for (country_name, code) in rs:
            print('{} ({})'.format(country_name, code))
        rs.close()
        con.close()
    except mysql.connector.Error as err:
        print(err)

#If a user selects 2 from the main menu, the program should prompt for the country information
#to add to the database. Once given, the program (a) check to make sure the same country code does not
#already exist, and if not, (b) add the corresponding country to the databse, and otherwise,
#(c) notify the user that the country alread exists.
def addCountry():
    try:
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        db = 'chuynh_DB'
        # create a connection
        con = mysql.connector.connect(user=usr, password=pwd, host=hst, database=db)
        cCode = str(raw_input("Country code: "))
        cName = str(raw_input("Country name: "))
        gdp = input("Country per capita gdp (USD): ")
        inflt = input("Country inflation (pct): ")
        # create and execute query
        rs = con.cursor()
        query = 'SELECT code, country_name FROM Country'
        rs.execute(query)
        #flag is to check if the country already exists
        matchFlag = False
        for code, country_name in rs:
            if code == cCode:
                matchFlag = True
        rs.close()
        if matchFlag == True:
            print("")
            print("This country already exists in the database.")
        else:
            try:
                rs2 = con.cursor()
                query2 = 'INSERT INTO Country VALUES (%s, %s, %s, %s)'
                rs2.execute(query2, (cCode, cName, gdp, inflt))
                print("")
                print("Country has been added.")
                con.commit()
                rs2.close()
            except mysql.connector.Error as err:
                print(err)
            con.close()
    except mysql.connector.Error as err:
        print(err)

#Once given, your program should then display all countries with a gdp equal to or higher
#than the value given and an inflation equal to or lower than the inflation given. The countries
#should be displayed from highest-to-lowest gdp such that if two countries have the same gdp,
#they should be displayed from lowest-to-highest inflation. Additionally, only the number of
#countries entered should be displayed. For example, using the example above, if ten countries
#satisfy the conditions given, then only the first five are displayed, and if only three countries
#satisfy the above conditions, then only the three are shown. Each country should be displayed
#on a single line as “name (code), gdp, inflation”, e.g., United States (US), 57466, 2.1.
#Note that your program should not perform any sorting and should not reduce the size of the
#result set (i.e., you should use ORDER BY and LIMIT in your prepared statement).
def findCountries():
    try:
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        db = 'chuynh_DB'
        # create a connection
        con = mysql.connector.connect(user=usr, password=pwd, host=hst, database=db)
        num = input("Number of countries to display: ")
        gdp = input("Minimum per capita gdp (USD): ")
        inflt = input("Maximum inflation (pct): ")
        rs = con.cursor()
        query = 'SELECT code, country_name, gdp_in_dollars_per_person, inflation_in_percent FROM Country WHERE gdp_in_dollars_per_person >= %s AND inflation_in_percent <= %s ORDER BY gdp_in_dollars_per_person DESC, inflation_in_percent LIMIT %s'
        rs.execute(query, (gdp, inflt, num))
        print("")
        for(code, country_name, gdp_in_dollars_per_person, inflation_in_percent) in rs:
            print("{} ({}), {}, {}".format(country_name, code, gdp_in_dollars_per_person, inflation_in_percent))
        rs.close()
        con.close()
    except mysql.connector.Error as err:
        print(err)

#Once given, your program should (a) check to make sure the country code already exists, and
#if so, (b) update the corresponding gdp and inflation, and otherwise, (c) notify the user that
#the country does not exist.
def updateCountry():
    try:
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        db = 'chuynh_DB'
        # create a connection
        con = mysql.connector.connect(user=usr, password=pwd, host=hst, database=db)
        cCode = str(raw_input("Country code: "))
        gdp = input("Country per capita gdp (USD): ")
        inflt = input("Country inflation (pct): ")
        rs = con.cursor()
        query = 'SELECT code, country_name FROM Country'
        rs.execute(query)
        # flag is to check if the country already exists
        matchFlag = False
        for code, country_name in rs:
            if code == cCode:
                matchFlag = True
        rs.close()
        if matchFlag == False:
            print("")
            print("This country does not exist in the database.")
        else:
            try:
                rs2 = con.cursor()
                query2 = 'UPDATE Country SET gdp_in_dollars_per_person = %s, inflation_in_percent = %s WHERE code = %s'
                rs2.execute(query2, (gdp, inflt, cCode))
                con.commit()
                print("")
                print("Information have been updated.")
                rs2.close()
            except mysql.connector.Error as err:
                print(err)
            con.close()
    except mysql.connector.Error as err:
        print(err)

#Main Menu
def main():
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
        else:
            print("Not a valid selection, please pick from the choices above.")

if __name__ == '__main__':
    main()