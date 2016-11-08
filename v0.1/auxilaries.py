
def get_label(settings, label, units):
    string = []
    if label in settings.keys():
        string.append(settings[label])
    if units in settings.keys():
        string.append('[' + settings[units] + ']')
    string = ' '.join(string)
    if string == '':
        raise KeyError
    else:
        return string
