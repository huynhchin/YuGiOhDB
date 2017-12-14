#CPSC 321: Final Project: YuGiOh Database
#Chin Huynh and Jon Reid

import mysql.connector
import config

#Establishing a connection to the DB, close when the program exists.
try:
    usr = config.mysql['user']
    pwd = config.mysql['password']
    hst = config.mysql['host']
    db = 'chuynh_DB'
    # create a connection
    con = mysql.connector.connect(user=usr, password=pwd, host=hst, database=db)
except mysql.connector.Error as err:
    print(err)


#Look up an existing deck, and display a list of all cards in the deck.
def existDeck():
    rs = con.cursor()
    query = 'SELECT * FROM Deck'
    rs.execute(query)
    print("Deck List:")
    for (name, description) in rs:
        print('{} ({})'.format(name, description))
    print("")
    dName = str(raw_input("Which deck do you want to look at? (Enter Name) "))
    rs2 = con.cursor()
    query2 = "SELECT nameM FROM ConsistsMo WHERE nameD = %s UNION SELECT nameSpell From ConsistsMa WHERE nameD = %s UNION SELECT nameT FROM ConsistsTr WHERE nameD = %s"
    rs2.execute(query2, (dName, dName, dName))
    print("")
    print("Cards in Deck:")
    for (name) in rs2:
        print(name[0].encode('utf-8'))
    rs2.close()
    rs.close()


#Display all monster, magic, and trap cards not in any deck.
def cardNotInDeck():
    print("")
    print("Monster cards not in Deck: ")
    rs = con.cursor()
    query = "SELECT m.name FROM Monster m LEFT JOIN ConsistsMo c ON m.name = c.nameM WHERE c.nameD IS NULL"
    rs.execute(query)
    for (name) in rs:
        print(name[0].encode('utf-8'))
    print("")
    print("Spell cards not in Deck: ")
    rs2 = con.cursor()
    query2 = "SELECT m.name FROM Magic m LEFT JOIN ConsistsMa c ON m.name = c.nameSpell WHERE c.nameD IS NULL"
    rs2.execute(query2)
    for (name) in rs2:
        print(name[0].encode('utf-8'))
    print("")
    print("Trap cards not in Deck: ")
    rs3 = con.cursor()
    query3 = "SELECT t.name FROM Trap t LEFT JOIN ConsistsTr c ON t.name = c.nameT WHERE c.nameD IS NULL"
    rs3.execute(query3)
    for (name) in rs3:
        print(name[0].encode('utf-8'))
    rs3.close()
    rs2.close()
    rs.close()


#Counts how many cards are in the deck.
def sumCard(dName):
    rs2 = con.cursor()
    query2 = "SELECT COUNT(*) FROM (SELECT nameM FROM ConsistsMo WHERE nameD = %s UNION SELECT nameSpell From ConsistsMa WHERE nameD = %s UNION SELECT nameT FROM ConsistsTr WHERE nameD = %s) AS Cards"
    rs2.execute(query2, (dName, dName, dName))
    row2 = rs2.fetchall()
    rs2.close()
    return row2[0][0]


#This function is called in deck analyze and it gives return statistics on a deck.
def summarizeDeck():
    rs = con.cursor()
    query = 'SELECT * FROM Deck'
    rs.execute(query)
    print("Deck List:")
    for (name, description) in rs:
        print('{} ({})'.format(name, description))
    print("")
    rs2 = con.cursor()
    decision = str(raw_input("Which deck do you want to analyze? (Enter Name) "))
    print("")
    dName = decision
    sum = sumCard(dName)
    query2 = "SELECT d.name, AVG(m.Attack_Points) AS Average_Attack, AVG(m.Defense_Point) AS Average_Defense, AVG(m.level) AS Average_Lvl FROM Deck d, ConsistsMo c, Monster m WHERE m.name = c.nameM AND c.nameD = d.name GROUP BY d.name HAVING d.name = '%s'" %dName
    rs2.execute(query2)
    for (name, avg_attck, avg_defense, avg_lvl) in rs2:
        print('{}: Average Attack = ({}), Average Defense = ({}), Average Lvl = ({}), Total Number of Cards = {}'.format(name, avg_attck, avg_defense, avg_lvl, sum))
    rs2.close()
    rs.close()


