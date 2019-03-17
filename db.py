import pyrebase


class Db:
    def __init__(self):
        """ Initialises the database, and links db to firebase. """

        config = {
            'apiKey': 'AIzaSyBwE0IwlvsrnzQ6mcFmq-F_opuWiA_YfhI',
            'authDomain': 'unihack19-6452a.firebaseapp.com',
            'databaseURL': 'https://unihack19-6452a.firebaseio.com',
            'storageBucket': 'unihack19-6452a.appspot.com',
            'serviceAccount': 'serviceAccountCredentials.json'
        }
        self.db = pyrebase.initialize_app(config).database()

    def get_traffic(self):
        """
        :return: Flattened list of live traffic information in Firebase
        """
        query = dict(self.db.child('traffic').get().val())
        streets = ['street_n', 'street_e', 'street_s', 'street_w']
        traffic_list = [query[street] for street in streets]
        self.db.child('traffic').update({'street_n': [0, 0, 0],
                                         'street_e': [0, 0, 0],
                                         'street_s': [0, 0, 0],
                                         'street_w': [0, 0, 0]})

        flattened_traffic = [item for sublist in traffic_list for item in sublist]
        return flattened_traffic

    def add_event(self, lights, cars):
        """
           Adds an event to the db, with light and car info provided. eventNo
           will be the tick number.
        """
        live = self.db.child('traffic').child('live').get().val()
        if not live:
            live = []
        live.append({'light_config': lights, 'cars': cars})
        self.db.child('traffic').update({'live': live})

    def reset_events(self):
        self.db.child('traffic').update({'live': []})
