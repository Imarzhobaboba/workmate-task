import csv
import argparse
import tabulate

def is_numeric(value: str) -> bool:
    """Проверяю, можно ли сделать строку числом или нет"""
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def filter_data(data, args):
    for i in args.where:
        if i == '=':
            operator = '='
            column, value = (args.where).split('=')
            break
        if i == '<':
            operator = '<'
            column, value = (args.where).split('<')
            break
        if i == '>':
            column, value = (args.where).split('>')
            operator = '>'
            break
    filtered = []
    for row in data:
        row_value = row[column]
        
        if operator == '=':
            if str(row_value) == value:
                filtered.append(row)
        elif operator == '>':
            '''Проверяем, число ли это'''
            if is_numeric(row_value):
                if float(row_value) > float(value):
                    filtered.append(row)
            # Это условие выполняется, если значение это строка, а не число
            elif row_value > value:
                filtered.append(row)
        elif operator == '<':
            '''Проверяем, число ли это'''
            if is_numeric(row_value):
                if float(row_value) < float(value):
                    filtered.append(row)
            # Это условие выполняется, если значение это строка, а не число
            elif row_value < value:
                filtered.append(row)
    
    return filtered

def aggregate_data(data, args):
    column, aggregation = (args.aggregate).split('=')
    numeric_values = []
    for row in data:
        value = row[column]
        if is_numeric(value):
            numeric_values.append(float(value))
    
    if not numeric_values:
        return None
    
    result = {'column': column, 'aggregation': aggregation}
    
    if aggregation == 'avg':
        result['value'] = sum(numeric_values) / len(numeric_values)
    elif aggregation == 'min':
        result['value'] = min(numeric_values)
    elif aggregation == 'max':
        result['value'] = max(numeric_values)
    else:
        raise ValueError(f"Unknown aggregation operation: {aggregation}")
    
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-file", "--file", help="File path")
    parser.add_argument("-where", "--where", help="Filter by where")
    parser.add_argument("-aggregate", "--aggregate", help="Aggregate")

    args = parser.parse_args()
    try:
        with open(args.file, mode='r') as f:    
            csv_dict = list(csv.DictReader(f=f))
            if args.where:
                filtered_data = filter_data(csv_dict, args)
            else:
                filtered_data = csv_dict
            answer = tabulate.tabulate(filtered_data, headers="keys", tablefmt="grid")
            if args.aggregate:
                aggregated_data = aggregate_data(filtered_data, args)
                answer = tabulate.tabulate([[aggregated_data['value']]], headers=[aggregated_data["aggregation"]], tablefmt="grid")
                print(answer)
            else:
                print(answer)
    except Exception as e:
        print('Incorrect input')