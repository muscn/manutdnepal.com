import dbsettings


class MembershipSetting(dbsettings.Group):
    membership_fee = dbsettings.FloatValue('Membership Fee')
    enable_esewa = dbsettings.BooleanValue()
    welcome_letter_content = dbsettings.TextValue()


membership_settings = MembershipSetting('Membership Settings')