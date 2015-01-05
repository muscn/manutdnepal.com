import dbsettings


class ContactSettings(dbsettings.Group):
    address = dbsettings.TextValue(required=False)
    phone = dbsettings.StringValue(required=False)
    fax = dbsettings.StringValue(required=False)
    email = dbsettings.StringValue(required=False)
    location_name = dbsettings.StringValue(required=False)
    latitude = dbsettings.StringValue(required=False)
    longitude = dbsettings.StringValue(required=False)


contact_settings = ContactSettings('Contact Settings')