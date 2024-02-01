import rules

@rules.predicate
def is_todo_owner(user, todo):
    return user == todo.user_id