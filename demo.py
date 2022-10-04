from transit_mapper import TransitMapper


def walking_isochrones_from_IDEO_office():
    walking_mapper = TransitMapper()
    address = "626 W Jackson Blvd, Chicago IL"
    trip_times=[45, 30, 15]
    walking_mapper.walking_isochrone(address=address, trip_times=trip_times)


if __name__ == "__main__":
    # data_directory = "data/"
    # chicago_mapper = TransitMapper(
    #     data_directory=data_directory, 
    #     city="Chicago, Illinois")

    walking_isochrones_from_IDEO_office()
