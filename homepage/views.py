from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from django.db.models import Count
from transactions.models import Demand, Supplier_details, Customer

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        if not self.request.user.is_authenticated:
            return render(request, "landingpage.html")

        # Retrieve counts
        overall_demand_count = Demand.objects.filter(is_deleted=False).count()
        supplier_count = Supplier_details.objects.filter().count()
        my_demand_count = Demand.objects.filter(user=self.request.user).count()
        my_demand_with_quote_count = Demand.objects.filter(user=self.request.user, quote_id__isnull=False).count()
        demand_approved_count = Demand.objects.filter(user=self.request.user, status="Approved").count()
        customer_count = Customer.objects.count()  # Assuming you have a Customer model
        recent_demands = Demand.objects.filter(is_deleted=False).order_by('-created_at')[:5]
        my_recent_demands = Demand.objects.filter(user=self.request.user, is_deleted=False)
        my_recent_demands = my_recent_demands.annotate(quote_count=Count('quote'))[:5]


        context = {
            'overall_demand_count': overall_demand_count,
            'supplier_count': supplier_count,
            'my_demand_count': my_demand_count,
            'my_demand_with_quote_count': my_demand_with_quote_count,
            'demand_approved_count': demand_approved_count,
            'customer_count': customer_count,
            'recent_demands':recent_demands,
            'my_recent_demands':my_recent_demands,

        }
        return render(request, self.template_name, context)
class AboutView(TemplateView):
    template_name = "about.html"