def roles_permitidos(roles):
    def check(user):
        return (
            user.is_authenticated and
            (user.is_superuser or user.groups.filter(name__in=roles).exists())
        )
    return check