#The user creates his own deck.
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


#This function adds a card to a deck. It makes sure the deck exists, if it doesn't then it will ask if the user
#wants to create one or just simple rerun the function and let the user tries again.
def addCard():
    dName = str(raw_input("Enter deck's name: "))
    rs = con.cursor()
    query = "SELECT name FROM (SELECT name FROM Deck) AS nameDeck WHERE name = '%s'" % dName
    rs.execute(query)
    rs.fetchall()
    if (rs.rowcount == 0):
        print("")
        print("Deck doesn't exist.")
        print("")
        create = str(raw_input("Do you want to create this deck? (y or n) "))
        print("")
        if (create == 'y' or create == 'yes'):
            createDeck()
        elif (create == 'n' or create == 'no'):
            addCard()
    else:
        print("")
        confirm = str(raw_input("Do you know what card you want to add? (y or n) "))
        print("")
        if (confirm == 'y' or confirm == 'yes'):
            Ctype = str(raw_input("Is this card a monster, spell, or trap card? "))
            print("")
            if (Ctype == 'monster'):
                m_copy = input("Enter amount of copies you want: ")
                m_name = str(raw_input("Enter the monster name: "))
                query2 = "INSERT INTO ConsistsMo VALUES (%s, %s, %s)"
                rs.execute(query2, (m_copy, m_name, dName))
                con.commit()
                print("")
                print("Card has been added.")
            elif (Ctype == 'spell'):
                s_copy = input("Enter amount of copies you want: ")
                s_name = str(raw_input("Enter the spell name: "))
                query3 = "INSERT INTO ConsistsMa VALUES (%s, %s, %s)"
                rs.execute(query3, (s_copy, s_name, dName))
                con.commit()
                print("")
                print("Card has been added.")
            elif (Ctype == 'trap'):
                t_copy = input("Enter amount of copies you want: ")
                t_name = str(raw_input("Enter the trap name: "))
                query4 = "INSERT INTO ConsistsTr VALUES (%s, %s, %s)"
                rs.execute(query4, (t_copy, t_name, dName))
                con.commit()
                print("")
                print("Card has been added.")
        elif (confirm == 'n' or confirm == 'no'):
            analyzeDeck()


