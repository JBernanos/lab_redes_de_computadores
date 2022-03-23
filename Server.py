import socket
import ast;
import json;

server_ip_address = "192.168.15.2";
server_port = 32016;

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM); 
server.bind((server_ip_address, server_port)); 

server.listen();
client, end = server.accept();

stop = False;
users = [];
with open('database.txt') as file:
    lines = [line.rstrip() for line in file]
    for i in range(len(lines)):
        line = lines[i].split(';');
        userDict = {
            "name": line[0],
            "age": line[1],
            "id": line[2]
        };
        users.append(userDict);

while stop != True:
    data = client.recv(1024).decode('utf-8');
    data = ast.literal_eval(data);

    if data["operation"] == "create":
        user_id = data["id"];
        isPresent = False;
        for i in range(len(users)):
            if users[i]["id"] == user_id:
                isPresent = True;

        if isPresent == False:        
            users.append(data);
            message = f"User with id {user_id} created!";
            message = message.encode('utf-8');
            client.send(message);
        else:
            message = f"Id already used!";
            message = message.encode('utf-8');
            client.send(message);


    elif data["operation"] == "update":
        user_id = data["user_id"];
        user_to_update = -1;
        for i in range(len(users)):
            if users[i]["id"] == user_id:
                user_to_update = i;
        if user_to_update != -1:
            users[i]["name"] = data["name"];
            users[i]["age"] = data["age"];
            message = f"User with id {user_id} updated!";
            message = message.encode('utf-8');
            client.send(message);
        else:
            message = "Cannot find user to update!";
            message = message.encode('utf-8');
            client.send(message);

    elif data["operation"] == "remove":
        user_id = data["user_id"];
        user_to_remove = -1;
        for i in range(len(users)):
            if users[i]["id"] == user_id:
                user_to_remove = i;
        if user_to_remove != -1:
            del users[user_to_remove];
            message = f"User with id {user_id} deleted!";
            message = message.encode('utf-8');
            client.send(message);

        else:
            message = "Cannot find user to delete!";
            message = message.encode('utf-8');
            client.send(message);

    elif data["operation"] == "search":
        user_id = data["user_id"];
        user_to_show = -1;
        for i in range(len(users)):
            if users[i]["id"] == user_id:
                user_to_show = i;
        if user_to_show != -1:
            user_to_string = users[user_to_show];
            user_to_string = json.dumps(user_to_string);
            user_to_string = user_to_string.encode('utf-8');
            client.send(user_to_string);
        else:
            message = ["Cannot find user!"];
            message = json.dumps(message);
            message = message.encode('utf-8');
            client.send(message);
    
    elif data["operation"] == "show":
        users_to_string = json.dumps(users);
        users_to_string = users_to_string.encode('utf-8');
        client.send(users_to_string);
                
    elif data["operation"] == "quit":
        stop = True;

with open('database.txt', 'w') as file:
    for user in users:
        file.write("%s;" % user["name"]);
        file.write("%s;" % user["age"]);
        file.write("%s;" % user["id"]);
        file.write("\n");

client.close();
server.close();