import re
from DatabaseHandler import DatabaseHandler
from datetime import datetime
import json
import math


class validation:
    def validate_registration(self, payload):
        name = payload['name']
        surname = payload['surname']
        username = payload['username']
        email = payload['email']
        password = payload['password']
        phone = payload['phone']
        # print(payload)
        if not name:
            return False, 'Name is empty'
        if not surname:
            return False, 'Surname is empty'
        if not username:
            return False, 'Username is empty'
        elif len(DatabaseHandler().data_modifier.read('client', f'username="{username}"')) > 0:
            return False, 'Username already exists'
        if not email:
            return False, 'Email  is empty'
        elif len(DatabaseHandler().data_modifier.read('client', f'email="{email}"')) > 0:
            return False, 'Email already exists'
        if len(password) < 8:
            return False, 'Password is empty'
        if not phone:
            return False, 'Phone is empty'
        return True, ''

    def validate_login(self, payload):
        username = payload['username']
        password = payload['password']

        if not username:
            return False, 'username'
        if len(password) < 8:
            return False, 'password'

        return True, ''

    def validate_booking(self, payload):
        # print(payload)
        message = ''

        city = payload['city']
        checkIn = payload['checkIn']
        checkOut = payload['checkOut']
        type = payload['type']
        count = payload['count']

        # if city in city List:
        if not len(city):
            message += 'City is incorrect'
        if len(checkIn) != 10 or len(checkOut) != 10:
            message += 'Date is incorrect'
        if type not in ['standard', 'double', 'family', 'separate']:
            message += 'Type is incorrect'
        if count not in range(2, 5):
            message += 'Count is incorrect'
        # print(city, checkIn, checkOut, type, count)
        return True

    def validate_date(self, in1, in2):
        # Convert the date strings to datetime objects
        # date1 checkIn
        # date1 checkOut
        date1 = datetime.strptime(in1, '%Y-%m-%d')
        date2 = datetime.strptime(in2, '%Y-%m-%d')
        difference = (date2 - date1).days
        if difference:
            return difference
        else:
            return None

    def calculate_pricing(self, username='lizard', booking_id=16):
        db_client_id = DatabaseHandler().data_modifier.read('client', f'username="{username}"', 'ClientID')[0][0]
        db_booking = DatabaseHandler().data_modifier.read_as_dict('booking',
                                                                  f'client_ClientID={db_client_id} AND BookingID={booking_id}')[
            0]
        db_booking_id = db_booking['BookingID']
        db_rooms = DatabaseHandler().data_modifier.read_as_dict('room', f'booking_BookingID="{db_booking_id}"')
        db_hotel_id = db_rooms[0]['hotel_HotelID']
        hotel = DatabaseHandler().data_modifier.read_as_dict('hotel', f'HotelID={db_hotel_id}')

        # print(db_client_id)
        # print(db_booking_id)
        # print(db_hotel_id)
        # print(db_rooms)
        # print(hotel)

        # rooms = DatabaseHandler().data_modifier.read_as_dict('room', f'booking_BookingID="{lastBookingId}"')
        # print(rooms)

        month = db_booking['CheckInDate'].month
        if 3 < month < 9:
            season = 'PeakPricing'
        else:
            season = 'OffPeakPricing'

        db = DatabaseHandler()
        # city = 'Belfast'

        stay_duration = (db_booking['CheckOutDate'] - db_booking['CheckInDate']).days
        checkIn = db_booking['CheckInDate']
        datebooked = db_booking['BookingCreationDate']
        advancedBooking = (checkIn - datebooked).days
        discount = 0

        # print(advancedBooking)
        if 79 < int(advancedBooking) < 90:
            discount = 0.3
        elif 59 < int(advancedBooking) < 79:
            discount = 0.2
        elif 45 < int(advancedBooking) < 59:
            discount = 0.1

        rooms = {}
        for i in range(len(db_rooms)):
            rooms["Room" + str(i + 1)] = {'type': db_rooms[i]['Type']}

        # print(hotel)

        receipt = {}
        standardRoomCount = 0
        totalCost = 0

        for i in range(len(rooms)):
            # print('iter ', i)
            type_rate = {'standard': 1, 'double': 1.2, 'family': 1.5}
            standardRoomPrice = db.data_modifier.read('hotel', f'HotelID="{db_hotel_id}"', season)[0][0]
            type_pricing = type_rate[rooms['Room' + str(i + 1)]['type']] * standardRoomPrice
            extra_room_fee = 0
            if 'standard' in rooms['Room' + str(i + 1)]['type']:
                standardRoomCount += 1
                if standardRoomCount > 1:  # 10% tax
                    extra_room_fee = 0.1
                    standardRoomCount = 0

            total = type_pricing * stay_duration
            total = math.floor(total * (1 + extra_room_fee))
            totalCost += total
            if total % 1 == 0:
                total = int(total)
            receipt['Room' + str(i + 1)] = {'total_price': total, 'room_price': standardRoomPrice,
                                            'type_rate': type_rate[rooms['Room' + str(i + 1)]['type']],
                                            'stay_duration': stay_duration,
                                            'extra_standard_room_fee': extra_room_fee}
        receipt['advanced_booking_discount'] = discount
        total = totalCost - totalCost * discount
        if total % 1 == 0:
            receipt['Total'] = int(total)
        else:
            receipt['Total'] = total
        # print(json.dumps(receipt, indent=2))
        # print(receipt)
        return receipt
