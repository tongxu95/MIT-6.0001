#MIT 6.0001 Introduction to Computer Science and Programming in Python, Problem Set 1c
#Function: Finding the right amount to save away； portion to save so that you will be able to 
#afford the down payment (25%) to a 1M dollar house in 3 years.
base_salary=float(input('Enter the starting salary: '))
semi_annual_raise=.07
r=0.04
total_cost=1000000
portion_down_payment=0.25*total_cost
epilson=100
low=0
high=100000
guess=round((low+high)/2)
num_guesses=0
maximum_saving=0
current_saving=0
annual_salary=base_salary
for i in range(1,37):
    maximum_saving += maximum_saving*r/12
    maximum_saving += annual_salary/12
    if i%6 == 0:
        annual_salary += annual_salary*semi_annual_raise
if maximum_saving < portion_down_payment:
    print('It is not possible to pay the down payment in three years.')
while abs(current_saving-portion_down_payment) >= epilson:
    current_saving=0
    annual_salary=base_salary
    for i in range(1,37):
        current_saving += current_saving*r/12
        current_saving += annual_salary*(guess/10000)/12
        if i%6 == 0:
            annual_salary += annual_salary*semi_annual_raise
    num_guesses += 1
    if current_saving>portion_down_payment:
        high=guess
    else:
        low=guess
    guess=round((low+high)/2)
print('best saving rate:', guess/10000)
print('Steps in bisection search:',num_guesses)

