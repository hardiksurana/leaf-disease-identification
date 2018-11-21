# nameList = ["Harsh","Hardik","Gaurav"]
# emailList = ["harsh@gmail.com","hardik@gmail.com","gaurav@gmail.com"]
# usernamesList = ["Harsh","Hardik","Gaurav"]
# passwordList = ["Harsh","Hardik","Gaurav"]



def getDetailsOfUser(mysql,username):

    query = "SELECT name from register where username='" + username + "'"

    print("query is ",query)
    conn = mysql.connect()
    cursor = conn.cursor()
    res = cursor.execute(query)
    data = cursor.fetchall()
    print("data for details of user is ",data)
    nameOfUser = data[0][0]



def loginCheck(mysql,username,password):

	# indexFromUsernames = -1
	# for i in range(len(usernamesList)):
	# 	if(username == usernamesList[i]):
	# 		indexFromUsernames = i
	# if(indexFromUsernames != -1):
	# 	if(passwordList[indexFromUsernames] == password):
	# 		return True
	# 	else:
	# 		return False
	# else:
	# 	return False
    query = "SELECT password from Login where username='" + username + "'"
    # query = "SELECT * FROM Login WHERE {0}ID={1}".format(username,password)
    print("query is ", query)
    conn = mysql.connect()
    cursor =conn.cursor()
    res = cursor.execute(query)
    data = cursor.fetchall()
    print("data inside login is ", data)
    try:
        if(data[0][0]!=password):
            return False
        else:
            return True
    except Exception as e:
    	return False


def isExistingUser(mysql,username):

	# indexFromUsernames = -1
    query = "SELECT username from register where username='" + username + "'"
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
	# for i in range(len(usernamesList)):
	# 	if(username == usernamesList[i]):
	# 		return True
	# if(indexFromUsernames == -1):
	# 	return False
    print("data is ", data)
    try:
        if(username != data[0][0]):
            return False
        else:
            return True
    except Exception as e:
        return False
 #    print("data is ", data)
	# # if(len(data[0]))

 #    return True

def insertNewUser(mysql,newInputDict):

	# nameList.append(newInputDict["name"])
	# emailList.append(newInputDict["email"])
	# usernamesList.append(newInputDict["username"])
	# passwordList.append(newInputDict["password"])
    # query="INSERT INTO {0}register VALUES('{1}','{2}','{3}','{4}')".format(\
    #         newInputDict["name"],
    #         newInputDict["email"],
    #         newInputDict["username"],
    #         newInputDict["password"]
    #     )
    query = "Insert into register values ('" + newInputDict["name"] + "','" +\
    newInputDict["email"] + "','" +\
    newInputDict["username"] + "','" +\
    newInputDict["password"] + "'" +\
    ")"
    query1 = "Insert into Login values ('" + newInputDict["username"] + "','" +\
    newInputDict["password"] + "'" +\
    ")"
    print("query is ", query)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.execute(query1)
    conn.commit()
	# print("nameList is ",nameList)
	# print("emailList is ",emailList)
	# print("usernamesList is ",usernamesList)
	# print("passwordList is ",passwordList)

    return True
	
