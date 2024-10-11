from graphclass import Drawing, simple_node_label, simple_list_label

drawing = Drawing()

def add_table(listname, listitems):
    label = simple_list_label(listname, listitems)
    drawing.add_item(listname, drawing.item_view(label, shape='plaintext'))

def add_item(text):
    drawing.add_item(text,
        node    = drawing.item_view(simple_node_label(text), style = 'filled'),
        cluster = drawing.item_view(simple_node_label(text), style = 'filled', fillcolor = "#add8e6"),
        point   = drawing.item_view("", shape='point', width='0.1')
    )
    return text

s1 = add_item("DataBase")

drawing.add_parent("Employees", "DataBase")
add_table("Employees", ["id", "first_name", "last_name", "position", "salary"])

drawing.add_parent("Departments", "DataBase")
add_table("Departments", ["id", "department_name", "manager_id"])

drawing.add_parent("Customers", "DataBase")
add_table("Customers", ["id", "first_name", "last_name", "address", "phone", "email"])

drawing.add_parent("Products", "DataBase")
add_table("Products", ["id", "name", "description", "price", "stock_quantity"])

drawing.add_parent("Orders", "DataBase")
add_table("Orders", ["id", "customer_id", "order_date", "order_amount", "status"])

drawing.add_parent("OrderDetails", "DataBase")
add_table("OrderDetails", ["order_id", "product_id", "quantity", "cost"])

drawing.add_link("Customers:id", "Orders:customer_id")
drawing.add_link("Products:id", "OrderDetails:product_id")
drawing.add_link("Orders:id", "OrderDetails:order_id")
drawing.add_link("Employees:id", "Departments:manager_id")

res = drawing.html("Demo")

with open('./src/Demo/Demo.html', 'w') as file:
    file.write(res)
