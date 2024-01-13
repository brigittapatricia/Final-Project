import statistics

class Employee(object):
    def __init__(self, id=0, name='', code='', total_sales=0, utilization=0, hours_worked=0, base_pay=0, bonus=0):
        self.__emp_id = id
        self.__emp_name = name
        self.__emp_code = code
        self.__emp_total_sales = total_sales
        self.__emp_utilization = utilization
        self.emp_hours_worked = hours_worked
        self.__emp_base_pay = base_pay
        self._emp_bonus = bonus

    def get_id(self):
        return self.__emp_id

    def set_id(self, new_id):
        if len(str(new_id)) == 3:
            self.__emp_id = new_id

    new_id = property(get_id, set_id)

    def get_name(self):
        return self.__emp_name

    def get_code(self):
        return self.__emp_code

    def get_total_sales(self):
        return self.__emp_total_sales

    def get_base_pay(self):
        return self.__emp_base_pay

    def utilization_rate(self):
        return round((self.emp_hours_worked / 2000) * 100, 2)

    def print_data(self):
        print(f"ID: {self.get_id()}")
        print(f"Name: {self.get_name()}")
        print(f"Utilization: {self.utilization_rate()}")
        print(f"Base pay: ${int(self.get_base_pay()):,}")
        print(f"Bonus: ${self.__emp_bonus:,}")
        print("===HIDDEN DATA===")
        print(f"Hours worked: {self.emp_hours_worked:,}")

class Consultant(Employee):
    bonus_cap = 50000

    def __init__(self, id=0, name='', code='', total_sales=0, utilization=0, evaluation_score=0, hours_worked=0, base_pay=0, bonus=0, bonus_percentage=0):
        super().__init__(id, name, code, total_sales, utilization, hours_worked, base_pay, bonus)
        self.__consultant_evaluation_score = evaluation_score
        self.__consultant_bonus_rate = bonus_percentage

    def get_evaluation_score(self):
        return self.__consultant_evaluation_score

    def get_bonus_rate(self):
        return self.__consultant_bonus_rate

    def set_bonus_rate(self, new_bonus):
        self.__consultant_bonus_rate = new_bonus

    new_bonus = property(get_bonus_rate, set_bonus_rate)

    def calc_bonus(self, bonus_rate):
        print(f"Calculating bonus for Consultant {self.get_id()} with rate {bonus_rate}") # print statements to debug
        if self.utilization_rate() > 60 and self.get_evaluation_score() >= 75:
            calculated_bonus = round(float(self.get_base_pay()) * bonus_rate)
            final_bonus = min(calculated_bonus, Consultant.bonus_cap)
            print(f"Calculated bonus: {final_bonus}")
            return final_bonus
        else:
            print("Not eligible for bonus.")
            return 0

    def open_evaluation(self):
        punctuation_chars = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        POSITIVE_KEYWORDS = ['excellent', 'good', 'prompt', 'dependable']
        NEGATIVE_KEYWORDS = ['poor', 'error', 'unreliable', 'late']
        evaluate = {}
        with open('evaluation.txt', 'r') as file:
            for line in file:
                parts = line.strip().split('#')
                if len(parts) == 2:
                    id, text = parts
                    text = ''.join([char for char in text if char not in punctuation_chars])
                    positive_count = 0
                    negative_count = 0
                    for word in text.split():
                        word_lower = word.lower()
                        if word_lower in POSITIVE_KEYWORDS:
                            positive_count += 1
                        elif word_lower in NEGATIVE_KEYWORDS:
                            negative_count += 1
                    total_keywords = positive_count + negative_count
                    evaluate[id] = (positive_count / total_keywords) * 100 if total_keywords > 0 else 50
        return evaluate

class Director(Employee):
    bonus_cap = 150000

    def __init__(self, id=0, name='', code='', total_sales=0, utilization=0, new_sales=0, hours_worked=0, base_pay=0, bonus=0, bonus_percentage=0):
        super().__init__(id, name, code, total_sales, utilization, hours_worked, base_pay, bonus)
        self.__director_new_sales = new_sales
        self.__director_bonus_rate = bonus_percentage

    def get_bonus_rate(self):
        return self.__director_bonus_rate

    def set_bonus_rate(self, new_bonus):
        self.__director_bonus_rate = new_bonus

    new_bonus = property(get_bonus_rate, set_bonus_rate)

    def get_new_sales(self):
        return self.__director_new_sales

    def calc_bonus(self, bonus_rate):
        print(f"Calculating bonus for Director {self.get_id()} with rate {bonus_rate}") # print statements to debug
        if self.utilization_rate() > 60:
            calculated_bonus = round(self.get_total_sales() * bonus_rate)
            final_bonus = min(calculated_bonus, Director.bonus_cap)
            print(f"Calculated bonus: {final_bonus}")
            return final_bonus
        else:
            print("Not eligible for bonus.")
            return 0

