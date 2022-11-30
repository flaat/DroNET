class NaiveWiFiAdapter:

    def __init__(self):

        self.transmission_range = 50  # meters
        self.maximum_data_rate = 100  # KBytes/sec

    def to_network(self, data: bytes):
        """
        It receives data from the application level and put them into the medium
        after the proper encapsulation
        @param data:
        @return:
        """

        pass

    def from_network(self, data: bytes):

        pass