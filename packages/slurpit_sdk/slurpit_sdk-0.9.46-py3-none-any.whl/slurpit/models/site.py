from slurpit.models.basemodel import BaseModel

class Site(BaseModel):
    """
    This class represents a site.

    Args:
        id (int): Unique identifier for the site.
        sitename (str): Name of the site.
        description (str): Description of the site.
        street (str): Street of the site.
        number (str): Number of the site.
        zipcode (str): Zipcode of the site.
        city (str): City of the site.
        country (str): Country of the site.
        phonenumber (int): Phone number of the site.
        status (int): Status flag where 0 indicates enabled and 1 indicates disabled.
        longitude (str): Longitude of the site.
        latitude (str): Latitude of the site.
    """

    def __init__(
        self,
        id: int,
        sitename: str,
        description: str,
        street: str,
        number: str,
        zipcode: str,
        country: str,
        phonenumber: int,
        status: int,
        longitude: str,
        latitude: str,
        createddate: str = None,
        changeddate: str = None,
    ):
        self.id = int(id)
        self.sitename = sitename
        self.description = description
        self.street = street
        self.number = number
        self.zipcode = zipcode
        self.country = country
        self.phonenumber = phonenumber
        self.status = status
        self.longitude = longitude
        self.latitude = latitude
        self.createddate = createddate
        self.changeddate = changeddate