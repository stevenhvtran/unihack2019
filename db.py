import pyrebase


class Db:
    def __init__(self):
        """ Initialises the database, and links db to firebase. """

        config = {
            "apiKey": "AIzaSyBwE0IwlvsrnzQ6mcFmq-F_opuWiA_YfhI",
            "authDomain": "unihack19-6452a.firebaseapp.com",
            "databaseURL": "https://unihack19-6452a.firebaseio.com",
            "storageBucket": "unihack19-6452a.appspot.com",
            "serviceAccount": "serviceAccountCredentials.json"
        }
        self.db = pyrebase.initialize_app(config).database()

    def get_traffic(self):
        """
        :return: Flattened list of live traffic information in Firebase
        """

        traffic_list = list()
        traffic_list.append(
            self.db.child("traffic").child("street_n").get().val())
        traffic_list.append(
            self.db.child("traffic").child("street_e").get().val())
        traffic_list.append(
            self.db.child("traffic").child("street_s").get().val())
        traffic_list.append(
            self.db.child("traffic").child("street_w").get().val())

        flat_traffic = [item for sublist in traffic_list for item in sublist]
        return flat_traffic

    def remove_traffic(self, street, ):
        self.db.child("traffic").child("")

    def add_event(self, eventNo, lights, cars):
        '''
           adds an event to the db, with light and car info provided. eventNo
           will be the tick number.
        '''
        self.db.child("traffic").child("live").child(eventNo).update({"lightConfig": lights})
        self.db.child("traffic").child("live").child(eventNo).update({"carsInfo": cars})
