from sicop.budget.models import Budget, Commitment, ProvisionCart, ProvisionCartBudget
from sicop.project.models import Project
from sicop.area.models import Area
from sicop.business_unit.models import BusinessUnit
from sicop.cost_center.models import CostCenter
import re
import unicodedata
from django.utils.translation import gettext as _


def text_to_slug(text):
    text = text.lower()
    text = re.sub(r"\s+", "_", text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-z0-9_]", "", text)
    return text


# Report functions by areas
def get_current_budget_by_area(area: Area):
    projects = Project.objects.filter(area=area)
    unit_value = 0
    initial_value = 0
    available_budget = 0
    budget_addition = 0
    released_amount = 0
    report_requested_budget = 0
    for project in projects:
        unit_value, initial_value, available_budget, budget_addition, released_amount, report_requested_budget = (
            get_current_budget_by_project(project)
        )
        # if project.name == "Defensoría 2024":
        unit_value += unit_value
        initial_value += initial_value
        available_budget += available_budget
        budget_addition += budget_addition
        released_amount += released_amount
        report_requested_budget += report_requested_budget
    if area.name == "Proyectos":
        print(
            "================================> ID",
            project.id,
            " -> initial_value",
            initial_value,
        )
    return (
        unit_value,
        initial_value,
        available_budget,
        budget_addition,
        released_amount,
        report_requested_budget,
    )


def get_total_cap_requested_by_area(area: Area):
    caps = ProvisionCart.objects.filter(
        project__area=area,
        approved=True,
        rejected=False,
        annulled=False,
        finished=True,
    )
    total_provisioned_amount = 0
    total_required_amount = 0
    for cap in caps:
        total_provisioned_amount += cap.total_provisioned_amount
        total_required_amount += cap.total_required_amount
    return total_provisioned_amount, total_required_amount


def get_total_commiment_by_area(area: Area):
    total_commiment = 0
    commitments = Commitment.objects.filter(
        provision_cart__project__area=area,
        provision_cart__approved=True,
        provision_cart__rejected=False,
        provision_cart__annulled=False,
        finished=True,
    )
    for commitment in commitments:
        total_commiment += commitment.real_provision_budget_amount
    return total_commiment


