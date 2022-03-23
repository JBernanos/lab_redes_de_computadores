import socket;
import json
  
server_ip_address = "192.168.15.2";
server_port = 32016;

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
client.connect((server_ip_address, server_port));

stop = False;

while stop != True:
    print("=============================");
    print("1-Cadastrar Cliente \n2-Atualizar Registro \n3-Excluir Registro \n4-Buscar Registro \n5-Listar Registros \n6-Sair");
    option = input("Escolha uma opção: ");
    print("=============================");

    if option == "1":
        user = {
            "operation": "create",
            "name": "X",
            "age": "0",
            "id": "01"
        };
        name = input("Informe o nome: ");
        user["name"] = name;
        age = input("Informe a idade: ");
        user["age"] = age;
        user_id = input("Informe o id: ");
        user["id"] = user_id;
        
        user = str(user).encode('utf-8');
        client.send(user);
        data = client.recv(1024).decode('utf-8');
        print(data);

    elif option == "2":
        user_id = input("Informe o ID do usuário que deseja atualizar: ");
        user = {
            "operation": "update",
            "name": "X",
            "age": "0",
            "user_id": user_id
        };

        name = input("Informe o nome: ");
        user["name"] = name;
        age = input("Informe a idade: ");
        user["age"] = age;

        user = str(user).encode('utf-8');
        client.send(user);
        data = client.recv(1024).decode('utf-8');
        print(data);

    elif option == "3":
        user_id = input("Informe o ID do usuário que deseja remover: ");
        data = {
            "operation": "remove",
            "user_id": user_id
        };

        data = str(data).encode('utf-8');
        client.send(data);
        data = client.recv(1024).decode('utf-8');
        print(data);

    elif option == "4":
        user_id = input("Informe o ID do usuário que deseja pesquisar: ");
        data = {
            "operation": "search",
            "user_id": user_id
        };

        data = str(data).encode('utf-8');
        client.send(data);

        user = client.recv(1024).decode('utf-8');
        user = json.loads(user);
        if type(user) == list:
            print(user[0]);
        else:
            print("ID -> ", user["id"]);
            print("Name -> ", user["name"]);
            print("Age -> ", user["age"]);

    elif option == "5":
        data = {
            "operation": "show"
        };

        data = str(data).encode('utf-8');
        client.send(data);

        users = client.recv(1024).decode('utf-8');
        users = json.loads(users);

        if len(users) > 0:
            for i in range(len(users)):
                print("=============================");
                print("ID -> ", users[i]["id"]);
                print("Name -> ", users[i]["name"]);
                print("Age -> ", users[i]["age"]);
        else:
            print("No users to show!");

    elif option == "6":
        data = {
            "operation": "quit"
        };

        data = str(data).encode('utf-8');
        client.send(data);
        stop = True;

client.close();