#In this function, you can search for any card in the database. You can look up monster, spell, trap, see what card isn't in any deck, and get
#an analyze of a deck. The analyze consists of name of the deck, avgerage attack points in the deck, average defense points in the deck, and average level
#in the deck.
def analyzeDeck():
    print("What category would you like to search on?")
    print("")
    print("1. Look up Monster Card")
    print("2. Look up Magic Card")
    print("3. Look up Trap Card")
    print("4. Look up Cards Lacking a Deck")
    print("5. Analyze Deck")
    print("")
    choice = input("Enter your choice (1-5): ")
    print("")
    if choice == 1:
        print("1. Look up by Name")
        print("2. Look up by Level")
        print("3. Look up by Attack")
        print("4. Look up by Defense")
        print("5. Look up by Type")
        print("6. Look up by Class")
        print("")
        choice2 = input("Enter choice: ")
        print("")
        if choice2 == 1:
            rs = con.cursor()
            c_name = str(raw_input('Enter card name: '))
            query = "Select * from Monster where name = '%s'" % c_name
            rs.execute(query)
            print("")
            row = rs.fetchone()
            if row is not None:
                result = "{}:\nClass = {}\nType = {}\nLevel = {}\nAttack Points = {}\nDefense Points = {}\nDescription = {}\nTips = {}\n"
                result = result.format(row[5], row[0], row[2], row[4], row[6], row[7], row[3], row[1])
                print(result)
            rs.close()
        elif choice2 == 2:
            rs2 = con.cursor()
            c_level = input('Enter Card level (1-12): ')
            # query2 = "SELECT * FROM Monster WHERE level = '%s'" %c_level
            query2 = "SELECT name, class, type, level, Attack_Points, Defense_Point, description, tips FROM Monster WHERE level = '%s'" % c_level
            rs2.execute(query2)
            print("")
            row2 = rs2.fetchall()
            i = 1
            for result in row2:
                print(i)
                print(" | ".join(map(str, result)))
                i += 1
            rs2.close()
        elif choice2 == 3:
            rs3 = con.cursor()
            c_Attack_min = input('Enter Min Value: ')
            c_Attack_max = input('Enter Max Value: ')
            query3 = "Select name, class, type, level, Attack_Points, Defense_Point, description, tips from Monster where Attack_Points between '%s' AND '%s' ORDER BY Attack_Points DESC" % (
                c_Attack_min, c_Attack_max)
            rs3.execute(query3)
            print("")
            row3 = rs3.fetchall()
            i = 1
            for result in row3:
                print(i)
                print(" | ".join(map(str, result)))
                i += 1
            rs3.close()
        elif choice2 == 4:
            rs4 = con.cursor()
            c_Defense_min = input('Enter Min Value: ')
            c_Defense_max = input('Enter Max Value: ')
            query4 = "Select name, class, type, level, Attack_Points, Defense_Point, description, tips from Monster where Defense_Point between '%s' AND '%s' ORDER BY Defense_Point DESC" % (
                c_Defense_min, c_Defense_max)
            rs4.execute(query4)
            print("")
            row4 = rs4.fetchall()
            i = 1
            for result in row4:
                print(i)
                print(" | ".join(map(str, result)))
                i += 1
            rs4.close()
        elif choice2 == 5:
            rs5 = con.cursor()
            c_type = str(raw_input('Enter type of Monster: '))
            c_type = '%' + c_type + '%'
            query5 = "Select name, class, type, level, Attack_Points, Defense_Point, description, tips from Monster where type LIKE '%s'" % c_type
            rs5.execute(query5)
            print("")
            row5 = rs5.fetchall()
            i = 1
            for result in row5:
                print(i)
                print(" | ".join(map(str, result)))
                i += 1
            rs5.close()
        elif choice2 == 6:
            rs6 = con.cursor()
            c_class = str(raw_input('Enter Card Class (Dark, Light, Earth, Water, Fire, Divine): '))
            query6 = "Select name, class, type, level, Attack_Points, Defense_Point, description, tips from Monster where class = '%s'" % c_class
            rs6.execute(query6)
            print("")
            row6 = rs6.fetchall()
            i = 1
            for result in row6:
                print(i)
                print(" | ".join(map(str, result)))
                i += 1
            rs6.close()
    elif choice == 2:
        print("1. Look up by name")
        print("2. Look up by type")
        print("")
        choice2 = input("Enter choice: ")
        print("")
        if choice2 == 1:
            rs = con.cursor()
            c_name = str(raw_input('Enter card name: '))
            query = "Select * from Magic where name = '%s'" % c_name
            rs.execute(query)
            print("")
            row = rs.fetchone()
            if row is not None:
                result = "{}:\nType = {}\nDescription = {}\nTips = {}\n"
                result = result.format(row[3], row[1], row[2], row[0])
                print(result)
            rs.close()
        elif choice2 == 2:
            rs5 = con.cursor()
            c_type = str(raw_input('Enter type of Spell: '))
            c_type = '%' + c_type + '%'
            query5 = "Select name, type, description, tips from Magic where type LIKE '%s'" % c_type
            rs5.execute(query5)
            print("")
            row5 = rs5.fetchall()
            i = 1
            for result in row5:
                print(i)
                print(" | ".join(map(str, result)))
                i += 1
            rs5.close()
    elif choice == 3:
        print("1. Look up by name")
        print("2. Look up by type")
        print("")
        choice2 = input("Enter choice: ")
        print("")
        if choice2 == 1:
            rs = con.cursor()
            c_name = str(raw_input('Enter card name: '))
            query = "Select * from Trap where name = '%s'" % c_name
            rs.execute(query)
            print("")
            row = rs.fetchone()
            if row is not None:
                result = "{}:\nType = {}\nDescription = {}\nTips = {}\n"
                result = result.format(row[3], row[1], row[2], row[0])
                print(result)
            rs.close()
        elif choice2 == 2:
            rs5 = con.cursor()
            c_type = str(raw_input('Enter type of Trap: '))
            c_type = '%' + c_type + '%'
            query5 = "Select name, type, description, tips from Trap where type LIKE '%s'" % c_type
            rs5.execute(query5)
            print("")
            row5 = rs5.fetchall()
            i = 1
            for result in row5:
                print(i)
                print(" | ".join(map(str, result)))
                i += 1
            rs5.close()
    elif choice == 4:
        cardNotInDeck()
    elif choice == 5:
        summarizeDeck()
    else:
        print("Not a valid detection. Please pick from the choices above")


