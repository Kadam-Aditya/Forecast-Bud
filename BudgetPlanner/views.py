from datetime import datetime
from itertools import count
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Expense
from .models import ReportDate
from .models import AiReportDate
from .models import AiReportDateM
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import base64
import io
import pandas as pd
from datetime import timedelta
from matplotlib.backends.backend_agg import FigureCanvasAgg
import joblib
from joblib import dump, load


def calculate_total_expenses(user, start_date, end_date):
    try:
        # Filter expenses based on the user and date range
        expenses = Expense.objects.filter(owner=user, date__range=[start_date, end_date])

        # Print the SQL query (optional)
        print(expenses.query)

        # Calculate the total sum of expenses
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        return total_expenses
    except Exception as e:
        # Handle exceptions as needed (e.g., logging, returning a default value)
        print(f"Error calculating total expenses: {e}")
        return 0
    

def calculate_expenses_by_category(user, start_date, end_date):
    try:
        # Filter expenses based on the user and date range
        expenses = Expense.objects.filter(owner=user, date__range=[start_date, end_date])

        # Calculate total expenses for each category
        expenses_by_category = expenses.values('category').annotate(total_expenses=Sum('amount'))

        # Create a dictionary to store results
        result = {entry['category']: entry['total_expenses'] for entry in expenses_by_category}

        return result
    except Exception as e:
        # Handle exceptions as needed (e.g., logging, returning a default value)
        print(f"Error calculating expenses by category: {e}")
        return {}


# views.py
from .models import ReportDate

def saved_budgets_view1(request):
    if request.method == 'POST':
        budget_id = request.POST.get('budget_id')  # Assuming you have a hidden field in your form for budget_id
        budget = ReportDate.objects.get(id=budget_id)  # Retrieve the budget from the database

        start_date1 = budget.start_date
        end_date1 = budget.end_date
        budget_title = budget.budget_title
        education_budget = budget.education_budget
        medical_budget = budget.medical_budget
        food_budget = budget.food_budget
        entertainment_budget = budget.entertainment_budget
        transport_budget = budget.transport_budget
        personal_care_budget = budget.personal_care_budget
        housing_bills_budget = budget.housing_bills_budget

        total_expenses = calculate_total_expenses(request.user, start_date1, end_date1)
        budget_remaining = budget.total_budget - total_expenses
        expenses_by_category = calculate_expenses_by_category(request.user, start_date1, end_date1)

        return render(request, 'Budget Planner/budget2.html', {
            'total_expenses': total_expenses,
            'start_date': start_date1,
            'end_date': end_date1,
            'budget_remaining': budget_remaining,
            'total_budget': budget.total_budget,
            'expenses_by_category': expenses_by_category,
            'budget_title': budget_title,
            'education_budget': education_budget,
            'medical_budget': medical_budget,
            'food_budget': food_budget,
            'entertainment_budget': entertainment_budget,
            'transport_budget': transport_budget,
            'personal_care_budget': personal_care_budget,
            'housing_bills_budget': housing_bills_budget,
        })
    
    return render(request, 'Budget Planner/budget.html')


def ai_saved_budgets_view(request):
        user = request.user
        ai_report_data = AiReportDate.objects.filter(user=user).first()  

        if ai_report_data is None:
        # If no saved budget found, return an error message or redirect
            return render(request, 'Budget Planner/ai_budget.html', {'error_message': 'No saved budget found for this user. First generate a budget.'})

        start_date1 = ai_report_data.start_date
        end_date1 = ai_report_data.end_date
        education_budget = ai_report_data.education_budget
        medical_budget = ai_report_data.medical_budget
        food_budget = ai_report_data.food_budget
        entertainment_budget = ai_report_data.entertainment_budget
        transport_budget = ai_report_data.transport_budget
        personal_care_budget = ai_report_data.personal_care_budget
        housing_bills_budget = ai_report_data.housing_bills_budget
        print(education_budget)

        total_expenses = calculate_total_expenses(request.user, start_date1, end_date1)
        budget_remaining = ai_report_data.total_weekly_budget - total_expenses
        expenses_by_category = calculate_expenses_by_category(request.user, start_date1, end_date1)

        return render(request, 'Budget Planner/saved_ai_weekly_result.html', {
            'total_expenses': total_expenses,
            'start_date': start_date1,
            'end_date': end_date1,
            'budget_remaining': budget_remaining,
            'total_weekly_budget': ai_report_data.total_weekly_budget,
            'expenses_by_category': expenses_by_category,
            'education_budget': education_budget,
            'medical_budget': medical_budget,
            'food_budget': food_budget,
            'entertainment_budget': entertainment_budget,
            'transport_budget': transport_budget,
            'personal_care_budget': personal_care_budget,
            'housing_bills_budget': housing_bills_budget,
        })


