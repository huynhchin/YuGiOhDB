# Main menu displayed to user.
def MainMenu():
    # while loop keeps running while True
    while True:
        # Main menu choices
        print ("1. Look at Existing Deck")
        print ("2. Create you Own Deck")
        print ("3. Look up Specific Card")
        print ("4. Exit")
        choice = input("Enter your choice (1-4): ")
        if choice == 1:
            print ("Choice 1...List countries")
            print("")
            listCountries()
        elif choice == 2:
            print ("Choice 2...Add country")
            print("")
            addCountry()
        elif choice == 3:
            print ("Choice 3...Find countries based on gdp and inflation")
            print("")
            findCountries()
        elif choice == 4:
            print ("Choice 4...Update country\'s gdp and inflation")
            print("")
            updateCountries()
        elif choice == 5:
            print ("Choice 5...Exit")
            print("")
            quit()    # exits loop and exits script
        else:
            raw_input("Not a valid choice. Please enter any key and try again...")
            print("")
            
# Shows names and codes of all countries in DB .      
def listCountries():
    try:
        # connection info
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        dab = 'jreid2_DB'
		
        # establish a connection
        con = mysql.connector.connect(user=usr,password=pwd, host=hst, database=dab)

        # create a result set
        rs = con.cursor()
        query = 'SELECT country_name, code FROM country'
        rs.execute(query)
		
        # print results
        for (name, code) in rs:
            print ("{} ({})".format(name, code))
        print("")
        MainMenu()
        
        rs.close()
        con.close()

    except mysql.connector.Error as err:
        print (err)

# Asks user for information to add new country to DB.
# Asks for country code, name, gdp, and inflation and
# notifies user if the country already exists in DB.
def addCountry():
    try: 
        # connection info
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        dab = 'jreid2_DB'

        #establish a connection
        con = mysql.connector.connect(user=usr,password=pwd, host=hst,
                                      database=dab)
        # gatheers category information from user
        input_code = str(raw_input("Country code................: "))
        name = str(raw_input("Country name................: "))
        gdp = float(raw_input("Country per capita gdp (USD): "))
        inflation = float(raw_input("Country inflation (pct).....: "))

        rs = con.cursor()
        code_country = 'SELECT code, country_name FROM country'
        rs.execute(code_country)
        
        # establishes boolean variable for country code as initially false
        code_note = False

        #adds code and country name to rs
        for code, country_name in rs:
            if code == input_code:
                code_note = True
                
        rs.close()
		
		#Notifies user if country exists 
        if code_note == True:
            print ("Country already exists in database")
        else:
            # inserts new country values into db
            try:
                rs2 = con.cursor()
                # insert the country into the db
                insert = 'INSERT INTO country VALUES(%s, %s, %s, %s)'
                rs2.execute(insert,(input_code, name, gdp, inflation))
                print "Country added to database"
                con.commit()
                rs2.close()
            except mysql.connector.Error as err:
                print err
                
            print("")
            con.close()
            MainMenu()
    except mysql.connector.Error as err:
            print (err)

# Presents all countries with a gdp equal to or greater
# than value input and an inflation equal to or less
# than inflation input. Countries are displayed
# from highest-to-lowest gdp. 
# Only the number of countries entered should be shown.
# If two countries have the same gdp, they are displayed from
# lowest-to-highest inflation.
def findCountries():
    try: 
        # connection info
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        dab = 'jreid2_DB'

        # establish a connection
        con = mysql.connector.connect(user=usr,password=pwd, host=hst,
                                      database=dab)
        # receives input from user
        num_countries = int(raw_input("Number of countries to display: "))
        min_gdp = float(raw_input("Minimum per capita gdp (USD)..: "))
        max_inflation = float(raw_input("Maximum inflation (pct).......: "))

        # create and execute query
        rs = con.cursor()
        # query used to retrieve the country's name, code, gdp, and inflation values
        query = 'SELECT country_name, code, gdp, inflation FROM country WHERE country.gdp >= %s AND country.inflation <= %s ORDER BY gdp DESC, inflation LIMIT %s'
        rs.execute(query, (min_gdp, max_inflation, num_countries))

        # display result
        for (country_name, code, gdp, inflation) in rs:
            print ("{} ({}), {}, {}".format(country_name, code, gdp, inflation))
        print ("")
        MainMenu()
        
        rs.close()
        con.close()

    except mysql.connector.Error as err:
        print (err)
        
# Updates an  existing country's gdp and inflation data.
# Asks user for the country code, revised gdp, and revised
# inflation.
def updateCountries():
    try: 
        # connection info
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        dab = 'jreid2_DB'

        # Establishes a connection
        con = mysql.connector.connect(user=usr,password=pwd, host=hst,
                                      database=dab)

        # Input to be Updated
        code = str(raw_input("Country code................: "))
        gdp = str(raw_input("Country per capita gdp (USD): "))
        inflation = str(raw_input("Country inflation (pct).....: "))

        rs = con.cursor()
		#SQL query
        country_codes = "SELECT code FROM country WHERE code='" + code+"';"
        
        rs.execute(country_codes, (code))

        text = ""
        # saves country code from query to text
        for t in rs:
            text += str(t)
        # checks for equivalent country code found
        # based on the user's input
        if(text == ""):
            print ("Country does not exist in database")
            print ("")
            return
        else:
            # updates country's gdp and inflation if match is valid
            update = 'UPDATE country SET gdp = %s, inflation = %s  WHERE code = %s'
            rs.execute(update, (gdp, inflation, code))
            con.commit()
        # commit the changes
        con.commit()

        print ("")
        MainMenu()
        
        rs.close()
        con.close()

    except mysql.connector.Error as err:
        print (err)
    
def main():
    try:
        # connection info
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        dab = 'jreid2_DB'

        # Establishes a connection
        con = mysql.connector.connect(user=usr,password=pwd, host=hst,
                                      database=dab)
        MainMenu()
        con.commit()
        rs.close()
        con.close()
                
    except mysql.connector.Error as err:
        print (err)

if __name__ == '__main__':
    main()
