import pyrebase


class Db:
    def __init__(self):
        '''
            initialises the database, and links db to firebase.
        '''
        config = {
            "apiKey": "AIzaSyBwE0IwlvsrnzQ6mcFmq-F_opuWiA_YfhI",
            "authDomain": "unihack19-6452a.firebaseapp.com",
            "databaseURL": "https://unihack19-6452a.firebaseio.com",
            "storageBucket": "unihack19-6452a.appspot.com",
            "serviceAccount": "serviceAccountCredentials.json"
        }
        self.db = pyrebase.initialize_app(config).database()

    def get_traffic(self):
        '''
            gets the traffic info as a nested loop from the live demo.
        '''
        query = dict(self.db.child("traffic").get().val())
        streets = ['street_n', 'street_e', 'street_s', 'street_w']
        traffic_list = [query[street] for street in streets]
        self.db.child('traffic').update({'street_n': [0, 0, 0],
                                        'street_e': [0, 0, 0],
                                        'street_s': [0, 0, 0],
                                        'street_w': [0, 0, 0]})

        flattened_traffic = [item for sublist in traffic_list for item in sublist]
        return flattened_traffic

    def remove_traffic(self, street, ):
        self.db.child("traffic").child("")

    def add_event(self, eventNo, lights, cars):
        '''
           adds an event to the db, with light and car info provided. eventNo
           will be the tick number.
        '''
        self.db.child("traffic").child("live").child(eventNo).update({"lightConfig": lights})
        self.db.child("traffic").child("live").child(eventNo).update({"carsInfo": cars})


db = Db()
print(db.get_traffic())