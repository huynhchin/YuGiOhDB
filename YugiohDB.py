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
    query2 = "SELECT nameM FROM ConsistsMo WHERE nameD = %s UNION SELECT nameS From ConsistsMa WHERE nameD = %s UNION SELECT nameT FROM ConsistsTr WHERE nameD = %s"
    rs2.execute(query2, (dName, dName, dName))
    print("")
    print("Cards in Deck:")
    for (name) in rs2:
        print(name[0].encode('utf-8'))
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
    print("Deck has been created.")
    rs.close()

#add card to a deck
def addCard():
    dName = str(raw_input("Enter deck's name: "))
    rs = con.cursor()
    query = "SELECT name FROM Deck WHERE %s EXISTS (SELECT name FROM Deck)"
    rs.execute(query, dName)
    if (rs == False):
        print("Deck doesn't exist.")
        create = str(raw_input("Do you want to create this deck? (y or n) "))
        if (create == 'y' or create == 'yes'):
            createDeck()
        elif (create == 'n' or create == 'no'):
            addCard()
    else:
        confirm = str(raw_input("Do you know what card you want to add? (y or n) "))
        if (confirm == 'y' or confirm == 'yes'):
            Ctype = str(raw_input("Is this card a monster, spell, or trap card? "))
            if (Ctype == 'monster'):
                m_copy = input("Enter amount of copies you want: ")
                m_name = input("Enter the monster name: ")
                query2 = "INSERT INTO ConsistsMo VALUES (%s, %s, %s)"
                rs.execute(query2, (m_copy, m_name, dName))
                print("")
                print("Card has been added.")
            elif (Ctype == 'spell'):
                s_copy = input("Enter amount of copies you want: ")
                s_name = input("Enter the spell name: ")
                query3 = "INSERT INTO ConsistsMa VALUES (%s, %s, %s)"
                rs.execute(query3, (s_copy, s_name, dName))
                print("")
                print("Card has been added.")
            elif (Ctype == 'trap'):
                t_copy = input("Enter amount of copies you want: ")
                t_name = input("Enter the trap name: ")
                query4 = "INSERT INTO ConsistsTr VALUES (%s, %s, %s)"
                rs.execute(query4, (t_copy, t_name, dName))
                print("")
                print("Card has been added.")
        elif (confirm == 'n' or confirm == 'no'):
            analyzeDeck()

def analyzeDeck():
    print("What category would you like to search cards on?")
    print("")
    print("1. Look up by Monster name")
    print("2. Look up by Monster class")
    print("3. Look up by Monster Attack Points")
    print("4. Look up by Monster Defense Points")
    print("5. Look up by Monster level")
    print("6. Look up by Monster type")
    print("7. Look up spell")
    print("8. Look up trap")
    print("9. Look up by 2 filters")
    print("10. Exit")
    choice = input("Enter your choice (1-9): ")
    rs = con.cursor
    print("")
    if choice == 1:
        cname = str(raw_input("Enter card name: ")
        query = 'Select name from Monster where name = %s'
        rs.execute(query, cname)
        print("")
        for (cname) in rs:
            print(cname[0].encode('utf-8'))
    elif choice == 2:
        cclass = str(raw_input("Enter card class (Dark, Light, Earth, Water, Fire, etc.: ")
        query = 'Select name from Monster where class = %s'
        rs.execute(query, cclass)
        print("")
        for (cclass) in rs:
            print(cclass[0].encode('utf-8'))
    elif choice == 3:
        cname = str(raw_input("Enter card name: ")
        query = 'Select name from Monster where name = %s'
        rs.execute(query, cname)
        print("")
        for (name) in rs:
            print(name[0].encode('utf-8'))
    elif choice == 4:
        cname = str(raw_input("Enter card name: ")
        query = 'Select name from Monster where name = %s'
        rs.execute(query, cname)
        print("")
        for (name) in rs:
            print(name[0].encode('utf-8'))
    elif choice == 5:
        cname = str(raw_input("Enter card name: ")
        query = 'Select name from Monster where name = %s'
        rs.execute(query, cname)
        print("")
        for (name) in rs:
            print(name[0].encode('utf-8'))
    elif choice == 6:
        cname = str(raw_input("Enter card name: ")
        query = 'Select name from Monster where name = %s'
        rs.execute(query, cname)
        print("")
        for (name) in rs:
            print(name[0].encode('utf-8'))
    elif choice == 7:
        cname = str(raw_input("Enter card name: ")
        query = 'Select name from Monster where name = %s'
        rs.execute(query, cname)
        print("")
        for (name) in rs:
            print(name[0].encode('utf-8'))
    elif choice == 8:
        cname = str(raw_input("Enter card name: ")
        query = 'Select name from Monster where name = %s'
        rs.execute(query, cname)
        print("")
        for (name) in rs:
            print(name[0].encode('utf-8'))
    elif choice == 9:
        cname = str(raw_input("Enter card name: ")
        query = 'Select name from Monster where name = %s'
        rs.execute(query, cname)
        print("")
        for (name) in rs:
            print(name[0].encode('utf-8'))
    elif choice == 10:

    else:
        print("Not a valid delection. Please pick from the choices above")

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
            analyzeDeck()
        elif command == 5:
            con.close()
            exitProgram = True
        else:
            print("Not a valid selection, please pick from the choices above.")

if __name__ == '__main__':
    main()