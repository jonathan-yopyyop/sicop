from sicop.budget.models import Budget, Commitment
from sicop.project.models import Project
from sicop.area.models import Area
import re
import unicodedata
from django.utils.translation import gettext as _


def text_to_slug(text):
    text = text.lower()
    text = re.sub(r"\s+", "_", text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-z0-9_]", "", text)
    return text


def get_budget_by_areas():
    projects = Project.objects.filter()
    areas = Area.objects.all()
    budgets = []
    for area in areas:
        area_budget = 0
        area_used_budget = 0
        area_available_budget = 0
        area_commitments = 0
        commitments = Commitment.objects.filter(provision_cart__project__area=area)
        for commitment in commitments:
            area_commitments += commitment.provision_budget_amount
        for project in projects:
            if project.area == area:
                budget = Budget.objects.filter(project=project).first()
                if budget:
                    area_budget += budget.unit_value
                    area_available_budget += budget.available_budget
                    area_used_budget += budget.unit_value - budget.available_budget
        total_to_evaluate = area_available_budget + area_used_budget + area_commitments
        if total_to_evaluate == 0:
            area_available_budget_percentage = 0
            area_used_budget_percentage = 0
            area_commitments_percentage = 0

        else:
            area_available_budget_percentage = (area_available_budget / total_to_evaluate) * 100
            area_used_budget_percentage = (area_used_budget / total_to_evaluate) * 100
            area_commitments_percentage = (area_commitments / total_to_evaluate) * 100
        budgets.append(
            {
                "area": area.name,
                "id": area.id,
                "slug": text_to_slug(area.name),
                "budget": area_budget,
                "available_budget": area_available_budget,
                "area_used_budget": area_used_budget,
                "area_commitments": area_commitments,
                "area_available_budget_percentage": f"{area_available_budget_percentage:.2f}",
                "area_used_budget_percentage": f"{area_used_budget_percentage:.2f}",
                "area_commitments_percentage": f"{area_commitments_percentage:.2f}",
                "data": {
                    "labels": [_("Available"), _("Used"), _("Commitments")],
                    "datasets": [
                        {
                            "label": area.name,
                            "data": [
                                f"{area_available_budget_percentage:.2f}",
                                f"{area_used_budget_percentage:.2f}",
                                f"{area_commitments_percentage:.2f}",
                            ],
                            "backgroundColor": [
                                "rgb(255, 99, 132)",
                                "rgb(54, 162, 235)",
                                "rgb(255, 205, 86)",
                            ],
                            "hoverOffset": 4,
                        }
                    ],
                },
            }
        )
    return budgets


def get_budget_by_projects_in_area(area: Area):
    projects = Project.objects.filter(area=area)
    budgets = []
    for project in projects:
        commitments = Commitment.objects.filter(provision_cart__project=project)
        project_commitments = 0
        project_budget = project.budget
        for commitment in commitments:
            project_commitments += commitment.provision_budget_amount
        pending = project_budget - project_commitments
        commitment_percentage = (project_commitments / project_budget) * 100
        pending_percentage = (pending / project_budget) * 100
        budgets.append(
            {
                "project": project.name,
                "id": project.id,
                "slug": text_to_slug(project.name),
                "budget": project_budget,
                "commitments": project_commitments,
                "pending": pending,
                "commitment_percentage": f"{commitment_percentage:.2f}",
                "pending_percentage": f"{pending_percentage:.2f}",
                "data": {
                    "labels": [_("Commitments"), _("Pending")],
                    "datasets": [
                        {
                            "label": project.name,
                            "data": [f"{commitment_percentage:.2f}", f"{pending_percentage:.2f}"],
                            "backgroundColor": ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
                            "hoverOffset": 4,
                        }
                    ],
                },
            }
        )
    return budgets