def ai_saved_budgets_view_m(request):
        user = request.user
        ai_report_data = AiReportDateM.objects.filter(user=user).first()  

        if ai_report_data is None:
        # If no saved budget found, return an error message or redirect
            return render(request, 'Budget Planner/ai_budget.html', {'error_message': 'No saved budget found for this user. First generate a budget.'})

        start_date1 = ai_report_data.start_date
        end_date1 = ai_report_data.end_date
        education_budget = ai_report_data.education_budget
        medical_budget = ai_report_data.medical_budget
        food_budget = ai_report_data.food_budget
        entertainment_budget = ai_report_data.entertainment_budget
        transport_budget = ai_report_data.transport_budget
        personal_care_budget = ai_report_data.personal_care_budget
        housing_bills_budget = ai_report_data.housing_bills_budget

        total_expenses = calculate_total_expenses(request.user, start_date1, end_date1)
        budget_remaining = ai_report_data.total_monthly_budget - total_expenses
        expenses_by_category = calculate_expenses_by_category(request.user, start_date1, end_date1)

        return render(request, 'Budget Planner/saved_ai_monthly_result.html', {
            'total_expenses': total_expenses,
            'start_date': start_date1,
            'end_date': end_date1,
            'budget_remaining': budget_remaining,
            'total_monthly_budget': ai_report_data.total_monthly_budget,
            'expenses_by_category': expenses_by_category,
            'education_budget': education_budget,
            'medical_budget': medical_budget,
            'food_budget': food_budget,
            'entertainment_budget': entertainment_budget,
            'transport_budget': transport_budget,
            'personal_care_budget': personal_care_budget,
            'housing_bills_budget': housing_bills_budget,
        })

