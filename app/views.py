"""
app View/Controller
"""
import json
import random

from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.html import mark_safe

from .models import PlayerStatistic

class Dashboard(TemplateView):

    template_name = 'dashboard.html'

    def _random_color(self):
        """
        Generate random rgba color
        """
        rand_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255), 
            0.6
        )
        return 'rgba{}'.format(rand_color)

    def _build_graph_data(self, queryset):
        """
        queryset : PlayerStatistic queryset instance

        Builds data to be used by chart.js radar graph. Sample data format:
        {
          labels: ['pts', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf'],
          datasets: [{
            label: 'Player 1',
            data: [65, 59, 90, 81, 56, 55, 40],
            borderColor: 'rgba(255, 99, 132, 0.6)',
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
          }, {}
          ]
        }

        """
        data = {}
        data['labels'] = ['pts', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf']
        datasets = []
        for stat in queryset:
            color = self._random_color()
            datasets.append({
                'label': stat.player,
                'data': [getattr(stat, att) for att in data['labels']],
                'borderColor': color,
                'backgroundColor': color
            })

        data['datasets'] = datasets
        return json.dumps(data)


    def get_context_data(self, **kwargs):
        """
        Add graph_data to the response context
        """
        context = super().get_context_data(**kwargs)
        context['graph_data'] = self._build_graph_data(
            PlayerStatistic.objects.filter(rank__lte=10)
        )
        return context
