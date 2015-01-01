import dbsettings


class MembershipSetting(dbsettings.Group):
    membership_fee = dbsettings.FloatValue('Membership Fee')


membership_settings = MembershipSetting('Membership Settings')