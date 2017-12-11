import mysql.connector
import config

try:
    usr = config.mysql['user']
    pwd = config.mysql['password']
    hst = config.mysql['host']
    db = 'chuynh_DB'
    # create a connection
    con = mysql.connector.connect(user=usr, password=pwd, host=hst, database=db)
except mysql.connector.Error as err:
        print(err)

#look at existing deck
def existDeck():
    rs = con.cursor()
    query = 'SELECT * FROM Deck'
    rs.execute(query)
    for (name, description) in rs:
        print('{} ({})'.format(name, description))
    print("")
    dName = str(raw_input("Which deck do you want to look at? (Enter Name) "))
    rs2 = con.cursor()
    query2 = "SELECT nameM, copy FROM ConsistsMo WHERE nameD = %s UNION SELECT nameS, copy From ConsistsMa WHERE nameD = %s UNION SELECT nameT, copy FROM ConsistsTr WHERE nameD = %s"
    rs2.execute(query2, (dName, dName, dName))
    print("")
    print("Cards in Deck:")
    for (name) in rs2:
        print(name[0].encode('utf-8'), name[1])
    rs2.close()
    rs.close()

#the user creates his own deck
def createDeck():
    dName = str(raw_input("Enter name for deck: "))
    description = str(raw_input("Enter a description for this deck: "))
    rs = con.cursor()
    query = 'INSERT INTO Deck VALUES (%s, %s)'
    rs.execute(query, (dName, description))
    con.commit()
    print("")
    print("Deck has been added.")
    rs.close()

#add card to a deck
def addCard():
    dName = str(raw_input("Enter deck's name: "))
    rs = con.cursor()
    query = "SELECT name FROM Deck WHERE %s EXISTS (SELECT name FROM Deck)"
    rs.execute(query, dName)
    if (rs == False):
        print("Deck doesn't exist.")
        create = str(raw_input("Do you want to create a deck with this name? (y or n) "))
        if()

#Main Menu
def main():
    exitProgram = False
    while exitProgram == False:
        print("")
        print("1. Look at existing deck.")
        print("2. Create your own deck.")
        print("3. Add card to a deck.")
        print("4. Look at specific card")
        print("5. Exit")
        command = input("Enter your choice (1-5): ")
        print("")
        if command == 1:
            existDeck()
        elif command == 2:
            createDeck()
        elif command == 3:
            print("3")
        elif command == 4:
            print("4")
        elif command == 5:
            con.close()
            exitProgram = True
        else:
            print("Not a valid selection, please pick from the choices above.")

if __name__ == '__main__':
    main()