def get_budget_by_areas():
    areas = Area.objects.all()
    budgets = []
    for area in areas:
        (
            unit_value,
            initial_value,
            available_budget,
            budget_addition,
            released_amount,
            report_requested_budget,
        ) = get_current_budget_by_area(area)
        total_provisioned_amount, total_required_amount = get_total_cap_requested_by_area(area)
        total_commiment = get_total_commiment_by_area(area)
        # Graph totals
        total_current_budget = initial_value
        total_requested_budget = report_requested_budget - released_amount
        total_available_budget = total_current_budget - total_requested_budget
        total_to_be_committed = total_requested_budget - total_commiment

        # total_available_budget = available_budget - total_provisioned_amount
        total_by_engaded = total_provisioned_amount - total_commiment
        # Graph percents
        if available_budget == 0:
            total_commitet_percentage = 0
            total_available_budget_percentage = 0
            total_by_engaded_percentage = 0
        else:
            total_commitet_percentage = round(((total_commiment / total_current_budget) * 100), 1)
            total_available_budget_percentage = round(((total_available_budget / total_current_budget) * 100), 1)
            total_by_engaded_percentage = round(((total_by_engaded / total_current_budget) * 100), 1)
            difference = 100 - (
                total_commitet_percentage + total_available_budget_percentage + total_by_engaded_percentage
            )
            if difference > 0:
                total_by_engaded_percentage += difference

        budgets.append(
            {
                "area": area.name,
                "id": area.id,
                "slug": text_to_slug(area.name),
                "values": {
                    "total_current_budget": total_current_budget,
                    "total_available_budget": total_available_budget,
                    "total_commiment": total_commiment,
                    "total_to_be_committed": total_to_be_committed,
                },
                "data": {
                    "labels": [_("Available"), _("Engaged"), _("By Engaged")],
                    "datasets": [
                        {
                            "label": area.name,
                            "data": [
                                f"{total_available_budget_percentage}",
                                f"{total_commitet_percentage}",
                                f"{total_by_engaded_percentage}",
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


# Report functions by proyects
def get_current_budget_by_project(project: Project):
    budgets = Budget.objects.filter(project=project)
    unit_value = 0
    initial_value = 0
    available_budget = 0
    budget_addition = 0
    released_amount = 0
    report_requested_budget = 0
    for budget in budgets:
        unit_value += budget.unit_value
        initial_value += budget.initial_value
        available_budget += budget.available_budget
        budget_addition += budget.budget_addition
        released_amount += budget.released_amount
        report_requested_budget += budget.report_requested_budget

    return unit_value, initial_value, available_budget, budget_addition, released_amount, report_requested_budget


def get_total_cap_requested_by_project(project: Project):
    caps = ProvisionCart.objects.filter(
        project=project,
        approved=True,
        rejected=False,
        annulled=False,
        finished=True,
    )
    total_provisioned_amount = 0
    total_required_amount = 0
    for cap in caps:
        # if not cap.has_commitment:
        #     if project.name == "Defensoría 2024":
        #         print(
        #             "ID",
        #             cap.id,
        #             " -> cap.total_provisioned_amount",
        #             cap.total_provisioned_amount,
        #             " -> cap.total_required_amount",
        #             cap.total_required_amount,
        #         )
        total_provisioned_amount += cap.total_provisioned_amount
        total_required_amount += cap.total_required_amount
    return total_provisioned_amount, total_required_amount


def get_total_commiment_by_project(project: Project):
    total_commiment = 0
    commitments = Commitment.objects.filter(
        provision_cart__project=project,
        provision_cart__approved=True,
        provision_cart__rejected=False,
        provision_cart__annulled=False,
        finished=True,
    )
    for commitment in commitments:
        total_commiment += commitment.real_provision_budget_amount
    return total_commiment


def get_budget_by_projects_in_area(area: Area):
    projects = Project.objects.filter(area=area)
    budgets = []

    for project in projects:
        unit_value, initial_value, available_budget, budget_addition, released_amount, report_requested_budget = (
            get_current_budget_by_project(project)
        )
        total_provisioned_amount, total_required_amount = get_total_cap_requested_by_project(project)
        # Graph totals
        total_commiment = get_total_commiment_by_project(project)
        # Graph totals
        total_current_budget = initial_value
        total_requested_budget = total_provisioned_amount
        total_available_budget = total_current_budget - total_requested_budget
        total_to_be_committed = total_provisioned_amount - total_commiment

        # total_available_budget = available_budget - total_provisioned_amount
        total_by_engaded = total_requested_budget - total_commiment
        # Graph percents
        if total_current_budget == 0:
            total_commitet_percentage = 0
            total_available_budget_percentage = 0
            total_by_engaded_percentage = 0
        else:
            total_commitet_percentage = round(((total_to_be_committed / total_current_budget) * 100), 1)
            total_available_budget_percentage = round(((total_available_budget / total_current_budget) * 100), 1)
            total_by_engaded_percentage = round(((total_by_engaded / total_current_budget) * 100), 1)
            difference = 100 - (
                total_commitet_percentage + total_available_budget_percentage + total_by_engaded_percentage
            )
            if difference > 0:
                total_by_engaded_percentage += difference

        budgets.append(
            {
                "project": project.name,
                "id": project.id,
                "slug": text_to_slug(project.name),
                "values": {
                    "total_current_budget": total_current_budget,
                    "total_available_budget": total_available_budget,
                    "total_commiment": total_commiment,
                    "total_to_be_committed": total_to_be_committed,
                },
                "data": {
                    "labels": [_("Available"), _("Engaged"), _("By Engaged")],
                    "datasets": [
                        {
                            "label": project.name,
                            "data": [
                                f"{total_available_budget_percentage}",
                                f"{total_by_engaded_percentage}",
                                f"{total_commitet_percentage}",
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


# Functions by project
def get_total_cap_requested_by_budget(budget: Budget):
    provision_cart_query_set = ProvisionCartBudget.objects.filter(
        budget=budget,
        provision_cart__approved=True,
        provision_cart__rejected=False,
        provision_cart__annulled=False,
        provision_cart__finished=True,
    )
    provosioned_amount = 0
    commitment_amount = 0

    if provision_cart_query_set.count() > 0:
        provision_budget = provision_cart_query_set.last()
        provosioned_amount = provision_budget.provosioned_amount
        provision_cart = provision_budget.provision_cart
        provosioned_amount = provision_budget.provosioned_amount
        commitment_query_set = Commitment.objects.filter(
            provision_cart=provision_cart,
            finished=True,
        )
        if commitment_query_set.count() > 0:
            commitment_amount = provision_budget.provosioned_amount - provision_budget.released_amount

    return provosioned_amount, commitment_amount


def get_current_budget_by_project_detail(project: Project):
    budgets = Budget.objects.filter(project=project)
    unit_value = 0
    initial_value = 0
    available_budget = 0
    budget_addition = 0
    released_amount = 0
    report_requested_budget = 0
    for budget in budgets:
        unit_value += budget.unit_value
        initial_value += budget.initial_value
        available_budget += budget.available_budget
        budget_addition += budget.budget_addition
        released_amount += budget.released_amount
        report_requested_budget += budget.report_requested_budget

    return unit_value, initial_value, available_budget, budget_addition, released_amount, report_requested_budget


def get_total_cap_requested_by_project_detail(project: Project):
    caps = ProvisionCart.objects.filter(
        project=project,
        approved=True,
        rejected=False,
        annulled=False,
        finished=True,
    )
    total_provisioned_amount = 0
    total_required_amount = 0
    for cap in caps:
        total_provisioned_amount += cap.total_provisioned_amount
        total_required_amount += cap.total_required_amount
    return total_provisioned_amount, total_required_amount


def get_total_commiment_by_project_detail(project: Project):
    total_commiment = 0
    commitments = Commitment.objects.filter(
        provision_cart__project=project,
        provision_cart__approved=True,
        provision_cart__rejected=False,
        provision_cart__annulled=False,
        finished=True,
    )
    for commitment in commitments:
        total_commiment += commitment.real_provision_budget_amount
    return total_commiment


def get_project_detail(project: Project):
    # Totals for the table
    unit_value, initial_value, available_budget, budget_addition, released_amount, report_requested_budget = (
        get_current_budget_by_project_detail(project)
    )
    totals_commiment = get_total_commiment_by_project_detail(project)
    totals_provisioned_amount = report_requested_budget - released_amount
    totals_current_budget = initial_value + budget_addition
    totals_available_budget = totals_current_budget - totals_provisioned_amount
    totals_by_engaded = totals_provisioned_amount - totals_commiment
    # Total percentages
    if totals_current_budget > 0:
        totals_available_budget_percentage = (totals_available_budget / totals_current_budget) * 100
    else:
        totals_available_budget_percentage = 0
    if totals_available_budget == 0:
        totals_by_engaded_percentage = 0
        totals_commiment_percentage = 0
    else:
        totals_by_engaded_percentage = round(((totals_by_engaded / totals_provisioned_amount) * 100), 1)
        totals_commiment_percentage = round(((totals_commiment / totals_provisioned_amount) * 100), 1)
        difference = 100 - (
            totals_commiment_percentage + totals_available_budget_percentage + totals_by_engaded_percentage
        )
        if difference > 0:
            totals_by_engaded_percentage += difference
    totals = {
        "provisioned_amount": 0,
        "total_available_budget": totals_available_budget,
        "total_commiment": totals_commiment,
        "total_by_engaded": totals_by_engaded,
        "total_commitet_percentage": f"{totals_commiment_percentage}",
        "total_available_budget_percentage": f"{totals_available_budget_percentage}",
        "total_by_engaded_percentage": f"{totals_by_engaded_percentage}",
    }
    totals["provisioned_amount"] = totals_provisioned_amount
    totals["total_budget"] = totals_current_budget

    # Table detail by budget
    budgets = []
    project_budgets = project.project_budgets.all()
    for project_budget in project_budgets:
        # Budget data
        budget: Budget = project_budget
        provisioned_amount, commitment_amount = get_total_cap_requested_by_budget(budget)
        budget_initial_value = budget.initial_value
        budget_budget_addition = budget.budget_addition
        budget_released_amount = budget.released_amount
        budget_report_requested_budget = budget.report_requested_budget
        # Budget data end
        budget_totals_provisioned_amount = budget_report_requested_budget - budget_released_amount
        budget_totals_current_budget = budget_initial_value + budget_budget_addition
        budget_totals_available_budget = budget_totals_current_budget - budget_totals_current_budget
        budget_totals_by_engaded = budget_totals_provisioned_amount - commitment_amount
        # Total budget percentages
        if budget_totals_current_budget > 0:
            budget_totals_available_budget_percentage = (
                budget_totals_available_budget / budget_totals_current_budget
            ) * 100
        else:
            budget_totals_available_budget_percentage = 0
        if budget_totals_provisioned_amount == 0:
            budget_totals_by_engaded_percentage = 0
            budget_totals_commiment_percentage = 0
        else:
            budget_totals_by_engaded_percentage = round(
                ((budget_totals_by_engaded / budget_totals_provisioned_amount) * 100),
            )
            budget_totals_commiment_percentage = round(
                ((commitment_amount / budget_totals_provisioned_amount) * 100),
            )

        data = {
            "budget": budget,
            "initial_value": budget_totals_current_budget,
            "available_budget": budget_totals_available_budget,
            "provisioned_amount": budget_totals_provisioned_amount,
            "available_percentage": f"{budget_totals_available_budget_percentage}",
            "commitment_amount": commitment_amount,
            "commitment_percentage": f"{budget_totals_commiment_percentage}",
            "by_engaged": budget_totals_by_engaded,
            "by_engaged_percentage": f"{budget_totals_by_engaded_percentage}",
        }
        budgets.append(data)

    return budgets, totals


# Report functions by BusinessUnit
def get_current_budget_by_business_unit(business_unit: BusinessUnit):
    cost_centers = business_unit.cost_centers.all()
    budgets = Budget.objects.filter(cost_centers__in=cost_centers)
    unit_value = 0
    initial_value = 0
    available_budget = 0
    for budget in budgets:
        unit_value += budget.unit_value
        initial_value += budget.initial_value
        available_budget += budget.available_budget
    return unit_value, initial_value, available_budget


def get_current_budget_by_cost_center(cost_center: CostCenter):
    budgets = Budget.objects.filter(cost_centers__in=[cost_center])
    unit_value = 0
    initial_value = 0
    available_budget = 0
    for budget in budgets:
        unit_value += budget.unit_value
        initial_value += budget.initial_value
        available_budget += budget.available_budget
    return unit_value, initial_value, available_budget


def get_total_cap_requested_by_business_unit(business_unit: BusinessUnit):
    cost_centers = business_unit.cost_centers.all()
    budgets = Budget.objects.filter(cost_centers__in=cost_centers)
    projects = []
    for budget in budgets:
        projects.append(budget.project)

    caps = ProvisionCart.objects.filter(
        project__in=projects,
        approved=True,
        rejected=False,
        annulled=False,
        finished=True,
    )
    total_provisioned_amount = 0
    total_required_amount = 0
    for cap in caps:
        total_provisioned_amount += cap.total_provisioned_amount
        total_required_amount += cap.total_required_amount
    return total_provisioned_amount, total_required_amount


def get_total_cap_requested_by_cost_center(cost_center: CostCenter):
    budgets = Budget.objects.filter(cost_centers__in=[cost_center])
    projects = []
    for budget in budgets:
        projects.append(budget.project)

    caps = ProvisionCart.objects.filter(
        project__in=projects,
        approved=True,
        rejected=False,
        annulled=False,
        finished=True,
    )
    total_provisioned_amount = 0
    total_required_amount = 0
    for cap in caps:
        total_provisioned_amount += cap.total_provisioned_amount
        total_required_amount += cap.total_required_amount
    return total_provisioned_amount, total_required_amount


def get_total_commiment_by_business_unit(business_unit: BusinessUnit):
    total_commiment = 0
    cost_centers = business_unit.cost_centers.all()
    budgets = Budget.objects.filter(cost_centers__in=cost_centers)
    projects = []
    for budget in budgets:
        projects.append(budget.project)
    commitments = Commitment.objects.filter(
        provision_cart__project__in=projects,
        provision_cart__approved=True,
        provision_cart__rejected=False,
        provision_cart__annulled=False,
        finished=True,
    )
    for commitment in commitments:
        total_commiment += commitment.real_provision_budget_amount
    return total_commiment


def get_total_commiment_by_cost_center(cost_center: CostCenter):
    total_commiment = 0
    budgets = Budget.objects.filter(cost_centers__in=[cost_center])
    projects = []
    for budget in budgets:
        projects.append(budget.project)
    commitments = Commitment.objects.filter(
        provision_cart__project__in=projects,
        provision_cart__approved=True,
        provision_cart__rejected=False,
        provision_cart__annulled=False,
        finished=True,
    )
    for commitment in commitments:
        total_commiment += commitment.real_provision_budget_amount
    return total_commiment


def get_budget_by_business_unit(business_unit: BusinessUnit):
    unit_value, initial_value, available_budget = get_current_budget_by_business_unit(business_unit)
    total_provisioned_amount, total_required_amount = get_total_cap_requested_by_business_unit(business_unit)
    total_commiment = get_total_commiment_by_business_unit(business_unit)
    # Graph totals
    total_available_budget = available_budget - total_provisioned_amount
    total_by_engaded = total_provisioned_amount - total_commiment
    # Graph percents
    if available_budget == 0:
        total_commitet_percentage = 0
        total_available_budget_percentage = 0
        total_by_engaded_percentage = 0
    else:
        total_commitet_percentage = round(((total_commiment / available_budget) * 100), 1)
        total_available_budget_percentage = round(((total_available_budget / available_budget) * 100), 1)
        total_by_engaded_percentage = round(((total_by_engaded / available_budget) * 100), 1)
        difference = 100 - (
            total_commitet_percentage + total_available_budget_percentage + total_by_engaded_percentage
        )
        if difference > 0:
            total_by_engaded_percentage += difference

    cost_centers = business_unit.cost_centers.all()
    cost_center_data = []

    for cost_center in cost_centers:
        # Totals
        cost_center_unit_value, cost_center_initial_value, cost_center_available_budget = (
            get_current_budget_by_cost_center(cost_center)
        )
        cost_center_total_provisioned_amount, cost_center_total_required_amount = (
            get_total_cap_requested_by_cost_center(cost_center)
        )
        cost_center_total_commiment = get_total_commiment_by_cost_center(cost_center)
        # Graph totals
        cost_center_total_available_budget = cost_center_available_budget - cost_center_total_provisioned_amount
        cost_center_total_by_engaded = cost_center_total_provisioned_amount - cost_center_total_commiment
        # Graph percents
        if cost_center_available_budget == 0:
            cost_center_total_commitet_percentage = 0
            cost_center_total_available_budget_percentage = 0
            cost_center_total_by_engaded_percentage = 0
        else:
            cost_center_total_commitet_percentage = round(
                ((cost_center_total_commiment / cost_center_available_budget) * 100), 2
            )
            cost_center_total_available_budget_percentage = round(
                ((cost_center_total_available_budget / cost_center_available_budget) * 100), 2
            )
            cost_center_total_by_engaded_percentage = round(
                ((cost_center_total_by_engaded / cost_center_available_budget) * 100), 2
            )
        # Totals end
        cost_center_data.append(
            {
                "id": cost_center.id,
                "name": cost_center.name,
                "cost_center_id": cost_center.cost_center_id,
                "cost_center_initial_value": cost_center_initial_value,
                "cost_center_total_commiment": cost_center_total_commiment,
                "cost_center_total_available_budget": cost_center_total_available_budget,
                "cost_center_total_provisioned_amount": cost_center_total_provisioned_amount,
                "cost_center_total_by_engaded": cost_center_total_by_engaded,
                "cost_center_total_commitet_percentage": f"{cost_center_total_commitet_percentage}",
                "cost_center_total_available_budget_percentage": f"{cost_center_total_available_budget_percentage}",
                "cost_center_total_by_engaded_percentage": f"{cost_center_total_by_engaded_percentage}",
            }
        )
    if initial_value > 0:
        grand_total_available_budget_percentage = round(((total_available_budget / initial_value) * 100), 1)
        grand_total_commitet_percentage = round(((total_commiment / initial_value) * 100), 1)
        grand_total_by_engaded_percentage = round(((total_by_engaded / initial_value) * 100), 1)
        grand_total_provisioned_percentage = round(((total_provisioned_amount / initial_value) * 100), 1)
    else:
        grand_total_available_budget_percentage = 0
        grand_total_commitet_percentage = 0
        grand_total_by_engaded_percentage = 0
        grand_total_provisioned_percentage = 0

    graph_data = {
        "values": {
            "initial_value": initial_value,
            "total_available_budget": total_available_budget,
            "total_commiment": total_commiment,
            "total_by_engaded": total_by_engaded,
            "total_provisioned_amount": total_provisioned_amount,
            "grand_total_available_budget_percentage": f"{grand_total_available_budget_percentage}",
            "grand_total_provisioned_percentage": f"{grand_total_provisioned_percentage}",
            "grand_total_commitet_percentage": f"{grand_total_commitet_percentage}",
            "grand_total_by_engaded_percentage": f"{grand_total_by_engaded_percentage}",
        },
        "data": {
            "labels": [_("Available"), _("Engaged"), _("By Engaged")],
            "datasets": [
                {
                    "label": business_unit.name,
                    "data": [
                        f"{total_available_budget_percentage}",
                        f"{total_commitet_percentage}",
                        f"{total_by_engaded_percentage}",
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

    return cost_center_data, graph_data