def generate_report_view(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        budget_str = request.POST.get('total_budget')
        budget_title = request.POST.get('budget_title')
        education_budget = request.POST.get('education_budget')
        medical_budget = request.POST.get('medical_budget')
        food_budget = request.POST.get('food_budget')
        entertainment_budget = request.POST.get('entertainment_budget')
        transport_budget = request.POST.get('transport_budget')
        personal_care_budget = request.POST.get('personal_care_budget')
        housing_bills_budget = request.POST.get('housing_bills_budget')

        start_date1 = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date1 = datetime.strptime(end_date_str, '%Y-%m-%d').date()


        if start_date1 and end_date1:
                
                print(budget_str)
                print(education_budget)
                education_budget = float(education_budget) if education_budget else 0.0
                medical_budget = float(medical_budget) if medical_budget else 0.0
                food_budget = float(food_budget) if food_budget else 0.0
                entertainment_budget = float(entertainment_budget) if entertainment_budget else 0.0
                transport_budget = float(transport_budget) if transport_budget else 0.0
                personal_care_budget = float(personal_care_budget) if personal_care_budget else 0.0
                housing_bills_budget = float(housing_bills_budget) if housing_bills_budget else 0.0


                report = ReportDate(
                    user=request.user,
                    start_date=start_date1,
                    end_date=end_date1,
                    total_budget=float(budget_str),
                    budget_title=budget_title,
                    education_budget=float(education_budget),
                    medical_budget=float(medical_budget),
                    food_budget=float(food_budget),
                    entertainment_budget=float(entertainment_budget),
                    transport_budget=float(transport_budget),
                    personal_care_budget=float(personal_care_budget),
                    housing_bills_budget=float(housing_bills_budget)
                )
                report.save()

      # Pass the user parameter to calculate_total_expenses
                total_expenses = calculate_total_expenses(request.user, start_date1, end_date1)
                budget = float(budget_str)
                budget_remaining = budget-total_expenses
                expenses_by_category = calculate_expenses_by_category(request.user, start_date1, end_date1)

                return render(request, 'Budget Planner/budget2.html', {
                    'total_expenses': total_expenses,
                    'start_date': start_date1,
                    'end_date': end_date1,
                    'budget_remaining': budget_remaining,
                    'total_budget': budget,
                    'expenses_by_category': expenses_by_category,
                    'budget_title': budget_title,
                    'education_budget': education_budget,
                    'medical_budget': medical_budget,
                    'food_budget': food_budget,
                    'entertainment_budget': entertainment_budget,
                    'transport_budget': transport_budget,
                    'personal_care_budget': personal_care_budget,
                    'housing_bills_budget': housing_bills_budget,
 
                })


    return render(request, 'Budget Planner/budget.html')


def index(request):
    return render(request, 'Budget Planner/index.html')

def ai_view(request):
    return render(request, 'Budget Planner/ai_budget.html')


def saved_budgets_view(request):
    saved_budgets = ReportDate.objects.filter(user=request.user)
    return render(request, 'Budget Planner/saved_budgets.html', {'saved_budgets': saved_budgets})


def delete_budget(request, budget_id):
    budget = get_object_or_404(ReportDate, id=budget_id)
    budget.delete()
    saved_budgets = ReportDate.objects.filter(user=request.user)
    return render(request, 'Budget Planner/saved_budgets.html', {'saved_budgets': saved_budgets})


def edit_budget(request, budget_id):
    budget = get_object_or_404(ReportDate, id=budget_id)

    if request.method == 'POST':
        budget.total_budget = request.POST.get('total_budget')
        budget.budget_title = request.POST.get('budget_title')
        budget.education_budget = request.POST.get('education_budget')
        budget.medical_budget = request.POST.get('medical_budget')
        budget.food_budget = request.POST.get('food_budget')
        budget.entertainment_budget = request.POST.get('entertainment_budget')
        budget.transport_budget = request.POST.get('transport_budget')
        budget.personal_care_budget = request.POST.get('personal_care_budget')
        budget.housing_bills_budget = request.POST.get('housing_bills_budget')

        budget.save()
        return redirect('Saved Budgets')  # Redirect to the saved budgets page after editing

    return render(request, 'Budget Planner/edit_budget.html', {'budget': budget})





def generate_budget_plan(user_expenses):
    
    models_path = Path('E:/My Projects/MAIN PROJECTS/Forecast-Bud/ARIMA_Model/models_dict.pkl')
    params_path = Path('E:/My Projects/MAIN PROJECTS/Forecast-Bud/ARIMA_Model/best_params_dict.pkl')
    
    # Load models and params only when function is called
    models_dict = joblib.load(models_path)
    params_dict = joblib.load(params_path)
    

    user_expenses['date'] = pd.to_datetime(user_expenses['date'])
    
    if 'category' in user_expenses.columns:
        categories = user_expenses['category'].unique()
        print(categories)
        if len(categories) < 7:
            return {'error': '  Please add at least one expense for all categories (minimum 7 categories required). Go to the Expenses section to add expenses and generate your first personalized budget.'}
        predictions = {}
        total_last_four_predictions_dict = {}
        second_predictions = {}
        grand_total_last_four_predictions = 0
        second_predictions_grand_total = 0

        try:

            for category in categories:
                print(f"Predicting with ARIMA model for category: {category}")

                category_data = user_expenses[user_expenses['category'] == category]
                ts_data_aggregated_category = category_data.resample('W', on='date')['amount'].sum()
                print(ts_data_aggregated_category)



                # results = models_dict[category].filter(ts_data_aggregated_category.index.min(), ts_data_aggregated_category.index.max())
                results = models_dict[category]
                print('results',results)
                print(results.summary())
                # forecast = results.get_forecast(steps=7) 
                start_date = pd.Timestamp.today().normalize()-pd.DateOffset(days=7)
                print(start_date)
                forecast = results.get_prediction(start=start_date,
                                                  end=ts_data_aggregated_category.index.max() + pd.Timedelta(days=28))
                predicted_values = forecast.predicted_mean.astype(int)
                print('predicted',predicted_values)

                last_four_predictions = predicted_values[-4:]
                total_last_four_predictions = last_four_predictions.sum()
                print(total_last_four_predictions)
                total_last_four_predictions_dict[category] = total_last_four_predictions

                second_prediction_value = predicted_values.iloc[1]
                second_predictions[category] = second_prediction_value

                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(ts_data_aggregated_category.index, ts_data_aggregated_category, label='User Expenses (Aggregated)')
                ax.plot(predicted_values.index, predicted_values, label='Predicted Values (Aggregated)')
                ax.set_title(f"{category} - ARIMA Model with Time Series Aggregation")
                ax.set_xlabel('Date')
                ax.set_ylabel('Amount')
                ax.legend()

                canvas = FigureCanvasAgg(fig)
                buf = io.BytesIO()
                canvas.print_png(buf)
                buf.seek(0)

                # Convert the image to base64
                encoded_image = base64.b64encode(buf.read()).decode('utf-8')

                predictions[category] = {
                    'user_expenses': ts_data_aggregated_category.tolist(),
                    'predicted_values': predicted_values,
                    'plot_image': encoded_image,
                }

        except Exception as e:
            print(f"Error predicting with ARIMA model: {e}")
            return {'error': str(e)}

        finally:
            plt.close()

        grand_total_last_four_predictions = sum(total_last_four_predictions_dict.values())
        print(grand_total_last_four_predictions)
        second_predictions_grand_total = sum(second_predictions.values())
        print(second_predictions_grand_total)

        
        return {
            'predictions': {
                'predictions': predictions,
                'second_predictions_grand_total': second_predictions_grand_total,
                'grand_total_last_four_predictions': grand_total_last_four_predictions,
                'second_predictions': second_predictions,
                'total_last_four_predictions_dict': total_last_four_predictions_dict,
            },
        }
    else:
        return {'error': 'Category column not found in the DataFrame'}


def budget_planner(request):
    # Assuming you have a form for user input or retrieve expenses from the database
    # In this example, I'm assuming you have a model named Expense
    user_expenses = Expense.objects.all().values('date', 'category', 'amount')

    if not user_expenses:
        return render(request, 'Budget Planner/ai_budget.html', {'error_message': 'Please add at least one expense for all categories (minimum 7 categories required). Go to the Expenses section to add expenses and generate your first personalized budget.'})

    # Convert user_expenses to a DataFrame
    user_expenses_df = pd.DataFrame(user_expenses)


    result = generate_budget_plan(user_expenses_df)



    if 'error' in result:
        # Handle the case where the 'category' column is not found
        return render(request, 'Budget Planner/ai_budget.html', {'error_message': result['error']})
    else:
        if 'ai_budget_result' in request.POST:
            # Render the template with predictions
            return render(request, 'Budget Planner/ai_budget_result.html', {'predictions': result['predictions']['predictions']})
        elif 'ai_weekly_result' in request.POST:

            AiReportDate.objects.filter(user=request.user).delete()

            today_date = datetime.today().date()
            date_after_six_days = today_date + timedelta(days=6)
            total_weekly_budget = result['predictions']['second_predictions_grand_total']
            weekly_dictionary = result['predictions']['second_predictions']
            total_expenses = calculate_total_expenses(request.user, today_date, date_after_six_days)

            remaining_budget = total_weekly_budget - total_expenses
            expenses_by_category = calculate_expenses_by_category(request.user, today_date, date_after_six_days)
            display_names_mapping = {
                'Personal care': 'Personal_Care',
                'Housing/Bills': 'Housing_Bills',
            }

            weekly_dictionary = {display_names_mapping.get(k, k): v for k, v in weekly_dictionary.items()}

            report = AiReportDate(
                user=request.user,
                start_date=today_date,
                end_date=date_after_six_days,
                total_weekly_budget=float(total_weekly_budget),
                education_budget=float(weekly_dictionary['Education']),
                medical_budget = float(weekly_dictionary['Medical']),
                food_budget = float(weekly_dictionary['Food']),
                entertainment_budget = float(weekly_dictionary['Entertainment']),
                transport_budget = float(weekly_dictionary['Transport']),
                personal_care_budget = float(weekly_dictionary['Personal_Care']),
                housing_bills_budget = float(weekly_dictionary['Housing_Bills']),

                )
            report.save()


            return render(request, 'Budget Planner/ai_weekly_result.html', {
                'total_weekly_budget': total_weekly_budget,
                'weekly_dictionary': weekly_dictionary,
                'today_date': today_date,
                'date_after_six_days': date_after_six_days,
                'total_expenses': total_expenses,
                'remaining_budget': remaining_budget,
                'expenses_by_category': expenses_by_category,
            })
        elif 'ai_monthly_result' in request.POST:
            AiReportDateM.objects.filter(user=request.user).delete()

            total_monthly_budget = result['predictions']['grand_total_last_four_predictions']
            monthly_dictionary = result['predictions']['total_last_four_predictions_dict']
            today_date = datetime.today().date()
            date_after_30_days = today_date + timedelta(days=29)
            total_expenses = calculate_total_expenses(request.user, today_date, date_after_30_days)
            remaining_budget = total_monthly_budget - total_expenses
            expenses_by_category = calculate_expenses_by_category(request.user, today_date, date_after_30_days)

            display_names_mapping = {
                'Personal care': 'Personal_Care',
                'Housing/Bills': 'Housing_Bills',
            }

            monthly_dictionary = {display_names_mapping.get(k, k): v for k, v in monthly_dictionary.items()}

            report = AiReportDateM(
                user=request.user,
                start_date=today_date,
                end_date=date_after_30_days,
                total_monthly_budget=float(total_monthly_budget),
                education_budget=float(monthly_dictionary['Education']),
                medical_budget = float(monthly_dictionary['Medical']),
                food_budget = float(monthly_dictionary['Food']),
                entertainment_budget = float(monthly_dictionary['Entertainment']),
                transport_budget = float(monthly_dictionary['Transport']),
                personal_care_budget = float(monthly_dictionary['Personal_Care']),
                housing_bills_budget = float(monthly_dictionary['Housing_Bills']),

                )
            report.save()

            return render(request, 'Budget Planner/ai_monthly_result.html', {
                'total_monthly_budget': total_monthly_budget,
                'monthly_dictionary': monthly_dictionary,
                'today_date': today_date,
                'date_after_30_days': date_after_30_days,
                'total_expenses': total_expenses,
                'remaining_budget': remaining_budget,
                'expenses_by_category': expenses_by_category,
                })
        else:
            # Handle cases where none of the buttons were clicked
            return HttpResponse("Invalid request")
