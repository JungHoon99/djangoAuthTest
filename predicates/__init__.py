from rules.predicates import is_active, is_superuser
from .base_predicates import is_todo_owner
import rules

active_todo_owner = is_todo_owner & is_active
todo_can_view = is_active & is_todo_owner | is_superuser

rules.add_perm('can_view_todo', active_todo_owner)