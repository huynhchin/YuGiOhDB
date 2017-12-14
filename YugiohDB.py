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


def analyzeDeck():
		print("What category would you like to search cards on?")
		print("")
		print("1. Look up Monster Card")
		print("2. Look up Magic Card")
		print("3. Look up Trap Card")
		print("")
		choice = input("Enter your choice (1-3): ")
		print("")
		if choice == 1:
			print("1. Look up by name")
			print("2. Look up by level")
			print("3. Look up by Attack")
			print("4. Look up by Defense")
			print("5. Look up by Type")
			print("6. Look up by Class")
			print("7. Look up by 2 filters")
			print("")
			choice2 = input("Enter choice: ")
			print("")
			if choice2 == 1:
				rs = con.cursor()
				c_name = str(raw_input('Enter card name: '))
				query = "Select * from Monster where name = '%s'" %c_name
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
				#query2 = "SELECT * FROM Monster WHERE level = '%s'" %c_level
				query2 = "SELECT name, class, type, level, Attack_Points, Defense_Point, description, tips FROM Monster WHERE level = '%s'" %c_level
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
				query3 = "Select name, class, type, level, Attack_Points, Defense_Point, description, tips from Monster where Attack_Points between '%s' AND '%s' ORDER BY Attack_Points DESC" %(c_Attack_min, c_Attack_max)
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
				query4 = "Select name, class, type, level, Attack_Points, Defense_Point, description, tips from Monster where Defense_Point between '%s' AND '%s' ORDER BY Defense_Point DESC" %(c_Defense_min, c_Defense_max)
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
				query5 = "Select name, class, type, level, Attack_Points, Defense_Point, description, tips from Monster where type LIKE '%s'" %c_type
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
				query6 = "Select name, class, type, level, Attack_Points, Defense_Point, description, tips from Monster where class = '%s'" %c_class
				rs6.execute(query6)
				print("")
				row6 = rs6.fetchall()
				i = 1
				for result in row6:
					print(i)
					print(" | ".join(map(str, result)))
					i += 1
				rs6.close()
			elif (choice2 == 7):
				print('Which filters do you want?')
				print("1. Look up by Level")
				print("2. Look up by Attack")
				print("3. Look up by Defense")
				print("4. Look up by Type")
				print("5. Look up by Class")
				print("")
				filter1 = input('Enter Number of 1st filter: ')
				filter2 = input('Enter Number of 2nd filter: ')
				if (filter1 == 1 and filter2 == 2) or (filter1 == 2 and filter2 == 1):
					rs7 = con.cursor()
					print("")
					f_level = input('Enter Card Level: ')
					c_Attack_min = input('Enter Attack Min Value: ')
					c_Attack_max = input('Enter Attack Max Value: ')
					query7 = "Select name, class, type, level, Attack_Points, Defense_Point, description, tips from Monster where level = '%s' AND Attack_Points between '%s' AND '%s'" %(f_level, c_Attack_min, c_Attack_max)
					rs7.execute(query7)
					print("")
					row7 = rs7.fetchall()
					i = 1
					for result in row7:
						print(i)
						print(" | ".join(map(str, result)))
						i += 1
					rs7.close()
##						
##				elif (filter1 == 1 and filter2 == 3) or (filter1 == 3 and filter2 == 1):
##					print('1')
##				elif (filter1 == 2 and filter2 == 3) or (filter1 == 3 and filter2 == 2):
##					print('1')
##				elif (filter1 == 1 and filter2 == 4) or (filter1 == 4 and filter2 == 1):
##					print('1')
##				elif (filter1 == 2 and filter2 == 4) or (filter1 == 4 and filter2 == 2):
##					print('1')
##				elif (filter1 == 3 and filter2 == 4) or (filter1 == 4 and filter2 == 3):
##					print('1')
##				elif (filter1 == 1 and filter2 == 5) or (filter1 == 5 and filter2 == 1):
##					print('1')
##v				elif (filter1 == 2 and filter2 == 5) or (filter1 == 5 and filter2 == 2):
##					print('1')
##				elif (filter1 == 3 and filter2 == 5) or (filter1 == 5 and filter2 == 3):
##					print('1')
##				elif (filter1 == 4 and filter2 == 5) or (filter1 == 5 and filter2 == 4):
##					print('1')
##				elif (filter1 == 1 and filter2 == 6) or (filter1 == 6 and filter2 == 1):
##					print('1')
##				elif (filter1 == 2 and filter2 == 6) or (filter1 == 6 and filter2 == 2):
#v#					print('1')
##				elif (filter1 == 3 and filter2 == 6) or (filter1 == 6 and filter2 == 3):
##					print('1')
##				elif (filter1 == 4 and filter2 == 6) or (filter1 == 6 and filter2 == 4):
##					print('1')
 ##              elif (filter1 == 5 and filter2 == 6) or (filter1 == 6 and filter2 == 5):
##		elif choice == 2:
##			print('1')
##		elif choice == 3:
##			print('1')				
##		else:
##			print("Not a valid delection. Please pick from the choices above")


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
            addCard()
        elif command == 4:
            analyzeDeck()
        elif command == 5:
            con.close()
            exitProgram = True
        else:
            print("Not a valid selection, please pick from the choices above.")

if __name__ == '__main__':
    main()