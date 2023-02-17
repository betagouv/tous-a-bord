def belongs_to_group(group_name):
    return lambda user : user.groups.filter(name=group_name).exists()
