import dbsettings


class MembershipSetting(dbsettings.Group):
    membership_fee = dbsettings.FloatValue('Membership Fee')
    enable_esewa = dbsettings.BooleanValue()


membership_settings = MembershipSetting('Membership Settings')