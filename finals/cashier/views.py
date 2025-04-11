from django.shortcuts import render

# Create your views here.
def cashier(request):
    meals = [   'Beef Tapa',
                'Beef Pares',
                'Beef Nilaga',
                'Beef Walastik',
                'Boneless Bangus',
                'Garlic Longganisa',
                'Spicy Longganisa',
                'Delicious Longganisa',
                'Grilled Porkchop',
                'Grilled Liempo',
                'Pork Adobo',
                'Pork Marinated',
                'Pork Tocino',
                'Pork Steak',
                'Pork Sisig',
                'Lechon Kawali',
                'Crispy Kare-kare',
                'Crispy Binagoongan',
                'Pigar-Pigar',
                'Salpicao',
                'Chicken Pastil',
            ]
    return render(request, 'cashier/cashier.html', {'meals': meals})