def median(dictionary):
    values = sorted(dictionary.values())
    n = len(values)
    if n % 2 == 1:
        return values[n // 2]
    else:
        return (values[n // 2 - 1] + values[n // 2]) / 2

def standard_deviation(dictionary):
    values = list(dictionary.values())
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance ** 0.5

def sales():
    sales_dic = {}
    with open('sales.txt', 'r') as file:
        for line in file:
            employee_id, total_sales = map(str.strip, line.split(','))
            sales_dic[employee_id] = int(total_sales)
    return sales_dic

def hours_worked():
    hours_dic = {}
    with open('timesheet.txt', 'r') as file:
        for line in file:
            employee_id, hours = map(str.strip, line.split(','))
            hours_dic[employee_id] = hours_dic.get(employee_id, 0) + int(hours)
    return hours_dic

def beginning_data():
    begin_dic = {}
    with open('emp_beg_yr.txt') as file:
        next(file)  # Skip header
        for line in file:
            employee_id, last_name, first_name, job_code, base_pay = map(str.strip, line.split(','))
            begin_dic[employee_id] = Employee(id=employee_id, name=f"{first_name} {last_name}", code=job_code, base_pay=float(base_pay))
    return begin_dic

def sum_bonus(big_dic, bonus_rate):
    total_bonus = 0
    for emp_id, employee in big_dic.items():
        if isinstance(employee, Consultant) or isinstance(employee, Director):
            bonus = employee.calc_bonus(bonus_rate)
            employee._emp_bonus = bonus  # Update the protected attribute
            total_bonus += bonus
    return total_bonus

def write_final_data(big_dic):
    with open('FINAL_emp_end_yr.txt', 'w') as file:
        file.write("ID,LastName,FirstName,JobCode,BasePay,Utilization,Evaluation/Sales,Bonus\n")
        for emp_id, employee in big_dic.items():
            name_split = employee.get_name().split()
            last_name = name_split[1] if len(name_split) > 1 else ""
            first_name = name_split[0] if name_split else ""
            evaluation_or_sales = employee.get_evaluation_score() if isinstance(employee, Consultant) else employee.get_total_sales()
            line = f"{employee.get_id()},{last_name},{first_name},{employee.get_code()},{employee.get_base_pay()},{employee.utilization_rate()},{evaluation_or_sales},{employee._emp_bonus}\n"
            file.write(line)

def open_files():
    big_dic = beginning_data()
    sales_dic = sales()
    hours_dic = hours_worked()

    # Update big_dic with sales and hours data
    for emp_id in big_dic:
        big_dic[emp_id].__emp_total_sales = sales_dic.get(emp_id, 0)
        big_dic[emp_id].emp_hours_worked = hours_dic.get(emp_id, 0)

    while True:
        try:
            entered_rate = float(input("Enter bonus rate (0-100): ")) / 100
            if 0 <= entered_rate <= 1:
                total_bonus = sum_bonus(big_dic, entered_rate)
                print(f"Total bonus at {entered_rate * 100}% rate: ${total_bonus:,}")
            else:
                print("Please enter a rate between 0 and 100.")
        except ValueError:
            print("Please enter a numeric value.")

        finalize = input("Finalize this rate? (y/n): ").lower()
        if finalize == 'y':
            sum_bonus(big_dic, entered_rate)  # Recalculate bonuses with final rate
            write_final_data(big_dic)
            break

    return big_dic

def get_employee_info(big_dic):
    ask_id = input("Employee ID: ")
    while ask_id not in big_dic:
        ask_id = input("Unavailable. Enter a new one: ")
    
    employee = big_dic[ask_id]
    job_code = employee.get_code()

    if job_code == "C":
        employee.print_data()
    elif job_code == "D":
        employee.print_data()

    def print_analytics(dictionary):
        values = list(dictionary.values())
        if values:
            print(f"Number of data points: {len(values)}")
            print(f"Minimum: {min(values)}")
            print(f"Maximum: {max(values)}")
            print(f"Median: {statistics.median(values)}")
            print(f"Mean: {statistics.mean(values)}")
            print(f"Standard Deviation: {statistics.stdev(values)}")
        else:
            print("No data available.")
    
    def max_utilization_and_sales(big_dic, utilization_dic, sales_dic):
        if utilization_dic:
            max_utilization_id = max(utilization_dic, key=utilization_dic.get)
            print(f"Employee with Max Utilization: {max_utilization_id} - {big_dic[max_utilization_id].get_name()}")
        
        if sales_dic:
            max_sales_id = max(sales_dic, key=sales_dic.get)
            print(f"Employee with Max Sales: {max_sales_id} - {big_dic[max_sales_id].get_name()}")
    
    def poor_performance(big_dic, evaluation_dic):
        for emp_id, employee in big_dic.items():
            if isinstance(employee, Consultant):
                evaluation_score = evaluation_dic.get(emp_id, 0)
                if employee.utilization_rate() < 60 or evaluation_score < 75:
                    print(f"Employee {emp_id} - {employee.get_name()} is underperforming.")
    
    def error_file(find_in_sales_list, find_in_timesheet_list, find_in_evaluation_list, very_new_list):
        with open("error.txt", "w") as file:
            for employee_id in find_in_sales_list:
                if employee_id not in very_new_list:
                    file.write(f"{employee_id} in sales.txt but not in beginning data\n")
            for employee_id in find_in_timesheet_list:
                if employee_id not in very_new_list:
                    file.write(f"{employee_id} in timesheet.txt but not in beginning data\n")
            for employee_id in find_in_evaluation_list:
                if employee_id not in very_new_list:
                    file.write(f"{employee_id} in evaluation.txt but not in beginning data\n")


    total_sales = sales()
    total_utilization = hours_worked()
    first_data = beginning_data()
    return first_data, total_sales, total_utilization

first_data = open_files()

