import mysql.connector

from backend.DatabaseControl import DatabaseControl
from flask import Flask
from flask_bcrypt import Bcrypt


class DatabaseHandler:
    app = Flask(__name__)
    app.secret_key = 'SECRET_KEY'

    def __init__(self):
        self.data_modifier = DatabaseControl(host='localhost', user='root', password='Prosto123!',
                                             database='hotel_management')

    def create_room(self, roomNumber: int, type: str, internet: str, tv: str, miniBar: str, breakfast: str,
                    hotel_HotelID: int, booking_BookingID: int, booking_client_ClientID: int):
        room = {
            'RoomNumber': roomNumber,
            'Type': type,
            'Internet': internet,
            'TV': tv,
            'MiniBar': miniBar,
            'Breakfast': breakfast,
            'hotel_HotelID': hotel_HotelID,
            'booking_BookingID': booking_BookingID,
            'booking_client_ClientID': booking_client_ClientID
        }
        return self.data_modifier.create('room', room)

    def create_booking(self, bookingCreationDate: str, checkInDate: str, checkOutDate: str, status: str, cost: float,
                       CancellationFee: float,
                       fk_clientId: int):
        # status (Cancelled, Complete, Pending)
        booking = {
            'bookingCreationDate': bookingCreationDate,
            'checkInDate': checkInDate,
            'checkOutDate': checkOutDate,
            'status': status,
            'cost': cost,
            'CancellationFee': CancellationFee,
            'client_ClientID': fk_clientId,
        }
        return self.data_modifier.create('booking', booking)

    def create_client(self, name='', surname='', email='', username='', password='', phone=''):
        client = {
            'name': str(name),
            'surname': str(surname),
            'email': str(email),
            'username': str(username),
            'password': str(password),
            'phone': str(phone)
        }
        self.data_modifier.create('client', client)

    def create_admin(self, name='', surname='', username='', password='', email=''):
        admin = {
            'name': str(name),
            'surname': str(surname),
            'username': str(username),
            'password': str(password),
            'email': str(email)
        }
        self.data_modifier.create('admin', admin)

    def create_hotel(self, city, capacity, peak_pricing, off_peak_pricing):
        hotel = {
            'Name': f'WH-{city}',
            'City': str(city),
            'RoomCapacity': str(capacity),
            'PeakPricing': peak_pricing,
            'OffPeakPricing': off_peak_pricing,
            'SingleRoomAvailability': str(0.3 * int(capacity)),
            'DoubleRoomAvailability': str(0.5 * int(capacity)),
            'FamilyRoomAvailability': str(0.2 * int(capacity))}
        self.data_modifier.create('hotel', hotel)

    # deletes all table data, and resets id value
    def delete_table(self, table_name):
        self.data_modifier.delete(table_name, '1=1')
        self.data_modifier.resetIncrement(table_name, 1)

    def exit_sql(self):
        del self.data_modifier

    def upload_hotel_list(self, table_name):
        with open(table_name, 'r') as f:
            for i in f:
                a = i.replace('\n', '').split(', ')
                self.create_hotel(a[0], a[1], a[2], a[3])

        # upload_hotel_list_table('table.txt')

    def display_data(self):
        for i in self.data_modifier.all_tables():
            # print(f'Table: {i[0]}')
            data = self.data_modifier.read(i[0])
            # print(data)
            features = self.data_modifier.features(i[0])
            if len(features) > 0:
                print(features, end='\n')
        return

    def field_exists(self, username, table='client'):
        if len(self.data_modifier.read(table, f'username="{username}"')) > 0:
            return True
        return False

    def get_table_names(self):
        names = []
        for i in DatabaseHandler().data_modifier.all_tables():
            names.append(i[0])
            print(i[0])
        return names

    def reinitialize_database(self):
        db = DatabaseHandler()
        db.delete_table('admin')
        db.delete_table('room')
        db.delete_table('booking')
        db.delete_table('client')
        db.delete_table('hotel')

        bcrypt = Bcrypt(self.app)
        db.upload_hotel_list('table.txt')

        d.create_client('Jardani', 'Jovonov', 'jonathanJ@outlook.com', 'Jardani1',
                        bcrypt.generate_password_hash('thisIsDaisy').decode('utf-8'), '+37125509477')
        d.create_client('Liam', 'Morgan', 'liamMorgann@gmail.com', 'liamM1',
                        bcrypt.generate_password_hash('realPass1').decode('utf-8'),
                        '+7125509477')
        d.create_admin('Alex', 'Jones', 'newAcc1', bcrypt.generate_password_hash('lxyz2Akl').decode('utf-8'),
                       'a123personal@gmail.com', )


d = DatabaseHandler()

# restart database data, to make testing easier
# d.reinitialize_database()
# d.display_data()

# upload hotel data from brief
# DatabaseHandler().upload_hotel_list('table.txt')

d.exit_sql()

# CRUD functionality
# new_client_id = self.data_modifier.create('client',user1)
# clients = self.data_modifier.read('client')
# self.data_modifier.update('client', {'address': '456 Elm St'}, 'id = 1')
# self.data_modifier.delete('client', 'id = 1')

# DELETE all table data with resetting id
# self.data_modifier.delete('hotel','1=1')
# self.data_modifier.resetIncrement('hotel', 1)
