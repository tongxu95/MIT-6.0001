#MIT 6.0001 Introduction to Computer Science and Programming in Python, Problem Set 1b
#Function: Saving, with a raise
annual_salary=float(input('Enter your annual salary: '))
portion_saved=float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost=float(input('Enter the cost of your dream home: '))
semi_annual_raise=float(input('Enter the semi-annual raise, as a decimal: '))
portion_down_payment=0.25*total_cost
current_saving=0
r=0.04
i=0
while current_saving < portion_down_payment:
    current_saving += current_saving*r/12
    current_saving += annual_salary*portion_saved/12
    i+=1
    if i%6 == 0:
        annual_salary += annual_salary*semi_annual_raise
print('Number of months:', i)