#Take in a deck, then the program checks to see if deck exists or not. If deck doesn't exists then tell user to type name in again.
#If deck does exists, then the program prints out a list of all cards in the deck. Then prompt the user to enter name of card to
#delete. Then the program checks if the card exists in deck, if it does then delete it else tell the user the name isn't valid then
#rerun the program from the beginning.
def deleteCard():
    dName = str(raw_input("Enter deck's name: "))
    rs = con.cursor()
    query = "SELECT name FROM (SELECT name FROM Deck) AS nameDeck WHERE name = '%s'" %dName
    rs.execute(query)
    row = rs.fetchall()
    if (rs.rowcount == 0):
        print("")
        print("Deck's name is wrong, try again.")
        print("")
        deleteCard()
    elif row is not None:
        rs2 = con.cursor()
        query2 = "SELECT nameM FROM ConsistsMo WHERE nameD = %s UNION SELECT nameSpell From ConsistsMa WHERE nameD = %s UNION SELECT nameT FROM ConsistsTr WHERE nameD = %s"
        rs2.execute(query2, (dName, dName, dName))
        print("")
        print("Cards in Deck:")
        for (name) in rs2:
            print(name[0].encode('utf-8'))
        rs2.close()
        print("")
        cName = str(raw_input("Enter card's name to remove from deck: "))
        rs3 = con.cursor()
        rs4 = con.cursor()
        rs5 = con.cursor()
        rs6 = con.cursor()
        query4 = "SELECT nameM FROM (SELECT nameM, nameD FROM ConsistsMo) AS twoNameM WHERE nameM = '%s' AND nameD = '%s'" %(cName, dName)
        query5 = "SELECT nameSpell FROM (SELECT nameSpell, nameD FROM ConsistsMa) AS twoNameSpell WHERE nameSpell = '%s' AND nameD = '%s'" %(cName, dName)
        query6 = "SELECT nameT FROM (SELECT nameT, nameD FROM ConsistsTr) AS twoNameT WHERE nameT = '%s' AND nameD = '%s'" %(cName, dName)
        rs4.execute(query4)
        rs4.fetchall()
        rs5.execute(query5)
        rs5.fetchall()
        rs6.execute(query6)
        rs6.fetchall()
        if (rs4.rowcount > 0):
            query3 = "DELETE FROM ConsistsMo WHERE nameM = '%s'" % (cName)
            rs3.execute(query3)
            con.commit()
            print("")
            print("Card has been deleted.")
        elif (rs5.rowcount > 0):
            query3 = "DELETE FROM ConsistsMa WHERE nameSpell = '%s'" % (cName)
            rs3.execute(query3)
            con.commit()
            print("")
            print("Card has been deleted.")
        elif (rs6.rowcount > 0):
            query3 = "DELETE FROM ConsistsTr WHERE nameT = '%s'" % (cName)
            rs3.execute(query3)
            con.commit()
            print("")
            print("Card has been deleted.")
        else:
            print("")
            print("Name is not valid, try again.")
            print("")
            deleteCard()
        rs6.close()
        rs5.close()
        rs4.close()
        rs3.close()
    rs.close()


# Main Menu
def main():
    exitProgram = False
    while exitProgram == False:
        print("")
        print("1. Look at existing deck.")
        print("2. Create your own deck.")
        print("3. Add card to a deck.")
        print("4. Look at specific card")
        print("5. Delete card from deck")
        print("6. Exit")
        command = input("Enter your choice (1-6): ")
        print("")
        if command == 1:
            existDeck()
        elif command == 2:
            createDeck()
        elif command == 3:
            addCard()
        elif command == 4:
            analyzeDeck()
        elif command == 5:
            deleteCard()
        elif command == 6:
            con.close()
            exitProgram = True
        else:
            print("Not a valid selection, please pick from the choices above.")


if __name__ == '__main__':
    main()
