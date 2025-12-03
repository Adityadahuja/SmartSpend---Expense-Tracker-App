from datetime import datetime

def merge_sort_expenses(expenses, key='date', reverse=False):
    """
    Sorts a list of Expense objects using Merge Sort.
    :param expenses: List of Expense objects
    :param key: Attribute to sort by ('date' or 'amount')
    :param reverse: Boolean to sort in descending order
    :return: Sorted list of Expense objects
    """
    if len(expenses) <= 1:
        return expenses

    mid = len(expenses) // 2
    left_half = merge_sort_expenses(expenses[:mid], key, reverse)
    right_half = merge_sort_expenses(expenses[mid:], key, reverse)

    return _merge(left_half, right_half, key, reverse)

def _merge(left, right, key, reverse):
    sorted_list = []
    i = j = 0

    while i < len(left) and j < len(right):
        val_left = getattr(left[i], key)
        val_right = getattr(right[j], key)

        if reverse:
            condition = val_left > val_right
        else:
            condition = val_left < val_right

        if condition:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list

def binary_search_date(expenses, target_date):
    """
    Searches for expenses on a specific date using Binary Search.
    Assumes expenses are sorted by date.
    :param expenses: Sorted list of Expense objects
    :param target_date: datetime.date object or string 'YYYY-MM-DD'
    :return: List of expenses on that date
    """
    if not expenses:
        return []

    # Ensure target_date is a date object for comparison
    if isinstance(target_date, str):
        target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
    elif isinstance(target_date, datetime):
        target_date = target_date.date()

    low = 0
    high = len(expenses) - 1
    found_index = -1

    while low <= high:
        mid = (low + high) // 2
        mid_date = expenses[mid].date.date()

        if mid_date == target_date:
            found_index = mid
            break
        elif mid_date < target_date:
            low = mid + 1
        else:
            high = mid - 1

    if found_index == -1:
        return []

    # Since there might be multiple expenses on the same date, expand left and right
    result = [expenses[found_index]]
    
    # Expand left
    i = found_index - 1
    while i >= 0 and expenses[i].date.date() == target_date:
        result.insert(0, expenses[i])
        i -= 1
        
    # Expand right
    i = found_index + 1
    while i < len(expenses) and expenses[i].date.date() == target_date:
        result.append(expenses[i])
        i += 1

    return result

def aggregate_by_category(expenses):
    """
    Aggregates expenses by category using a Hash Map (Dictionary).
    :param expenses: List of Expense objects
    :return: Dictionary {category_name: total_amount}
    """
    category_totals = {}
    
    for expense in expenses:
        cat_name = expense.category.name if expense.category else 'Uncategorized'
        if cat_name in category_totals:
            category_totals[cat_name] += expense.amount
        else:
            category_totals[cat_name] = expense.amount
            
    return category_totals

def compute_daily_prefix_sum(expenses):
    """
    Computes daily cumulative spending using Prefix Sum.
    Assumes expenses are sorted by date.
    :param expenses: List of Expense objects
    :return: List of tuples (date, daily_total, cumulative_total)
    """
    if not expenses:
        return []

    # First, aggregate by day to handle multiple expenses per day
    daily_map = {}
    for expense in expenses:
        day = expense.date.date()
        daily_map[day] = daily_map.get(day, 0) + expense.amount
    
    # Sort days
    sorted_days = sorted(daily_map.keys())
    
    result = []
    current_cumulative = 0
    
    for day in sorted_days:
        daily_total = daily_map[day]
        current_cumulative += daily_total
        result.append({
            'date': day.strftime('%Y-%m-%d'),
            'daily_total': daily_total,
            'cumulative_total': current_cumulative
        })
        
    return result
