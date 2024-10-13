from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from NEMO_floor_plans.forms import FloorPlanForm, FloorPlanNodeForm
from NEMO_floor_plans.models import FloorPlan, FloorPlanIcon, FloorPlanNode
from NEMO.apps.sensors.models import Sensor
from NEMO.views.pagination import SortedPaginator


def floor_plan_list_page(request):
    floor_plans_list = FloorPlan.objects.all()
    return SortedPaginator(floor_plans_list, request, order_by="-name").get_current_page()


@login_required
def floor_plans(request, floor_plan_id=None):
    if request.method == "POST":
        # If action is to set or remove floor plan as default
        if "set_default" in request.POST or "remove_default" in request.POST:
            target_floor_plan_id = (
                request.POST["set_default"] if "set_default" in request.POST else request.POST["remove_default"]
            )
            target_floor_plan = get_object_or_404(FloorPlan, id=target_floor_plan_id)
            target_floor_plan.is_default = "set_default" in request.POST
            target_floor_plan.save()
            return redirect("floor_plans")

    loaded_floor_plan = (
        FloorPlan.objects.get(id=floor_plan_id) if floor_plan_id else FloorPlan.objects.filter(is_default=True).first()
    )
    page = floor_plan_list_page(request)
    node_list = [node.serialize() for node in (loaded_floor_plan.nodes.all() if loaded_floor_plan else [])]

    return render(
        request,
        "floor_plans.html",
        {
            "page": page,
            "loaded_floor_plan": loaded_floor_plan,
            "node_list": node_list,
        },
    )


def floor_plan_node_save(request, floor_plan):
    floor_plan_node_id = request.POST.get("id")
    form_data = request.POST.copy()
    form_data["floor_plan"] = floor_plan.id

    if floor_plan_node_id:
        floor_plan_node = FloorPlanNode.objects.get(id=floor_plan_node_id, floor_plan=floor_plan)
        floor_plan_node_form = FloorPlanNodeForm(form_data, instance=floor_plan_node)
    else:
        floor_plan_node_form = FloorPlanNodeForm(form_data)

    if floor_plan_node_form.is_valid():
        floor_plan_node = floor_plan_node_form.save()
        floor_plan_node.save()
        return True, floor_plan_node.id, None
    return False, floor_plan_node_form.instance.id, floor_plan_node_form


@login_required
def floor_plan_edit(request, floor_plan_id):
    selected_node_id = None
    node_form = None
    floor_plan_form = None
    loaded_floor_plan = get_object_or_404(FloorPlan, id=floor_plan_id)
    if request.method == "POST":
        # If action is to delete a node
        if "delete_node" in request.POST:
            FloorPlanNode.objects.get(id=request.POST["id"], floor_plan__id=floor_plan_id).delete()
            return redirect("floor_plan_edit", floor_plan_id=floor_plan_id)

        # If action is to save/create a node
        if "save_node" in request.POST:
            save_successful, selected_node_id, node_form = floor_plan_node_save(request, loaded_floor_plan)
            if save_successful:
                return redirect("floor_plan_edit", floor_plan_id=floor_plan_id)

        # If action is to save the floor plan
        if "save_floor_plan" in request.POST:
            # object get or 404
            floor_plan_form = FloorPlanForm(request.POST, request.FILES, instance=loaded_floor_plan)
            if floor_plan_form.is_valid():
                floor_plan_form.save()
                return redirect("floor_plan_edit", floor_plan_id=floor_plan_id)

    node_list = [node.serialize() for node in loaded_floor_plan.nodes.all()]
    icons = FloorPlanIcon.objects.all()
    types = FloorPlanNode.NodeType.Choices
    sensors = Sensor.objects.all()
    return render(
        request,
        "floor_plan_editor.html",
        {
            "loaded_floor_plan": loaded_floor_plan,
            "node_list": node_list,
            "icons": icons,
            "types": types,
            "sensors": sensors,
            "selected_node_id": selected_node_id,
            "node_form": node_form,
            "floor_plan_form": floor_plan_form,
            "floor_plans": FloorPlan.objects.all(),
        },
    )
